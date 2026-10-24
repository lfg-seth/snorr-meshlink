#!/usr/bin/env python3
"""Update one inventoried RAK4631 with the pinned production image and profile."""

import argparse
import base64
import contextlib
import copy
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = Path(__file__).with_name("repeater-profiles.json")
LOCAL_MANIFEST_PATH = ROOT / "docs" / "operations" / "repeater-production-image.json"


class UpdateError(Exception):
    """An actionable failure safe to print without exposing configuration."""


def normalize_number(value):
    match = re.fullmatch(r"R?0*([1-6])", value.strip().upper())
    if not match:
        raise UpdateError("Choose an inventoried repeater, R001 through R006.")
    return f"R{int(match[1]):03d}"


def serial_matches(actual, expected):
    return bool(actual) and actual.strip().upper() == expected.upper()


def select_port(ports, profile, explicit=None):
    candidates = [p for p in ports if serial_matches(p.serial_number, profile["usbSerial"])]
    if explicit:
        candidates = [p for p in candidates if p.device.casefold() == explicit.casefold()]
    if len(candidates) != 1:
        raise UpdateError("Expected exactly one port with this repeater's recorded USB serial; check cable/port and close other serial tools.")
    return candidates[0]


def disk_matches(serial, pnp_id, expected):
    if serial_matches(serial, expected):
        return True
    return any(serial_matches(token, expected) for token in re.split(r"[\\&]", pnp_id or ""))


def windows_volumes():
    script = r"""
$ErrorActionPreference = 'Stop'
$rows = @(foreach ($disk in Get-CimInstance Win32_DiskDrive) {
    if ($disk.InterfaceType -eq 'USB' -or $disk.PNPDeviceID -like 'USBSTOR*') {
        foreach ($part in Get-CimAssociatedInstance -InputObject $disk -Association Win32_DiskDriveToDiskPartition) {
            foreach ($volume in Get-CimAssociatedInstance -InputObject $part -Association Win32_LogicalDiskToPartition) {
                @{root = $volume.DeviceID + '\'; serial = $disk.SerialNumber; pnp = $disk.PNPDeviceID}
            }
        }
    }
})
ConvertTo-Json -InputObject $rows -Compress
"""
    result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script], check=True, capture_output=True, text=True, timeout=20)
    return json.loads(result.stdout or "[]")


def linux_volumes():
    result = subprocess.run(["lsblk", "--json", "--output", "PATH,SERIAL,TRAN,MOUNTPOINTS"], check=True, capture_output=True, text=True, timeout=10)
    rows = []

    def visit(device, serial="", usb=False):
        serial = device.get("serial") or serial
        usb = usb or device.get("tran") == "usb"
        if usb:
            rows.extend({"root": mount, "serial": serial, "pnp": ""} for mount in device.get("mountpoints", []) if mount)
        for child in device.get("children", []):
            visit(child, serial, usb)

    for device in json.loads(result.stdout)["blockdevices"]:
        visit(device)
    return rows


def find_uf2_volume(rows, usb_serial):
    matches = []
    for row in rows:
        if not disk_matches(row.get("serial"), row.get("pnp"), usb_serial):
            continue
        root = Path(row["root"])
        info = root / "INFO_UF2.TXT"
        if not info.is_file():
            continue
        fields = dict(line.split(":", 1) for line in info.read_text(errors="replace").splitlines() if ":" in line)
        if fields.get("Board-ID", "").strip() != "WisBlock-RAK4631-Board":
            raise UpdateError("USB serial matched but UF2 Board-ID is not WisBlock-RAK4631-Board.")
        matches.append(root)
    if len(matches) > 1:
        raise UpdateError("Multiple UF2 volumes match the USB identity; refusing to choose.")
    return matches[0] if matches else None


def validate_uf2(path):
    data = path.read_bytes()
    if not data or len(data) % 512:
        raise UpdateError("Invalid UF2 length.")
    addresses = set()
    for offset in range(0, len(data), 512):
        magic0, magic1, flags, address, size, number, total, family = struct.unpack_from("<8I", data, offset)
        end_magic = struct.unpack_from("<I", data, offset + 508)[0]
        if ((magic0, magic1, end_magic) != (0x0A324655, 0x9E5D5157, 0x0AB16F30)
                or flags != 0x2000 or family != 0xADA52840 or size != 256
                or number != offset // 512 or total != len(data) // 512
                or address < 0x26000 or address + size > 0xED000
                or address in addresses):
            raise UpdateError("UF2 is not an application-only nRF52840 image with unique valid blocks.")
        addresses.add(address)


def load_release(profiles):
    tag = profiles.get("releaseTag")
    if not isinstance(tag, str) or not re.fullmatch(r"snorr-rak4631-\d+\.\d+\.\d+\.[0-9a-f]{7}-pre\.\d+", tag):
        raise UpdateError("No supported production release is pinned in repeater-profiles.json.")
    path = ROOT / "firmware" / ".github" / "releases" / f"{tag}.json"
    manifest_bytes = path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if (manifest.get("schemaVersion") != 1 or manifest.get("repository") != "lfg-seth/firmware"
            or manifest.get("tag") != tag or manifest.get("target") != "rak4631"):
        raise UpdateError("Pinned manifest is not the expected production RAK4631 release.")
    if manifest.get("snorrNeighborLoraIntervalSeconds") != 180:
        raise UpdateError("Pinned release does not certify the required compiled 180-second SNNS cadence.")
    if manifest.get("publishedArtifact") is False:
        raise UpdateError("An unpublished build requires explicit --local-bundle selection; it cannot be the public release pin.")
    for asset in manifest["artifacts"]:
        if Path(asset["name"]).name != asset["name"] or "/" in asset["name"] or "\\" in asset["name"]:
            raise UpdateError("Unsafe asset name in release manifest.")
    return manifest, manifest_bytes


def released_image(manifest, manifest_bytes):
    sys.path.insert(0, str(ROOT / "firmware" / "bin"))
    from verify_snorr_release import download_release, verify_assets

    directory = ROOT / "private" / "bench" / "releases" / manifest["tag"]
    if not directory.exists() or not any(directory.iterdir()):
        directory.mkdir(parents=True, exist_ok=True)
        download_release(manifest["tag"], directory, manifest_bytes)
    verify_assets(directory, manifest_bytes)
    images = [asset for asset in manifest["artifacts"] if asset["name"].endswith(".uf2")]
    if len(images) != 1:
        raise UpdateError("Expected one UF2 in the verified release.")
    image = directory / images[0]["name"]
    validate_uf2(image)
    return image


def local_bundle_image(directory):
    manifest_bytes = LOCAL_MANIFEST_PATH.read_bytes()
    manifest = json.loads(manifest_bytes)
    if (manifest.get("schemaVersion") != 1 or manifest.get("repository") != "lfg-seth/firmware"
            or manifest.get("target") != "rak4631"
            or manifest.get("source") != "0634b775f65804968f5a18a7e8824db415556db2"
            or manifest.get("version") != "2.7.26.0634b77"
            or manifest.get("tag") != "snorr-rak4631-2.7.26.0634b77-pre.1"
            or manifest.get("publishedArtifact") is not False
            or manifest.get("hardwareVerified") is not False
            or manifest.get("snorrNeighborLoraIntervalSeconds") != 180):
        raise UpdateError("Tracked local-build manifest does not match the explicit unpublished RAK production build.")
    expected_names = {"firmware-rak4631-2.7.26.0634b77.uf2", "firmware-rak4631-2.7.26.0634b77-ota.zip"}
    if len(manifest.get("artifacts", [])) != 2 or {asset["name"] for asset in manifest["artifacts"]} != expected_names:
        raise UpdateError("Tracked local-build manifest has an unexpected asset set.")
    sys.path.insert(0, str(ROOT / "firmware" / "bin"))
    from verify_snorr_release import verify_assets

    verify_assets(directory, manifest_bytes)
    image = directory / "firmware-rak4631-2.7.26.0634b77.uf2"
    validate_uf2(image)
    return manifest, manifest_bytes, image


def wire(message):
    return base64.b64encode(message.SerializeToString(deterministic=True)).decode("ascii")


def snapshot(interface, port, usb_serial):
    from google.protobuf.json_format import MessageToDict

    info = interface.getMyNodeInfo()
    if not info or not interface.metadata or not interface.localNode.channels:
        raise UpdateError("Node did not return complete identity, metadata and channels.")
    node = interface.localNode
    return {
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "port": port, "usbSerial": usb_serial, "user": copy.deepcopy(info["user"]),
        "hardwareId": interface.myInfo.device_id.hex(),
        "myInfo": MessageToDict(interface.myInfo), "metadata": MessageToDict(interface.metadata),
        "localConfig": MessageToDict(node.localConfig), "moduleConfig": MessageToDict(node.moduleConfig),
        "channels": [MessageToDict(channel) for channel in node.channels],
        "localWire": wire(node.localConfig), "moduleWire": wire(node.moduleConfig),
        "channelsWire": [wire(channel) for channel in node.channels],
    }


def validate_node(interface, state, profile):
    from meshtastic.util import DEFAULT_KEY

    if state["user"].get("id") != profile["nodeId"]:
        raise UpdateError("Radio node ID does not match the selected repeater; no write performed.")
    if state["user"].get("hwModel") != "RAK4631" or state["metadata"].get("hwModel") != "RAK4631":
        raise UpdateError("Connected radio does not independently identify as RAK4631.")
    security = interface.localNode.localConfig.security
    if (len(security.private_key) != 32 or len(security.public_key) != 32
            or not any(security.private_key) or not any(security.public_key)):
        raise UpdateError("Expected an existing PKI identity; provision it separately rather than replacing keys.")
    primary = [channel for channel in interface.localNode.channels if channel.role == 1]
    if (len(primary) != 1 or not primary[0].settings.name
            or len(primary[0].settings.psk) not in (16, 32)
            or not any(primary[0].settings.psk)
            or (len(primary[0].settings.psk) == 16
                and primary[0].settings.psk[:15] == DEFAULT_KEY[:15])):
        raise UpdateError("Expected an existing private primary channel; provision the pilot channel separately.")
    radio = interface.localNode.localConfig.lora
    if not radio.region or not radio.tx_enabled:
        raise UpdateError("Expected an already provisioned region and enabled repeater LoRa transmitter.")


def configure_in_memory(interface, profiles, profile):
    node = interface.localNode
    node.localConfig.device.role = 0  # CLIENT; no name, key or radio replacement.
    telemetry = node.moduleConfig.telemetry
    telemetry.device_telemetry_enabled = True
    telemetry.device_update_interval = profiles["reportIntervalSeconds"]
    telemetry.environment_measurement_enabled = profile["environment"]
    telemetry.environment_update_interval = profiles["reportIntervalSeconds"]
    telemetry.power_measurement_enabled = profile["power"]
    telemetry.power_update_interval = profiles["reportIntervalSeconds"]
    neighbor = node.moduleConfig.neighbor_info
    neighbor.enabled = True
    neighbor.transmit_over_lora = True
    neighbor.update_interval = profiles["standardNeighborIntervalSeconds"]


def assert_preserved(expected, actual):
    if expected.get("hardwareId") != actual.get("hardwareId"):
        raise UpdateError("Hardware identity changed unexpectedly.")
    for name in ("localWire", "moduleWire", "channelsWire"):
        if expected[name] != actual[name]:
            raise UpdateError(f"Full saved {name} differs from the intended profile; inspect private snapshots before continuing.")
    before_user, after_user = copy.deepcopy(expected["user"]), copy.deepcopy(actual["user"])
    before_user.pop("role", None)
    after_user.pop("role", None)
    if before_user != after_user:
        raise UpdateError("Owner/identity changed unexpectedly; inspect private snapshots before continuing.")


def private_json(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
    path.chmod(0o600)


@contextlib.contextmanager
def quiet_serial(log):
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        yield


def connect(port):
    from meshtastic.serial_interface import SerialInterface

    return SerialInterface(devPath=port, timeout=25)


def wait_application(profile, timeout=120):
    from serial.tools.list_ports import comports

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        matches = [port for port in comports() if serial_matches(port.serial_number, profile["usbSerial"])]
        if len(matches) > 1:
            raise UpdateError("Multiple serial ports match this repeater after reboot.")
        if len(matches) == 1:
            try:
                interface = connect(matches[0].device)
            except Exception:
                time.sleep(2)
                continue
            return interface, matches[0].device
        time.sleep(1)
    raise UpdateError("The selected repeater did not return as a Meshtastic application; its private backup is retained.")


def uf2_volume_reader():
    if sys.platform not in ("win32", "linux"):
        raise UpdateError("Automatic UF2 volume identification supports Windows and Linux only.")
    return windows_volumes if sys.platform == "win32" else linux_volumes


def prepare_node_for_update(interface, port, profiles, profile, bench, dry_run=False, config_only=False):
    try:
        before = snapshot(interface, port, profile["usbSerial"])
        validate_node(interface, before, profile)
        private_json(bench / "before.json", before)
        configure_in_memory(interface, profiles, profile)
        intended = snapshot(interface, port, profile["usbSerial"])
        private_json(bench / "intended.json", intended)
        if not dry_run and not config_only:
            enumerate_volumes = uf2_volume_reader()
            enumerate_volumes()
            interface.localNode.enterDFUMode()
            time.sleep(0.5)
    finally:
        interface.close()
    return before, intended


def flash_uf2(profile, image):
    enumerate_volumes = uf2_volume_reader()
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        volume = find_uf2_volume(enumerate_volumes(), profile["usbSerial"])
        if volume:
            shutil.copyfile(image, volume / "SNORR.UF2")
            return
        time.sleep(1)
    raise UpdateError("No mounted RAK4631 UF2 volume matches the selected USB serial. On Linux enable desktop automount or mount the device, then rerun after reconnecting it.")


def show_plan(number, profiles, profile):
    print(f"{number}: {profile['nodeId']}; RAK4631; USB {profile['usbSerial']}")
    print(f"Pinned release: {profiles.get('releaseTag') or '(not pinned)'}")
    print(f"CLIENT; battery/device {profiles['reportIntervalSeconds']} s; environment {'on' if profile['environment'] else 'off'}; INA219 power {'on' if profile['power'] else 'off'}.")
    print("Enabled sensor reports: 180 s; RAK SNNS: 180 s plus jitter/airtime deferral; standard NeighborInfo: 21600 s.")
    print("Preserve this radio's complete owner/keys/private channel and other configuration; application-only UF2, no reset.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--number", help="R001–R006; prompts when omitted")
    parser.add_argument("--port", help="Optional application port, e.g. COM21 or /dev/ttyACM0")
    parser.add_argument("--dry-run", action="store_true", help="Identify/back up the board and verify assets; no flash or saved configuration writes")
    parser.add_argument("--show-plan", action="store_true", help="Show the tracked release/profile without opening hardware")
    parser.add_argument("--config-only", action="store_true", help="Apply/verify the profile only, requiring the exact pinned firmware already installed")
    parser.add_argument("--output-dir", type=Path, help="New evidence directory beneath this repository's private/ (default: unique private/bench/<number>-update-<time>)")
    parser.add_argument("--local-bundle", type=Path, help="Explicit unpublished local build, checked against the fixed tracked production-image manifest; never an automatic fallback")
    args = parser.parse_args(argv)
    bench = None
    dry_run_complete = False
    console = sys.stdout
    try:
        number = normalize_number(args.number or input("Repeater number (R001–R006): "))
        profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        if profiles.get("schemaVersion") != 1 or profiles.get("reportIntervalSeconds") != 180 or profiles.get("standardNeighborIntervalSeconds", 0) < 14400:
            raise UpdateError("Unsupported production profile schema or intervals.")
        profile = profiles["nodes"][number]
        show_plan(number, profiles, profile)
        if args.local_bundle:
            print(f"Explicit unpublished local-build bundle: {args.local_bundle}; fixed tracked manifest: {LOCAL_MANIFEST_PATH.name}")
        if args.show_plan:
            return 0
        if args.local_bundle:
            manifest, manifest_bytes, image = local_bundle_image(args.local_bundle.resolve())
            print("Verified local build; public release CI/download provenance remains pending.")
        else:
            manifest, manifest_bytes = load_release(profiles)
        try:
            from serial.tools.list_ports import comports
            import meshtastic
        except ImportError:
            raise UpdateError("Install dependencies using python -m pip install -r scripts/bench/repeater-requirements.txt") from None
        port = select_port(comports(), profile, args.port)
        if not args.local_bundle:
            image = released_image(manifest, manifest_bytes)
        print(f"Verified image SHA256: {hashlib.sha256(image.read_bytes()).hexdigest()}")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        bench = (args.output_dir or ROOT / "private" / "bench" / f"{number}-update-{stamp}").resolve()
        try:
            bench.relative_to((ROOT / "private").resolve())
        except ValueError:
            bench = None
            raise UpdateError("Evidence output must remain beneath this repository's ignored private/ directory.") from None
        if bench.exists():
            bench = None
            raise UpdateError("Evidence output directory already exists; choose a new directory to preserve prior backups.")
        bench.mkdir(parents=True, mode=0o700)
        logging.disable(logging.CRITICAL)
        print(f"Identifying/backing up {port.device}; private evidence: {bench.relative_to(ROOT)}", flush=True)
        with (bench / "serial.log").open("x", encoding="utf-8") as log, quiet_serial(log):
            interface = connect(port.device)
            before, intended = prepare_node_for_update(interface, port.device, profiles, profile, bench, args.dry_run, args.config_only)
            if args.dry_run:
                dry_run_complete = True
                return 0
            if not args.config_only:
                print("Flashing application-only UF2 on the identity-matched RAK volume...", file=console, flush=True)
                flash_uf2(profile, image)
                time.sleep(8)
            print("Checking installed firmware and preserved identity/profile...", file=console, flush=True)
            interface, current_port = wait_application(profile)
            try:
                flashed = snapshot(interface, current_port, profile["usbSerial"])
                private_json(bench / "after-flash.json", flashed)
                validate_node(interface, flashed, profile)
                if flashed["metadata"].get("firmwareVersion") != manifest["version"] or flashed["myInfo"].get("pioEnv") != "rak4631":
                    raise UpdateError("Firmware readback differs from the pinned binary version.")
                assert_preserved(before, flashed)
                print("Saving the 3-minute fitted-sensor profile...", file=console, flush=True)
                configure_in_memory(interface, profiles, profile)
                interface.localNode.beginSettingsTransaction()
                for section in ("device", "telemetry", "neighbor_info"):
                    interface.localNode.writeConfig(section)
                    time.sleep(0.2)
                interface.localNode.commitSettingsTransaction()
                time.sleep(2)
            finally:
                interface.close()
            time.sleep(15)
            interface, current_port = wait_application(profile)
            try:
                final = snapshot(interface, current_port, profile["usbSerial"])
                private_json(bench / "verified.json", final)
                validate_node(interface, final, profile)
                assert_preserved(intended, final)
                if final["metadata"].get("firmwareVersion") != manifest["version"]:
                    raise UpdateError("Final firmware version does not match the pinned release.")
                interface.localNode.reboot(2)
                time.sleep(1)
            finally:
                interface.close()
            time.sleep(12)
            print("Independently checking the complete saved profile after reboot...", file=console, flush=True)
            interface, current_port = wait_application(profile)
            try:
                rebooted = snapshot(interface, current_port, profile["usbSerial"])
                private_json(bench / "reboot-verified.json", rebooted)
                validate_node(interface, rebooted, profile)
                assert_preserved(intended, rebooted)
                interface.localNode.setTime()
                time.sleep(1)
            finally:
                interface.close()
        private_json(bench / "result.json", {"number": number, "release": manifest["tag"], "version": manifest["version"], "publishedArtifact": manifest.get("publishedArtifact", True), "uf2Sha256": hashlib.sha256(image.read_bytes()).hexdigest(), "fullProfileVerifiedAfterReboot": True, "gatewayDeliveryVerified": False})
        private_json(bench / "finalverified-radio.json", {
            "schemaVersion": 1, "repeaterNumber": number, "nodeId": profile["nodeId"],
            "hardwareId": rebooted["hardwareId"], "hwModel": "RAK4631",
            "version": manifest["version"], "source": manifest["source"],
            "releaseTag": manifest["tag"], "uf2Sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
            "publishedArtifact": manifest.get("publishedArtifact", True),
            "keysPreserved": True, "profileVerified": True,
            "deviceTelemetrySeconds": profiles["reportIntervalSeconds"],
            "powerTelemetrySeconds": profiles["reportIntervalSeconds"],
            "environmentTelemetrySeconds": profiles["reportIntervalSeconds"],
            "environmentMeasurementEnabled": profile["environment"],
            "powerMeasurementEnabled": profile["power"],
            "sensorProfile": ("environment-and-ina219" if profile["environment"] else "ina219-only") if profile["power"] else "environment-only",
            "noTemperatureSensor": not profile["environment"],
            "effectiveSnnsCadenceSeconds": manifest["snorrNeighborLoraIntervalSeconds"],
            "standardNeighborInfoIntervalSeconds": profiles["standardNeighborIntervalSeconds"],
        })
        print(f"PASS {number}: {manifest['version']}; complete intended profile/identity/keys verified after reboot.")
        print("Serial closed. Fresh RF/MQTT/portal receipt and sustained cadence still require observation.")
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        if bench and bench.is_dir():
            with contextlib.suppress(OSError):
                (bench / "failure.log").write_text(traceback.format_exc(), encoding="utf-8")
        if isinstance(exc, UpdateError):
            print(f"STOP: {exc}", file=sys.stderr)
        else:
            print("STOP: update failed or was interrupted; inspect the retained private evidence before retrying." if bench else "STOP: could not prepare the updater; check the release pin, dependencies and connected board.", file=sys.stderr)
        return 1
    finally:
        if dry_run_complete:
            print("Dry run complete: backup and verified image retained; no flash or saved configuration writes.")


if __name__ == "__main__":
    raise SystemExit(main())

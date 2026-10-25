#!/usr/bin/env python3
"""Set one inventoried RAK's long name, role, fixed location and B002 admin access."""

import argparse
import base64
import copy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import importlib.util
import json
import logging
import os
from pathlib import Path
import sys
import threading
import time
import traceback

SPEC = importlib.util.spec_from_file_location(
    "repeater_updater", Path(__file__).with_name("update-repeater.py"))
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)

# Public key only, from B002 !699ca878's matching 2026-10-24 reboot readbacks.
B002_PUBLIC_KEY = "l5VRR8C6wnkeSNP1KiYKPYEBv/Of10/4rU+VHmlq2ks="


def prompt_name():
    while True:
        name = input("Meshtastic long name (short name stays unchanged): ").strip()
        # Firmware User.long_name is a 40-byte C string, including its terminator.
        if name and len(name.encode("utf-8")) <= 39 and not any(ord(c) < 32 or ord(c) == 127 for c in name):
            return name
        print("Enter a nonblank name of at most 39 UTF-8 bytes, without control characters.")


def write_reconciliation(evidence, report):
    """Readable private handoff; deliberately exclude keys and complete profiles."""
    lines = ["SNORR router configuration — portal reconciliation", *(
        f"{key}: {value}" for key, value in report.items())]
    before_path = evidence / "before.json"
    if before_path.exists():
        try:
            before = json.loads(before_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # A failed backup may have left partial JSON; still finalize the log.
            before = {}
            lines.append("Before snapshot: unreadable/incomplete; inspect failure.log")
        user = before.get("user", {})
        lines.extend([
            f"Previous long name: {user.get('longName', '(unknown)')}",
            f"Preserved short name: {user.get('shortName', '(unknown)')}",
            f"Firmware: {before.get('metadata', {}).get('firmwareVersion', '(unknown)')}",
        ])
    lines.extend([
        "B002 admin: requested; preserve existing admins",
        "Portal database: not updated by this script; reconcile only against verified radio state",
        "RF/gateway delivery: not verified by this script",
        "Evidence: " + str(evidence),
    ])
    path = evidence / "reconciliation.txt"
    pending = evidence / "reconciliation.tmp"
    pending.write_text("\n".join(lines) + "\n", encoding="utf-8")
    pending.chmod(0o600)
    pending.replace(path)


def coordinate(value, limit):
    try:
        decimal = Decimal(value.strip())
        if not decimal.is_finite() or abs(decimal) > limit:
            raise ValueError()
        return int((decimal * 10_000_000).to_integral_value(rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError):
        raise updater.UpdateError(f"Enter decimal degrees between -{limit} and {limit}.") from None


def prompt_location():
    values = []
    for label, limit in (("Latitude", 90), ("Longitude", 180)):
        while True:
            try:
                values.append(coordinate(input(f"{label} (decimal degrees): "), limit))
                break
            except updater.UpdateError as error:
                print(str(error))
    return tuple(values)


def capture(interface, port, profile):
    # PhoneAPI substitutes role defaults for power.ls_secs; read the saved value.
    phone_power = updater.wire(interface.localNode.localConfig.power)
    interface.localNode.localConfig.power.CopyFrom(read_saved_power(interface))
    state = updater.snapshot(interface, port, profile["usbSerial"])
    state["phoneApiPowerWire"] = phone_power
    state["user"].setdefault("isUnmessagable", False)
    state["savedPosition"] = copy.deepcopy(interface.getMyNodeInfo().get("position", {}))
    state["savedPosition"].pop("raw", None)
    return state


def read_saved_power(interface):
    from meshtastic.protobuf import admin_pb2, config_pb2

    event = threading.Event()
    power = config_pb2.Config.PowerConfig()

    def received(packet):
        raw = packet.get("decoded", {}).get("admin", {}).get("raw")
        if raw is not None and raw.HasField("get_config_response") and raw.get_config_response.HasField("power"):
            power.CopyFrom(raw.get_config_response.power)
            event.set()

    request = admin_pb2.AdminMessage(get_config_request=admin_pb2.AdminMessage.POWER_CONFIG)
    interface.localNode._sendAdmin(request, wantResponse=True, onResponse=received)
    if not event.wait(15):
        raise updater.UpdateError("Saved power config read timed out; no automatic retry or write.")
    return power


def assert_metadata(intended, actual):
    wanted, saved = copy.deepcopy(intended["metadata"]), copy.deepcopy(actual["metadata"])
    if wanted.pop("role", "CLIENT") != saved.pop("role", "CLIENT") or wanted != saved:
        raise updater.UpdateError("Firmware metadata or announced role changed unexpectedly; inspect private evidence.")


def position_matches(position, coordinates):
    # SDK NodeInfo dictionaries expose protobuf latitudeI/longitudeI.
    try:
        return bool(position) and all(int(position.get(field, 0)) == expected for field, expected in
                   zip(("latitudeI", "longitudeI"), coordinates))
    except (KeyError, ValueError, TypeError):
        return False


def change_role(interface, port, profile, role, apply, evidence, coordinates, long_name):
    """Validate and back up before saving the selected settings in a transaction."""
    before = capture(interface, port, profile)
    updater.validate_node(interface, before, profile)
    updater.private_json(evidence / "before.json", before)
    config = interface.localNode.localConfig
    key = base64.b64decode(B002_PUBLIC_KEY, validate=True)
    if len(key) != 32 or not any(key):
        raise updater.UpdateError("Invalid recorded B002 public key.")
    admins = config.security.admin_key
    if key not in admins and len(admins) >= 3:
        raise updater.UpdateError("All three admin key slots are occupied; existing keys were preserved. Resolve the allowlist before retrying.")
    original_wire = updater.wire(config)
    device = config.device
    roles = device.DESCRIPTOR.fields_by_name["role"].enum_type
    previous = roles.values_by_number[device.role].name
    device.role = roles.values_by_name[role].number
    config.position.fixed_position = True
    if key not in admins:
        admins.append(key)
    intended = capture(interface, port, profile)
    intended["user"]["longName"] = long_name
    intended["metadata"]["role"] = role
    intended["fixedCoordinates"] = list(coordinates)
    updater.private_json(evidence / "intended.json", intended)
    changed = (original_wire != updater.wire(config)
               or before["user"].get("longName") != long_name
               or not position_matches(before["savedPosition"], coordinates))
    if not apply or not changed:
        return previous, intended, False
    # No retry: a lost response can follow an executed/rebooting write.
    node = interface.localNode
    node.beginSettingsTransaction()
    for section in ("device", "position", "security"):
        node.writeConfig(section)
        time.sleep(0.2)
    if before["user"].get("longName") != long_name:
        # Omit short_name entirely; preserve flags the SDK would otherwise default.
        node.setOwner(long_name=long_name,
                      is_licensed=before["user"].get("isLicensed", False),
                      is_unmessagable=before["user"].get("isUnmessagable"))
        time.sleep(0.2)
    # Integer coordinates avoid binary floating point truncation in the SDK.
    # Keep the existing altitude (or 0/unspecified); no elevation is invented.
    node.setFixedPosition(coordinates[0], coordinates[1], before["savedPosition"].get("altitude", 0))
    time.sleep(0.2)
    node.commitSettingsTransaction()
    time.sleep(2)
    return previous, intended, True


def restore_role_defaults(profile, intended, evidence):
    """One planned restoration after the new role has taken effect; never retry."""
    from meshtastic.protobuf import localonly_pb2

    interface, port = updater.wait_application(profile)
    try:
        actual = capture(interface, port, profile)
        updater.private_json(evidence / "role-defaults.json", actual)
        updater.validate_node(interface, actual, profile)
        assert_metadata(intended, actual)
        if not position_matches(actual["savedPosition"], intended["fixedCoordinates"]):
            raise updater.UpdateError("Fixed point changed after role save; restoration stopped.")
        wanted_local = localonly_pb2.LocalConfig.FromString(base64.b64decode(intended["localWire"]))
        wanted_module = localonly_pb2.LocalModuleConfig.FromString(base64.b64decode(intended["moduleWire"]))
        local = copy.deepcopy(interface.localNode.localConfig)
        module = copy.deepcopy(interface.localNode.moduleConfig)
        if local.device.role != wanted_local.device.role:
            raise updater.UpdateError("Saved role does not match the request; restoration stopped.")
        # Only fields changed by NodeDB::installRoleDefaults and its interval helpers.
        local_fields = {
            "device": ("rebroadcast_mode",),
            "position": ("gps_update_interval", "position_broadcast_secs"),
            "power": ("ls_secs", "min_wake_secs", "sds_secs", "wait_bluetooth_secs", "is_power_saving"),
            "display": ("screen_on_secs",),
        }
        module_fields = {
            "telemetry": ("device_update_interval", "environment_update_interval", "power_update_interval",
                          "air_quality_interval", "health_update_interval"),
            "neighbor_info": ("update_interval",),
            "paxcounter": ("paxcounter_update_interval",),
        }
        sections = []
        for current, wanted, fields in ((local, wanted_local, local_fields), (module, wanted_module, module_fields)):
            for section, names in fields.items():
                values, target = getattr(current, section), getattr(wanted, section)
                original = updater.wire(values)
                for field in names:
                    if getattr(values, field) != getattr(target, field):
                        setattr(values, field, getattr(target, field))
                if original != updater.wire(values):
                    sections.append(section)
        proposed = copy.deepcopy(actual)
        proposed["localWire"], proposed["moduleWire"] = updater.wire(local), updater.wire(module)
        proposed["user"]["isUnmessagable"] = intended["user"]["isUnmessagable"]
        # Any changed key/channel/identity or setting outside the known reset fields stops writes.
        updater.assert_preserved(intended, proposed)
        owner_changed = actual["user"]["isUnmessagable"] != intended["user"]["isUnmessagable"]
        updater.private_json(evidence / "restoration-plan.json", {"sections": sections, "ownerFlag": owner_changed})
        if not sections and not owner_changed:
            return False
        node = interface.localNode
        node.localConfig.CopyFrom(local)
        node.moduleConfig.CopyFrom(module)
        node.beginSettingsTransaction()
        for section in sections:
            node.writeConfig(section)
            time.sleep(0.2)
        if owner_changed:
            node.setOwner(long_name=intended["user"]["longName"],
                          is_licensed=intended["user"].get("isLicensed", False),
                          is_unmessagable=intended["user"]["isUnmessagable"])
            time.sleep(0.2)
        node.commitSettingsTransaction()
        time.sleep(1)
        return True
    finally:
        interface.close()


def verify(profile, intended, evidence, name):
    interface, port = updater.wait_application(profile)
    try:
        actual = capture(interface, port, profile)
        updater.private_json(evidence / name, actual)
        updater.validate_node(interface, actual, profile)
        updater.assert_preserved(intended, actual)
        assert_metadata(intended, actual)
        if not position_matches(actual["savedPosition"], intended["fixedCoordinates"]):
            raise updater.UpdateError("Saved fixed coordinates do not match; inspect private evidence.")
    finally:
        interface.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", help="R001 through R006 (one connected RAK)")
    parser.add_argument("--role", choices=("ROUTER", "CLIENT"), default="ROUTER")
    parser.add_argument("--port", help="Optional port; recorded USB serial must still match")
    parser.add_argument("--apply", action="store_true", help="Save long name, role, fixed location and B002 admin; default only reads/backups")
    args = parser.parse_args(argv)
    evidence = None
    report = {}
    old_umask = os.umask(0o077)
    old_logging_disable = logging.root.manager.disable
    try:
        number = updater.normalize_number(args.number)
        long_name = prompt_name()
        coordinates = prompt_location()
        print(f"Plan: {number} -> {args.role}; long name {long_name!r}; preserve short name; set fixed location; authorize B002 !699ca878 (preserving existing admins).")
        profile = json.loads(updater.PROFILE_PATH.read_text())["nodes"][number]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        evidence = updater.ROOT / "private" / "bench" / f"{number}-role-{stamp}"
        evidence.mkdir(parents=True, mode=0o700)
        report = {
            "Started UTC": datetime.now(timezone.utc).isoformat(),
            "Device number": number, "Node ID": profile["nodeId"],
            "USB serial": profile["usbSerial"],
            "Mode": "APPLY" if args.apply else "READ ONLY",
            "Requested long name": long_name, "Requested role": args.role,
            "Requested fixed latitude": f"{Decimal(coordinates[0]) / 10_000_000:.7f}",
            "Requested fixed longitude": f"{Decimal(coordinates[1]) / 10_000_000:.7f}",
            "Result": "IN PROGRESS — saved state unverified",
            "Post-save verification": "not completed",
            "Post-reboot verification": "not completed",
            "Role-default restoration": "not attempted",
        }
        write_reconciliation(evidence, report)
        print(f"Private reconciliation log: {evidence / 'reconciliation.txt'}", flush=True)
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            raise updater.UpdateError("Install scripts/bench/repeater-requirements.txt in a Python virtual environment.") from None
        port = updater.select_port(comports(), profile, args.port)
        print(f"{number} {profile['nodeId']} on {port.device}; private backup: {evidence}", flush=True)
        logging.disable(logging.CRITICAL)
        with (evidence / "serial.log").open("x", encoding="utf-8") as log, updater.quiet_serial(log):
            interface = updater.connect(port.device)
            try:
                previous, intended, changed = change_role(
                    interface, port.device, profile, args.role, args.apply, evidence, coordinates, long_name)
            finally:
                interface.close()
            if changed:
                time.sleep(15)
                restored = False
                if previous != args.role:
                    restored = restore_role_defaults(profile, intended, evidence)
                    report["Role-default restoration"] = "saved; awaiting verification" if restored else "checked; no reset fields differed"
                    write_reconciliation(evidence, report)
                    if restored:
                        time.sleep(15)
                else:
                    report["Role-default restoration"] = "not needed; role unchanged"
                verify(profile, intended, evidence, "verified.json")
                report["Post-save verification"] = "passed"
                write_reconciliation(evidence, report)
                # Explicit reboot proves the role persisted, beyond a live config read.
                interface, _ = updater.wait_application(profile)
                try:
                    interface.localNode.reboot(2)
                    time.sleep(1)
                finally:
                    interface.close()
                time.sleep(12)
                verify(profile, intended, evidence, "reboot-verified.json")
                report["Post-reboot verification"] = "passed"
                if restored:
                    report["Role-default restoration"] = "verified through reboot"
        if changed:
            report["Result"] = "VERIFIED THROUGH REBOOT"
            print(f"{number}: {previous} -> {args.role}; long name, fixed location and B002 admin saved; short name preserved; full profile verified through reboot.")
        elif args.apply:
            report["Result"] = "ALREADY MATCHED — backed up, no write or reboot performed"
            print(f"{number}: long name, role, fixed location and B002 admin already match; backed up, no write needed.")
        else:
            report["Result"] = "READ ONLY — proposed settings were not saved"
            print(f"READ ONLY: {number} is {previous}; proposed long name, {args.role}, fixed location and B002 admin. Repeat with --apply to save.")
        return 0
    except (Exception, KeyboardInterrupt) as error:
        report["Result"] = "FAILED — saved state unverified; inspect evidence before reconciling or retrying"
        report["Failure type"] = type(error).__name__
        if evidence:
            with (evidence / "failure.log").open("w", encoding="utf-8") as log:
                traceback.print_exc(file=log)
        print("Configuration operation failed. No automatic retry or rollback. Inspect private evidence; read saved role, position and admins over USB before retrying.", file=sys.stderr)
        if isinstance(error, updater.UpdateError):
            print(str(error), file=sys.stderr)
        if evidence:
            print(f"Private evidence: {evidence}", file=sys.stderr)
        return 1
    finally:
        try:
            if evidence and evidence.is_dir():
                report["Finished UTC"] = datetime.now(timezone.utc).isoformat()
                write_reconciliation(evidence, report)
        finally:
            logging.disable(old_logging_disable)
            os.umask(old_umask)


if __name__ == "__main__":
    sys.exit(main())

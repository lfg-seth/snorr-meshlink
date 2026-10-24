"""Offline checks: no serial ports, USB writes or network calls."""

import copy
import importlib.util
import json
import hashlib
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "update-repeater.py"
SPEC = importlib.util.spec_from_file_location("update_repeater", SCRIPT)
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


def port(name, serial):
    return SimpleNamespace(device=name, serial_number=serial)


def uf2_block(address=0x26000, family=0xADA52840, number=0, total=1):
    data = bytearray(512)
    struct.pack_into("<8I", data, 0, 0x0A324655, 0x9E5D5157, 0x2000, address, 256, number, total, family)
    struct.pack_into("<I", data, 508, 0x0AB16F30)
    return data


class IdentityChecks(unittest.TestCase):
    def setUp(self):
        self.profile = {"usbSerial": "E9B12C5CA98FBCB8"}

    def test_friendly_numbers(self):
        for value in ("6", "006", "r006", " R6 "):
            self.assertEqual(updater.normalize_number(value), "R006")

    def test_unknown_numbers_fail(self):
        for value in ("0", "7", "R007", "R006;echo", "G001", ""):
            with self.subTest(value=value), self.assertRaises(updater.UpdateError):
                updater.normalize_number(value)

    def test_port_uses_usb_serial_not_last_com(self):
        selected = updater.select_port([port("COM21", "E9B12C5CA98FBCB8"), port("COM5", "OTHER")], self.profile)
        self.assertEqual(selected.device, "COM21")

    def test_explicit_other_port_fails(self):
        with self.assertRaises(updater.UpdateError):
            updater.select_port([port("COM21", "E9B12C5CA98FBCB8"), port("COM5", "OTHER")], self.profile, "COM5")

    def test_missing_or_duplicate_serial_fails(self):
        for ports in ([], [port("COM5", None)], [port("COM1", "E9B12C5CA98FBCB8"), port("COM2", "E9B12C5CA98FBCB8")]):
            with self.assertRaises(updater.UpdateError):
                updater.select_port(ports, self.profile)

    def test_windows_disk_identity_is_exact_token(self):
        expected = self.profile["usbSerial"]
        self.assertTrue(updater.disk_matches(None, rf"USBSTOR\DISK&VEN_ADAFRUIT\{expected}&0", expected))
        self.assertFalse(updater.disk_matches(None, rf"USBSTOR\OTHER{expected}&0", expected))
        self.assertFalse(updater.disk_matches("OTHER", "", expected))

    def test_same_usb_dfu_port_can_change_name(self):
        selected = updater.select_port([port("COM22", "e9b12c5ca98fbcb8")], self.profile)
        self.assertEqual(selected.device, "COM22")

    def test_uf2_volume_rejects_wrong_board_and_other_usb(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            info = root / "INFO_UF2.TXT"
            info.write_text("Board-ID: Feather-nRF52840\n")
            rows = [{"root": str(root), "serial": "OTHER"}]
            self.assertIsNone(updater.find_uf2_volume(rows, self.profile["usbSerial"]))
            rows[0]["serial"] = self.profile["usbSerial"]
            with self.assertRaises(updater.UpdateError):
                updater.find_uf2_volume(rows, self.profile["usbSerial"])
            info.write_text("UF2 Bootloader 0.4.3\nBoard-ID: WisBlock-RAK4631-Board\n")
            self.assertEqual(updater.find_uf2_volume(rows, self.profile["usbSerial"]), root)
            with self.assertRaises(updater.UpdateError):
                updater.find_uf2_volume(rows * 2, self.profile["usbSerial"])


class ImageChecks(unittest.TestCase):
    def validate(self, data):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "firmware.uf2"
            path.write_bytes(data)
            updater.validate_uf2(path)

    def test_application_only_uf2(self):
        self.validate(uf2_block())

    def test_bootloader_softdevice_settings_and_other_family_fail(self):
        for block in (uf2_block(0), uf2_block(0xED000), uf2_block(family=0xE48BFF56)):
            with self.assertRaises(updater.UpdateError):
                self.validate(block)

    def test_duplicate_blocks_and_invalid_number_fail(self):
        with self.assertRaises(updater.UpdateError):
            self.validate(uf2_block(total=2) + uf2_block(number=1, total=2))
        with self.assertRaises(updater.UpdateError):
            self.validate(uf2_block(number=1))

    def test_partial_image_and_wrong_magic_fail(self):
        for data in (b"", uf2_block()[:-1], bytes(512)):
            with self.assertRaises(updater.UpdateError):
                self.validate(data)

    def test_unpinned_release_cannot_flash(self):
        for tag in (None, "latest", "../secret", "snorr-rak4631-2.7.26.0000000"):
            with self.assertRaises(updater.UpdateError):
                updater.load_release({"releaseTag": tag})


class ConfigurationChecks(unittest.TestCase):
    def setUp(self):
        self.profiles = json.loads(updater.PROFILE_PATH.read_text())

    def test_private_channel_gate_rejects_full_public_default_key_family(self):
        from meshtastic.util import DEFAULT_KEY

        settings = SimpleNamespace(name="pilot-fixture", psk=DEFAULT_KEY)
        interface = SimpleNamespace(localNode=SimpleNamespace(
            localConfig=SimpleNamespace(
                security=SimpleNamespace(private_key=bytes(range(32)), public_key=bytes(range(1, 33))),
                lora=SimpleNamespace(region=1, tx_enabled=True),
            ),
            channels=[SimpleNamespace(role=1, settings=settings)],
        ))
        state = {"user": {"id": "!fixture", "hwModel": "RAK4631"}, "metadata": {"hwModel": "RAK4631"}}
        profile = {"nodeId": "!fixture"}
        public_keys = [DEFAULT_KEY, b"", b"\x01", bytes(16)]
        public_keys.extend(DEFAULT_KEY[:15] + bytes([index]) for index in range(256))
        for key in public_keys:
            settings.psk = key
            with self.assertRaisesRegex(updater.UpdateError, "private primary channel"):
                updater.validate_node(interface, state, profile)
        for size in (16, 32):
            settings.psk = bytes(range(1, size + 1))
            updater.validate_node(interface, state, profile)

    def test_tracked_sensor_exceptions(self):
        for number, profile in self.profiles["nodes"].items():
            self.assertEqual(profile["environment"], number != "R006")
            self.assertEqual(profile["power"], number in ("R004", "R006"))
        self.assertEqual(len({p["nodeId"] for p in self.profiles["nodes"].values()}), 6)
        self.assertEqual(len({p["usbSerial"] for p in self.profiles["nodes"].values()}), 6)

    def test_fitted_stats_180_and_standard_neighbor_separate(self):
        for number, profile in self.profiles["nodes"].items():
            with self.subTest(number=number):
                local = SimpleNamespace(device=SimpleNamespace(role=2), security="private identity", lora="private pilot radio", power="existing INA address")
                modules = SimpleNamespace(telemetry=SimpleNamespace(), neighbor_info=SimpleNamespace(), mqtt="preserved")
                interface = SimpleNamespace(localNode=SimpleNamespace(localConfig=local, moduleConfig=modules))
                updater.configure_in_memory(interface, self.profiles, profile)
                self.assertEqual(local.device.role, 0)
                self.assertEqual(local.security, "private identity")
                self.assertEqual(local.lora, "private pilot radio")
                self.assertEqual(local.power, "existing INA address")
                self.assertEqual(modules.telemetry.device_update_interval, 180)
                self.assertEqual(modules.telemetry.environment_update_interval, 180)
                self.assertEqual(modules.telemetry.power_update_interval, 180)
                self.assertTrue(modules.telemetry.device_telemetry_enabled)
                self.assertEqual(modules.telemetry.environment_measurement_enabled, profile["environment"])
                self.assertEqual(modules.telemetry.power_measurement_enabled, profile["power"])
                self.assertTrue(modules.neighbor_info.enabled)
                self.assertTrue(modules.neighbor_info.transmit_over_lora)
                self.assertEqual(modules.neighbor_info.update_interval, 21600)
                self.assertEqual(modules.mqtt, "preserved")

    def test_full_preservation_detects_keys_channels_or_owner_changes(self):
        before = {"localWire": "all-local-config-and-keys", "moduleWire": "all-modules", "channelsWire": ["private-channel"], "user": {"id": "!fixture", "longName": "R006", "publicKey": "existing-key"}}
        updater.assert_preserved(before, copy.deepcopy(before))
        for field in ("localWire", "moduleWire", "channelsWire", "user"):
            changed = copy.deepcopy(before)
            changed[field] = {} if field == "user" else "different"
            with self.assertRaises(updater.UpdateError):
                updater.assert_preserved(before, changed)

    def test_firmware_metadata_is_not_confused_with_saved_config(self):
        before = {"localWire": "same", "moduleWire": "same", "channelsWire": [], "user": {"id": "!fixture"}, "metadata": {"firmwareVersion": "old"}}
        after = copy.deepcopy(before)
        after["metadata"]["firmwareVersion"] = "new"
        updater.assert_preserved(before, after)

    def test_plan_never_opens_hardware(self):
        with patch.object(updater, "connect", side_effect=AssertionError("Must not access hardware")), patch.object(updater, "released_image", side_effect=AssertionError("Must not download")):
            self.assertEqual(updater.main(["--number", "6", "--show-plan"]), 0)

    def test_private_json_never_overwrites_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "before.json"
            updater.private_json(path, {"protected": True})
            with self.assertRaises(FileExistsError):
                updater.private_json(path, {"protected": False})
            self.assertEqual(json.loads(path.read_text()), {"protected": True})


class LocalBundleChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bundle = self.root / "bundle"
        self.bundle.mkdir()
        self.manifest_path = self.root / "tracked-local.json"
        self.manifest = json.loads(updater.LOCAL_MANIFEST_PATH.read_bytes())
        payloads = [uf2_block(), b"synthetic OTA fixture"]
        for asset, payload in zip(self.manifest["artifacts"], payloads):
            asset["bytes"] = len(payload)
            asset["sha256"] = hashlib.sha256(payload).hexdigest()
            (self.bundle / asset["name"]).write_bytes(payload)
        self.write_manifests()
        self.patcher = patch.object(updater, "LOCAL_MANIFEST_PATH", self.manifest_path)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def write_manifests(self):
        manifest_bytes = (json.dumps(self.manifest, indent=2) + "\n").encode()
        self.manifest_path.write_bytes(manifest_bytes)
        (self.bundle / "build-manifest.json").write_bytes(manifest_bytes)
        checksums = "".join(f"{asset['sha256']}  {asset['name']}\n" for asset in self.manifest["artifacts"])
        (self.bundle / "SHA256SUMS").write_bytes(checksums.encode())

    def test_explicit_local_bundle_and_unpublished_provenance(self):
        manifest, _, image = updater.local_bundle_image(self.bundle)
        self.assertIs(manifest["publishedArtifact"], False)
        self.assertIs(manifest["hardwareVerified"], False)
        self.assertEqual(image.name, "firmware-rak4631-2.7.26.0634b77.uf2")

    def test_fixed_contract_rejects_published_claim_or_different_source(self):
        for key, value in (("publishedArtifact", True), ("hardwareVerified", True), ("source", "0" * 40), ("snorrNeighborLoraIntervalSeconds", 300)):
            with self.subTest(key=key):
                original = self.manifest[key]
                self.manifest[key] = value
                self.write_manifests()
                with self.assertRaises(updater.UpdateError):
                    updater.local_bundle_image(self.bundle)
                self.manifest[key] = original

    def test_local_bundle_requires_exact_manifest_bytes(self):
        path = self.bundle / "build-manifest.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "manifest differs"):
            updater.local_bundle_image(self.bundle)

    def test_local_bundle_rejects_modified_asset(self):
        path = self.bundle / self.manifest["artifacts"][0]["name"]
        data = bytearray(path.read_bytes())
        data[100] ^= 1
        path.write_bytes(data)
        with self.assertRaisesRegex(ValueError, "Size/SHA256 mismatch"):
            updater.local_bundle_image(self.bundle)

    def test_local_bundle_rejects_extra_missing_or_changed_checksums(self):
        extra = self.bundle / "extra.txt"
        extra.write_text("unexpected")
        with self.assertRaisesRegex(ValueError, "asset set differs"):
            updater.local_bundle_image(self.bundle)
        extra.unlink()
        sums = self.bundle / "SHA256SUMS"
        sums.write_text("altered")
        with self.assertRaisesRegex(ValueError, "Checksum list differs"):
            updater.local_bundle_image(self.bundle)
        sums.unlink()
        with self.assertRaisesRegex(ValueError, "asset set differs"):
            updater.local_bundle_image(self.bundle)

    def test_default_never_implicitly_uses_local_bundle(self):
        with patch.object(updater, "load_release", side_effect=updater.UpdateError("Public pin pending")) as public, patch.object(updater, "local_bundle_image") as local:
            self.assertEqual(updater.main(["--number", "R006"]), 1)
            public.assert_called_once()
            local.assert_not_called()

    def test_unpublished_manifest_cannot_be_used_as_public_pin(self):
        manifest_dir = self.root / "firmware" / ".github" / "releases"
        manifest_dir.mkdir(parents=True)
        tag = self.manifest["tag"]
        (manifest_dir / f"{tag}.json").write_bytes(self.manifest_path.read_bytes())
        with patch.object(updater, "ROOT", self.root), self.assertRaisesRegex(updater.UpdateError, "requires explicit --local-bundle"):
            updater.load_release({"releaseTag": tag})

    def test_explicit_flag_selects_local_instead_of_public(self):
        with patch.object(updater, "load_release") as public, patch.object(updater, "local_bundle_image", side_effect=updater.UpdateError("Selected explicit local bundle")) as local:
            self.assertEqual(updater.main(["--number", "R006", "--local-bundle", str(self.bundle)]), 1)
            local.assert_called_once_with(self.bundle.resolve())
            public.assert_not_called()


class DfuModeChecks(unittest.TestCase):
    def prepare(self, dry_run=False, config_only=False, backup_failure=False, storage_failure=False):
        self.events = []
        interface = SimpleNamespace(
            localNode=SimpleNamespace(enterDFUMode=lambda: self.events.append("API DFU")),
            close=lambda: self.events.append("close"),
        )
        def save(path, _state):
            self.events.append(path.name)
            if backup_failure and path.name == "intended.json":
                raise OSError("backup failure")
        def enumerate_volumes():
            self.events.append("storage preflight")
            if storage_failure:
                raise OSError("storage unavailable")
            return []
        with patch.object(updater, "snapshot", side_effect=[{"state": "before"}, {"state": "intended"}]), patch.object(updater, "validate_node", side_effect=lambda *_: self.events.append("identity validated")), patch.object(updater, "private_json", side_effect=save), patch.object(updater, "configure_in_memory"), patch.object(updater, "uf2_volume_reader", return_value=enumerate_volumes), patch.object(updater.time, "sleep"):
            return updater.prepare_node_for_update(interface, "COM1", {}, {"usbSerial": "fixture"}, Path("private/fixture"), dry_run, config_only)

    def test_normal_update_requests_api_dfu_after_backups_before_close(self):
        before, intended = self.prepare()
        self.assertEqual(before, {"state": "before"})
        self.assertEqual(intended, {"state": "intended"})
        self.assertEqual(self.events, ["identity validated", "before.json", "intended.json", "storage preflight", "API DFU", "close"])

    def test_dry_run_never_requests_dfu(self):
        self.prepare(dry_run=True)
        self.assertEqual(self.events, ["identity validated", "before.json", "intended.json", "close"])

    def test_config_only_never_requests_dfu(self):
        self.prepare(config_only=True)
        self.assertEqual(self.events, ["identity validated", "before.json", "intended.json", "close"])

    def test_backup_failure_never_requests_dfu_and_closes(self):
        with self.assertRaises(OSError):
            self.prepare(backup_failure=True)
        self.assertNotIn("API DFU", self.events)
        self.assertEqual(self.events[-1], "close")

    def test_storage_failure_never_requests_dfu_and_closes(self):
        with self.assertRaises(OSError):
            self.prepare(storage_failure=True)
        self.assertNotIn("API DFU", self.events)
        self.assertEqual(self.events[-1], "close")

    def test_uf2_writer_only_waits_for_identified_volume(self):
        with patch.object(updater, "uf2_volume_reader", return_value=lambda: [{"root": "fixture"}]), patch.object(updater, "find_uf2_volume", return_value=Path("identified-volume")) as find, patch.object(updater.shutil, "copyfile") as copyfile, patch.object(updater, "connect", side_effect=AssertionError("No application connection in UF2 writer")):
            updater.flash_uf2({"usbSerial": "fixture-serial"}, Path("application.uf2"))
            find.assert_called_once_with([{"root": "fixture"}], "fixture-serial")
            copyfile.assert_called_once_with(Path("application.uf2"), Path("identified-volume/SNORR.UF2"))


if __name__ == "__main__":
    unittest.main()

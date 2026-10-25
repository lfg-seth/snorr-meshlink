"""Offline safety checks; these do not establish hardware acceptance."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

SPEC = importlib.util.spec_from_file_location(
    "set_repeater_role", Path(__file__).resolve().parents[1] / "set-repeater-role.py")
roles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(roles)


class RoleChangeTests(unittest.TestCase):
    def setUp(self):
        enum = SimpleNamespace(
            values_by_number={0: SimpleNamespace(name="CLIENT"), 2: SimpleNamespace(name="ROUTER")},
            values_by_name={"CLIENT": SimpleNamespace(number=0), "ROUTER": SimpleNamespace(number=2)})
        self.device = SimpleNamespace(role=0, sentinel="preserve", DESCRIPTOR=SimpleNamespace(
            fields_by_name={"role": SimpleNamespace(enum_type=enum)}))
        self.node = Mock(localConfig=SimpleNamespace(device=self.device))
        self.interface = Mock(localNode=self.node)
        self.profile = {"usbSerial": "recorded"}
        self.patches = [
            patch.object(roles.updater, "snapshot", side_effect=lambda *args: {"role": self.device.role}),
            patch.object(roles.updater, "validate_node"),
            patch.object(roles.updater, "private_json"),
            patch.object(roles.time, "sleep")]
        self.snapshot, self.validate, self.backup, _ = [p.start() for p in self.patches]
        for p in self.patches:
            self.addCleanup(p.stop)

    def change(self, apply=True, role="ROUTER"):
        return roles.change_role(self.interface, "/dev/test", self.profile, role, apply, Path("private"))

    def test_preview_never_writes(self):
        self.assertEqual(self.change(False), ("CLIENT", {"role": 2}, False))
        self.node.writeConfig.assert_not_called()

    def test_wrong_identity_stops_before_backup_or_write(self):
        self.validate.side_effect = roles.updater.UpdateError("identity mismatch")
        with self.assertRaises(roles.updater.UpdateError):
            self.change()
        self.backup.assert_not_called()
        self.node.writeConfig.assert_not_called()

    def test_backup_failure_prevents_write(self):
        self.backup.side_effect = OSError("disk full")
        with self.assertRaises(OSError):
            self.change()
        self.node.writeConfig.assert_not_called()

    def test_only_device_section_written_after_backup(self):
        def write(section):
            self.assertEqual(self.backup.call_count, 2)
            self.assertEqual(section, "device")
            self.assertEqual(self.device.sentinel, "preserve")
        self.node.writeConfig.side_effect = write
        self.assertTrue(self.change()[2])
        self.node.writeConfig.assert_called_once_with("device")

    def test_ambiguous_write_never_retried(self):
        self.node.writeConfig.side_effect = TimeoutError()
        with self.assertRaises(TimeoutError):
            self.change()
        self.node.writeConfig.assert_called_once()

    def test_already_selected_role_does_not_write(self):
        self.device.role = 2
        self.assertFalse(self.change()[2])
        self.node.writeConfig.assert_not_called()

    def test_client_rollback(self):
        self.device.role = 2
        self.assertEqual(self.change(role="CLIENT"), ("ROUTER", {"role": 0}, True))


class ReadbackTests(unittest.TestCase):
    def test_failed_profile_comparison_closes_connection(self):
        interface = Mock()
        with patch.object(roles.updater, "wait_application", return_value=(interface, "port")), \
                patch.object(roles.updater, "snapshot", return_value={}), \
                patch.object(roles.updater, "private_json"), \
                patch.object(roles.updater, "validate_node"), \
                patch.object(roles.updater, "assert_preserved", side_effect=roles.updater.UpdateError("mismatch")):
            with self.assertRaises(roles.updater.UpdateError):
                roles.verify({"usbSerial": "recorded"}, {}, Path("private"), "verified.json")
        interface.close.assert_called_once()

    def test_firmware_change_rejected_even_with_matching_profile(self):
        interface = Mock()
        with patch.object(roles.updater, "wait_application", return_value=(interface, "port")), \
                patch.object(roles.updater, "snapshot", return_value={"metadata": {"firmwareVersion": "other"}}), \
                patch.object(roles.updater, "private_json"), \
                patch.object(roles.updater, "validate_node"), \
                patch.object(roles.updater, "assert_preserved"):
            with self.assertRaises(roles.updater.UpdateError):
                roles.verify({"usbSerial": "recorded"}, {"metadata": {}}, Path("private"), "verified.json")
        interface.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()

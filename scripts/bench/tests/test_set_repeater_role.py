"""Offline safety checks; these do not establish hardware acceptance."""
import importlib.util
import base64
from pathlib import Path
import unittest
from unittest.mock import Mock, patch, call
from meshtastic.protobuf import localonly_pb2

SPEC = importlib.util.spec_from_file_location(
    "set_repeater_role", Path(__file__).resolve().parents[1] / "set-repeater-role.py")
roles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(roles)


class RoleChangeTests(unittest.TestCase):
    def setUp(self):
        self.config = localonly_pb2.LocalConfig()
        self.device = self.config.device
        self.device.node_info_broadcast_secs = 12345
        self.config.security.private_key = b"p" * 32
        self.config.security.admin_key.append(b"a" * 32)
        self.key = base64.b64decode(roles.B002_PUBLIC_KEY)
        self.node = Mock(localConfig=self.config)
        self.interface = Mock(localNode=self.node)
        self.coordinates = (361234567, -1157654321)
        self.position = {"latitudeI": 360000000, "longitudeI": -1150000000, "altitude": 2000}
        self.interface.getMyNodeInfo.return_value = {"position": self.position}
        self.profile = {"usbSerial": "recorded"}
        self.patches = [
            patch.object(roles.updater, "snapshot", side_effect=lambda *args: {"localWire": roles.updater.wire(self.config)}),
            patch.object(roles.updater, "validate_node"),
            patch.object(roles.updater, "private_json"),
            patch.object(roles.time, "sleep")]
        self.snapshot, self.validate, self.backup, _ = [p.start() for p in self.patches]
        for p in self.patches:
            self.addCleanup(p.stop)

    def change(self, apply=True, role="ROUTER"):
        return roles.change_role(self.interface, "/dev/test", self.profile, role, apply, Path("private"), self.coordinates)

    def test_preview_never_writes(self):
        self.assertFalse(self.change(False)[2])
        self.node.writeConfig.assert_not_called()
        self.node.beginSettingsTransaction.assert_not_called()
        self.node.setFixedPosition.assert_not_called()

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

    def test_profile_and_existing_admins_preserved(self):
        def write(section):
            self.assertEqual(self.backup.call_count, 2)
            self.assertEqual(self.device.node_info_broadcast_secs, 12345)
            self.assertEqual(self.config.security.private_key, b"p" * 32)
        self.node.writeConfig.side_effect = write
        self.assertTrue(self.change()[2])
        self.assertEqual(list(self.config.security.admin_key), [b"a" * 32, self.key])
        self.assertTrue(self.config.position.fixed_position)
        self.assertEqual(self.node.method_calls, [call.beginSettingsTransaction(),
            call.writeConfig("device"), call.writeConfig("position"), call.writeConfig("security"),
            call.setFixedPosition(*self.coordinates, 2000), call.commitSettingsTransaction()])

    def test_ambiguous_write_never_retried(self):
        self.node.writeConfig.side_effect = TimeoutError()
        with self.assertRaises(TimeoutError):
            self.change()
        self.node.writeConfig.assert_called_once()

    def test_already_selected_role_does_not_write(self):
        self.device.role = 2
        self.config.position.fixed_position = True
        self.config.security.admin_key.append(self.key)
        self.position.update(zip(("latitudeI", "longitudeI"), self.coordinates))
        self.assertFalse(self.change()[2])
        self.node.writeConfig.assert_not_called()

    def test_client_rollback(self):
        self.device.role = 2
        self.assertTrue(self.change(role="CLIENT")[2])
        self.assertEqual(self.device.role, 0)

    def test_admin_slots_full_stops_before_transaction(self):
        self.config.security.admin_key.extend([b"b" * 32, b"c" * 32])
        with self.assertRaises(roles.updater.UpdateError):
            self.change()
        self.node.beginSettingsTransaction.assert_not_called()
        self.assertEqual(len(self.config.security.admin_key), 3)

    def test_existing_b002_admin_is_not_duplicated_when_full(self):
        self.config.security.admin_key.extend([b"b" * 32, self.key])
        self.change()
        self.assertEqual(len(self.config.security.admin_key), 3)

    def test_role_already_matches_still_updates_location_and_admin(self):
        self.device.role = 2
        self.assertTrue(self.change()[2])
        self.node.setFixedPosition.assert_called_once()


class ReadbackTests(unittest.TestCase):
    def test_failed_profile_comparison_closes_connection(self):
        interface = Mock()
        with patch.object(roles.updater, "wait_application", return_value=(interface, "port")), \
                patch.object(roles, "capture", return_value={}), \
                patch.object(roles.updater, "private_json"), \
                patch.object(roles.updater, "validate_node"), \
                patch.object(roles.updater, "assert_preserved", side_effect=roles.updater.UpdateError("mismatch")):
            with self.assertRaises(roles.updater.UpdateError):
                roles.verify({"usbSerial": "recorded"}, {}, Path("private"), "verified.json")
        interface.close.assert_called_once()

    def test_firmware_change_rejected_even_with_matching_profile(self):
        interface = Mock()
        with patch.object(roles.updater, "wait_application", return_value=(interface, "port")), \
                patch.object(roles, "capture", return_value={"metadata": {"firmwareVersion": "other"}}), \
                patch.object(roles.updater, "private_json"), \
                patch.object(roles.updater, "validate_node"), \
                patch.object(roles.updater, "assert_preserved"):
            with self.assertRaises(roles.updater.UpdateError):
                roles.verify({"usbSerial": "recorded"}, {"metadata": {}}, Path("private"), "verified.json")
        interface.close.assert_called_once()

    def test_wrong_saved_coordinates_rejected(self):
        interface = Mock()
        with patch.object(roles.updater, "wait_application", return_value=(interface, "port")), \
                patch.object(roles, "capture", return_value={"metadata": {}, "savedPosition": {"latitudeI": 12}}), \
                patch.object(roles.updater, "private_json"), \
                patch.object(roles.updater, "validate_node"), \
                patch.object(roles.updater, "assert_preserved"):
            with self.assertRaises(roles.updater.UpdateError):
                roles.verify({"usbSerial": "recorded"}, {"metadata": {}, "fixedCoordinates": [10, 20]}, Path("private"), "verified.json")
        interface.close.assert_called_once()


class CoordinateTests(unittest.TestCase):
    def test_decimal_degrees_and_rounding(self):
        self.assertEqual(roles.coordinate(" -115.12345678 ", 180), -1151234568)
        self.assertEqual(roles.coordinate("0", 90), 0)
        self.assertEqual(roles.coordinate("90", 90), 900000000)

    def test_invalid_and_out_of_range_input(self):
        for value in ("nan", "Infinity", "", "36,123", "91", "-90.0000001"):
            with self.subTest(value=value), self.assertRaises(roles.updater.UpdateError):
                roles.coordinate(value, 90)

    def test_prompt_repeats_bad_input(self):
        with patch("builtins.input", side_effect=["bad", "36.1", "-115.2"]), patch("builtins.print"):
            self.assertEqual(roles.prompt_location(), (361000000, -1152000000))

    def test_zero_protobuf_defaults_and_missing_position(self):
        self.assertTrue(roles.position_matches({"longitudeI": 100}, (0, 100)))
        self.assertFalse(roles.position_matches({}, (0, 0)))


if __name__ == "__main__":
    unittest.main()

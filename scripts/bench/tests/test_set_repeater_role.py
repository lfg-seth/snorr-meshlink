"""Offline safety checks; these do not establish hardware acceptance."""
import importlib.util
import base64
import copy
from pathlib import Path
import tempfile
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
        self.user = {"longName": "Old site", "shortName": "R001", "isLicensed": True, "isUnmessagable": True}
        self.patches = [
            patch.object(roles.updater, "snapshot", side_effect=lambda *args: {"localWire": roles.updater.wire(self.config), "user": copy.deepcopy(self.user)}),
            patch.object(roles.updater, "validate_node"),
            patch.object(roles.updater, "private_json"),
            patch.object(roles.time, "sleep")]
        self.snapshot, self.validate, self.backup, _ = [p.start() for p in self.patches]
        for p in self.patches:
            self.addCleanup(p.stop)

    def change(self, apply=True, role="ROUTER"):
        return roles.change_role(self.interface, "/dev/test", self.profile, role, apply, Path("private"), self.coordinates, "New site")

    def test_preview_never_writes(self):
        self.assertFalse(self.change(False)[2])
        self.node.writeConfig.assert_not_called()
        self.node.beginSettingsTransaction.assert_not_called()
        self.node.setFixedPosition.assert_not_called()
        self.node.setOwner.assert_not_called()

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
            call.setOwner(long_name="New site", is_licensed=True, is_unmessagable=True),
            call.setFixedPosition(*self.coordinates, 2000), call.commitSettingsTransaction()])
        intended = self.backup.call_args.args[1]
        self.assertEqual(intended["user"], {**self.user, "longName": "New site"})

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
        self.user["longName"] = "New site"
        self.assertFalse(self.change()[2])
        self.node.writeConfig.assert_not_called()
        self.node.setOwner.assert_not_called()

    def test_name_only_change_is_saved_without_changing_short_name_or_flags(self):
        self.device.role = 2
        self.config.position.fixed_position = True
        self.config.security.admin_key.append(self.key)
        self.position.update(zip(("latitudeI", "longitudeI"), self.coordinates))
        self.assertTrue(self.change()[2])
        self.node.setOwner.assert_called_once_with(
            long_name="New site", is_licensed=True, is_unmessagable=True)

    def test_matching_name_not_rewritten_when_other_settings_change(self):
        self.user["longName"] = "New site"
        self.assertTrue(self.change()[2])
        self.node.setOwner.assert_not_called()

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


class NameAndLogTests(unittest.TestCase):
    def test_name_prompt_validates_utf8_size_and_reprompts(self):
        with patch("builtins.input", side_effect=[" ", "x" * 40, "é" * 20, "bad\x00name", "  Reverence  "]), patch("builtins.print"):
            self.assertEqual(roles.prompt_name(), "Reverence")

    def test_name_fits_exact_firmware_boundary(self):
        with patch("builtins.input", return_value="é" * 19 + "x"):
            self.assertEqual(len(roles.prompt_name().encode("utf-8")), 39)

    def test_failed_backup_still_produces_readable_failure_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp)
            (evidence / "before.json").write_text('{"partial":')
            roles.write_reconciliation(evidence, {"Result": "FAILED"})
            content = (evidence / "reconciliation.txt").read_text()
        self.assertIn("Result: FAILED", content)
        self.assertIn("Before snapshot: unreadable/incomplete", content)

    def run_main(self, root, *, apply=False, changed=False, failure=None, verification=None):
        interface = Mock()
        def change(*args):
            evidence = args[5]
            roles.updater.private_json(evidence / "before.json", {
                "user": {"longName": "Old site", "shortName": "R001", "publicKey": "SECRET"},
                "localConfig": {"security": {"privateKey": "SECRET"}},
                "metadata": {"firmwareVersion": "fixture"},
            })
            if failure:
                raise failure
            return "CLIENT", {}, changed
        with patch.object(roles.updater, "ROOT", root), \
                patch.object(roles, "prompt_name", return_value="New site"), \
                patch.object(roles, "prompt_location", return_value=(361234567, -1157654321)), \
                patch.object(roles.updater, "select_port", return_value=Mock(device="/dev/test")), \
                patch.object(roles.updater, "connect", return_value=interface), \
                patch.object(roles.updater, "wait_application", return_value=(interface, "/dev/test")), \
                patch.object(roles, "change_role", side_effect=change), \
                patch.object(roles, "verify", side_effect=verification), patch.object(roles.time, "sleep"), \
                patch("builtins.print"):
            result = roles.main(["R001"] + (["--apply"] if apply else []))
        log_path, = root.glob("private/bench/*/reconciliation.txt")
        content = log_path.read_text()
        self.assertIn("Requested long name: New site", content)
        self.assertIn("Preserved short name: R001", content)
        self.assertIn("Requested fixed latitude: 36.1234567", content)
        self.assertIn("Requested fixed longitude: -115.7654321", content)
        self.assertNotIn("SECRET", content)
        self.assertEqual(log_path.stat().st_mode & 0o777, 0o600)
        return result, content

    def test_preview_log_does_not_claim_settings_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, content = self.run_main(Path(tmp))
        self.assertEqual(result, 0)
        self.assertIn("READ ONLY — proposed settings were not saved", content)
        self.assertIn("Post-reboot verification: not completed", content)

    def test_verified_log_records_success_only_after_both_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, content = self.run_main(Path(tmp), apply=True, changed=True)
        self.assertEqual(result, 0)
        self.assertIn("Result: VERIFIED THROUGH REBOOT", content)
        self.assertIn("Post-save verification: passed", content)
        self.assertIn("Post-reboot verification: passed", content)

    def test_failed_write_log_marks_saved_state_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, content = self.run_main(Path(tmp), apply=True, failure=TimeoutError("SECRET"))
        self.assertEqual(result, 1)
        self.assertIn("Result: FAILED — saved state unverified", content)
        self.assertIn("Failure type: TimeoutError", content)

    def test_failed_reboot_check_keeps_partial_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, content = self.run_main(Path(tmp), apply=True, changed=True,
                verification=[None, roles.updater.UpdateError("mismatch")])
        self.assertEqual(result, 1)
        self.assertIn("Result: FAILED — saved state unverified", content)
        self.assertIn("Post-save verification: passed", content)
        self.assertIn("Post-reboot verification: not completed", content)

    def test_already_matched_log_does_not_claim_reboot_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, content = self.run_main(Path(tmp), apply=True)
        self.assertEqual(result, 0)
        self.assertIn("ALREADY MATCHED", content)
        self.assertIn("Post-reboot verification: not completed", content)


if __name__ == "__main__":
    unittest.main()

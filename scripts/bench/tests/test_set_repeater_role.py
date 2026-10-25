"""Offline safety checks; these do not establish hardware acceptance."""
import importlib.util
import io
import base64
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch, call
from meshtastic.protobuf import admin_pb2, localonly_pb2, mesh_pb2
from google.protobuf.json_format import MessageToDict

SPEC = importlib.util.spec_from_file_location(
    "set_repeater_role", Path(__file__).resolve().parents[1] / "set-repeater-role.py")
roles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(roles)


class RouterLifecycleTests(unittest.TestCase):
    """Model firmware resets on a role transition, across fresh USB sessions."""

    def run_lifecycle(self, *, same_name=False, fault=None, fail_restoration=False, apply=True):
        local = localonly_pb2.LocalConfig()
        local.device.rebroadcast_mode = 3  # LOCAL_ONLY
        local.power.ls_secs = 300
        local.position.gps_update_interval = 60
        local.position.position_broadcast_secs = 120
        local.display.screen_on_secs = 42
        module = localonly_pb2.LocalModuleConfig()
        for field in ('device_update_interval', 'environment_update_interval', 'power_update_interval'):
            setattr(module.telemetry, field, 180)
        module.telemetry.device_telemetry_enabled = True
        module.telemetry.environment_measurement_enabled = True
        module.telemetry.power_measurement_enabled = True
        module.neighbor_info.update_interval = 21600
        module.neighbor_info.enabled = True
        module.neighbor_info.transmit_over_lora = True
        module.paxcounter.paxcounter_update_interval = 7200
        module.telemetry.air_quality_interval = 300
        module.telemetry.health_update_interval = 600
        user = {'id': '!a65601b3', 'longName': 'Old site', 'shortName': 'R001', 'isUnmessagable': False}
        if same_name:
            user['longName'] = 'New site'
        position = {'latitudeI': 1, 'longitudeI': 2}
        calls = []
        commits = []

        class Interface:
            def __init__(self):
                self.localNode = Mock(localConfig=copy.deepcopy(local), moduleConfig=copy.deepcopy(module))
                self.localNode.localConfig.power.ls_secs = 86400 if local.device.role == 2 else 300
                def write(section):
                    calls.append(section)
                    if fail_restoration and commits:
                        raise TimeoutError('ambiguous restore write')
                    if section in local.DESCRIPTOR.fields_by_name:
                        value = getattr(self.localNode.localConfig, section)
                        role_changed = section == 'device' and value.role != local.device.role
                        getattr(local, section).CopyFrom(value)
                        if role_changed and local.device.role == 2:
                            local.device.rebroadcast_mode = 5  # CORE_PORTNUMS_ONLY
                            local.power.ls_secs = 86400
                            local.position.gps_update_interval = 30
                            local.position.position_broadcast_secs = 900
                            local.display.screen_on_secs = 10
                            module.telemetry.device_update_interval = 43200
                            module.telemetry.environment_update_interval = 0
                            module.telemetry.power_update_interval = 0
                            module.neighbor_info.update_interval = 0
                            module.paxcounter.paxcounter_update_interval = 0
                            module.telemetry.air_quality_interval = 0
                            module.telemetry.health_update_interval = 0
                            user['isUnmessagable'] = True
                    else:
                        getattr(module, section).CopyFrom(getattr(self.localNode.moduleConfig, section))
                self.localNode.writeConfig.side_effect = write
                def owner(**kwargs):
                    user['longName'] = kwargs['long_name']
                    if kwargs.get('is_unmessagable') is not None:
                        user['isUnmessagable'] = kwargs['is_unmessagable']
                self.localNode.setOwner.side_effect = owner
                self.localNode.setFixedPosition.side_effect = lambda lat, lon, alt: position.update(latitudeI=lat, longitudeI=lon)
                def commit():
                    commits.append(True)
                    if len(commits) == 1:
                        if fault == 'key':
                            local.security.private_key = b'changed-key'
                        elif fault == 'setting':
                            local.lora.tx_power = 27
                        elif fault == 'name':
                            user['shortName'] = 'BAD'
                        elif fault == 'role':
                            local.device.role = 0
                        elif fault == 'point':
                            position['latitudeI'] += 1
                self.localNode.commitSettingsTransaction.side_effect = commit
            def getMyNodeInfo(self):
                return {'user': copy.deepcopy(user), 'position': copy.deepcopy(position)}
            def close(self):
                pass

        def snapshot(interface, port, serial):
            role = 'ROUTER' if local.device.role == 2 else 'CLIENT'
            return {'localWire': roles.updater.wire(interface.localNode.localConfig),
                    'moduleWire': roles.updater.wire(interface.localNode.moduleConfig),
                    'channelsWire': ['unchanged'], 'hardwareId': 'fixture',
                    'localConfig': MessageToDict(interface.localNode.localConfig),
                    'moduleConfig': MessageToDict(interface.localNode.moduleConfig),
                    'metadata': {'firmwareVersion': 'fixture', 'role': role},
                    'user': {**copy.deepcopy(user), 'role': role}}

        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(roles.updater, 'ROOT', Path(tmp)), \
                patch.object(roles, 'prompt_name', return_value='New site'), \
                patch.object(roles, 'prompt_location', return_value=(100, 200)), \
                patch.object(roles.updater, 'select_port', return_value=Mock(device='fixture')), \
                patch.object(roles.updater, 'connect', side_effect=lambda *_: Interface()), \
                patch.object(roles.updater, 'wait_application', side_effect=lambda *_: (Interface(), 'fixture')), \
                patch.object(roles.updater, 'snapshot', side_effect=snapshot), \
                patch.object(roles.updater, 'validate_node'), \
                patch.object(roles, 'read_saved_power', side_effect=lambda iface: copy.deepcopy(local.power), create=True), \
                patch.object(roles.time, 'sleep'), patch('sys.stdout', new_callable=io.StringIO), \
                patch('sys.stderr', new_callable=io.StringIO):
            result = roles.main(['R001'] + (['--apply'] if apply else []))
            log_path, = Path(tmp).glob('private/bench/*/reconciliation.txt')
            summary = log_path.read_text()
            if result:
                summary += (log_path.parent / 'failure.log').read_text()
        return result, summary, local, module, user, calls, commits

    def test_router_change_preserves_three_minute_profile_through_reboot(self):
        result, summary, local, module, user, calls, commits = self.run_lifecycle()
        self.assertEqual(module.telemetry.device_update_interval, 180, summary)
        self.assertEqual(module.telemetry.environment_update_interval, 180, summary)
        self.assertEqual(module.telemetry.power_update_interval, 180, summary)
        self.assertEqual(module.neighbor_info.update_interval, 21600)
        self.assertEqual(local.power.ls_secs, 300)
        self.assertEqual(local.device.rebroadcast_mode, 3)
        self.assertEqual(local.position.gps_update_interval, 60)
        self.assertEqual(local.position.position_broadcast_secs, 120)
        self.assertEqual(local.display.screen_on_secs, 42)
        self.assertEqual(module.paxcounter.paxcounter_update_interval, 7200)
        self.assertEqual(module.telemetry.air_quality_interval, 300)
        self.assertEqual(module.telemetry.health_update_interval, 600)
        self.assertEqual((user['longName'], user['shortName']), ('New site', 'R001'))
        self.assertFalse(user['isUnmessagable'])
        self.assertEqual(result, 0, summary)
        self.assertIn('VERIFIED THROUGH REBOOT', summary)
        self.assertEqual(len(commits), 2)

    def test_matching_name_still_restores_original_owner_flag(self):
        result, summary, local, module, user, calls, commits = self.run_lifecycle(same_name=True)
        self.assertEqual(result, 0, summary)
        self.assertFalse(user['isUnmessagable'])

    def test_unexpected_changes_stop_before_restoration_writes(self):
        for fault in ('key', 'setting', 'name', 'role', 'point'):
            with self.subTest(fault=fault):
                result, summary, local, module, user, calls, commits = self.run_lifecycle(fault=fault)
                self.assertEqual(result, 1, summary)
                self.assertEqual(calls, ['device', 'position', 'security'])
                self.assertEqual(len(commits), 1)
                self.assertIn('Result: FAILED', summary)
                self.assertIn('Post-save verification: not completed', summary)

    def test_ambiguous_restoration_write_is_not_retried(self):
        result, summary, local, module, user, calls, commits = self.run_lifecycle(fail_restoration=True)
        self.assertEqual(result, 1, summary)
        self.assertEqual(calls, ['device', 'position', 'security', 'device'])
        self.assertEqual(len(commits), 1)

    def test_preview_never_changes_radio_or_restores(self):
        result, summary, local, module, user, calls, commits = self.run_lifecycle(apply=False)
        self.assertEqual(result, 0, summary)
        self.assertEqual(local.device.role, 0)
        self.assertEqual(calls, [])
        self.assertEqual(commits, [])


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
            patch.object(roles.updater, "snapshot", side_effect=lambda *args: {"localWire": roles.updater.wire(self.config), "user": copy.deepcopy(self.user), "metadata": {}}),
            patch.object(roles.updater, "validate_node"),
            patch.object(roles.updater, "private_json"),
            patch.object(roles.time, "sleep"),
            patch.object(roles, "read_saved_power", side_effect=lambda *_: copy.deepcopy(self.config.power))]
        self.snapshot, self.validate, self.backup, _, self.power = [p.start() for p in self.patches]
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

    def test_saved_power_timeout_prevents_backup_and_write(self):
        self.power.side_effect = roles.updater.UpdateError('power read timed out')
        with self.assertRaises(roles.updater.UpdateError):
            self.change()
        self.backup.assert_not_called()
        self.node.beginSettingsTransaction.assert_not_called()

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


class SavedReadTests(unittest.TestCase):
    def test_power_read_uses_admin_response_and_ignores_ack(self):
        interface = Mock()
        response = admin_pb2.AdminMessage()
        response.get_config_response.power.ls_secs = 300
        def send(request, *, wantResponse, onResponse):
            self.assertEqual(request.get_config_request, admin_pb2.AdminMessage.POWER_CONFIG)
            self.assertTrue(wantResponse)
            onResponse({'decoded': {'routing': {}}})
            onResponse({'decoded': {'admin': {'raw': response}}})
        interface.localNode._sendAdmin.side_effect = send
        self.assertEqual(roles.read_saved_power(interface).ls_secs, 300)
        interface.localNode._sendAdmin.assert_called_once()
        interface.localNode.writeConfig.assert_not_called()

    def test_power_read_timeout_has_no_retry(self):
        interface = Mock()
        event = Mock()
        event.wait.return_value = False
        with patch.object(roles.threading, 'Event', return_value=event):
            with self.assertRaisesRegex(roles.updater.UpdateError, 'timed out'):
                roles.read_saved_power(interface)
        interface.localNode._sendAdmin.assert_called_once()
        event.wait.assert_called_once_with(15)

    def test_capture_removes_raw_position_and_reads_saved_sleep_value(self):
        config = localonly_pb2.LocalConfig()
        config.power.ls_secs = 86400
        interface = Mock(localNode=Mock(localConfig=config))
        interface.getMyNodeInfo.return_value = {'position': {
            'latitudeI': 100, 'longitudeI': 200,
            'raw': mesh_pb2.Position(latitude_i=100, longitude_i=200)}}
        saved = copy.deepcopy(config.power)
        saved.ls_secs = 300
        with patch.object(roles, 'read_saved_power', return_value=saved), \
                patch.object(roles.updater, 'snapshot', side_effect=lambda *_: {'user': {}, 'localWire': roles.updater.wire(config)}):
            state = roles.capture(interface, 'fixture', {'usbSerial': 'fixture'})
        json.dumps(state)
        self.assertEqual(state['savedPosition'], {'latitudeI': 100, 'longitudeI': 200})
        self.assertEqual(config.power.ls_secs, 300)
        self.assertNotEqual(state['phoneApiPowerWire'], roles.updater.wire(config.power))

    def test_expected_role_metadata_and_default_client_are_accepted(self):
        roles.assert_metadata({'metadata': {'role': 'ROUTER', 'firmwareVersion': 'same'}},
                              {'metadata': {'role': 'ROUTER', 'firmwareVersion': 'same'}})
        roles.assert_metadata({'metadata': {'role': 'CLIENT'}}, {'metadata': {}})

    def test_changed_firmware_or_wrong_role_is_rejected(self):
        for actual in ({'role': 'CLIENT', 'firmwareVersion': 'same'},
                       {'role': 'ROUTER', 'firmwareVersion': 'changed'}):
            with self.subTest(actual=actual), self.assertRaises(roles.updater.UpdateError):
                roles.assert_metadata({'metadata': {'role': 'ROUTER', 'firmwareVersion': 'same'}},
                                      {'metadata': actual})


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
                patch.object(roles, "restore_role_defaults", return_value=True), \
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

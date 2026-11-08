"""Hardware-free triage safety/correlation tests using real SDK protobufs."""

import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from meshtastic.protobuf import channel_pb2, localonly_pb2, mesh_pb2, portnums_pb2, telemetry_pb2

SPEC = importlib.util.spec_from_file_location("check_rak", Path(__file__).resolve().parents[1] / "check-rak.py")
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)


def fixture():
    local = localonly_pb2.LocalConfig()
    local.device.role = 2
    local.device.node_info_broadcast_secs = 777
    local.security.private_key = b"P" * 32
    local.security.public_key = b"K" * 32
    local.security.admin_key.append(b"A" * 32)
    local.position.fixed_position = True
    local.power.powermon_enables = 7
    local.lora.region = 1
    local.lora.tx_enabled = True
    module = localonly_pb2.LocalModuleConfig()
    module.telemetry.device_update_interval = 180
    module.mqtt.password = "fixture-secret"
    channels = [channel_pb2.Channel(index=i, role=1 if i == 0 else 0) for i in range(8)]
    channels[0].settings.name = "fixture"
    channels[0].settings.psk = b"C" * 32
    state = {"usbSerial": "USB-1", "hardwareId": "aabb", "user": {"id": "!00000001", "longName": "fixture"},
             "metadata": {"hwModel": "RAK4631", "firmwareVersion": "test"},
             "localWire": check.updater.wire(local), "moduleWire": check.updater.wire(module),
             "channelsWire": [check.updater.wire(c) for c in channels]}
    return state


class PreservationTests(unittest.TestCase):
    def test_diagnostic_profile_roundtrip_preserves_security_and_unrelated_settings(self):
        before = fixture()
        original = copy.deepcopy(before)
        local, module, channels = check.diagnostic_state(before, "US", "B123456", b"T" * 32, True, True)
        old_local, old_module, _ = check.load_messages(before)
        self.assertEqual(local.security, old_local.security)
        self.assertEqual(local.position, old_local.position)
        self.assertEqual(local.power, old_local.power)
        self.assertEqual(module.mqtt, old_module.mqtt)
        self.assertTrue(module.telemetry.environment_measurement_enabled)
        self.assertTrue(module.telemetry.power_measurement_enabled)
        self.assertFalse(any(c.role for c in channels[1:]))
        self.assertTrue(all(c.HasField("settings") for c in channels))
        self.assertEqual(channels[0].settings.psk, b"T" * 32)
        self.assertEqual(before, original)
        restored = check.load_messages(before)
        self.assertEqual([check.updater.wire(x) for x in restored[:2]], [before["localWire"], before["moduleWire"]])

    def test_long_fast_profile_explicitly_matches_firmware_derived_modem_values(self):
        local, _, _ = check.diagnostic_state(fixture(), "US", "B123456", b"T" * 32)
        self.assertEqual((local.lora.bandwidth, local.lora.spread_factor, local.lora.coding_rate), (250, 11, 5))

    def test_uninitialized_key_material_is_backed_up_but_not_changed_by_triage(self):
        before = fixture()
        local, _, _ = check.load_messages(before)
        local.security.ClearField("private_key")
        local.security.ClearField("public_key")
        before["localWire"] = check.updater.wire(local)
        radio = check.Radio(SimpleNamespace(device="COM9", serial_number="USB-1"), None)
        radio.snapshot = Mock(return_value=before)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "original.json"
            with self.assertRaises(check.updater.UpdateError):
                radio.backup(path)
            self.assertTrue(path.exists())
            self.assertFalse(radio.dirty)

    def test_region_and_unexpanded_defaults_require_separate_baseline_preparation(self):
        for scenario in ("region", "mqtt", "preset"):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as temporary:
                before = fixture()
                local, module, _ = check.load_messages(before)
                if scenario == "region":
                    local.lora.region = 0
                elif scenario == "mqtt":
                    module.mqtt.root = "msh"
                else:
                    local.lora.use_preset = True
                before.update(localWire=check.updater.wire(local), moduleWire=check.updater.wire(module))
                radio = check.Radio(SimpleNamespace(device="COM9", serial_number="USB-1"), None)
                radio.snapshot = Mock(return_value=before)
                path = Path(temporary) / "original.json"
                with self.assertRaises(check.updater.UpdateError):
                    radio.backup(path)
                self.assertTrue(path.exists())
                self.assertFalse(radio.dirty)

    def test_full_comparison_detects_key_channel_firmware_and_hardware_changes(self):
        before = fixture()
        for key, value in (("localWire", "changed"), ("moduleWire", "changed"),
                           ("channelsWire", []), ("hardwareId", "different"), ("usbSerial", "other"),
                           ("metadata", {"firmwareVersion": "other"})):
            with self.subTest(key=key):
                after = copy.deepcopy(before)
                after[key] = value
                with self.assertRaises(check.updater.UpdateError):
                    check.same_config(before, after)

    def test_durable_backup_failure_and_missing_identity_prevent_writes(self):
        radio = check.Radio(SimpleNamespace(device="COM9", serial_number="USB-1"), None)
        radio.snapshot = Mock(return_value=fixture())
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "original.json"
            with patch.object(check.updater, "private_json", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    radio.backup(path)
            self.assertFalse(radio.dirty)
            radio.port.serial_number = None
            with self.assertRaises(check.updater.UpdateError):
                radio.backup(path)
            self.assertTrue(path.exists())
            self.assertFalse(radio.dirty)

    def test_changed_identity_stops_apply_and_restore_before_first_write(self):
        radio = check.Radio(SimpleNamespace(device="COM9", serial_number="USB-1"), None)
        radio.before = fixture()
        wrong = fixture()
        wrong["hardwareId"] = "different"
        radio.snapshot = Mock(return_value=wrong)
        radio.interface = Mock()
        with patch.object(check, "write_settings") as write:
            with self.assertRaises(check.updater.UpdateError):
                radio.apply(check.load_messages(radio.before))
            radio.dirty = True
            with self.assertRaises(check.updater.UpdateError):
                radio.restore(Path("unused"))
            write.assert_not_called()

    def test_interrupted_transaction_remains_marked_for_recovery(self):
        radio = check.Radio(SimpleNamespace(device="COM9", serial_number="USB-1"), None)
        radio.before = fixture()
        radio.snapshot = Mock(return_value=fixture())
        radio.interface = Mock()
        with patch.object(check, "write_settings", side_effect=TimeoutError("ambiguous write")) as write:
            with self.assertRaises(TimeoutError):
                radio.apply(check.load_messages(radio.before))
            self.assertTrue(radio.dirty)
            write.assert_called_once()

    def test_fixed_coordinates_are_preserved_without_comparing_position_timestamps(self):
        before = fixture()
        before["selfNodeInfo"] = {"position": {"latitudeI": 360000000, "longitudeI": -1150000000, "time": 1}}
        after = copy.deepcopy(before)
        after["selfNodeInfo"]["position"]["time"] = 2
        check.same_config(before, after)
        after["selfNodeInfo"]["position"]["latitudeI"] += 1
        with self.assertRaises(check.updater.UpdateError):
            check.same_config(before, after)

    def test_restore_requires_full_reboot_readback_before_clearing_dirty(self):
        radio = check.Radio(SimpleNamespace(device="COM9", serial_number="USB-1"), None)
        radio.before = fixture()
        radio.dirty = True
        radio.interface = Mock()
        radio.reconnect = Mock()
        changed = fixture()
        changed["channelsWire"] = []
        radio.snapshot = Mock(side_effect=[fixture(), changed])
        with tempfile.TemporaryDirectory() as temporary, patch.object(check, "write_settings"):
            with self.assertRaises(check.updater.UpdateError):
                radio.restore(Path(temporary))
            self.assertTrue(radio.dirty)
            self.assertEqual(radio.reconnect.call_count, 2)
            radio.interface.localNode.reboot.assert_called_once_with(1)
            self.assertTrue((Path(temporary) / "restored.json").exists())

    def test_transaction_writes_only_owned_sections_and_channels(self):
        local, module, channels = check.load_messages(fixture())
        node = Mock(localConfig=localonly_pb2.LocalConfig(), moduleConfig=localonly_pb2.LocalModuleConfig(),
                    channels=[channel_pb2.Channel(index=i) for i in range(8)])
        with patch.object(check.time, "sleep"):
            check.write_settings(SimpleNamespace(localNode=node), (local, module, channels))
        self.assertEqual([c.args[0] for c in node.writeConfig.call_args_list], ["device", "lora", "telemetry"])
        self.assertEqual([c.args[0] for c in node.writeChannel.call_args_list], list(range(8)))
        self.assertEqual(node.method_calls[0][0], "beginSettingsTransaction")
        self.assertEqual(node.method_calls[-1][0], "commitSettingsTransaction")


class EvidenceTests(unittest.TestCase):
    def test_radio_requires_exact_direct_receive_not_ack_or_relay(self):
        sent = mesh_pb2.MeshPacket(id=123)
        raw = mesh_pb2.MeshPacket(id=123, to=2)
        setattr(raw, "from", 1)
        raw.decoded.portnum = portnums_pb2.PRIVATE_APP
        raw.decoded.payload = b"RAKCHECK1:nonce"
        self.assertTrue(check.probe_matches(raw, sent, 1, 2, raw.decoded.payload))
        mutations = [("id", 999), ("from", 3), ("to", 4), ("hop_start", 1), ("hop_limit", 1)]
        for name, value in mutations:
            bad = copy.deepcopy(raw)
            setattr(bad, name, value)
            self.assertFalse(check.probe_matches(bad, sent, 1, 2, raw.decoded.payload))
        for field, value in (("portnum", portnums_pb2.ROUTING_APP), ("payload", b"stale")):
            bad = copy.deepcopy(raw)
            setattr(bad.decoded, field, value)
            self.assertFalse(check.probe_matches(bad, sent, 1, 2, raw.decoded.payload))

    def test_inbox_rejects_wrong_usb_interface_and_stale_packets(self):
        inbox = check.Inbox()
        left, right = object(), object()
        start = time.monotonic()
        raw = mesh_pb2.MeshPacket(id=123)
        inbox.receive({"raw": raw}, left)
        self.assertIsNone(inbox.wait(right, start, lambda p: p.id == 123, 0))
        self.assertIsNone(inbox.wait(left, time.monotonic() + 1, lambda p: p.id == 123, 0))
        self.assertEqual(inbox.wait(left, start, lambda p: p.id == 123, 0).id, 123)

    def test_sensor_reply_requires_matching_source_request_and_variant(self):
        inbox = check.Inbox()
        sender = Mock()
        sent = mesh_pb2.MeshPacket(id=123)
        def deliver(*args, **kwargs):
            for source, request, variant in ((8, 123, "power_metrics"), (7, 99, "power_metrics"),
                                              (7, 123, "environment_metrics"), (7, 123, "power_metrics")):
                data = telemetry_pb2.Telemetry()
                getattr(data, variant).SetInParent()
                if variant == "power_metrics":
                    data.power_metrics.ch1_current = -280
                raw = mesh_pb2.MeshPacket()
                setattr(raw, "from", source)
                raw.decoded.request_id = request
                raw.decoded.portnum = portnums_pb2.TELEMETRY_APP
                raw.decoded.payload = data.SerializeToString()
                inbox.receive({"raw": raw}, sender)
            return sent
        sender.sendData.side_effect = deliver
        result = check.telemetry(inbox, sender, 7, "power_metrics", 0)
        self.assertEqual(result["powerMetrics"]["ch1Current"], -280)
        self.assertFalse(sender.sendData.call_args.kwargs["wantAck"])
        self.assertEqual(sender.sendData.call_args.kwargs["hopLimit"], 0)

    def test_partial_nonfinite_and_missing_sensor_data_never_pass(self):
        for sample in (None, {}, {"powerMetrics": {"ch1Current": "NaN"}}, {"powerMetrics": {"ch1Current": float("nan")}}):
            report = {"checks": {}}
            check.sensor_check(report, "ina", sample, "powerMetrics", ("ch1Current",))
            self.assertEqual(report["checks"]["ina"]["status"], "INCONCLUSIVE")

    def test_failed_inspection_never_connects_or_changes_hardware(self):
        ui = Mock()
        ui.ask.side_effect = ["smoked", "reverse polarity"]
        ui.yes.return_value = False
        with tempfile.TemporaryDirectory() as temporary, patch.object(check, "Radio") as radio:
            result = check.run_board(ui, None, None, SimpleNamespace(device="COM9", serial_number="USB"),
                                     Path(temporary), None, None)
        radio.assert_not_called()
        self.assertEqual(result["verdict"], "FAIL")

    def test_backup_failure_still_reports_failure_and_closes_board(self):
        ui = Mock()
        ui.ask.return_value = "fixture"
        ui.yes.side_effect = [True, False, False]
        with tempfile.TemporaryDirectory() as temporary:
            log = (Path(temporary) / "sdk.log").open("w", encoding="utf-8")
            self.addCleanup(log.close)
            with patch.object(check, "Radio") as cls:
                radio = cls.return_value
                radio.dirty = False
                radio.backup.side_effect = OSError("disk full")
                result = check.run_board(ui, Mock(), check.Inbox(), SimpleNamespace(device="COM9", serial_number="USB"),
                                         Path(temporary), None, log)
                radio.apply.assert_not_called()
                radio.close.assert_called_once()
            reports = list(Path(temporary).glob("board-*/report.json"))
            self.assertEqual(json.loads(reports[0].read_text())["verdict"], "FAIL")
            self.assertEqual(result["checks"]["run"]["status"], "FAIL")
            log.close()

    def test_uninitialized_board_gets_inconclusive_report_without_writes(self):
        ui = Mock()
        ui.ask.return_value = "new-board"
        ui.yes.side_effect = [True, False, False]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with (root / "sdk.log").open("w", encoding="utf-8") as log, patch.object(check, "Radio") as cls:
                radio = cls.return_value
                radio.dirty = False
                radio.backup.side_effect = check.PreparationRequired("Initialization required; backup retained.")
                result = check.run_board(ui, Mock(), check.Inbox(), SimpleNamespace(device="COM9", serial_number="USB"),
                                         root, None, log)
                self.assertEqual(result["verdict"], "INCONCLUSIVE")
                radio.apply.assert_not_called()
                radio.restore.assert_not_called()

    def test_complete_run_records_battery_response_and_restores_even_after_rf_failure(self):
        for rf_works in (True, False):
            with self.subTest(rf_works=rf_works), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with (root / "sdk.log").open("w", encoding="utf-8") as log:
                    ui = Mock()
                    ui.ask.side_effect = ["R-test", "flex history", "battery branch / R100", "on", "", "", ""]
                    ui.yes.side_effect = [True, True, True]
                    ui.number.side_effect = [5.0, 0.35]
                    peer = Mock()
                    peer.before = {"hardwareId": "peer", "user": {"id": "!00000002"}}
                    def sample(inbox, sender, destination, variant, *args):
                        if variant == "power_metrics":
                            return {"powerMetrics": {"ch1Current": 25 if sender is peer.interface else -280, "ch1Voltage": 3.7}}
                        if variant == "environment_metrics":
                            return {"environmentMetrics": {"temperature": 21, "relativeHumidity": 40}}
                        return {"deviceMetrics": {"voltage": 3.7}}
                    with patch.object(check, "Radio") as cls, patch.object(check, "telemetry", side_effect=sample), \
                            patch.object(check, "probe", return_value=[{"received": rf_works}] * 3):
                        radio = cls.return_value
                        radio.before = fixture()
                        radio.dirty = True
                        radio.interface.localNode.nodeNum = 1
                        radio.snapshot.return_value = fixture()
                        result = check.run_board(ui, peer, check.Inbox(), SimpleNamespace(device="COM9", serial_number="USB-1"),
                                                 root, ("US", "B123456", b"T" * 32), log)
                        radio.restore.assert_called_once()
                        self.assertEqual(result["verdict"], "PASS" if rf_works else "FAIL")
                        self.assertEqual(result["checks"]["ina219_response"]["status"], "PASS")
                        self.assertEqual(result["samples"]["ina219CurrentComparison"][0]["usbConnected_mA"], -280)
                        self.assertEqual(result["checks"]["restore_reboot"]["status"], "PASS")

    def test_batch_continues_after_failed_board_and_always_restores_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            ui = Mock()
            ui.yes.return_value = True
            ui.ask.return_value = ""
            port = SimpleNamespace(device="COM9", serial_number="USB-1")
            with patch.object(check.updater, "ROOT", Path(temporary)), patch.object(check, "UI", return_value=ui), \
                    patch.object(check, "Radio") as cls, patch.object(check, "choose_port", side_effect=[port, port, port, None]), \
                    patch.object(check, "run_board", side_effect=[{"label": "one", "verdict": "FAIL"}, {"label": "two", "verdict": "PASS"}]) as run:
                cls.return_value.before = fixture()
                cls.return_value.snapshot.return_value = fixture()
                cls.return_value.dirty = True
                self.assertEqual(check.main(["--peer", "COM5"]), 1)
                self.assertEqual(run.call_count, 2)
                cls.return_value.restore.assert_called_once()
                cls.return_value.close.assert_called_once()

    def test_manual_recovery_failure_does_not_automatically_retry_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            backup = root / "original.json"
            backup.write_text(json.dumps(fixture()), encoding="utf-8")
            ui = Mock()
            with patch.object(check.updater, "ROOT", root), patch.object(check, "UI", return_value=ui), \
                    patch.object(check, "Radio") as cls, patch.object(check, "choose_port", return_value=Mock()):
                cls.return_value.dirty = True
                cls.return_value.restore.side_effect = TimeoutError("ambiguous commit")
                self.assertEqual(check.main(["--recover", str(backup), "--port", "COM9"]), 1)
                cls.return_value.restore.assert_called_once()
                cls.return_value.close.assert_called_once()

    def test_unresponsive_board_is_recorded_without_opening_serial(self):
        ui = Mock()
        ui.ask.side_effect = ["dead-unit", "smoke history; no USB"]
        with tempfile.TemporaryDirectory() as temporary, patch.object(check, "Radio") as radio:
            result = check.record_missing(ui, Path(temporary))
            radio.assert_not_called()
            self.assertEqual(result["verdict"], "FAIL")
            self.assertFalse(list(Path(temporary).glob("board-*/original.json")))

    def test_failed_reference_cleanup_overrides_successful_batch_exit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ui = Mock()
            ui.yes.return_value = True
            with patch.object(check.updater, "ROOT", root), patch.object(check, "UI", return_value=ui), \
                    patch.object(check, "Radio") as cls, patch.object(check, "choose_port", side_effect=[Mock(), None]):
                cls.return_value.before = fixture()
                cls.return_value.snapshot.return_value = fixture()
                cls.return_value.dirty = True
                cls.return_value.restore.side_effect = TimeoutError("device lost")
                with self.assertRaises(SystemExit) as exit_code:
                    check.main(["--peer", "COM5"])
                self.assertEqual(exit_code.exception.code, 1)
                status = list(root.glob("private/bench/rak-check-*/reference/status.json"))[0]
                self.assertTrue(json.loads(status.read_text())["restoreRequired"])
                cls.return_value.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()

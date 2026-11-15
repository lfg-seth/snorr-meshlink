"""Read-only hot-plug identity checks; no real serial ports are opened."""
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace as NS
import tempfile
import unittest
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("watch_raks", Path(__file__).parents[1] / "watch-raks.py")
watch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watch)


def port(usb="ABC", device="COM19", vid=0x239A, pid=0x8029):
    return NS(serial_number=usb, device=device, vid=vid, pid=pid)


def identity(p):
    return {"nodeId": "!12345678", "name": "R001", "role": "CLIENT", "port": p.device,
            "usbSerial": p.serial_number, "firmware": "2.7.26.test", "hardwareId": "01"}


class HotPlugTests(unittest.TestCase):
    def test_heltec_and_bootloader_are_not_opened(self):
        ports = [port(), port("V4", "COM31", 0x303A, 0x1001), port("BOOT", "COM20", pid=0x0029)]
        self.assertEqual(watch.candidates(ports, []), [ports[0]])

    def test_duplicate_or_missing_usb_is_never_guessed(self):
        self.assertEqual(watch.candidates([port(), port("abc", "COM20"), port(None)], []), [])

    def test_reference_exclusion_is_case_insensitive(self):
        self.assertEqual(watch.candidates([port("AbC")], ["abc"]), [])

    def test_reference_is_visible_by_default_and_can_be_annotated(self):
        reference = port("70DF102F58D2A034", "COM27")
        self.assertEqual(watch.candidates([reference], []), [reference])
        row = identity(reference)
        row["reference"] = True
        self.assertIn("REFERENCE", watch.show(row))
        self.assertTrue(watch.show(row).startswith("!12345678"))

    def test_unplugged_cached_nodes_are_not_reported_connected(self):
        known = {"A": identity(port("A")), "B": identity(port("B", "COM20"))}
        output = []
        present = watch.update_presence(known, [port("B", "COM20")], [], output.append)
        self.assertEqual(present, {"B"})
        self.assertFalse(known["A"]["connected"])
        self.assertTrue(known["B"]["connected"])
        self.assertEqual(len(output), 1)
        watch.update_presence(known, [port("B", "COM20")], [], output.append)
        self.assertEqual(len(output), 1)

    def test_stale_running_file_does_not_claim_a_dead_process_is_running(self):
        with patch.object(watch, "process_running", return_value=False):
            state = watch.live_status({"pid": 1234, "running": True, "paused": True, "busyPort": "COM19"})
        self.assertFalse(state["running"])
        self.assertTrue(state["stale"])
        self.assertFalse(state["paused"])
        self.assertIsNone(state["busyPort"])

    def test_current_process_query_is_read_only_and_alive(self):
        self.assertTrue(watch.process_running(os.getpid()))
        self.assertFalse(watch.process_running(0))

    def test_each_new_port_prints_once_and_replug_refreshes(self):
        seen, output, opened = set(), [], []
        def probe(p):
            opened.append(p.device)
            return identity(p)
        watch.poll([port()], seen, [], probe, output.append)
        watch.poll([port()], seen, [], probe, output.append)
        self.assertEqual(opened, ["COM19"])
        watch.poll([], seen, [], probe, output.append)
        watch.poll([port(device="COM21")], seen, [], probe, output.append)
        self.assertEqual(opened, ["COM19", "COM21"])
        self.assertEqual(len(output), 2)
        self.assertTrue(output[0].startswith("!12345678"))

    def test_multiple_boards_map_by_usb_not_enumeration_order(self):
        seen, output = set(), []
        rows = watch.poll([port("B", "COM7"), port("A", "COM9")], seen, [], identity, output.append)
        self.assertEqual([(r["usbSerial"], r["port"]) for r in rows], [("B", "COM7"), ("A", "COM9")])

    def test_pause_stops_before_another_board_is_opened(self):
        opened = []
        def probe(p):
            opened.append(p.device)
            return identity(p)
        watch.poll([port(), port("B", "COM20")], set(), [], probe, lambda _: None, lambda: bool(opened))
        self.assertEqual(opened, ["COM19"])

    def test_error_body_never_reaches_console_and_board_is_retryable(self):
        seen, output = set(), []
        def broken(p):
            raise RuntimeError("secret password channel-key")
        watch.poll([port()], seen, [], broken, output.append)
        self.assertNotIn("secret", output[0])
        self.assertNotIn("password", output[0])
        self.assertFalse(seen)

    def test_terminal_controls_are_removed(self):
        self.assertEqual(watch.clean("R001\n\r\x1b\u202e"), "R001")


class IdentificationTests(unittest.TestCase):
    def make_interface(self, fail=False, model=9, node_id="!12345678"):
        role_enum = NS(values_by_number={0: NS(name="CLIENT")})
        value = NS(metadata=NS(hw_model=model, firmware_version="2.7.26.test", role=0,
                              DESCRIPTOR=NS(fields_by_name={"role": NS(enum_type=role_enum)})),
                   myInfo=NS(my_node_num=0x12345678, device_id=b"\x01"), closed=False)
        def connect():
            print("secret SDK material")
            if fail:
                raise RuntimeError("connection failed")
        value.connect = connect
        value.close = lambda: setattr(value, "closed", True)
        value.getMyNodeInfo = lambda: {"user": {"id": node_id, "shortName": "R001", "privateKey": "secret"}}
        return value

    def test_projected_identity_has_no_keys_and_port_is_closed(self):
        interface, log = self.make_interface(), io.StringIO()
        result = watch.identify(port(), log, factory=lambda **_: interface)
        self.assertTrue(interface.closed)
        self.assertEqual(result["nodeId"], "!12345678")
        self.assertEqual(result["role"], "CLIENT")
        self.assertNotIn("secret", str(result))
        self.assertIn("secret SDK material", log.getvalue())

    def test_connection_failure_still_closes_interface(self):
        interface = self.make_interface(fail=True)
        with self.assertRaises(RuntimeError):
            watch.identify(port(), io.StringIO(), factory=lambda **_: interface)
        self.assertTrue(interface.closed)

    def test_wrong_model_or_inconsistent_identity_is_rejected(self):
        for interface in (self.make_interface(model=99), self.make_interface(node_id="!abcdef01"),
                          self.make_interface(node_id="bad")):
            with self.subTest(interface=interface), self.assertRaises(ValueError):
                watch.identify(port(), io.StringIO(), factory=lambda **_: interface)
            self.assertTrue(interface.closed)

    def test_station_lock_is_exclusive_and_released(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "watch.lock"
            with watch.station_lease(path):
                with self.assertRaises(OSError):
                    with watch.station_lease(path):
                        self.fail("Concurrent watcher acquired the same station")
            with watch.station_lease(path):
                pass


class StationStatusTests(unittest.TestCase):
    now = datetime(2026, 11, 13, 4, 0, tzinfo=timezone.utc)

    def status(self, **changes):
        value = {"pid": 1234, "processStart": "instance-one", "running": True,
                 "paused": True, "busyPort": None, "heartbeatUtc": self.now.isoformat()}
        value.update(changes)
        return value

    def test_recent_matching_instance_preserves_pause_acknowledgement(self):
        with patch.object(watch, "process_running", return_value=True), \
             patch.object(watch, "process_token", return_value="instance-one"):
            state = watch.live_status(self.status(), now=self.now)
        self.assertTrue(state["running"])
        self.assertTrue(state["paused"])
        self.assertFalse(state["stale"])

    def test_reused_pid_cannot_authorize_a_stale_pause(self):
        with patch.object(watch, "process_running", return_value=True), \
             patch.object(watch, "process_token", return_value="instance-two"):
            state = watch.live_status(self.status(), now=self.now)
        self.assertFalse(state["running"])
        self.assertFalse(state["paused"])
        self.assertTrue(state["stale"])

    def test_old_missing_invalid_and_future_heartbeats_fail_closed(self):
        for heartbeat in ((self.now - timedelta(seconds=31)).isoformat(), "", "bad", None,
                          (self.now + timedelta(seconds=1)).isoformat(), "2026-11-13T04:00:00"):
            with self.subTest(heartbeat=heartbeat), \
                 patch.object(watch, "process_running", return_value=True), \
                 patch.object(watch, "process_token", return_value="instance-one"):
                state = watch.live_status(self.status(heartbeatUtc=heartbeat), now=self.now)
            self.assertFalse(state["running"])
            self.assertFalse(state["paused"])
            self.assertTrue(state["stale"])

    def test_unverifiable_creation_identity_fails_closed(self):
        with patch.object(watch, "process_running", return_value=True), \
             patch.object(watch, "process_token", return_value=None):
            state = watch.live_status(self.status(), now=self.now)
        self.assertFalse(state["paused"])
        self.assertTrue(state["stale"])

    def test_real_process_creation_token_is_stable_and_read_only(self):
        first = watch.process_token(os.getpid())
        if os.name == "nt" or Path("/proc/self/stat").exists():
            self.assertIsNotNone(first)
        self.assertEqual(first, watch.process_token(os.getpid()))
        self.assertIsNone(watch.process_token(0))

    def test_dead_station_stop_does_not_create_a_marker(self):
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "stop"
            with patch.object(watch, "live_status", return_value={"running": False}):
                self.assertFalse(watch.request_stop(marker, self.status()))
            self.assertFalse(marker.exists())

    def test_stop_request_is_bound_to_one_process_instance(self):
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "stop"
            state = self.status()
            with patch.object(watch, "live_status", return_value=state):
                self.assertTrue(watch.request_stop(marker, state))
            self.assertTrue(watch.stop_requested(marker, state))
            self.assertFalse(watch.stop_requested(marker, self.status(processStart="instance-two")))
            self.assertFalse(watch.stop_requested(marker, self.status(pid=5678)))
            marker.write_text("Stop requested.\n", encoding="utf-8")
            self.assertFalse(watch.stop_requested(marker, state))
            marker.write_text("[]", encoding="utf-8")
            self.assertFalse(watch.stop_requested(marker, state))

    def test_each_read_refreshes_heartbeat_before_and_after_closing(self):
        writes = []
        def write(path, value):
            writes.append((path.name, dict(value) if isinstance(value, dict) else value))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            station = root / "private/station"
            with patch.object(watch, "ROOT", root), \
                 patch("serial.tools.list_ports.comports", return_value=[port("A"), port("B", "COM20")]), \
                 patch.object(watch, "process_token", return_value="instance-one"), \
                 patch.object(watch, "identify", side_effect=lambda p, _: identity(p)), \
                 patch.object(watch, "atomic_json", side_effect=write), \
                 patch.object(watch, "datetime", wraps=datetime) as clock, \
                 patch("sys.stdout", io.StringIO()):
                clock.now.side_effect = [self.now + timedelta(seconds=i) for i in range(6)]
                self.assertEqual(watch.main(["--once", "--station-dir", str(station)]), 0)
        statuses = [value for name, value in writes if name == "status.json"]
        self.assertEqual([(s["busyPort"], s["heartbeatUtc"]) for s in statuses[:4]],
                         [("COM19", (self.now + timedelta(seconds=2)).isoformat()),
                          (None, (self.now + timedelta(seconds=3)).isoformat()),
                          ("COM20", (self.now + timedelta(seconds=4)).isoformat()),
                          (None, (self.now + timedelta(seconds=5)).isoformat())])


if __name__ == "__main__":
    unittest.main()

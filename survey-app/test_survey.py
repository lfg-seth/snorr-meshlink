"""No hardware or network required. Exercise v1, host recovery and the evidence store."""

import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from recorder import Recorder, command, load_adapter
from server import source_lease
from simulator import Simulator


class FirmwareSimulation(unittest.TestCase):
    def setUp(self):
        self.sim = Simulator()
        self.now = int(time.monotonic() * 1000)
        self.tick()

    def tick(self, elapsed=0, heartbeat=True):
        self.now += elapsed
        if heartbeat:
            self.sim.apply(command("heartbeat"), self.now)
        return self.sim.poll(self.now)

    def start(self, mode="survey"):
        self.sim.apply(command("start", {"mode": mode}), self.now)
        return self.tick()

    def test_gps_fault_and_explicit_resume(self):
        self.start()
        self.sim.change_scenario("Stale GPS", self.now)
        self.tick(2100)
        self.assertEqual(self.sim.state["run_state"], "paused")
        self.assertIsNone(self.sim.gps["lat_deg"])
        self.sim.change_scenario("Strong link", self.now)
        self.tick(1000)
        self.assertTrue(self.sim.gps["valid"])
        self.assertEqual(self.sim.state["run_state"], "paused")
        self.sim.apply(command("resume"), self.now)

    def test_bench_without_gps_and_heartbeat_timeout(self):
        self.sim.change_scenario("No GPS", self.now)
        self.tick(1001)
        with self.assertRaisesRegex(ValueError, "fresh survey fix"):
            self.start()
        attempt = next(e["data"] for e in self.start("bench") if e["name"] == "attempt")
        self.assertEqual(attempt["mode"], "bench")
        self.assertIsNone(attempt["gps"]["lon_deg"])
        self.assertTrue(any(e["name"] == "result" for e in self.tick(1000)))
        self.tick(5100, False)
        self.assertEqual(self.sim.state["run_state"], "paused")

    def test_asymmetry_quiet_late_timeout_and_backdown(self):
        self.sim.change_scenario("Asymmetric link", self.now)
        self.start()
        received = next(e["data"] for e in self.tick(650) if e["name"] == "result")
        self.assertGreater(received["downlink"]["snr_db"], received["uplink"]["snr_db"])
        self.assertEqual(received["gps"]["fix_age_ms"], 0)
        self.assertGreater(self.sim.state["quiet_remaining_s"], 0)
        self.sim.change_scenario("Timeouts", self.now)
        self.tick(2350)
        result = next(e["data"] for e in self.tick(1300) if e["name"] == "result")
        self.assertEqual(result["status"], "timeout")
        self.assertIsNone(result["uplink"])
        self.sim.change_scenario("Busy channel", self.now)
        self.tick(1700)
        self.assertTrue(self.sim.state["backdown"])
        self.sim.change_scenario("Late / duplicate", self.now)
        events = self.tick(1000)
        statuses = [e["data"]["status"] for e in events if e["name"] == "result"]
        self.assertEqual(statuses, ["success", "late"])
        self.assertEqual(self.sim.state["counts"], {"attempts": 3, "success": 2})

    def test_usb_loss_and_pending_cancellation(self):
        self.start()
        self.sim.change_scenario("USB loss", self.now + 5)
        self.assertIn(
            "transport_lost",
            [e["data"].get("status") for e in self.tick(heartbeat=False)],
        )
        self.sim.change_scenario("Strong link", self.now + 10)
        self.tick(2000)
        self.assertEqual(self.sim.state["run_state"], "paused")

    def test_envelopes_and_settings(self):
        cmd = command("start", {"mode": "survey"})
        for i in range(2):
            self.sim.send(cmd)
            ack = next(e["data"] for e in self.tick() if e["name"] == "ack")
            self.assertTrue(ack["ok"])
        for bad in [
            cmd | {"params": {"mode": "bench"}},
            command("not_supported"),
            command("resume") | {"v": 2},
            command("pause", {"made_up": True}),
            command("configure", {"profile": "invalid"}),
        ]:
            self.sim.send(bad)
            self.assertFalse(
                next(e["data"]["ok"] for e in self.tick() if e["name"] == "ack")
            )
        self.sim.apply(command("pause"), self.now)
        for bad in [
            {"heartbeat_timeout_ms": 1000},
            {"min_interval_ms": True},
            {"backdown_pct": 2},
        ]:
            with self.assertRaises(ValueError):
                self.sim.apply(command("configure", bad), self.now)
        self.sim.apply(
            command("configure", {"profile": "FAST (experimental)"}), self.now
        )
        self.sim.apply(command("set_target", {"target_id": "SIM-R02"}), self.now)
        self.assertEqual(self.sim.state["segment_id"], 3)


class DesktopRecorder(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.host = Recorder(Simulator(), self.temp.name)
        self.host.poll()
        self.token = "sim-controller-1"

    def tearDown(self):
        self.host.close()
        self.temp.cleanup()

    def send(self, name, params=None):
        return self.host.dispatch(command(name, params), self.token, self.host.revision)

    def test_command_ledger_and_restart(self):
        cmd = command("start", {"mode": "survey"})
        rev = self.host.revision
        a = self.host.dispatch(cmd, self.token, rev)
        self.assertTrue(a["ok"])
        self.assertEqual(self.host.dispatch(cmd, self.token, rev), a)
        with self.assertRaisesRegex(ValueError, "Another browser"):
            self.host.dispatch(command("stop"), "different-controller", rev)
        with self.assertRaisesRegex(ValueError, "state changed"):
            self.host.dispatch(command("resume"), self.token, rev)
        self.host.close()
        self.host = Recorder(Simulator(), self.temp.name)
        self.host.poll()
        self.assertEqual(self.host.dispatch(cmd, self.token, rev), a)
        self.assertEqual(self.host.state["run_state"], "idle")
        self.assertTrue(self.host.history(session=a["applied"]["session_id"]))

    def test_background_recording_without_any_browser(self):
        self.send("configure", {"response_timeout_ms": 150, "min_interval_ms": 500})
        self.send("start", {"mode": "survey"})
        self.host.start_worker()
        time.sleep(1.2)
        self.assertGreaterEqual(len(self.host.history(names=["result"])), 2)
        self.assertTrue(self.host.state["heartbeat_ok"])

    def test_disk_failure_stops_rf_and_refuses_start(self):
        self.send("start", {"mode": "survey"})
        with patch.object(
            self.host, "store", side_effect=sqlite3.OperationalError("disk full")
        ):
            self.host.adapter.emit("statistics", {})
            self.host.poll()
        self.assertFalse(self.host.recording)
        self.assertIn("disk full", self.host.error)
        self.assertEqual(self.host.adapter.state["run_state"], "stopped")
        self.assertGreater(self.host.dropped, 0)
        self.assertFalse(self.send("stop")["ok"])
        with self.assertRaisesRegex(ValueError, "disk full"):
            self.send("start", {"mode": "bench"})

    def test_origin_gaps_duplicate_and_queue_pressure(self):
        sim = self.host.adapter
        sim.change_scenario("Queue pressure", int(time.monotonic() * 1000))
        self.host.poll()
        self.assertEqual(self.host.gaps, 1)
        sim.seq += 3
        sim.emit("statistics", {"optional_future_value": 1})
        event = sim.events[-1]
        sim.events.append(event)
        sim.events.append(event | {"data_source": "live"})
        self.host.poll()
        self.assertGreaterEqual(self.host.gaps, 2)
        self.assertGreater(self.host.dropped, 0)
        self.assertTrue(self.host.history(names=["duplicate_delivery"]))
        self.assertTrue(self.host.history(names=["adapter_error"]))
        self.assertTrue(
            self.host.history(names=["statistics"])[0]["event"]["data"][
                "optional_future_value"
            ]
        )

    def test_transport_reconnect_pauses(self):
        self.send("start", {"mode": "survey"})
        with patch.object(self.host.adapter, "poll", side_effect=OSError("unplugged")):
            self.host.poll()
        self.assertEqual(self.host.adapter_error, "unplugged")
        self.host.poll()
        self.host.poll()
        self.assertIsNone(self.host.adapter_error)
        self.assertEqual(self.host.state["run_state"], "paused")

    def test_large_session_order_and_bounded_replay(self):
        self.send("start", {"mode": "bench"})
        sid = self.host.state["session_id"]
        for batch in range(50):
            for i in range(200):
                self.host.adapter.emit(
                    "gps",
                    {
                        "session_id": sid,
                        "valid": False,
                        "lat_deg": None,
                        "lon_deg": None,
                    },
                )
            self.host.poll()
        page = self.host.history(session=sid, names=["gps"], limit=500)
        self.assertEqual(len(page), 500)
        previous = self.host.history(
            before=page[0]["cursor"], session=sid, names=["gps"], limit=500
        )
        self.assertLess(previous[-1]["cursor"], page[0]["cursor"])
        self.assertGreaterEqual(
            self.host.db.execute(
                "SELECT events FROM sessions WHERE id=?", (sid,)
            ).fetchone()[0],
            10000,
        )

    def test_external_adapter_never_falls_back(self):
        with self.assertRaisesRegex(ValueError, "requires"):
            load_adapter("live", None)
        f = Path(self.temp.name) / "adapter.py"
        f.write_text(
            "from simulator import Simulator\ndef open_adapter(): return Simulator()\n"
        )
        with self.assertRaisesRegex(ValueError, "provenance"):
            load_adapter("live", f)
        with self.assertRaisesRegex(ValueError, "external"):
            load_adapter("simulation", f)

    def test_one_source_owner(self):
        with (
            source_lease(Path(self.temp.name)),
            self.assertRaisesRegex(RuntimeError, "already owns"),
            source_lease(Path(self.temp.name)),
        ):
            self.fail("Double ownership")


def browser_history_fixture(root):
    """A completed simulation recording for the optional browser load check."""
    host = Recorder(Simulator(), root)
    host.poll()
    host.dispatch(
        command("start", {"mode": "bench"}), "fixture-controller", host.revision
    )
    session = host.adapter.state["session_id"]
    for batch in range(40):
        for i in range(250):
            host.adapter.emit(
                "result",
                {
                    "session_id": session,
                    "segment_id": 1,
                    "mode": "bench",
                    "attempt_id": f"fixture-{batch}-{i}",
                    "target_id": "SIM-R01",
                    "status": "timeout",
                    "gps": {"valid": False, "lat_deg": None, "lon_deg": None},
                },
            )
        host.poll()
    host.close()


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--browser-fixture":
        browser_history_fixture(Path(sys.argv[2]))
    else:
        unittest.main()

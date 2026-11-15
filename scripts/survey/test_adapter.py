import json
import os
import tempfile
from pathlib import Path
import threading
import time
import unittest

from adapter import Decoder, LIMITS, MAGIC, OPS, REQUEST, SYNC, SurveyAdapter, payload
from bench import check_progress, summarize


def frame(s):
    b = MAGIC + s.encode("ascii")
    return SYNC + len(b).to_bytes(2, "big") + b


class Device:
    """Wire peer for testing the actual serial worker and its exclusive controller session."""

    def __init__(self, max_targets=8):
        self.stream = bytearray()
        self.lock = threading.Lock()
        self.seq = self.command_serial = self.starts = 0
        self.running = False
        self.closed = False
        self.epoch = 44
        self.hello_serials = []
        self.max_targets = max_targets
        self.targets = [3]
        self.settings = [v[2] for v in LIMITS.values()]

    @property
    def in_waiting(self):
        with self.lock:
            return len(self.stream)

    def emit(self, n, *data):
        self.seq += 1
        s = f"{self.epoch},{self.seq},5000,{n}," + ",".join(map(str, data))
        self.stream.extend(frame(s))

    def write(self, b):
        _, boot, serial, op, count, *raw = REQUEST.unpack(b[4:])
        name = OPS[op]
        args = raw[:count]
        with self.lock:
            err = 0
            if name == "hello":
                self.hello_serials.append(serial)
                self.emit("hello", 2, "test", 1, 110, 1, 0, 35, 10, 1, 1, self.command_serial, 1)
            elif boot != self.epoch:
                err = 1
            elif name == "start":
                if self.running:
                    err = 3
                else:
                    self.running = True
                    self.starts += 1
            elif name == "stop":
                self.running = False
            elif name == "configure":
                self.settings = args
            elif name == "set_target":
                self.targets = args
            if name in ("hello", "get_state", "configure", "start", "stop", "set_target"):
                self.emit(
                    "state",
                    int(self.running),
                    1,
                    37,
                    1,
                    3,
                    3000,
                    0,
                    0,
                    8,
                    8,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    self.command_serial,
                )
                self.emit("profile", 0, 0, 1)
                self.emit("settings", *self.settings)
                self.emit("targets", len(self.targets), *self.targets, *([0] * (self.max_targets - len(self.targets))))
            if name != "hello":
                self.command_serial = serial
            self.emit("ack", serial, op, err)
        return len(b)

    def read(self, n):
        time.sleep(0.001)
        with self.lock:
            block = bytes(self.stream[:n])
            del self.stream[:n]
            return block

    def close(self):
        self.closed = True


class AdapterTests(unittest.TestCase):
    def test_target_capacity_matches_firmware(self):
        ids = [f"!{i:08x}" for i in range(3, 13)]
        for limit in (8, 10):
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as t:
                dev = Device(max_targets=limit)
                with SurveyAdapter("fake", "!00000002", Path(t) / "events.jsonl", serial_factory=lambda **_: dev) as a:
                    self.assertEqual(a.hello["capabilities"]["max_targets"], limit)
                    reply = a.command(dict(v=1, kind="command", id="ten", name="set_target", params={"target_ids": ids}))
                    self.assertEqual(reply["data"]["ok"], limit == 10)
                    if limit == 10:
                        self.assertEqual(a.targets, ids)

    def test_frame_splits_resynchronization(self):
        d = Decoder()
        wire = b"log" + SYNC + b"\xff\xff" + b"text" + b"\x94\xc3\x00\x02ab" + frame("1,2,3,fault,gps_stale")
        chunks = []
        for b in wire:
            chunks.extend(d.feed(bytes([b])))
        self.assertEqual(chunks, [["1", "2", "3", "fault", "gps_stale"]])
        self.assertEqual(len(payload(14, 17, "set_target", [3])), 122)

    def test_commands_reconnect_and_correlation(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            dev = Device()

            def adapter(name):
                return SurveyAdapter("fake", "!00000002", root / name, serial_factory=lambda **_: dev)

            def command(a, name, cid, **p):
                return a.command(dict(v=1, kind="command", id=cid, name=name, params=p))["data"]

            with adapter("first.jsonl") as a:
                self.assertEqual(a.hello["node_id"], "!00000002")
                self.assertTrue(command(a, "configure", "config", min_attempt_interval_ms=2000)["ok"])
                self.assertFalse(command(a, "configure", "bad", invented=5)["ok"])
                self.assertTrue(command(a, "start", "once", mode="bench")["ok"])
                self.assertTrue(command(a, "start", "once", mode="bench")["ok"])
                self.assertFalse(command(a, "start", "once", mode="survey")["ok"])
                self.assertTrue(command(a, "stop", "finished")["ok"])
                with dev.lock:
                    dev.emit("sendfix", 37, 1, 0, 0, 0, 0, 0, 0, 0, 0xFFFFFFFF, 0, 0, 0)
                    dev.emit("attempt", 37, 1, 1, 3, 1, 1000, 2000, 45)
                    dev.emit("txfix", 37, 1, 1, 0, 0, 0, 1, 1700000000, 100, 30, 1, 1, 6)
                    dev.emit(
                        "result",
                        37,
                        1,
                        1,
                        3,
                        1,
                        "success",
                        123,
                        456,
                        1000,
                        1100,
                        1700,
                        2500,
                        -84,
                        -7,
                        -78,
                        0,
                        75,
                        610,
                        59,
                        51,
                    )
                received = None
                saw_replayed_ack = False
                for _ in range(100):
                    e = a.read_event(1)
                    if e["name"] == "ack" and e["data"].get("replayed"):
                        self.assertEqual(e["data"]["command_id"], "once")
                        saw_replayed_ack = True
                    if e["name"] == "result":
                        received = e["data"]
                        break
                self.assertTrue(saw_replayed_ack)
                self.assertEqual(received["uplink"], {"rssi_dbm": -84, "snr_db": -1.75})
                self.assertEqual(received["downlink"]["snr_db"], 0)
                self.assertEqual(received["gps"]["lat_deg"], 0)
                self.assertIsNone(received["enqueue_gps"]["lat_deg"])
                self.assertEqual(received["measured_tx_ms"], 600)
                self.assertEqual(received["rtt_ms"], 1400)
            self.assertTrue(dev.closed)
            with adapter("second.jsonl") as a:
                self.assertTrue(command(a, "start", "once", mode="bench")["ok"])
                self.assertEqual(dev.starts, 1)
                self.assertFalse(dev.running)
            self.assertTrue((root / "first.jsonl").stat().st_size > 0)

    def test_wrong_identity_rejects_before_writes(self):
        with tempfile.TemporaryDirectory() as t:
            d = Device()
            with self.assertRaises(ConnectionError):
                with SurveyAdapter(
                    "fake", "!00000009", Path(t) / "events.jsonl", serial_factory=lambda **_: d
                ):
                    pass
            self.assertEqual(d.hello_serials, [1])
            self.assertEqual(d.command_serial, 0)
            self.assertTrue(d.closed)

    def test_independent_tx_rx_and_quiet_accounts(self):
        client, target, witness = "!00000002", "!00000003", "!00000004"

        def event(name, millis, **data):
            return {
                "name": name,
                "firmware_ms": millis,
                "host_monotonic_ns": 10_000_000_000 + millis * 1_000_000,
                "data": data,
            }

        def packet(kind, millis, source, pid, **values):
            return event("statistics", millis, type=kind, packet_id=pid, **{"from": source}, **values)

        def tx(millis, source, pid, classification):
            return packet(
                "airtx",
                millis,
                source,
                pid,
                local_class=classification,
                to=0xFFFFFFFF,
                hop_start=0,
                hop_limit=0,
                want_ack=0,
            )

        def rx(millis, source, pid, rssi, snr):
            return packet("rx", millis, source, pid, port=310, rssi_dbm=rssi, snr_quarter_db=snr)

        quiet = event("quiet", 150, request_packet_id=99, target_id=target, remaining_ms=900000)
        result = event(
            "result",
            710,
            status="success",
            target_id=target,
            request_packet_id=99,
            reply_packet_id=100,
            rtt_ms=600,
            measured_tx_ms=244,
            wire_bytes=84,
            channel_util_pct=50,
            remote_util_pct=54,
            uplink={"rssi_dbm": -77, "snr_db": -1.25},
            downlink={"rssi_dbm": -88, "snr_db": 0},
        )
        logs = {
            client: [tx(110, 2, 99, 2), rx(710, 3, 100, -88, 0), result, packet("rx", 805, 4, 103, port=67)],
            target: [
                rx(150, 2, 99, -77, -5),
                quiet,
                event("statistics", 151, type="pong", request_packet_id=99, enqueued=True),
                tx(400, 3, 100, 2),
            ],
            witness: [
                quiet,
                tx(210, 4, 101, 1),
                tx(211, 2, 99, 0),
                tx(800, 4, 103, 0),
                tx(900, 4, 104, 0),
                tx(910000, 4, 102, 1),
            ],
        }
        with tempfile.TemporaryDirectory() as t:
            for observer, rows in logs.items():
                (Path(t) / (observer + ".jsonl")).write_text("".join(json.dumps(r) + "\n" for r in rows))
            s = summarize(Path(t), client, [target, witness], elapsed=60, started=10)
            self.assertEqual(s["longest_gap_between_successes_s"], {target: 59.29})
            self.assertEqual(s["all_observers_heard_by_target"], {target: 1})
            self.assertEqual(s["matched_tx_pairs_by_target"], {target: 1})
            self.assertEqual(s["uplink_metric_matches"], 1)
            self.assertEqual(s["downlink_metric_matches"], 1)
            self.assertEqual(s["observed_survey_forwards"], 1)
            self.assertEqual(s["observed_owned_background_tx_during_quiet"], 2)
            self.assertEqual(s["unverified_quiet_broadcasts"], 1)
            self.assertEqual(s["complete_witnesses_by_target"], {target: 1})
            self.assertEqual(s["client_channel_util_pct"]["median"], 50)
            self.assertEqual(s["unexpected_responders"], 0)

    @unittest.skipUnless(os.name == "posix", "POSIX serial ownership")
    def test_linux_port_contention(self):
        import pty
        import serial

        master, slave = pty.openpty()
        try:
            port = os.ttyname(slave)
            with tempfile.TemporaryDirectory() as t, serial.Serial(port, exclusive=True):
                with self.assertRaises(serial.SerialException):
                    with SurveyAdapter(port, "!00000002", Path(t) / "events.jsonl"):
                        pass
        finally:
            os.close(slave)
            os.close(master)

    def test_soak_requires_the_started_session_and_continuing_progress(self):
        client = SurveyAdapter("fake", "!00000002", "unused")
        client.state = {"session_id": 17, "mode": "bench", "run_state": "running"}
        client.events.put(
            {
                "name": "result",
                "host_monotonic_ns": 12_000_000_000,
                "data": {"session_id": 17, "attempt_id": 1, "status": "timeout"},
            }
        )
        self.assertEqual(check_progress(client, 17, "bench", 0, 5, 6, 13), (1, 12))
        with self.assertRaisesRegex(RuntimeError, "stopped completing"):
            check_progress(client, 17, "bench", 1, 12, 6, 19)
        for change in ({"mode": "survey"}, {"session_id": 22}, {"run_state": "idle"}):
            client.state = {"session_id": 17, "mode": "bench", "run_state": "running", **change}
            with self.assertRaisesRegex(RuntimeError, "state changed"):
                check_progress(client, 17, "bench", 1, 12, 6, 13)

    def test_summary_absent_measurements(self):
        with tempfile.TemporaryDirectory() as t:
            s = summarize(Path(t), "!00000002", ["!00000003"], 0)
            self.assertIsNone(s["rtt_ms"])
            self.assertIsNone(s["round_trips_per_min"])
            self.assertEqual(s["valid_gps_samples"], 0)


if __name__ == "__main__":
    unittest.main()

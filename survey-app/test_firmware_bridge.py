"""Transport-free tests for the public SurveyAdapter boundary and v1 data mapping."""

import importlib.util
import inspect
import os
import queue
import tempfile
import time
import unittest
from pathlib import Path

from firmware_bridge import FirmwareBridge
from recorder import Recorder, command


class MemoryClient:
    def __init__(self):
        self.host_boot = "host-fixture"
        self.heartbeat_ms = 750
        self.problem = None
        self.hello = {
            "node_id": "!0000000a",
            "hardware_model": 1,
            "role": "client",
            "commands": ["hello", "get_state", "heartbeat", "pause", "start", "stop"],
            "settings": {"gps_max_age_ms": (500, 10000, 2000)},
            "radio_profile": {"modem_preset": 1},
            "capabilities": {
                "heartbeat_interval_ms": [250, 5000, 1000],
                "radio_profile_control": ["production", "experimental_medium_fast"],
            },
        }
        self.events = queue.Queue()
        self.sent = []
        self.sequences = {"board": 0, self.host_boot: 0}
        self.closed = False

    def publish(self, name, data, boot="board"):
        self.sequences[boot] += 1
        self.events.put(
            {
                "v": 1,
                "kind": "event",
                "name": name,
                "data_source": "live",
                "seq": self.sequences[boot],
                "boot_id": boot,
                "data": data,
                "display_dropped_total": 0,
            }
        )

    def command(self, envelope):
        name = envelope["name"]
        self.sent.append(name)
        if name == "hello":
            self.publish("hello", self.hello)
        if name == "get_state":
            self.publish(
                "state",
                {
                    "run_state": "paused",
                    "session_id": 3,
                    "target_ids": ["!0000000b"],
                    "target_id": "!0000000b",
                    "settings": {"gps_max_age_ms": 2000},
                    "queue_capacity": 20,
                    "queue_free": 18,
                    "success": 7,
                    "timeout": 2,
                    "quiet_remaining_ms": 5300,
                    "interval_ms": 3100,
                    "heartbeat_healthy": 1,
                    "gps_fresh": 1,
                    "segment_id": 1,
                },
            )
        self.publish(
            "ack",
            {"command_id": envelope["id"], "ok": True, "applied": {}, "error": None},
            self.host_boot,
        )

    def read_event(self, timeout):
        return self.events.get(timeout=timeout)

    def close(self):
        self.closed = True


class BridgeTests(unittest.TestCase):
    def test_interleaved_ack_stream_and_numeric_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = MemoryClient()
            host = Recorder(FirmwareBridge(client), tmp)
            try:
                for _ in range(40):
                    host.poll()
                    if host.state.get("target_id"):
                        break
                    time.sleep(0.01)
                self.assertEqual(host.state["session_id"], "board/3")
                self.assertEqual(host.state["counts"], {"attempts": 9, "success": 7})
                self.assertEqual(host.state["queue_depth"], 2)
                self.assertTrue(host.state["heartbeat_ok"])
                self.assertEqual(host.hello["settings"]["gps_max_age_ms"]["max"], 10000)
                self.assertIn(
                    "experimental_medium_fast",
                    host.hello["settings"]["radio_profile"]["choices"],
                )
                self.assertEqual(host.state["settings"]["heartbeat_interval_ms"], 750)
                self.assertEqual(host.gaps, 0)
                # Interleaved USB-host ACK and device events have independent sequences.
                self.assertEqual(client.sent.count("get_state"), 1)
                client.publish(
                    "gps",
                    {
                        "session_id": 3,
                        "valid": True,
                        "lat_deg": 1,
                        "lon_deg": 2,
                        "fix_age_ms": 100,
                    },
                )
                host.poll()
                self.assertEqual(host.state["gps"]["fix_age_ms"], 100)
                client.publish(
                    "result",
                    {
                        "session_id": 3,
                        "attempt_id": 1,
                        "sequence": 1,
                        "status": "success",
                        "tx_start_ms": 130,
                        "rx_ms": 180,
                        "radio_profile": {"modem_preset": 1},
                    },
                )
                host.poll()
                row = host.history(names=["result"])[0]["event"]
                self.assertEqual(row["data"]["tx_mono_ms"], 130)
                self.assertEqual(row["adapter_data"]["session_id"], 3)
                self.assertEqual(
                    host.history(names=["ack"])[0]["event"]["event_stream"],
                    "adapter-host",
                )
                client.problem = "USB unavailable"
                host.poll()
                self.assertIn("USB unavailable", host.adapter_error)
            finally:
                client.problem = None
                host.close()
            self.assertTrue(client.closed)

    def test_requires_device_identity_before_open(self):
        def forbidden(*args):
            self.fail("No device should be opened")

        with self.assertRaisesRegex(ValueError, "explicit"):
            FirmwareBridge.open(forbidden, None, None, None)

    @unittest.skipUnless(
        os.getenv("SURVEY_FIRMWARE_MODULE"),
        "Set SURVEY_FIRMWARE_MODULE to inspect the firmware worktree API",
    )
    def test_actual_python_api_without_opening_serial(self):
        path = Path(os.environ["SURVEY_FIRMWARE_MODULE"])
        spec = importlib.util.spec_from_file_location("firmware_api_fixture", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        inspect.signature(module.SurveyAdapter).bind(
            "unused", "!0000000a", Path("unused")
        )
        inspect.signature(module.SurveyAdapter.command).bind(None, command("hello"))
        inspect.signature(module.SurveyAdapter.read_event).bind(None, timeout=0)

        def forbidden_serial(**kwargs):
            self.fail("Physical serial access is outside GUI QA")

        client = module.SurveyAdapter(
            "unused", "!0000000a", Path("unused"), serial_factory=forbidden_serial
        )
        bridge = FirmwareBridge(client)
        try:
            with self.assertRaises(queue.Empty):
                client.read_event(timeout=0)
            self.assertEqual(bridge.poll(0), [])
        finally:
            bridge.close()

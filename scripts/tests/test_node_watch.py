"""Offline freshness, replay, privacy and terminal checks for the node dashboard."""

from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import sqlite3
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


watch = module("node_watch", "scripts/watch-nodes.py")
sampler = module("node_readings", "scripts/server/node_readings.py")
NOW = 1794555000


def at(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat()


def node():
    return {"radio": "!12345678", "label": "R001", "registered": False, "kind": "repeater"}


class FreshnessTests(unittest.TestCase):
    def test_delayed_telemetry_uses_measurement_not_arrival(self):
        item = sampler.reading(3.8, at(NOW), at(NOW - 1800))
        self.assertEqual(watch.freshness(item, NOW), ("stale", 1800))

    def test_unknown_telemetry_clock_uses_receipt_but_gps_does_not(self):
        item = sampler.reading(3.8, at(NOW - 10))
        self.assertEqual(watch.freshness(item, NOW), ("fresh", 10))
        self.assertEqual(watch.freshness(item, NOW, gps=True), ("unknown", None))

    def test_future_clock_is_unknown(self):
        item = sampler.reading(3.8, at(NOW), at(NOW + 100))
        self.assertEqual(watch.freshness(item, NOW), ("unknown", None))

    def test_colors_age_without_new_snapshots(self):
        item = sampler.reading(3.8, at(NOW))
        for age, state in ((299, "fresh"), (300, "aging"), (899, "aging"), (900, "stale")):
            self.assertEqual(watch.freshness(item, NOW + age)[0], state)


class ArchiveTests(unittest.TestCase):
    def test_duplicate_transport_copy_cannot_renew_a_sample(self):
        state = sampler.Measurements([node()])
        state.put("!12345678", "voltage", 3.8, at(NOW - 100), sample="packet-a")
        state.put("!12345678", "voltage", 3.8, at(NOW), sample="packet-a")
        self.assertEqual(state.nodes["!12345678"]["readings"]["voltage"]["receivedAt"], at(NOW - 100))
        self.assertTrue(state.unique("packet-a"))
        self.assertFalse(state.unique("packet-a"))

    def test_out_of_order_source_cannot_replace_latest(self):
        state = sampler.Measurements([node()])
        state.put("!12345678", "voltage", 3.8, at(NOW), at(NOW - 5), "new")
        state.put("!12345678", "voltage", 4.2, at(NOW + 10), at(NOW - 100), "old")
        self.assertEqual(state.nodes["!12345678"]["readings"]["voltage"]["value"], 3.8)

    def test_metrics_keep_independent_clocks(self):
        state = sampler.Measurements([node()])
        state.put("!12345678", "voltage", 3.8, at(NOW - 1800))
        state.put("!12345678", "inaCurrent", 12, at(NOW))
        readings = state.nodes["!12345678"]["readings"]
        self.assertEqual(watch.freshness(readings["voltage"], NOW)[0], "stale")
        self.assertEqual(watch.freshness(readings["inaCurrent"], NOW)[0], "fresh")

    def test_seed_omits_coordinates_and_preserves_old_battery_age(self):
        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        db.execute("CREATE TABLE devices (key,lastContactAt,readings,latestPosition)")
        db.execute("INSERT INTO devices VALUES (?,?,?,?)", ("old-r005", at(NOW), json.dumps({
            "battery": {"value": 3.8, "receivedAt": at(NOW - 86400)}}), json.dumps({
            "latitude": 36.123456, "longitude": -115.123456, "measuredAt": at(NOW - 100),
            "receivedAt": at(NOW), "satellites": 6, "pdop": 2.3})))
        state = sampler.Measurements([node()])
        state.seed(db, {"old-r005": "!12345678"})
        output = json.dumps(state.nodes)
        self.assertNotIn("latitude", output)
        self.assertNotIn("longitude", output)
        self.assertNotIn("36.123456", output)
        self.assertEqual(watch.freshness(state.nodes["!12345678"]["readings"]["voltage"], NOW)[0], "stale")

    def test_physical_roster_overrides_old_portal_label(self):
        cfg = {"members": {"!11111111": "b002"}, "gateways": {"!22222222": "g001"},
               "infrastructure": {"!12345678": "r005", "!22222222": "g001"}}
        nodes = sampler.configured_nodes(cfg, {"!12345678": "R001", "!33333333": "R008"})
        actual = {n["radio"]: n for n in nodes}
        self.assertEqual(actual["!12345678"]["label"], "R001")
        self.assertFalse(actual["!33333333"]["registered"])
        self.assertEqual(actual["!22222222"]["kind"], "gateway")

    def test_invalid_numbers_and_other_payloads_are_ignored(self):
        values = dict(sampler.telemetry_values({"device_metrics": {"voltage": float("nan"), "battery_level": 102},
            "environment_metrics": {"temperature": 999, "current": -0.2}, "power_metrics": {"ch1_voltage": 4.1},
            "text": {"message": "private message"}}))
        self.assertEqual(values, {"envCurrent": -0.2, "inaVoltage": 4.1})


class TerminalTests(unittest.TestCase):
    def snapshot(self):
        n = node()
        n.update(lastContactAt=at(NOW), readings={"voltage": sampler.reading(3.8, at(NOW - 600)),
            "inaCurrent": sampler.reading(12.2, at(NOW)), "gps": sampler.reading({"satellites": 9}, at(NOW))})
        return {"at": at(NOW), "nodes": [n], "feed": {"connected": True, "heartbeatAt": at(NOW)}}

    def test_monochrome_has_freshness_and_current_inverted_once(self):
        text = watch.Dashboard(False, 300, 900).render(self.snapshot(), NOW, 0)
        self.assertIn("3.800~", text)
        self.assertIn("-12.2", text)
        self.assertIn("Archive only", text)
        self.assertNotIn("\033", text)
        self.assertNotIn("??", text)

    def test_flash_only_after_initial_snapshot_and_expires(self):
        d = watch.Dashboard(True, 300, 900)
        s = self.snapshot()
        d.observe(s, 0)
        self.assertNotIn(";7m", d.render(s, NOW, 0))
        s["nodes"][0]["readings"]["voltage"] = sampler.reading(3.8, at(NOW), sample="new-packet")
        d.observe(s, 1)
        self.assertIn("\033[32;7m", d.render(s, NOW, 1))
        self.assertNotIn(";7m", d.render(s, NOW, 3))

    def test_disconnect_does_not_refresh_feed_or_values(self):
        text = watch.Dashboard(False, 300, 900).render(self.snapshot(), NOW + 1800, 10, "SSH disconnected")
        self.assertIn("Feed OFFLINE", text)
        self.assertIn("3.800!", text)
        self.assertIn("SSH disconnected", text)

    def test_narrow_terminal_keeps_primary_table_and_offers_radio_view(self):
        text = watch.Dashboard(True, 300, 900).render(self.snapshot(), NOW, 0, width=80, height=20)
        ansi = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
        self.assertTrue(all(len(ansi.sub("", line)) < 80 for line in text.splitlines()))
        self.assertLess(len(text.splitlines()), 20)
        self.assertIn("--view radio", text)

    def test_feed_boolean_does_not_hide_dead_heartbeat(self):
        text = watch.Dashboard(False, 300, 900).render(self.snapshot(), NOW + 21, 0)
        self.assertIn("Feed OFFLINE", text)

    def test_legacy_battery_code_is_not_101_percent(self):
        self.assertEqual(watch.format_value("charge", {"value": 101}, 0), "USB*")

    def test_roster_rejects_duplicate_identity(self):
        path = Mock()
        path.read_text.return_value = ("| **R001 / name** | radio **!12345678** |\n"
                                       "| **R002 / name** | radio **!12345678** |\n")
        with self.assertRaises(ValueError):
            watch.load_roster(path)

    def test_terminal_control_in_labels_is_removed(self):
        s = self.snapshot()
        s["nodes"][0]["label"] = "R001\x1b]52;bad\x07"
        text = watch.Dashboard(False, 300, 900).render(s, NOW, 0)
        self.assertNotIn("\x1b", text)
        self.assertNotIn("\x07", text)


if __name__ == "__main__":
    unittest.main()

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


class WatchdogTests(unittest.TestCase):
    def item(self, period=180, received=NOW):
        return {"cadenceSeconds": period, "lastReceivedAt": at(received) if received is not None else None}

    def test_one_missed_cadence_yellow_two_missed_red(self):
        for period in (120, 180, 300, 3600, 10800, 21600, 86400):
            for age, expected in ((period - 1, "fresh"), (period, "aging"),
                                  (period * 2 - 1, "aging"), (period * 2, "stale")):
                with self.subTest(period=period, age=age):
                    state = watch.watchdog_status(self.item(period), NOW + age, NOW)
                    self.assertEqual(state["state"], expected)
                    self.assertEqual(state["missedCycles"], age // period)

    def test_polling_grace_does_not_add_an_extra_cycle(self):
        self.assertEqual(watch.watchdog_status(self.item(), NOW + 182, NOW, 3)["state"], "fresh")
        self.assertEqual(watch.watchdog_status(self.item(), NOW + 183, NOW, 3)["state"], "aging")
        self.assertEqual(watch.watchdog_status(self.item(), NOW + 363, NOW, 3)["state"], "stale")

    def test_daily_sd_stays_green_for_the_daily_cadence(self):
        state = watch.watchdog_status(self.item(86400), NOW + 20 * 3600, NOW)
        self.assertEqual(state["state"], "fresh")
        self.assertEqual(state["dueInSeconds"], 4 * 3600)

    def test_never_seen_expected_type_arms_and_counts_missing_cycles(self):
        item = self.item(received=None)
        self.assertEqual(watch.watchdog_status(item, NOW + 179, NOW)["state"], "unknown")
        self.assertEqual(watch.watchdog_status(item, NOW + 180, NOW)["state"], "aging")
        self.assertEqual(watch.watchdog_status(item, NOW + 360, NOW)["state"], "stale")

    def test_event_driven_packet_has_age_but_no_missed_deadline(self):
        state = watch.watchdog_status(self.item(None), NOW + 86400, NOW)
        self.assertEqual(state["state"], "event")
        self.assertEqual(state["ageSeconds"], 86400)
        self.assertEqual(state["missedCycles"], 0)
        self.assertIsNone(state["dueInSeconds"])

    def test_neighbor_packets_do_not_reset_missing_device_or_environment(self):
        state = sampler.Measurements([node()], {"!12345678": {"device": 180, "environment": 180, "snns": 180}})
        state.watch("!12345678", "device", at(NOW - 500), "device-old")
        state.watch("!12345678", "environment", at(NOW - 250), "env-old")
        state.watch("!12345678", "snns", at(NOW), "snns-new")
        d = watch.Dashboard(False)
        result = d.watchdogs(state.nodes["!12345678"], NOW)
        self.assertEqual(result["device"]["state"], "stale")
        self.assertEqual(result["environment"]["state"], "aging")
        self.assertEqual(result["snns"]["state"], "fresh")

    def test_duplicate_generation_does_not_pet_watchdog(self):
        state = sampler.Measurements([node()])
        state.watch("!12345678", "sd", at(NOW), "sd:1:9", cadence=86400)
        state.watch("!12345678", "sd", at(NOW + 10000), "sd:1:9", cadence=86400)
        self.assertEqual(state.nodes["!12345678"]["watchdogs"]["sd"]["lastReceivedAt"], at(NOW))

    def test_standard_neighbor_does_not_refresh_passive_neighbor_count(self):
        state = sampler.Measurements([node()])
        state.put("!12345678", "neighbors", 5, at(NOW - 500), sample="snns-old")
        state.watch("!12345678", "snns", at(NOW - 500), "snns-old", cadence=180)
        state.put("!12345678", "standardNeighbors", 9, at(NOW), sample="std-new")
        state.watch("!12345678", "neighbor_info", at(NOW), "std-new", cadence=21600)
        n = state.nodes["!12345678"]
        self.assertEqual(n["readings"]["neighbors"]["value"], 5)
        result = watch.Dashboard(False).watchdogs(n, NOW)
        self.assertEqual(result["snns"]["state"], "stale")
        self.assertEqual(result["neighbor_info"]["state"], "fresh")

    def test_reported_interval_overrides_saved_fallback(self):
        state = sampler.Measurements([node()], {"!12345678": {"gateway": 180}})
        state.watch("!12345678", "gateway", at(NOW), "g:1:1", cadence=300)
        item = state.nodes["!12345678"]["watchdogs"]["gateway"]
        self.assertEqual(item["cadenceSeconds"], 300)
        self.assertEqual(watch.watchdog_status(item, NOW + 299, NOW)["state"], "fresh")

    def test_reconnection_does_not_restart_never_seen_watchdogs(self):
        n = node()
        n.update(readings={}, watchdogs={"device": self.item(received=None)})
        d = watch.Dashboard(False)
        d.observe({"at": at(NOW), "nodes": [n]}, 0)
        d.observe({"at": at(NOW + 350), "nodes": [n]}, 350)
        self.assertEqual(d.watchdogs(n, NOW + 361)["device"]["state"], "stale")

    def test_reconnection_retains_a_known_receipt_missing_from_new_bootstrap(self):
        n = node()
        n.update(readings={}, watchdogs={"device": self.item()})
        d = watch.Dashboard(False)
        d.observe({"at": at(NOW), "nodes": [n]}, 0)
        n["watchdogs"]["device"] = self.item(received=None)
        d.observe({"at": at(NOW + 200), "nodes": [n]}, 200)
        self.assertEqual(d.watchdogs(n, NOW + 200)["device"]["state"], "aging")

    def test_gps_packet_can_be_on_time_without_a_known_fix_timestamp(self):
        n = node()
        n.update(readings={"gps": sampler.reading({"satellites": 9}, at(NOW))},
                 watchdogs={"position": self.item(3600)})
        d = watch.Dashboard(False)
        self.assertEqual(d.watchdogs(n, NOW)["position"]["state"], "fresh")
        self.assertEqual(d.metric_state(n, "gps", n["readings"]["gps"], NOW)[0], "unknown")

    def test_hourly_packets_do_not_extend_the_fifteen_minute_gps_fix_limit(self):
        n = node()
        n.update(readings={}, watchdogs={"position": self.item(3600)})
        item = sampler.reading({"satellites": 9}, at(NOW), at(NOW - 1000))
        self.assertEqual(watch.Dashboard(False).metric_state(n, "gps", item, NOW)[0], "stale")

    def test_new_environment_packet_does_not_refresh_an_omitted_humidity_value(self):
        n = node()
        n.update(readings={}, watchdogs={"environment": self.item()})
        humidity = sampler.reading(35, at(NOW - 500))
        d = watch.Dashboard(False)
        self.assertEqual(d.watchdogs(n, NOW)["environment"]["state"], "fresh")
        self.assertEqual(d.metric_state(n, "humidity", humidity, NOW)[0], "stale")

    def test_baselines_have_actual_hourly_gps_and_daily_sd_exceptions(self):
        data = watch.load_cadences(ROOT / "scripts/node-cadence.json")
        self.assertEqual(data["!da581e5f"]["position"], 3600)
        self.assertEqual(data["!1bbf0638"]["sd"], 86400)
        self.assertEqual(data["!699c2ed8"]["position"], 120)
        self.assertNotIn("environment", data["!699c2ed8"])
        self.assertNotIn("neighbor_info", data["!1bbf0638"])

    def test_watchdog_view_exposes_deadlines_and_independent_statuses(self):
        n = node()
        n.update(readings={}, watchdogs={"device": self.item(180, NOW - 200),
                                       "power": self.item(180, NOW - 400)})
        text = watch.Dashboard(False).render({"at": at(NOW), "nodes": [n]}, NOW, 0, view="watchdogs")
        self.assertIn("3m:+20s~", text)
        self.assertIn("3m:+3:40!", text)
        self.assertIn("1 late, 1 missed 2+", text)


class TerminalTests(unittest.TestCase):
    def snapshot(self):
        n = node()
        n.update(watchdogs={"device": {"cadenceSeconds": 180, "lastReceivedAt": at(NOW - 240)},
                            "power": {"cadenceSeconds": 180, "lastReceivedAt": at(NOW)},
                            "position": {"cadenceSeconds": 120, "lastReceivedAt": at(NOW)}},
                 lastContactAt=at(NOW), readings={"voltage": sampler.reading(3.8, at(NOW - 240)),
            "inaCurrent": sampler.reading(12.2, at(NOW)), "gps": sampler.reading({"satellites": 9}, at(NOW))})
        return {"at": at(NOW), "nodes": [n], "feed": {"connected": True, "heartbeatAt": at(NOW)}}

    def test_monochrome_has_freshness_and_current_inverted_once(self):
        text = watch.Dashboard(False).render(self.snapshot(), NOW, 0)
        self.assertIn("3.800~", text)
        self.assertIn("-12.2", text)
        self.assertIn("Archive only", text)
        self.assertNotIn("\033", text)
        self.assertNotIn("??", text)

    def test_flash_only_after_initial_snapshot_and_expires(self):
        d = watch.Dashboard(True)
        s = self.snapshot()
        d.observe(s, 0)
        self.assertNotIn(";7m", d.render(s, NOW, 0))
        s["nodes"][0]["readings"]["voltage"] = sampler.reading(3.8, at(NOW), sample="new-packet")
        d.observe(s, 1)
        self.assertIn("\033[32;7m", d.render(s, NOW, 1))
        self.assertNotIn(";7m", d.render(s, NOW, 3))

    def test_disconnect_does_not_refresh_feed_or_values(self):
        text = watch.Dashboard(False).render(self.snapshot(), NOW + 1800, 10, "SSH disconnected")
        self.assertIn("Feed OFFLINE", text)
        self.assertIn("3.800!", text)
        self.assertIn("SSH disconnected", text)

    def test_narrow_terminal_keeps_primary_table_and_offers_radio_view(self):
        text = watch.Dashboard(True).render(self.snapshot(), NOW, 0, width=80, height=20)
        ansi = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
        self.assertTrue(all(len(ansi.sub("", line)) < 80 for line in text.splitlines()))
        self.assertLess(len(text.splitlines()), 20)
        self.assertIn("--view radio", text)

    def test_feed_boolean_does_not_hide_dead_heartbeat(self):
        text = watch.Dashboard(False).render(self.snapshot(), NOW + 21, 0)
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
        text = watch.Dashboard(False).render(s, NOW, 0)
        self.assertNotIn("\x1b", text)
        self.assertNotIn("\x07", text)


if __name__ == "__main__":
    unittest.main()

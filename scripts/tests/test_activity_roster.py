"""A running Activity publisher picks up committed operator roster edits."""

from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
with patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    spec = importlib.util.spec_from_file_location("portal_activity", SCRIPTS / "portal-activity.py")
    activity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(activity)
    from server.node_readings import packet_route


class LiveRosterTests(unittest.TestCase):
    def test_add_rename_remove_without_restarting_publisher(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            database, target, config = root / "data.db", root / "cards.json", root / "config.json"
            config.write_text(json.dumps({"members": {}, "infrastructure": {"!00112244": "source"},
                                          "gateways": {"!00112255": "gateway"}}))
            with closing(sqlite3.connect(database, isolation_level=None)) as editor:
                editor.executescript("""
                    CREATE TABLE field_roster(radio, shortName, name, kind);
                    CREATE TABLE devices(key, lastContactAt, readings, latestPosition, configuration, shortName, kind);
                    CREATE TABLE mqtt_archive(receivedAt, envelope, topic);
                    CREATE TABLE packet_receipts(deviceId, receivedAt, gatewayId, outcome, packetKey);
                    CREATE TABLE feed(key, connected, forcedOffline, heartbeatAt);
                    INSERT INTO field_roster VALUES ('!00112244','R002','Source','repeater');
                    INSERT INTO devices VALUES ('source','2026-11-17T00:00:00Z','{}','{}','{}','R002','repeater');
                    INSERT INTO packet_receipts VALUES ('source','2026-11-17T00:00:00Z','gateway','accepted','key');
                """)
                snapshots = []
                edits = iter([
                    "INSERT INTO field_roster VALUES ('!00112233','R001','First site','repeater')",
                    "UPDATE field_roster SET name='New name' WHERE shortName='R001'",
                    "DELETE FROM field_roster WHERE shortName='R001'",
                ])

                def after_publish(_seconds):
                    cards = json.loads(target.read_text())["nodes"]
                    source = next(card for card in cards if card["name"] == "Source")
                    self.assertEqual(source["route"]["reportedHops"], 1)
                    self.assertEqual(source["heardThrough"], "!00112255")
                    self.assertEqual(source["heardThroughRadio"], "!00112255")
                    snapshots.append(([c["name"] for c in cards if c != source], source["route"].get("lastRelayCandidate")))
                    sql = next(edits, None)
                    if sql is None:
                        raise KeyboardInterrupt
                    editor.execute(sql)

                def decoder(cfg, state, backend, by_byte):
                    packet = SimpleNamespace(transport_mechanism=1, hop_start=2, hop_limit=1,
                                             rx_rssi=-90, rx_snr=0, relay_node=0x33)
                    return SimpleNamespace(persisted_route=lambda db, radio, gateway, at, key:
                                           packet_route(packet, radio, gateway, by_byte))

                with patch("server.node_readings.Decoder", decoder), patch("time.sleep", after_publish):
                    activity.main(database, target, config)
                self.assertEqual(snapshots, [([], None), (["First site"], "First site"),
                                             (["New name"], "New name"), ([], None)])

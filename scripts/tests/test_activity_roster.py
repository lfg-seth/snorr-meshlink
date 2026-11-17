"""A running Activity publisher picks up committed operator roster edits."""

from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
with patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    spec = importlib.util.spec_from_file_location("portal_activity", SCRIPTS / "portal-activity.py")
    activity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(activity)


class LiveRosterTests(unittest.TestCase):
    def test_add_rename_remove_without_restarting_publisher(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            database, target, config = root / "data.db", root / "cards.json", root / "config.json"
            config.write_text(json.dumps({"members": {}, "infrastructure": {}, "gateways": {}}))
            with closing(sqlite3.connect(database, isolation_level=None)) as editor:
                editor.executescript("""
                    CREATE TABLE field_roster(radio, shortName, name, kind);
                    CREATE TABLE devices(key, lastContactAt, readings, latestPosition, configuration, shortName, kind);
                    CREATE TABLE mqtt_archive(receivedAt, envelope, topic);
                    CREATE TABLE packet_receipts(deviceId, receivedAt, gatewayId, outcome);
                    CREATE TABLE feed(key, connected, forcedOffline, heartbeatAt);
                """)
                snapshots = []
                edits = iter([
                    "INSERT INTO field_roster VALUES ('!00112233','R001','First site','repeater')",
                    "UPDATE field_roster SET name='New name'",
                    "DELETE FROM field_roster",
                ])

                def after_publish(_seconds):
                    snapshots.append([card["name"] for card in json.loads(target.read_text())["nodes"]])
                    sql = next(edits, None)
                    if sql is None:
                        raise KeyboardInterrupt
                    editor.execute(sql)

                with patch("server.node_readings.Decoder"), patch("time.sleep", after_publish):
                    activity.main(database, target, config)
                self.assertEqual(snapshots, [[], ["First site"], ["New name"], []])

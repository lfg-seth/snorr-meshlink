"""Publish the placed fleet's sanitized activity cards from the local read-only sampler."""
import json
from pathlib import Path
import runpy
from contextlib import closing
import sqlite3
import time

from server.node_readings import run

ROOT = Path(__file__).resolve().parents[1]
DATABASE = Path("/var/lib/meshlink/pb_data/data.db")


def read_roster(db):
    rows = db.execute("SELECT radio, shortName, name, kind FROM field_roster")
    return {radio: {"shortName": label, "name": name, "kind": kind}
            for radio, label, name, kind in rows}


def main(database=DATABASE, target=Path("/run/meshlink-activity/snapshot.json"), config="/etc/meshlink/mqtt.json"):
    cli = runpy.run_path(str(ROOT / "scripts/watch-nodes.py"))
    dashboard = cli["Dashboard"](False, grace=3, show_inactive=True)

    def publish(snapshot):
        if read_roster(db) != sites:
            return False  # Reload selection and bootstrap recent readings for new radios.
        for node in snapshot["nodes"]:
            site = sites[node["radio"]]
            for reading in ("gps", "standardNeighbors"):
                node["readings"].pop(reading, None)
            for stream in ("position", "neighbor_info", "nodeinfo"):
                node["watchdogs"].pop(stream, None)
            if site["kind"] in ("stationBackhaul", "mobileGateway"):
                node["kind"] = "gateway"
            elif site["kind"] == "offlineRecorder":
                node["kind"] = "recorder"
                # Historical uplink readings predate the offline deployment.
                for stream in ("gateway", "wifi", "sd"):
                    node["readings"].pop(stream, None)
                    node["watchdogs"].pop(stream, None)
        dashboard.observe(snapshot, time.monotonic())
        cards = cli["card_snapshot"](dashboard, snapshot, time.time(), False, True, 3)
        for card in cards["nodes"]:
            card["name"] = sites[card["radio"]]["name"]
        pending = target.with_suffix(".pending")
        pending.write_text(json.dumps(cards, allow_nan=False, separators=(",", ":")), encoding="utf-8")
        pending.replace(target)

    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True, timeout=2)) as db:
        while True:
            sites = read_roster(db)
            labels = {radio: site["shortName"] for radio, site in sites.items()}
            reload_requested = run({"roster": labels, "selected": labels, "interval": 3, "hours": 24,
                                    "siteNames": {radio: site["name"] for radio, site in sites.items()},
                                    "cadences": cli["load_cadences"](ROOT / "scripts/node-cadence.json"),
                                    "config": config, "database": str(database),
                                    "backend": str(ROOT / "backend")}, publish)
            if not reload_requested:
                break


if __name__ == "__main__":
    main()

"""Publish field infrastructure and member tracker activity for the signed-in portal."""
import json
from pathlib import Path
import runpy
from contextlib import closing
import sqlite3
import time

from server.node_readings import epoch, run, utc

ROOT = Path(__file__).resolve().parents[1]
DATABASE = Path("/var/lib/meshlink/pb_data/data.db")
MEMBER_DEVICE_PERIOD = 180
TELEMETRY_PERIOD = 45 * 60
TELEMETRY_STREAMS = ("device", "environment", "power", "snns", "gateway", "wifi")


def apply_activity_cadence(watchdogs):
    """Use the field interval even when an older gateway receipt advertises less."""
    watchdogs.setdefault("device", {})
    for stream in TELEMETRY_STREAMS:
        if stream in watchdogs:
            watch = watchdogs[stream]
            watch["cadenceSeconds"] = max(TELEMETRY_PERIOD, watch.get("cadenceSeconds") or 0)




def read_roster(db, config, repeaters):
    sites = {}
    devices = {}
    for key, label, kind, radio in db.execute("""
        SELECT key, shortName, kind, json_extract(configuration, '$.radioNodeId') FROM devices
    """):
        devices[key] = label
        if radio:
            sites[radio] = {"shortName": label or radio, "kind": kind, "key": key}

    gateways = config.get("gateways", {})
    for radio, key in {**config.get("infrastructure", {}), **gateways}.items():
        kind = "stationBackhaul" if radio in gateways else "repeater"
        sites[radio] = {"shortName": devices.get(key) or radio, "kind": kind, "key": key}
    for radio, key in config["members"].items():
        sites[radio] = {"shortName": devices.get(key) or radio, "kind": "member", "key": key}

    # Physical repeater numbers survive storage-key changes and site removals.
    for radio, label in repeaters.items():
        sites[radio] = {**sites.get(radio, {}), "shortName": label, "kind": "repeater"}
    for radio, label, name, kind in db.execute("SELECT radio, shortName, name, kind FROM field_roster"):
        sites[radio] = {**sites.get(radio, {}), "shortName": label, "name": name, "kind": kind}
    return sites


def label_members(db, sites, cards):
    # A recent packet keeps its carrier at first receipt, even after a handoff.
    oldest_receipt = min((packet["received"] for packet in cards["packets"]), default=cards["now"])
    cutoff = utc(oldest_receipt).replace("+00:00", "Z")
    assignments = {}
    for key, name, start, end in db.execute("""
        SELECT a.deviceId, m.name, a.startedAt, a.endedAt
        FROM assignments a JOIN members m ON m.key = a.memberId
        WHERE a.endedAt = '' OR a.endedAt >= ?
        ORDER BY a.startedAt DESC
    """, (cutoff,)):
        assignments.setdefault(key, []).append((epoch(start), epoch(end), name))

    def assigned_name(site, at):
        return next((name for start, end, name in assignments.get(site["key"], [])
                     if start is not None and start <= at and (end is None or at < end)), None)

    for card in cards["nodes"]:
        site = sites[card["radio"]]
        name = assigned_name(site, cards["now"]) if site["kind"] == "member" else site.get("name")
        card["unassigned"] = name is None
        card["name"] = name or "Unassigned"
    for packet in cards["packets"]:
        site = sites[packet["radio"]]
        if site["kind"] == "member":
            packet["memberName"] = assigned_name(site, packet["received"])


def main(database=DATABASE, target=Path("/run/meshlink-activity/snapshot.json"), config="/etc/meshlink/mqtt.json"):
    cli = runpy.run_path(str(ROOT / "scripts/watch-nodes.py"))
    dashboard = cli["Dashboard"](False, grace=3, show_inactive=True)

    repeaters = cli["load_roster"](ROOT / "records/deployment-nodes.md")

    def current_roster():
        return read_roster(db, json.loads(Path(config).read_text()), repeaters)

    def publish(snapshot):
        if current_roster() != sites:
            return False  # Reload selection and bootstrap recent readings for new radios.
        # Prepare display copies; the sampler retains its raw intervals and readings.
        snapshot = {**snapshot, "nodes": [
            {**node, "watchdogs": {s: w.copy() for s, w in node["watchdogs"].items()},
             "readings": node["readings"].copy()} for node in snapshot["nodes"]
        ]}
        for node in snapshot["nodes"]:
            site = sites[node["radio"]]
            if site["kind"] == "member":
                device = node["watchdogs"].setdefault("device", {})
                if not device.get("cadenceSeconds"):
                    device["cadenceSeconds"] = MEMBER_DEVICE_PERIOD
                node["kind"] = "member"
                continue
            apply_activity_cadence(node["watchdogs"])
            for reading in ("gps", "standardNeighbors"):
                node["readings"].pop(reading, None)
            for stream in ("position", "neighbor_info", "nodeinfo"):
                node["watchdogs"].pop(stream, None)
            if site["kind"] in ("stationBackhaul", "mobileGateway", "gateway"):
                node["kind"] = "gateway"
            elif site["kind"] == "offlineRecorder":
                node["kind"] = "recorder"
                # Historical uplink readings predate the offline deployment.
                for stream in ("gateway", "wifi", "sd"):
                    node["readings"].pop(stream, None)
                    node["watchdogs"].pop(stream, None)
        dashboard.observe(snapshot, time.monotonic())
        cards = cli["card_snapshot"](dashboard, snapshot, time.time(), False, True, 3)
        cards["packets"] = snapshot["packets"]
        for card in cards["nodes"]:
            # All portal cards have a cadence. An unusable contact time means silence.
            if card["health"] == "unknown":
                card["health"] = "silent"
        label_members(db, sites, cards)
        pending = target.with_suffix(".pending")
        pending.write_text(json.dumps(cards, allow_nan=False, separators=(",", ":")), encoding="utf-8")
        pending.replace(target)

    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True, timeout=2)) as db:
        while True:
            sites = current_roster()
            labels = {radio: site["shortName"] for radio, site in sites.items()}
            reload_requested = run({"roster": labels, "selected": labels, "interval": 3, "hours": 24,
                                    "deviceRadios": {site["key"]: radio for radio, site in sites.items() if "key" in site},
                                    "siteNames": {radio: site.get("name", site["shortName"])
                                                  for radio, site in sites.items() if site["kind"] != "member"},
                                    "cadences": cli["load_cadences"](ROOT / "scripts/node-cadence.json"),
                                    "config": config, "database": str(database),
                                    "backend": str(ROOT / "backend")}, publish)
            if not reload_requested:
                break


if __name__ == "__main__":
    main()

"""Publish the placed fleet's sanitized activity cards from the local read-only sampler."""
import json
from pathlib import Path
import runpy
import time

from server.node_readings import run

ROOT = Path(__file__).resolve().parents[1]


def main():
    cli = runpy.run_path(str(ROOT / "scripts/watch-nodes.py"))
    sites = {site["radio"]: site for site in json.loads((ROOT / "portal/src/placements.json").read_text())}
    # Mobile gateways appear in Activity without a fixed deployment pin.
    sites["!849ad7a0"] = {"shortName": "G003", "name": "Seth Mobile", "mobileGateway": True}
    labels = {radio: site["shortName"] for radio, site in sites.items()}
    dashboard = cli["Dashboard"](False, grace=3, show_inactive=True)
    target = Path("/run/meshlink-activity/snapshot.json")

    def publish(snapshot):
        for node in snapshot["nodes"]:
            site = sites[node["radio"]]
            if site["shortName"].startswith("R"):
                for reading in ("gps", "standardNeighbors"):
                    node["readings"].pop(reading, None)
                for stream in ("position", "neighbor_info", "nodeinfo"):
                    node["watchdogs"].pop(stream, None)
            elif site.get("stationBackhaul") or site.get("mobileGateway"):
                node["kind"] = "gateway"
            elif site.get("offlineRecorder"):
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

    run({"roster": labels, "selected": labels, "interval": 3, "hours": 24,
         "cadences": cli["load_cadences"](ROOT / "scripts/node-cadence.json"),
         "config": "/etc/meshlink/mqtt.json", "database": "/var/lib/meshlink/pb_data/data.db",
         "backend": str(ROOT / "backend")}, publish)


if __name__ == "__main__":
    main()

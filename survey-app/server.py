"""Loopback-only survey host. Tailscale Serve owns the private TLS endpoint."""

import argparse
import csv
import io
import json
import mimetypes
import os
import re
import sqlite3
import threading
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from recorder import Recorder, compact, load_adapter

APP = Path(__file__).resolve().parent
DATA = APP.parent / "local-data" / "direct-hop-survey"
ASSETS = {"index.html", "app.js", "survey.css", "map.js"}
VIEWS = {
    "result",
    "gps",
    "attempt",
    "fault",
    "quiet",
    "state",
    "statistics",
    "gap",
    "duplicate_delivery",
    "transport_lost",
    "adapter_reconnected",
    "adapter_error",
    "ack",
    "host_open",
    "host_command",
    "hello",
    "site_record",
}
IDENT = re.compile(r"[\w.!\-]{1,100}\Z")


def valid_target_id(node):
    return (
        isinstance(node, str)
        and re.fullmatch(r"![0-9a-fA-F]{8}", node)
        and 1 < int(node[1:], 16) < 0xFFFFFFFF
    )


def read_target_roster(path):
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, dict):
        raise ValueError("Target roster must be an object keyed by mesh ID")
    names, sites = {}, {}
    for node, record in records.items():
        if not valid_target_id(node) or node.lower() in names:
            raise ValueError(f"Invalid or duplicate target mesh ID: {node}")
        node = node.lower()
        if not isinstance(record, dict) or any(
            not isinstance(record.get(key), str) or not record[key].strip()
            for key in ("short_name", "long_name")
        ):
            raise ValueError(f"Target {node} requires short_name and long_name")
        names[node] = {
            key: record[key].strip() for key in ("short_name", "long_name")
        }
        if "site" in record:
            site = record["site"]
            lat, lon = float(site["lat_deg"]), float(site["lon_deg"])
            label = site["name"]
            if (
                not -90 <= lat <= 90
                or not -180 <= lon <= 180
                or not isinstance(label, str)
                or not label.strip()
            ):
                raise ValueError(f"Invalid fixed site for {node}")
            sites[node] = {"lat_deg": lat, "lon_deg": lon, "site_name": label.strip()}
    return names, sites


@contextmanager
def source_lease(directory):
    """OS releases this lease automatically after a crash."""
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "owner.lock").open("a+b") as lease:
        if lease.tell() == 0:
            lease.write(b"0")
            lease.flush()
        lease.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(lease.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeError(
                "Another host already owns this source directory"
            ) from exc
        yield


class SurveyHandler(BaseHTTPRequestHandler):
    server_version = "SurveyHost/1"

    def log_message(self, *args):
        pass

    def reply(self, body, status=200, mime="application/json", **headers):
        if mime == "application/json":
            body = compact(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header(
            "Cache-Control",
            "no-store" if not mime.startswith("image/") else "private, max-age=300",
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
        )
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    @property
    def host(self):
        return self.server.recorder

    def do_GET(self):
        try:
            path = urlsplit(self.path)
            q = {k: vs[-1] for k, vs in parse_qs(path.query).items()}
            asset = path.path.removeprefix("/") or "index.html"
            if asset in ASSETS:
                self.reply(
                    (APP / "web" / asset).read_bytes(),
                    mime=mimetypes.guess_type(asset)[0] or "text/plain",
                )
            elif path.path in ("/map/area.json", "/map/terrain.png"):
                name = path.path.split("/")[-1]
                file = self.host.root.parent / "map" / name
                if file.is_file():
                    self.reply(
                        file.read_bytes(),
                        mime="image/png"
                        if name.endswith("png")
                        else "application/geo+json",
                    )
                else:
                    self.reply({"error": "Offline area is not installed"}, 404)
            elif path.path == "/api/state":
                snapshot = self.host.snapshot(self.headers.get("X-Survey-Controller"))
                self.reply(
                    snapshot | {
                        "known_targets": self.server.known_targets,
                        "target_names": self.server.target_names,
                    }
                )
            elif path.path == "/api/ack":
                with self.host.lock:
                    row = self.host.db.execute(
                        "SELECT ack FROM commands WHERE id=?", (q.get("id"),)
                    ).fetchone()
                self.reply({"ack": json.loads(row[0]) if row and row[0] else None})
            elif path.path == "/api/events":
                names = q["names"].split(",") if q.get("names") else None
                if names and not set(names) <= VIEWS:
                    raise ValueError("Unknown event selection")
                self.reply(
                    self.host.history(
                        int(q["after"]) if "after" in q else None,
                        int(q["before"]) if "before" in q else None,
                        q.get("session"),
                        names,
                        limit=min(500, max(1, int(q.get("limit", 220)))),
                    )
                )
            elif path.path == "/api/sessions":
                with self.host.lock:
                    rows = self.host.db.execute(
                        "SELECT id,first,last,events FROM sessions ORDER BY last DESC LIMIT 200"
                    )
                    sessions = [
                        {"id": s, "first": a, "last": b, "events": n}
                        for s, a, b, n in rows
                    ]
                self.reply(sessions)
            elif path.path in ("/export.csv", "/export.jsonl"):
                self.export(path.path.endswith("csv"), q.get("session"))
            else:
                self.reply({"error": "Unknown resource"}, 404)
        except (ValueError, TypeError) as e:
            self.reply({"error": str(e)}, 400)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass
        except (OSError, sqlite3.Error) as e:
            self.reply({"error": str(e)}, 503)

    def export(self, as_csv, session):
        self.send_response(200)
        ext = "csv" if as_csv else "jsonl"
        self.send_header(
            "Content-Type", "text/csv" if as_csv else "application/x-ndjson"
        )
        self.send_header(
            "Content-Disposition",
            f'attachment; filename="survey-{self.host.adapter.source}.{ext}"',
        )
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        fields = [
            "cursor",
            "received_ms",
            "data_source",
            "boot_id",
            "seq",
            "name",
            "session_id",
            "segment_id",
            "attempt_id",
            "target_id",
            "target_lat_deg",
            "target_lon_deg",
            "mode",
            "status",
            "profile",
            "rtt_ms",
            "enqueue_mono_ms",
            "tx_mono_ms",
            "receive_mono_ms",
            "local_util_pct",
            "remote_util_pct",
            "uplink_rssi_dbm",
            "uplink_snr_db",
            "downlink_rssi_dbm",
            "downlink_snr_db",
            "lat_deg",
            "lon_deg",
            "fix_utc_ms",
            "fix_age_ms",
            "reason",
        ]
        output = io.StringIO()
        writer = csv.DictWriter(output, fields, extrasaction="ignore")
        if as_csv:
            writer.writeheader()
        cursor, ceiling = 0, self.host.cursor
        while cursor < ceiling:
            rows = self.host.history(cursor, ceiling + 1, session, limit=300)
            if not rows:
                break
            for r in rows:
                e, d = r["event"], r["event"]["data"]
                if as_csv:
                    flat = r | e | d | (d.get("gps") or {})
                    fixed = e.get("host_context", {}).get("fixed_sites", {})
                    location = (
                        fixed.get(d.get("target_id"), d.get("target_location")) or {}
                    )
                    flat["target_lat_deg"] = location.get("lat_deg")
                    flat["target_lon_deg"] = location.get("lon_deg")
                    for direction in ("uplink", "downlink"):
                        for key, value in (d.get(direction) or {}).items():
                            flat[direction + "_" + key] = value
                    writer.writerow(flat)
                else:
                    output.write(compact(r) + "\n")
            self.wfile.write(output.getvalue().encode())
            output.seek(0)
            output.truncate()
            cursor = rows[-1]["cursor"]
        if output.tell():
            self.wfile.write(output.getvalue().encode())

    def do_POST(self):
        try:
            origin, host = self.headers.get("Origin"), self.headers.get("Host", "")
            if origin and urlsplit(origin).netloc != host:
                self.reply({"error": "Cross-origin request denied"}, 403)
                return
            size = int(self.headers.get("Content-Length", "0"))
            if (
                self.headers.get_content_type() != "application/json"
                or not 0 < size <= 32768
            ):
                raise ValueError("Expected a small JSON object")
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise TypeError("Expected JSON object")
            token = self.headers.get("X-Survey-Controller", "")
            if not 12 <= len(token) <= 100:
                raise ValueError("Missing browser control header")
            with self.host.lock:
                if self.path == "/api/control":
                    self.host.controller = token
                    result = {"ok": True}
                elif self.path == "/api/command":
                    result = self.host.dispatch(
                        payload.get("command"), token, payload.get("revision")
                    )
                elif (
                    self.path == "/api/simulation"
                    and self.host.adapter.source == "simulation"
                ):
                    self.host.check_controller(token)
                    self.host.adapter.change_scenario(
                        payload.get("scenario"), int(time.monotonic() * 1000)
                    )
                    self.host.poll()
                    result = {"ok": True}
                elif self.path == "/api/sites":
                    self.host.check_controller(token)
                    if self.host.state.get("run_state") == "running":
                        raise ValueError("Pause before editing fixed site records")
                    records = payload.get("sites")
                    if not isinstance(records, list) or not 1 <= len(records) <= 100:
                        raise ValueError("Expected 1–100 site records")
                    sites = {}
                    for row in records:
                        ident, lat, lon = (
                            row["id"],
                            float(row["lat_deg"]),
                            float(row["lon_deg"]),
                        )
                        if (
                            not IDENT.fullmatch(ident)
                            or not -90 <= lat <= 90
                            or not -180 <= lon <= 180
                        ):
                            raise ValueError("Invalid site ID or location")
                        sites[ident] = {"lat_deg": lat, "lon_deg": lon}
                    self.host.db.execute("BEGIN")
                    try:
                        for key, pos in sites.items():
                            self.host.db.execute(
                                "INSERT OR REPLACE INTO sites VALUES(?,?,?)",
                                (key, pos["lat_deg"], pos["lon_deg"]),
                            )
                        self.host.note("site_record", {"sites": sites})
                        self.host.db.commit()
                    except Exception:
                        self.host.db.rollback()
                        raise
                    self.host.site_records.update(sites)
                    result = {"ok": True}
                else:
                    self.reply({"error": "Unsupported endpoint for this source"}, 404)
                    return
            self.reply(result)
        except (ValueError, KeyError, TypeError) as e:
            self.reply({"ok": False, "error": str(e)}, 400)
        except (OSError, sqlite3.Error) as e:
            self.reply({"ok": False, "error": str(e)}, 503)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["simulation", "live"], required=True)
    parser.add_argument("--adapter", type=Path)
    parser.add_argument("--device", help="Explicit firmware client serial device")
    parser.add_argument("--expected-id", help="Expected firmware client node ID")
    parser.add_argument(
        "--known-target",
        action="append",
        default=[],
        metavar="NODE_ID",
        help="Offer this repeater in the live target selector (repeatable)",
    )
    parser.add_argument(
        "--target-roster", type=Path, help="JSON names and fixed sites for live targets"
    )
    parser.add_argument("--port", type=int, default=5187)
    parser.add_argument("--data-dir", type=Path, default=DATA)
    args = parser.parse_args()
    if args.known_target and args.source != "live":
        parser.error("--known-target requires --source live")
    if any(not valid_target_id(node) for node in args.known_target):
        parser.error("--known-target requires a non-reserved !xxxxxxxx node ID")
    names, sites = {}, {}
    if args.target_roster:
        if args.source != "live":
            parser.error("--target-roster requires --source live")
        try:
            names, sites = read_target_roster(args.target_roster)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            parser.error(f"Invalid target roster: {exc}")
    with source_lease(args.data_dir / args.source):
        serve(args, names, sites)


def serve(args, names, sites):
    server = ThreadingHTTPServer(("127.0.0.1", args.port), SurveyHandler)
    selected = dict.fromkeys(node.lower() for node in args.known_target)
    server.known_targets = list(selected | names)
    server.target_names = names
    adapter = load_adapter(
        args.source, args.adapter, args.device, args.expected_id, args.data_dir
    )
    host = server.recorder = Recorder(adapter, args.data_dir, configured_sites=sites)
    host.start_worker()
    stop_file = host.root / f"stop-{os.getpid()}"
    stop_file.unlink(missing_ok=True)

    def watch_stop():
        while not host.stop_event.wait(0.5):
            if stop_file.is_file():
                server.shutdown()
                return

    threading.Thread(target=watch_stop, daemon=True).start()
    print(
        f"{args.source} survey listening on http://127.0.0.1:{server.server_port}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        host.close()
        stop_file.unlink(missing_ok=True)


if __name__ == "__main__":
    main()

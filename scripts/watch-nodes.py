#!/usr/bin/env python3
"""Live node readings over read-only SSH; local Python and OpenSSH are enough."""

import argparse
from collections import deque
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
ESC = "\033["
COLORS = {"fresh": "32", "aging": "33", "stale": "31", "unknown": "90"}
METRICS = [
    ("Node", 10, None), ("Seen", 6, "contact"), ("Dev V", 7, "voltage"),
    ("Batt", 6, "charge"), ("INA V", 7, "inaVoltage"), ("mA", 8, "inaCurrent"),
    ("Temp C", 7, "temperature"), ("RH %", 6, "humidity"), ("Busy %", 7, "busy"),
    ("TX %", 6, "tx"), ("Up", 6, "uptime"), ("Nbr", 4, "neighbors"), ("GPS age", 7, "gps"),
]


def epoch(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None


def clean(value):
    return "".join(c for c in str(value) if c.isascii() and c.isprintable())


def duration(seconds):
    if seconds is None or seconds < 0:
        return "?"
    if seconds < 60:
        return f"{int(seconds)}s"
    if seconds < 3600:
        return f"{int(seconds // 60)}m"
    if seconds < 86400:
        return f"{seconds / 3600:.1f}h"
    return f"{int(seconds // 86400)}d"


def freshness(item, now, fresh=300, stale=900, gps=False):
    if not item:
        return "unknown", None
    if item.get("quality") == "future":
        return "unknown", None
    source = epoch(item.get("measuredAt"))
    if gps and source is None:
        return "unknown", None
    stamp = source if source is not None else epoch(item.get("receivedAt"))
    if stamp is None or stamp > now:
        return "unknown", None
    age = now - stamp
    return ("fresh" if age < fresh else "aging" if age < stale else "stale"), age


def format_value(metric, item, age):
    if not item:
        return "--"
    v = item["value"]
    if metric in ("contact", "gps"):
        return duration(age)
    if metric == "charge":
        return "USB*" if v == 101 else f"{v:.0f}%"
    if metric == "uptime":
        return duration(v)
    if metric in ("voltage", "inaVoltage"):
        return f"{v:.3f}"
    if metric == "inaCurrent":
        # Match the portal's single inversion at the display boundary.
        return f"{-v:+.1f}" if v else "0.0"
    if metric in ("temperature", "humidity", "busy"):
        return f"{v:.1f}"
    if metric == "tx":
        return f"{v:.2f}"
    return clean(v)


def load_roster(path):
    text = path.read_text(encoding="utf-8")
    roster = {}
    labels = set()
    for line in text.splitlines():
        label = re.match(r"\|\s*\*\*(R\d{3})\b", line)
        if not label:
            continue
        radio = re.search(r"radio\s+\*\*(![0-9a-fA-F]{8})\*\*", line)
        if not radio:
            raise ValueError(f"Missing radio ID for {label[1]} in roster")
        node = radio[1].lower()
        if node in roster or label[1] in labels:
            raise ValueError("Duplicate radio ID or label in roster")
        roster[node] = label[1]
        labels.add(label[1])
    if not roster:
        raise ValueError("No fresh Rxxx physical-radio rows found in roster")
    return roster


class Dashboard:
    def __init__(self, color, fresh, stale, flash=1.5):
        self.color, self.fresh, self.stale, self.flash = color, fresh, stale, flash
        self.samples = {}
        self.highlights = {}
        self.initialized = False

    def observe(self, snapshot, tick):
        for node in snapshot["nodes"]:
            for metric, item in node["readings"].items():
                key = (node["radio"], metric)
                signature = item.get("sample") or (item.get("receivedAt"), item.get("measuredAt"))
                if self.initialized and signature != self.samples.get(key):
                    self.highlights[key] = tick + self.flash
                self.samples[key] = signature
        self.initialized = True

    def cell(self, node, metric, width, now, tick):
        if metric is None:
            return clean(node["label"]).ljust(width)[:width]
        item = (dict(value=0, receivedAt=node["lastContactAt"], measuredAt=None)
                if metric == "contact" and node.get("lastContactAt") else node["readings"].get(metric))
        state, age = freshness(item, now, self.fresh, self.stale, gps=metric == "gps")
        value = format_value(metric, item, age)
        # Monochrome terminals still expose each cell's freshness.
        marker = {"fresh": "", "aging": "~", "stale": "!", "unknown": "?"}[state] if item else ""
        if not self.color:
            if not value.endswith(marker) or not marker:
                value += marker
        value = clean(value).rjust(width)[-width:]
        if not self.color:
            return value
        highlight = self.highlights.get((node["radio"], metric), 0) > tick
        return ESC + COLORS[state] + (";7" if highlight else "") + "m" + value + ESC + "0m"

    def render(self, snapshot, now, tick, status="", width=140, height=None, view="all"):
        feed = snapshot.get("feed", {})
        beat = epoch(feed.get("heartbeatAt"))
        online = feed.get("connected") and beat is not None and 0 <= now - beat < 20
        sampled = epoch(snapshot.get("at"))
        lag = now - sampled if sampled is not None else None
        title = "SNORR MeshLink | " + datetime.fromtimestamp(now).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        title += f" | Feed {'ONLINE' if online else 'OFFLINE'} | Snapshot {duration(lag)} ago"
        if self.color and (not online or lag is None or lag > 15):
            title = ESC + "31m" + title + ESC + "0m"
        lines = [title, "READ ONLY | " + (status or "Connected over SSH")]
        narrow = view == "all" and width < 100
        columns = METRICS[:8] if view == "power" or narrow else METRICS[:2] + METRICS[8:] if view == "radio" else METRICS
        sections = [("", columns)]
        for heading, columns in sections:
            if heading:
                lines.append(heading)
            lines.append(" ".join(name.ljust(size) for name, size, _ in columns))
            lines.append(" ".join("-" * size for _, size, _ in columns))
            for node in sorted(snapshot["nodes"], key=lambda n: (
                    0 if n["label"].startswith("R") else 1 if n["label"].startswith("G") else 2 if n["label"].startswith("Legacy") else 3,
                    n["label"])):
                lines.append(" ".join(self.cell(node, metric, size, now, tick) for _, size, metric in columns))
        lines += ["", "Fresh <5m green | Aging 5-15m yellow/~ | Stale >=15m red/! | Unknown gray/?".replace(
            "<5m", "<" + duration(self.fresh)).replace("5-15m", duration(self.fresh) + "-" + duration(self.stale)).replace(
            ">=15m", ">=" + duration(self.stale)),
            "New sample: brief highlight. mA: + charging / - discharging. USB*: charging or no detected battery.",
            "Telemetry ages use source time when known, receipt otherwise. GPS age always needs a GPS measurement time."]
        unregistered = [n["label"] for n in snapshot["nodes"] if not n.get("registered", True)]
        if unregistered:
            lines.append("Archive only (not registered in portal): " + ", ".join(clean(label) for label in unregistered))
        for node in snapshot["nodes"]:
            r = node["readings"]
            details = []
            gateway = r.get("gateway")
            if gateway:
                health = gateway["value"]
                state, age = freshness(gateway, now, health.get("intervalSeconds", 300) * 3,
                                       health.get("intervalSeconds", 300) * 3)
                details.append(f"Wi-Fi {'up' if health.get('wifiConnected') else 'down'}, MQTT "
                               f"{'up' if health.get('mqttConnected') else 'down'} (report {duration(age)} old"
                               + (", STALE" if state != "fresh" else "") + ")")
            if r.get("wifi"):
                state, age = freshness(r["wifi"], now, self.fresh, self.stale)
                wifi = r["wifi"]["value"]
                details.append(f"Wi-Fi {wifi.get('rssiDbm', '?')} dBm ({duration(age)} old)")
            if r.get("sd"):
                item = r["sd"]
                sd = item["value"]
                _, age = freshness(item, now, 86400, 3 * 86400)
                details.append(f"SD {sd.get('usedBytes', '?')}/{sd.get('totalBytes', '?')} bytes, "
                               f"{sd.get('dropped', '?')} dropped (daily report {duration(age)} old)")
            if r.get("gps"):
                item = r["gps"]
                gps = item["value"]
                _, arrival = freshness({**item, "measuredAt": None, "quality": "unknown"}, now, self.fresh, self.stale)
                details.append(f"GPS {gps.get('satellites') or '?'} sats, PDOP {gps.get('pdop') or '?'}, "
                               f"alt {gps.get('altitude', '?')}m (received {duration(arrival)} ago)")
            if details:
                lines.append(clean(node["label"] + ": " + "; ".join(details)))
        if snapshot.get("catchingUp"):
            lines.append("Catching up with archived arrivals...")
        if snapshot.get("skipped"):
            lines.append(f"Malformed/unsupported archive rows skipped: {snapshot['skipped']}")
        lines.append("Ctrl+C to exit. Values keep aging if the SSH connection or ingestion feed stops.")
        if narrow:
            lines.insert(2, "Narrow terminal: power view. Widen to 100 columns or use --view radio.")
        if height and len(lines) > height - 1:
            omitted = len(lines) - height + 2
            lines = lines[:height - 2] + [f"{omitted} detail lines hidden; enlarge terminal or use --once. Ctrl+C exits."]
        lines = [clip_line(line, width - 1) for line in lines]
        return "\n".join(lines)


def clip_line(line, width):
    tokens = re.findall(r"\x1b\[[0-9;?]*[A-Za-z]|.", line)
    visible = sum(not token.startswith("\x1b") for token in tokens)
    if visible <= width:
        return line
    result, count = [], 0
    for token in tokens:
        if not token.startswith("\x1b"):
            if count >= max(0, width - 1):
                break
            count += 1
        result.append(token)
    return "".join(result) + ">" + ESC + "0m" if "\x1b" in line else "".join(result) + ">"


class SSHStream:
    def __init__(self, args, roster):
        settings = {"roster": roster, "interval": args.interval, "hours": args.hours, "once": args.once,
                    "database": args.database, "config": args.config, "backend": args.backend}
        source = (ROOT / "scripts/server/node_readings.py").read_text(encoding="utf-8")
        source += "\nrun(json.loads(" + repr(json.dumps(settings)) + "))\n"
        self.process = subprocess.Popen(
            ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
             "-o", "ServerAliveInterval=10", "-o", "ServerAliveCountMax=2", args.host,
             args.remote_python, "-u", "-"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", bufsize=1)
        self.events = queue.Queue(maxsize=2)
        self.errors = deque(maxlen=3)
        threading.Thread(target=self.read, daemon=True).start()
        threading.Thread(target=self.read_errors, daemon=True).start()
        try:
            self.process.stdin.write(source)
            self.process.stdin.close()
        except (OSError, BrokenPipeError):
            self.close()
            raise

    def read(self):
        for line in self.process.stdout:
            try:
                item = json.loads(line)
                if not isinstance(item, dict) or ("nodes" not in item and "error" not in item):
                    continue
                if self.events.full():
                    self.events.get_nowait()
                self.events.put_nowait(item)
            except (ValueError, queue.Empty, queue.Full):
                pass

    def read_errors(self):
        for line in self.process.stderr:
            self.errors.append(clean(line)[:200])

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=3)
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            if stream and not stream.closed:
                stream.close()


def enable_ansi():
    if os.name != "nt":
        return True
    import ctypes
    from ctypes import wintypes
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    api.GetStdHandle.argtypes = [wintypes.DWORD]
    api.GetStdHandle.restype = wintypes.HANDLE
    api.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    api.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    handle = api.GetStdHandle(-11)
    mode = wintypes.DWORD()
    return bool(api.GetConsoleMode(handle, ctypes.byref(mode)) and api.SetConsoleMode(handle, mode.value | 4))


@contextmanager
def screen(enabled):
    try:
        if enabled:
            print(ESC + "?1049h" + ESC + "?25l", end="", flush=True)
        yield
    finally:
        if enabled:
            print(ESC + "0m" + ESC + "?25h" + ESC + "?1049l", end="", flush=True)


def demo_snapshot(tick):
    now = time.time()
    def item(v, age, sample):
        at = datetime.fromtimestamp(now - age, timezone.utc).isoformat()
        return {"value": v, "receivedAt": at, "measuredAt": at, "quality": "valid", "sample": sample}
    return {"schema": 1, "at": datetime.now(timezone.utc).isoformat(),
            "feed": {"connected": True, "heartbeatAt": datetime.now(timezone.utc).isoformat()},
            "nodes": [
                {"radio": "!00000001", "label": "R001", "lastContactAt": item(0, 3, "")['receivedAt'],
                 "registered": True, "readings": {"voltage": item(3.8 + math.sin(tick) / 100, 3, int(tick)),
                    "charge": item(65, 3, int(tick)), "inaVoltage": item(3.78, 12, int(tick)),
                    "inaCurrent": item(12.2, 12, int(tick)), "temperature": item(20.5, 600, 1),
                    "humidity": item(35, 1200, 1), "busy": item(18.4, 3, int(tick))}},
                {"radio": "!00000002", "label": "R002", "lastContactAt": None, "registered": False, "readings": {}}]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="root@meshlink.int.spp.lol", help="Existing SSH host/alias")
    parser.add_argument("--roster", type=Path, default=ROOT / "records/deployment-nodes.md")
    parser.add_argument("--interval", type=float, default=3, help="Server polling seconds (default: 3)")
    parser.add_argument("--hours", type=float, default=24, help="Archive startup window; older stored readings remain visible")
    parser.add_argument("--fresh", type=float, default=300, help="Green age limit in seconds")
    parser.add_argument("--stale", type=float, default=900, help="Red age threshold in seconds")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto")
    parser.add_argument("--no-color", action="store_const", const="never", dest="color")
    parser.add_argument("--plain", action="store_true", help="Print snapshots without cursor control")
    parser.add_argument("--once", action="store_true", help="Read one snapshot and exit")
    parser.add_argument("--json", action="store_true", help="Sanitized newline-delimited JSON, no terminal control")
    parser.add_argument("--demo", action="store_true", help="Synthetic color/highlight preview; no SSH")
    parser.add_argument("--view", choices=("all", "power", "radio"), default="all", help="Table columns (default: all)")
    parser.add_argument("--remote-python", default="/opt/meshlink-mqtt-venv/bin/python")
    parser.add_argument("--database", default="/var/lib/meshlink/pb_data/data.db")
    parser.add_argument("--config", default="/etc/meshlink/mqtt.json")
    parser.add_argument("--backend", default="/opt/meshlink/backend")
    args = parser.parse_args(argv)
    if not all(math.isfinite(v) for v in (args.interval, args.hours, args.fresh, args.stale)) or not (
            1 <= args.interval <= 300 and 0 < args.hours <= 168 and 0 < args.fresh < args.stale):
        parser.error("Use interval 1-300s, hours >0 and <=168, and 0 < fresh < stale")
    # These become remote-shell words, so allow only plain paths/SSH aliases.
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.@:-]*", args.host):
        parser.error("--host must be a plain SSH host/alias (configure ports/keys in SSH config)")
    if not re.fullmatch(r"/[A-Za-z0-9_./-]+", args.remote_python):
        parser.error("--remote-python must be an absolute path without spaces/metacharacters")
    try:
        roster = {} if args.demo else load_roster(args.roster)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if not args.demo and not shutil.which("ssh"):
        parser.error("OpenSSH ssh must be on PATH")
    tty = sys.stdout.isatty()
    # Windows console capabilities are authoritative: shells can inherit
    # TERM=dumb even when the console supports virtual-terminal sequences.
    ansi = tty and enable_ansi() and (os.name == "nt" or os.environ.get("TERM") != "dumb")
    interactive = ansi and not (args.once or args.plain or args.json)
    color = not args.json and (args.color == "always" or args.color == "auto" and ansi and "NO_COLOR" not in os.environ)
    dashboard = Dashboard(color, args.fresh, args.stale)
    stream, snapshot = None, None
    next_connect, backoff, last_data = 0, 2, None
    error = "Connecting..."
    start = time.monotonic()
    try:
        with screen(interactive):
            while True:
                tick = time.monotonic()
                new = None
                if args.demo:
                    if last_data is None or tick - last_data >= args.interval:
                        new = demo_snapshot(tick - start)
                        last_data = tick
                        error = "DEMO - synthetic readings"
                else:
                    if stream is None and tick >= next_connect:
                        try:
                            stream = SSHStream(args, roster)
                            error = "Connecting over SSH..."
                        except OSError as exc:
                            error = "SSH could not start: " + type(exc).__name__
                            next_connect = tick + backoff
                            backoff = min(30, backoff * 2)
                    if stream:
                        try:
                            new = stream.events.get(timeout=0.05)
                        except queue.Empty:
                            pass
                        if new and "error" in new:
                            error, new = clean(new["error"]), None
                            stream.errors.append(error)
                        elif new:
                            last_data, backoff, error = tick, 2, "Connected over SSH"
                        if stream.process.poll() is not None and stream.events.empty() and not new:
                            error = "SSH disconnected" + (": " + " / ".join(stream.errors) if stream.errors else "")
                            stream.close()
                            stream = None
                            if args.once:
                                print(error, file=sys.stderr)
                                return 1
                            next_connect = tick + backoff
                            backoff = min(30, backoff * 2)
                    if args.once and tick - start > 45:
                        print("Timed out waiting for a snapshot: " + error, file=sys.stderr)
                        return 1
                if new:
                    snapshot = new
                    dashboard.observe(snapshot, tick)
                if args.json:
                    if new:
                        print(json.dumps(new, allow_nan=False), flush=True)
                elif snapshot and (interactive or new):
                    size = shutil.get_terminal_size((140, 50))
                    width = size.columns if interactive else 140
                    display_status = error
                    if last_data is not None and tick - last_data > max(15, args.interval * 3):
                        display_status = "No new snapshots; retained values are aging. " + error
                    rendered = dashboard.render(snapshot, time.time(), tick, display_status, width,
                                                size.lines if interactive else None, args.view)
                    if interactive:
                        # Redraw in-place; clear each line to avoid leftover long values.
                        print(ESC + "H" + rendered.replace("\n", ESC + "K\n") + ESC + "K" + ESC + "J", end="", flush=True)
                    else:
                        print(rendered + "\n", flush=True)
                elif interactive:
                    print(ESC + "H" + clean(error) + ESC + "K" + ESC + "J", end="", flush=True)
                if args.once and new:
                    return 0
                time.sleep(0.2 if interactive else 0.1)
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print("Dashboard failed: " + type(exc).__name__, file=sys.stderr)
        return 1
    finally:
        if stream:
            stream.close()


if __name__ == "__main__":
    sys.exit(main())

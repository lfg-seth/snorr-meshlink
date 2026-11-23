"""Single laptop adapter owner and durable, source-isolated event store."""

import importlib.util
import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path

from simulator import Simulator


def compact(obj):
    return json.dumps(obj, allow_nan=False, separators=(",", ":"))


def command(name, params=None):
    return {
        "v": 1,
        "kind": "command",
        "id": uuid.uuid4().hex,
        "name": name,
        "params": params or {},
    }


def load_adapter(source, path, device=None, expected_id=None, root=None):
    if source == "simulation":
        if path or device or expected_id:
            raise ValueError("An external adapter requires --source live")
        return Simulator()
    if not path:
        raise ValueError("Live mode requires a v1 --adapter Python module")
    spec = importlib.util.spec_from_file_location("survey_live_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "SurveyAdapter"):
        from firmware_bridge import FirmwareBridge

        return FirmwareBridge.open(module.SurveyAdapter, device, expected_id, root)
    adapter = module.open_adapter()
    if adapter.source != "live":
        raise ValueError("Live adapter must declare live provenance")
    return adapter


class Recorder:
    def __init__(self, adapter, root, *, configured_sites=None):
        self.adapter = adapter
        self.root = Path(root) / adapter.source
        self.root.mkdir(parents=True, exist_ok=True)
        self.dbpath = self.root / "survey.sqlite3"
        self.lock = threading.RLock()
        self.db = sqlite3.connect(
            self.dbpath, check_same_thread=False, isolation_level=None
        )
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS events (
              cursor INTEGER PRIMARY KEY, received_ms INTEGER NOT NULL, boot TEXT NOT NULL,
              seq INTEGER NOT NULL, name TEXT NOT NULL, session TEXT, payload TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS by_boot ON events(boot,seq);
            CREATE INDEX IF NOT EXISTS by_session ON events(session,cursor);
            CREATE INDEX IF NOT EXISTS by_kind ON events(name,cursor);
            CREATE TABLE IF NOT EXISTS commands (id TEXT PRIMARY KEY, request TEXT, ack TEXT);
            CREATE TABLE IF NOT EXISTS sites (id TEXT PRIMARY KEY, lat REAL, lon REAL);
            CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, first INTEGER, last INTEGER, events INTEGER);
            INSERT OR IGNORE INTO sessions SELECT session,min(cursor),max(cursor),count(*) FROM events
              WHERE session IS NOT NULL GROUP BY session;
            CREATE TRIGGER IF NOT EXISTS index_session AFTER INSERT ON events WHEN new.session IS NOT NULL BEGIN
              INSERT INTO sessions VALUES(new.session,new.cursor,new.cursor,1)
                ON CONFLICT(id) DO UPDATE SET last=new.cursor,events=events+1;
            END;
        """)
        self.host_id = uuid.uuid4().hex
        self.cursor = self.db.execute(
            "SELECT coalesce(max(cursor),0) FROM events"
        ).fetchone()[0]
        self.first_cursor = self.cursor + 1
        self.host_seq = 0
        self.boot = None
        self.check_live_state = adapter.source == "live"
        self.sequences = {}
        self.state = {}
        self.hello = {}
        self.configured_sites = configured_sites or {}
        self.site_records = {
            i: {"lat_deg": a, "lon_deg": b}
            for i, a, b in self.db.execute("SELECT * FROM sites")
        }
        self.last_replies = {}
        for received_ms, payload in self.db.execute(
            "SELECT received_ms,payload FROM events WHERE name='result' ORDER BY cursor"
        ):
            self.remember_reply(json.loads(payload)["data"], received_ms)
        self.error = self.adapter_error = None
        self.needs_snapshot = False
        self.recording = True
        self.dropped = self.gaps = 0
        self.stop_event = threading.Event()
        self.controller = None
        self.revision = 0
        self.last_beat = -100000
        self.thread = None
        self.note("host_open", {"prior_history": self.cursor > 0})
        for name in ("hello", "get_state"):
            self.adapter.send(command(name))

    def note(self, name, data):
        self.host_seq += 1
        self.store(
            {
                "v": 1,
                "kind": "event",
                "boot_id": self.host_id,
                "seq": self.host_seq,
                "name": name,
                "data_source": self.adapter.source,
                "data": {"session_id": self.state.get("session_id")} | data,
            }
        )

    def store(self, event):
        d = event["data"]
        session = d.get("session_id", self.state.get("session_id"))
        if (
            self.state.get("run_state") == "stopped"
            and session == self.state.get("session_id")
            and event["name"] not in ("result", "fault", "host_command", "site_record")
        ):
            session = None
        received_ms = int(time.time() * 1000)
        row = self.db.execute(
            "INSERT INTO events(received_ms,boot,seq,name,session,payload) VALUES(?,?,?,?,?,?)",
            (
                received_ms,
                event["boot_id"],
                event["seq"],
                event["name"],
                session,
                compact(event),
            ),
        )
        self.cursor = row.lastrowid
        if event["name"] == "result":
            self.remember_reply(d, received_ms)

    def remember_reply(self, data, received_ms):
        target = data.get("target_id")
        if (
            isinstance(target, str)
            and target
            and data.get("status") == "success"
            and not data.get("duplicate")
        ):
            self.last_replies[target] = received_ms

    def accept(self, e):
        if (
            not isinstance(e, dict)
            or e.get("v") != 1
            or e.get("kind") != "event"
            or e.get("data_source") != self.adapter.source
            or not isinstance(e.get("data"), dict)
            or type(e.get("seq")) != int
            or not isinstance(e.get("boot_id"), str)
            or not isinstance(e.get("name"), str)
        ):
            self.note("adapter_error", {"reason": "Invalid v1 event or source"})
            raise ValueError("Invalid v1 event or source")
        boot, seq, d, name = e["boot_id"], e["seq"], e["data"], e["name"]
        previous = self.sequences.get(boot)
        if (previous is None or seq <= previous) and self.db.execute(
            "SELECT 1 FROM events WHERE boot=? AND seq=? LIMIT 1", (boot, seq)
        ).fetchone():
            self.note("duplicate_delivery", {"event": e})
            return
        if previous is None:
            previous = self.db.execute(
                "SELECT max(seq) FROM events WHERE boot=?", (boot,)
            ).fetchone()[0]
        on_device = e.get("event_stream") != "adapter-host"
        reboot = on_device and self.boot is not None and boot != self.boot
        if reboot:
            self.check_live_state = self.adapter.source == "live"
            self.adapter.send(command("hello"))
            self.adapter.send(command("get_state"))
        if reboot or previous is not None and seq > previous + 1:
            self.gaps += 1
            self.note(
                "gap",
                {
                    "previous_boot": self.boot,
                    "previous_seq": previous,
                    "next_seq": seq,
                    "next_boot": boot,
                },
            )
        if name in ("attempt", "result", "state"):
            e = e | {"host_context": {"fixed_sites": self.fixed_sites()}}
        self.store(e)
        self.sequences[boot] = max(seq, previous or 0)
        if len(self.sequences) > 16:
            del self.sequences[next(iter(self.sequences))]
        if on_device:
            self.boot = boot
        if name == "hello":
            self.hello = d
        elif name == "state":
            if self.check_live_state and "run_state" in d:
                self.check_live_state = False
                if d.get("run_state") == "running":
                    self.adapter.send(command("pause"))
            old_drops = self.state.get("queue_dropped", 0)
            new_drops = d.get("queue_dropped", 0)
            if (
                isinstance(new_drops, int)
                and isinstance(old_drops, int)
                and new_drops > old_drops
            ):
                self.gaps += 1
                self.note(
                    "gap",
                    {
                        "reason": "Adapter queue overflow",
                        "dropped": new_drops - old_drops,
                    },
                )
            signature = (
                "run_state",
                "mode",
                "session_id",
                "segment_id",
                "target_id",
                "transport",
                "fault",
            )
            if any(d.get(k) != self.state.get(k) for k in signature):
                self.revision += 1
            self.state = d
        elif name == "gps" and d.get("sample_at") in (None, "local_stream"):
            self.state = self.state | {"gps": d}
        elif name == "ack":
            self.db.execute(
                "UPDATE commands SET ack=? WHERE id=? AND ack IS NULL",
                (compact(d), d.get("command_id")),
            )

    def poll(self):
        now = int(time.monotonic() * 1000)
        # A recording failure latches until the operator repairs disk and restarts.
        if not self.recording:
            return
        try:
            cadence = self.state.get("settings", {}).get("heartbeat_interval_ms", 1000)
            if now - self.last_beat >= cadence:
                self.adapter.send(command("heartbeat"))
                self.last_beat = now
            events = list(self.adapter.poll(now))
            if self.needs_snapshot:
                self.adapter.send(command("pause"))
                self.adapter.send(command("hello"))
                self.adapter.send(command("get_state"))
                self.needs_snapshot = False
        except Exception as exc:  # noqa: BLE001 -- external adapter failure must reach the dashboard
            self.transport_failure(exc)
            return
        try:
            if self.adapter_error:
                self.note("adapter_reconnected", {"requires_explicit_resume": True})
            self.adapter_error = None
            self.db.execute("BEGIN")
            for event in events:
                try:
                    self.accept(event)
                except (ValueError, TypeError) as exc:
                    self.dropped += 1
                    self.note("gap", {"reason": str(exc), "dropped": 1})
            self.db.commit()
        except (sqlite3.Error, OSError) as exc:
            self.db.rollback()
            self.record_failure(exc, len(events))

    def record_failure(self, exc, lost=1):
        self.recording = False
        self.error = "Recording interrupted: " + str(exc)
        self.dropped += max(1, lost)
        try:
            self.adapter.send(command("stop"))
        except Exception as stop_error:  # noqa: BLE001 -- retain both plugin and disk errors
            self.error += (
                f"; stop unconfirmed ({stop_error}); host heartbeats suspended"
            )

    def transport_failure(self, exc):
        reason = str(exc)[:300]
        if reason != self.adapter_error:
            self.adapter_error = reason
            self.needs_snapshot = True
            try:
                self.note("transport_lost", {"reason": reason})
            except sqlite3.Error as disk:
                self.record_failure(disk)

    def start_worker(self):
        def loop():
            while not self.stop_event.is_set():
                with self.lock:
                    self.poll()
                self.stop_event.wait(0.1)

        self.thread = threading.Thread(target=loop, name="survey-recorder", daemon=True)
        self.thread.start()

    def dispatch(self, cmd, controller, revision):
        if (
            not isinstance(cmd, dict)
            or cmd.get("v") != 1
            or cmd.get("kind") != "command"
            or not isinstance(cmd.get("params"), dict)
        ):
            raise ValueError("Expected v1 command with params")
        cid, name = cmd.get("id"), cmd.get("name")
        if (
            not isinstance(cid, str)
            or not 1 <= len(cid) <= 100
            or not isinstance(name, str)
        ):
            raise ValueError("Invalid command ID or name")
        raw = json.dumps(cmd, sort_keys=True, allow_nan=False)
        with self.lock:
            self.check_controller(controller)
            if not self.recording and name == "stop":
                self.adapter.send(cmd)
                return {
                    "command_id": cid,
                    "ok": False,
                    "error": "Stop sent. Recording failure prevents a durable acknowledgement.",
                }
            saved = self.db.execute(
                "SELECT request,ack FROM commands WHERE id=?", (cid,)
            ).fetchone()
            if saved:
                if saved[0] != raw:
                    raise ValueError("Command ID already used with different content")
                return (
                    json.loads(saved[1])
                    if saved[1]
                    else {
                        "command_id": cid,
                        "ok": False,
                        "error": "Outcome pending or unknown. Inspect state.",
                    }
                )
            if name != "stop" and revision != self.revision:
                raise ValueError(
                    "Survey state changed. Review current state and try again."
                )
            if name != "stop" and (not self.recording or self.adapter_error):
                raise ValueError(self.error or self.adapter_error)
            if name not in self.hello.get("commands", []) or name == "heartbeat":
                raise ValueError("Unsupported operator command")
            try:
                self.db.execute("BEGIN")
                self.db.execute("INSERT INTO commands VALUES(?,?,NULL)", (cid, raw))
                self.note("host_command", {"command": cmd, "sites": self.site_records})
                self.db.commit()
            except sqlite3.Error as exc:
                self.db.rollback()
                self.record_failure(exc)
                raise
            try:
                self.adapter.send(cmd)
            except Exception as exc:
                self.transport_failure(exc)
                raise ValueError(
                    "Command outcome unknown. Inspect adapter state."
                ) from exc
            self.poll()
            saved = self.db.execute(
                "SELECT ack FROM commands WHERE id=?", (cid,)
            ).fetchone()[0]
            return (
                json.loads(saved)
                if saved
                else {
                    "command_id": cid,
                    "ok": None,
                    "error": "Awaiting adapter acknowledgement",
                }
            )

    def check_controller(self, token):
        if not isinstance(token, str) or not 12 <= len(token) <= 100:
            raise ValueError("Missing control token")
        if self.controller is None:
            self.controller = token
        if self.controller != token:
            raise ValueError("Another browser has controls. Take controls explicitly.")

    def fixed_sites(self):
        return self.configured_sites | self.site_records

    def snapshot(self, token):
        with self.lock:
            reply_ms = self.last_replies.get(self.state.get("target_id"))
            return {
                "host_id": self.host_id,
                "cursor": self.cursor,
                "first_cursor": self.first_cursor,
                "source": self.adapter.source,
                "state": self.state,
                "hello": self.hello,
                "sites": self.hello.get("targets", {}) | self.fixed_sites(),
                "last_reply_age_ms": (
                    max(0, int(time.time() * 1000) - reply_ms)
                    if reply_ms is not None
                    else None
                ),
                "revision": self.revision,
                "has_control": self.controller in (None, token),
                "recording": self.recording,
                "record_error": self.error,
                "adapter_error": self.adapter_error,
                "dropped": self.dropped,
                "gaps": self.gaps,
            }

    def history(self, after=None, before=None, session=None, names=None, limit=220):
        clauses, args = [], []
        for key, value in (
            ("cursor>?", after),
            ("cursor<?", before),
            ("session=?", session),
        ):
            if value is not None:
                clauses.append(key)
                args.append(value)
        if names:
            clauses.append("name IN (" + ",".join("?" for _ in names) + ")")
            args.extend(names)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        # Reader connection keeps slow clients/export out of the adapter lock.
        conn = sqlite3.connect(self.dbpath)
        try:
            rows = conn.execute(
                "SELECT cursor,received_ms,payload FROM events"
                + where
                + (
                    " ORDER BY cursor ASC"
                    if after is not None
                    else " ORDER BY cursor DESC"
                )
                + " LIMIT ?",
                [*args, limit],
            )
            result = [
                {"cursor": n, "received_ms": t, "event": json.loads(payload)}
                for n, t, payload in rows
            ]
            return result if after is not None else result[::-1]
        finally:
            conn.close()

    def close(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        with self.lock:
            try:
                self.adapter.send(command("stop"))
                self.poll()
            finally:
                if hasattr(self.adapter, "close"):
                    self.adapter.close()
                self.db.close()

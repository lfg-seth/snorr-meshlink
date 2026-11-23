"""Direct-hop v1 physical USB adapter. One thread owns each exclusive serial handle."""

from __future__ import annotations

import collections
import os
import json
import queue
import struct
import sqlite3
import threading
import time
from pathlib import Path

MAGIC = b"\x00SV1"
SYNC = b"\x94\xc3"
REQUEST = struct.Struct("<4sIIBB10I64s")
OPS = (
    "hello",
    "get_state",
    "configure",
    "start",
    "pause",
    "resume",
    "stop",
    "set_target",
    "heartbeat",
    "_enroll",
    "_clock",
    "_profile",
)
LIMITS = {
    "min_attempt_interval_ms": (1000, 60000, 3000),
    "response_timeout_ms": (1000, 30000, 4500),
    "max_attempt_interval_ms": (1000, 120000, 15000),
    "gps_max_age_ms": (500, 10000, 2000),
    "heartbeat_timeout_ms": (2000, 30000, 6000),
    "gps_update_interval_ms": (500, 5000, 1000),
    "utilization_target_pct": (5, 94, 65),
    "utilization_backdown_pct": (6, 95, 80),
    "adaptive": (0, 1, 1),
}
ERRORS = (
    "",
    "wrong_boot",
    "stale_command",
    "invalid_state_or_parameters",
    "enrollment",
    "interlock",
    "unsupported_command",
)


def node_id(number):
    return f"!{number:08x}"


def number(value):
    if not isinstance(value, str) or len(value) != 9 or value[0] != "!":
        raise ValueError("expected !xxxxxxxx node ID")
    if any(digit not in "0123456789abcdefABCDEF" for digit in value[1:]):
        raise ValueError("expected eight hexadecimal digits")
    n = int(value[1:], 16)
    if not 1 < n < 0xFFFFFFFF:
        raise ValueError("reserved node ID")
    return n


def payload(boot, sequence, name, args=(), keys=b""):
    if len(args) > 10 or len(keys) > 64:
        raise ValueError("oversize request")
    body = REQUEST.pack(
        MAGIC,
        boot,
        sequence,
        OPS.index(name),
        len(args),
        *args,
        *([0] * (10 - len(args))),
        keys.ljust(64, b"\0"),
    )
    return SYNC + struct.pack(">H", len(body)) + body


class Decoder:
    def __init__(self):
        self.buf = bytearray()

    def feed(self, block):
        self.buf.extend(block)
        while self.buf:
            start = self.buf.find(SYNC)
            if start < 0:
                self.buf[:] = self.buf[-1:] if self.buf[-1:] == SYNC[:1] else b""
                break
            del self.buf[:start]
            if len(self.buf) < 4:
                break
            length = int.from_bytes(self.buf[2:4], "big")
            if length > 512:
                del self.buf[0]
                continue
            if len(self.buf) < length + 4:
                break
            body = bytes(self.buf[4 : 4 + length])
            del self.buf[: 4 + length]
            if body.startswith(MAGIC):
                yield body[4:].decode("ascii").split(",")


def gps_data(values):
    session, attempt, valid, lat, lon, alt, has_alt, epoch, frac, age, quality, has_sats, sats = map(
        int, values[:13]
    )
    return dict(
        source="laptop" if values[13:] == ["1"] else "heltec",
        session_id=session,
        attempt_id=attempt,
        valid=bool(valid),
        lat_deg=lat / 1e7 if valid else None,
        lon_deg=lon / 1e7 if valid else None,
        altitude_m=alt if valid and has_alt else None,
        fix_utc_ms=epoch * 1000 + frac if valid else None,
        fix_age_ms=None if age == 0xFFFFFFFF else age,
        quality=quality if valid else None,
        satellites=sats if valid and has_sats else None,
    )


def laptop_heartbeat_args(params):
    fix = params.get("laptop_fix")
    if not isinstance(fix, dict) or not fix.get("valid"):
        return []
    try:
        age = fix["fix_age_ms"]
        sampled = params["sampled_ms"]
        stamp = fix["fix_utc_ms"]
        if any(type(value) is not int for value in (age, sampled, stamp)):
            return []
        delay = int(time.monotonic() * 1000) - sampled
        if age < 0 or delay < 0 or age + delay > 3000:
            return []
        epoch, millis = divmod(stamp, 1000)
        lat, lon = round(fix["lat_deg"] * 1e7), round(fix["lon_deg"] * 1e7)
        altitude, sats = fix.get("altitude_m"), fix.get("satellites")
        height = round(altitude) if altitude is not None else 0
        quality = fix["quality"]
        if (
            not 1700000000 <= epoch <= 0xFFFFFFFF
            or not -900000000 <= lat <= 900000000
            or not -1800000000 <= lon <= 1800000000
            or not -2**31 <= height < 2**31
            or quality not in (1, 2, 4, 5)
            or (sats is not None and (type(sats) is not int or not 0 <= sats <= 255))
        ):
            return []
        flags = int(altitude is not None) | (int(sats is not None) << 1)
        return [
            age + delay, epoch, millis, lat & 0xFFFFFFFF, lon & 0xFFFFFFFF,
            height & 0xFFFFFFFF, flags, quality, sats or 0,
        ]
    except (KeyError, ValueError, TypeError, OverflowError):
        return []


class SurveyAdapter:
    """Use as a context manager. command() awaits an ACK; read_event() streams live evidence."""

    def __init__(self, port, expected_id, log_path, *, serial_factory=None):
        self.port, self.expected_id = port, node_id(number(expected_id))
        self.path = Path(log_path)
        self.factory = serial_factory
        self.inbox = queue.Queue(64)
        self.events = queue.Queue(1024)
        self.closed = threading.Event()
        self.connected = threading.Event()
        self.problem = None
        self.decoder = Decoder()
        self.sequence = self.boot = self.last_event = 0
        self.host_sequence = self.host_drops = 0
        self.host_boot = f"host-{time.time_ns()}"
        self.hello = {}
        self.state = {}
        self.settings = {k: v[2] for k, v in LIMITS.items()}
        self.targets = []
        self.fixes = collections.OrderedDict()
        self.attempts = collections.OrderedDict()
        self.recent = collections.OrderedDict()
        self.heartbeat_ms = 1000
        self.auto_heartbeat = True
        self.ledger = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Each writer owns a new append-only evidence file. Existing histories are read separately.
        self.log = self.path.open("x", encoding="utf-8", buffering=1)
        try:
            if self.factory is None:
                import serial

                self.factory = serial.Serial
            options = {"exclusive": True} if os.name == "posix" else {}
            self.serial = self.factory(
                port=self.port, baudrate=115200, timeout=0.08, write_timeout=1, **options
            )
            self.thread = threading.Thread(target=self._run, name="survey-usb", daemon=True)
            self.thread.start()
            if not self.connected.wait(16) or self.problem:
                raise ConnectionError(self.problem or "survey hello timed out")
        except BaseException:
            self.close()
            raise
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self.closed.set()
        if hasattr(self, "thread") and self.thread is not threading.current_thread():
            self.thread.join(3)
        if hasattr(self, "serial"):
            self.serial.close()
        if hasattr(self, "log"):
            self.log.close()

    def read_event(self, timeout=1):
        return self.events.get(timeout=timeout)

    def _publish(self, event):
        event["host_receipt_utc_ms"] = time.time_ns() // 1000000
        event["host_monotonic_ns"] = time.monotonic_ns()
        if self.events.full():
            try:
                self.events.get_nowait()
            except queue.Empty:
                pass
            self.host_drops += 1
        event["display_dropped_total"] = self.host_drops
        self.log.write(json.dumps(event, allow_nan=False, separators=(",", ":")) + "\n")
        self.events.put_nowait(event)
        return event

    def _host(self, name, data):
        self.host_sequence += 1
        return self._publish(
            dict(
                v=1,
                kind="event",
                seq=self.host_sequence,
                boot_id=self.host_boot,
                name=name,
                data_source="live",
                data=data,
            )
        )

    def command(self, envelope, timeout=8):
        """Return normalized ACK. A timed-out submission is never automatically replayed."""
        reply = queue.Queue(1)
        if self.closed.is_set() or self.problem:
            raise ConnectionError(self.problem or "closed")
        if not isinstance(envelope, dict):
            envelope = {}
        self.inbox.put((envelope, reply), timeout=timeout)
        try:
            return reply.get(timeout=timeout)
        except queue.Empty as e:
            raise TimeoutError("USB command outcome unknown; get_state") from e

    def enroll(self, peer_id, public_key, cohort_key, timeout=8):
        """Physical commissioning API. Called explicitly outside the normalized GUI command surface."""
        if len(public_key) != 32 or len(cohort_key) != 32:
            raise ValueError("invalid enrollment key sizes")
        reply = queue.Queue(1)
        self.inbox.put(((number(peer_id), bytes(public_key) + bytes(cohort_key)), reply), timeout=timeout)
        return reply.get(timeout=timeout)

    def _write(self, name, args=(), keys=b""):
        self.sequence += 1
        frame = payload(self.boot, self.sequence, name, args, keys)
        if self.serial.write(frame) != len(frame):
            raise IOError("short USB write")
        return self.sequence

    def _next(self):
        block = self.serial.read(min(4096, max(1, self.serial.in_waiting)))
        for row in self.decoder.feed(block):
            if self.hello or row[3] == "hello":
                yield self._parse(row)

    def _parse(self, row):
        boot, seq, clock = map(int, row[:3])
        name = row[3]
        a = row[4:]
        if self.boot and self.boot != boot:
            raise ConnectionError("board_rebooted")
        if self.last_event and seq != self.last_event + 1:
            self._host("fault", dict(reason="event_gap", previous=self.last_event, next=seq))
        self.last_event = seq
        base = dict(v=1, kind="event", boot_id=f"{boot:08x}", seq=seq, data_source="live", firmware_ms=clock)
        if name == "hello":
            n, build, client, hw, region, preset, channel, power, use_preset, tx, serial, enrolled = a[:12]
            if node_id(int(n)) != self.expected_id:
                raise ConnectionError("unexpected physical node ID")
            self.boot = boot
            self.sequence = max(int(serial), self.sequence)
            profile = dict(
                region=int(region),
                modem_preset=int(preset),
                channel_num=int(channel),
                tx_power_dbm=int(power),
                use_preset=bool(int(use_preset)),
                tx_enabled=bool(int(tx)),
            )
            self.hello = dict(
                protocol=1,
                build=build,
                node_id=self.expected_id,
                hardware_model=int(hw),
                role="client" if int(client) else "responder",
                commands=list(OPS[:9]),
                settings=LIMITS,
                radio_profile=profile,
                enrolled=bool(int(enrolled)),
                capabilities={
                    "heartbeat_interval_ms": [250, 5000, 1000],
                    "max_targets": 8,
                    "radio_profile_control": ["production", "experimental_medium_fast"],
                    "quiet_duration_s": 900,
                    "gps_source": "local_gnss",
                    "laptop_gps": a[12:] == ["1"],
                },
            )
            data = dict(self.hello)
        elif name == "state":
            vals = list(map(int, a))
            keys = (
                "run",
                "bench",
                "session_id",
                "segment_id",
                "target",
                "interval_ms",
                "quiet_remaining_ms",
                "firmware_dropped",
                "queue_free",
                "queue_capacity",
                "success",
                "timeout",
                "deferred",
                "rejected",
                "suppressed",
                "gps_fresh",
                "heartbeat_healthy",
                "command_sequence",
            )
            self.state = dict(zip(keys, vals[:18], strict=True))
            if len(vals) == 19:
                self.state["laptop_fix_fresh"] = bool(vals[18])
            self.state.update(
                run_state=("idle", "running", "paused")[vals[0]],
                mode="bench" if vals[1] else "survey",
                target_id=node_id(vals[4]) if vals[4] else None,
                settings={**self.settings, "heartbeat_interval_ms": self.heartbeat_ms},
                target_ids=list(self.targets),
            )
            data = dict(self.state)
        elif name == "profile":
            actual = {
                **self.hello["radio_profile"],
                "experimental": bool(int(a[0])),
                "modem_preset": int(a[1]),
                "hardware_verified": bool(int(a[2])) if len(a) > 2 else None,
            }
            self.hello["radio_profile"] = actual
            self.state["radio_profile"] = actual
            name = "state"
            data = dict(self.state)
        elif name == "settings":
            self.settings = dict(zip(LIMITS, map(int, a), strict=True))
            self.state["settings"] = {**self.settings, "heartbeat_interval_ms": self.heartbeat_ms}
            name = "state"
            data = dict(self.state)
        elif name == "targets":
            self.targets = [node_id(int(v)) for v in a[1 : 1 + int(a[0])]]
            self.state["target_ids"] = list(self.targets)
            name = "state"
            data = dict(self.state)
        elif name in ("gps", "sendfix", "txfix"):
            data = gps_data(a)
            if name != "gps":
                key = (data["session_id"], data["attempt_id"])
                self.fixes.setdefault(key, {})[name] = dict(data)
                while len(self.fixes) > 64:
                    self.fixes.popitem(last=False)
                data["sample_at"] = "tx_start" if name == "txfix" else "enqueue"
            else:
                data["sample_at"] = "local_stream"
            name = "gps"
        elif name in ("attempt", "result"):
            sid, seg, attempt, tgt, bench = map(int, a[:5])
            data = dict(
                session_id=sid,
                segment_id=seg,
                attempt_id=attempt,
                sequence=attempt,
                target_id=node_id(tgt),
                mode="bench" if bench else "survey",
                build=self.hello["build"],
                radio_profile=self.hello["radio_profile"],
            )
            self.attempts[(sid, attempt)] = dict(data)
            while len(self.attempts) > 128:
                self.attempts.popitem(last=False)
            if name == "attempt":
                data.update(
                    status="pending",
                    enqueue_ms=int(a[5]),
                    interval_ms=int(a[6]),
                    channel_util_pct=int(a[7]),
                    gps=self.fixes.get((sid, attempt), {}).get("sendfix"),
                )
            else:
                status = a[5]
                req, pong, queued, tx, done, rx, ur, us, dr, ds, n, pred, util, rutil = map(int, a[6:])
                ok = status == "success"
                fixes = self.fixes.get((sid, attempt), {})
                data.update(
                    status=status,
                    request_packet_id=req or None,
                    reply_packet_id=pong or None,
                    enqueue_ms=queued,
                    tx_start_ms=tx or None,
                    tx_done_ms=done or None,
                    rx_ms=rx if ok else None,
                    rtt_ms=(rx - tx) & 0xFFFFFFFF if ok and tx else None,
                    wire_bytes=n or None,
                    predicted_airtime_ms=pred or None,
                    measured_tx_ms=(done - tx) & 0xFFFFFFFF if done and tx else None,
                    uplink={"rssi_dbm": ur if ok else None, "snr_db": us / 4 if ok else None},
                    downlink={"rssi_dbm": dr if ok else None, "snr_db": ds / 4 if ok else None},
                    channel_util_pct=util,
                    remote_util_pct=rutil if ok else None,
                    gps=fixes.get("txfix"),
                    enqueue_gps=fixes.get("sendfix"),
                    direct_evidence="validated_physical_zero_hop" if ok else None,
                )
        elif name == "late":
            sid, att, tgt, pid, dup, previous = map(int, a)
            name = "result"
            known = self.attempts.get((sid, att), {})
            data = dict(
                known,
                session_id=sid,
                segment_id=known.get("segment_id"),
                sequence=att,
                attempt_id=att,
                target_id=node_id(tgt),
                mode=known.get("mode"),
                build=self.hello["build"],
                radio_profile=known.get("radio_profile"),
                status="late",
                reply_packet_id=pid,
                duplicate=bool(dup),
                prior_completion_ms=previous if dup else None,
            )
        elif name == "quiet":
            src, req, tgt, left, rssi, snr = map(int, a)
            data = dict(
                source_id=node_id(src),
                request_packet_id=req,
                target_id=node_id(tgt),
                remaining_ms=left,
                observer_id=self.expected_id,
                rssi_dbm=rssi,
                snr_db=snr / 4,
            )
        elif name == "ack":
            serial, op, err = map(int, a)
            data = dict(
                wire_command_id=serial,
                op=op,
                ok=err == 0,
                error=ERRORS[err] if err < len(ERRORS) and err else None,
            )
            # Normalized command correlation is applied by the host, which owns string IDs.
            name = "statistics"
            data["type"] = "wire_ack"
        elif name == "fault":
            data = {"reason": a[0]}
        else:
            fields = {
                "rx": (
                    "from",
                    "to",
                    "packet_id",
                    "hop_start",
                    "hop_limit",
                    "want_ack",
                    "port",
                    "rssi_dbm",
                    "snr_quarter_db",
                ),
                "airtx": (
                    "from",
                    "to",
                    "packet_id",
                    "hop_start",
                    "hop_limit",
                    "want_ack",
                    "local_class",
                    "wire_bytes",
                    "predicted_airtime_ms",
                ),
                "pong": ("request_packet_id", "reply_packet_id", "enqueued", "attempt_id"),
                "tx": ("packet_id", "wire_bytes", "predicted_airtime_ms"),
                "txdone": ("packet_id",),
            }
            data = {"type": name, **dict(zip(fields.get(name, ()), map(int, a), strict=True))}
            name = "statistics"
        return self._publish({**base, "name": name, "data": data})

    def _exchange(self, name, args=(), keys=b""):
        serial = self._write(name, args, keys)
        deadline = time.monotonic() + 3
        while not self.closed.is_set() and time.monotonic() < deadline:
            matched = None
            for event in self._next():
                d = event["data"]
                if d.get("type") == "wire_ack" and d["wire_command_id"] == serial:
                    matched = d
            if matched is not None:
                return matched
        raise TimeoutError(f"{name} ACK unavailable")

    def _dispatch(self, cmd):
        cid = cmd.get("id")
        if not isinstance(cid, str) or not 0 < len(cid) <= 128:
            return self._host("ack", dict(command_id=None, ok=False, applied={}, error="invalid_command_id"))
        canonical = json.dumps(cmd, sort_keys=True, separators=(",", ":"))
        if cid in self.recent:
            original, reply = self.recent[cid]
            if original == canonical:
                return self._host("ack", {**reply["data"], "replayed": True})
            return self._host("ack", dict(command_id=cid, ok=False, applied={}, error="command_id_conflict"))
        name = cmd.get("name")
        params = cmd.get("params")
        applied = {}
        durable = name in ("configure", "set_target", "start", "resume", "pause", "stop")
        if durable:
            existing = self.ledger.execute(
                "SELECT request, reply FROM commands WHERE id=?", (cid,)
            ).fetchone()
            if existing:
                if existing[0] == canonical and existing[1] is not None:
                    return self._host("ack", {**json.loads(existing[1])["data"], "replayed": True})
                reason = "prior_outcome_unknown" if existing[0] == canonical else "command_id_conflict"
                return self._host("ack", dict(command_id=cid, ok=False, applied={}, error=reason))
            self.ledger.execute("INSERT INTO commands(id,request) VALUES (?,?)", (cid, canonical))
            self.ledger.commit()
        try:
            if (
                cmd.get("v") != 1
                or cmd.get("kind") != "command"
                or name not in OPS[:9]
                or not isinstance(params, dict)
            ):
                raise ValueError("unsupported envelope")
            args = []
            if name == "configure":
                if "radio_profile" in params:
                    if set(params) != {"radio_profile"}:
                        raise ValueError("change radio profile in a separate command")
                    choices = ("production", "experimental_medium_fast")
                    if params["radio_profile"] not in choices:
                        raise ValueError("unsupported radio profile")
                    name = "_profile"
                    args = [choices.index(params["radio_profile"])]
                    applied = {"radio_profile": params["radio_profile"]}
                unknown = set(params) - set(LIMITS) - {"heartbeat_interval_ms", "radio_profile"}
                if unknown:
                    raise ValueError("unsupported settings: " + ",".join(sorted(unknown)))
                new = {**self.settings, **{k: v for k, v in params.items() if k in LIMITS}}
                for k, v in new.items():
                    low, high, _ = LIMITS[k]
                    if not isinstance(v, int) or not low <= v <= high:
                        raise ValueError(k)
                beat = params.get("heartbeat_interval_ms", self.heartbeat_ms)
                if (
                    type(beat) is not int
                    or not 250 <= beat <= 5000
                    or 2 * beat > new["heartbeat_timeout_ms"]
                ):
                    raise ValueError("heartbeat_interval_ms")
                if name == "configure":
                    args = list(new.values())
                    applied = {**new, "heartbeat_interval_ms": beat}
            elif name == "set_target":
                if set(params) not in ({"target_id"}, {"target_ids"}):
                    raise ValueError("expected one target selection")
                ids = params["target_ids"] if "target_ids" in params else [params["target_id"]]
                if not isinstance(ids, list) or not 1 <= len(ids) <= 8:
                    raise ValueError("target count")
                args = list(map(number, ids))
                applied = {"target_ids": [node_id(n) for n in args]}
            elif name == "start":
                if set(params) - {"mode", "target_id"}:
                    raise ValueError("unsupported start parameters")
                mode = params.get("mode", "survey")
                if mode not in ("bench", "survey"):
                    raise ValueError("mode")
                if "target_id" in params:
                    target = number(params["target_id"])
                    sub = self._exchange("set_target", [target])
                    if not sub["ok"]:
                        raise ValueError(sub["error"])
                args = [int(mode == "bench")]
                applied = {"mode": mode, "target_ids": list(self.targets)}
            elif name == "heartbeat":
                if self.hello.get("capabilities", {}).get("laptop_gps"):
                    args = laptop_heartbeat_args(params)
            elif name == "hello" and not params:
                args = [1]
            elif params:
                raise ValueError("unexpected parameters")
            result = self._exchange(name, args)
            if result["ok"] and name == "configure":
                self.heartbeat_ms = beat
                self.state["settings"] = {**self.settings, "heartbeat_interval_ms": beat}
            if name == "get_state" and result["ok"]:
                applied = dict(self.state)
            if name == "hello" and result["ok"]:
                applied = dict(self.hello)
            ok, error = result["ok"], result["error"]
        except (ValueError, TypeError, KeyError) as e:
            ok, error = False, str(e)
        reply = self._host("ack", dict(command_id=cid, ok=ok, applied=applied if ok else {}, error=error))
        if durable:
            self.ledger.execute("UPDATE commands SET reply=? WHERE id=?", (json.dumps(reply), cid))
            self.ledger.commit()
        self.recent[cid] = (canonical, reply)
        while len(self.recent) > 256:
            self.recent.popitem(last=False)
        return reply

    def _run(self):
        try:
            # A nonzero Hello serial reads identity without pausing a different board.
            # The zero-serial reconnect handshake is sent only to the verified device.
            for handshake_serial in (1, 0):
                deadline = time.monotonic() + 4.5
                next_hello = 0
                acknowledged = False
                while not self.closed.is_set() and time.monotonic() < deadline:
                    if time.monotonic() >= next_hello:
                        self.serial.write(payload(0, handshake_serial, "hello", [1]))
                        next_hello = time.monotonic() + 1
                    for event in self._next():
                        data = event["data"]
                        if (
                            data.get("type") == "wire_ack"
                            and data.get("op") == OPS.index("hello")
                            and data["wire_command_id"] == handshake_serial
                            and data["ok"]
                        ):
                            acknowledged = True
                    if acknowledged:
                        break
                if not self.hello or not acknowledged:
                    raise ConnectionError("no survey firmware handshake")
            self.ledger = sqlite3.connect(self.path.parent / f".commands-{self.expected_id[1:]}.sqlite3")
            self.ledger.execute(
                "CREATE TABLE IF NOT EXISTS commands(id TEXT PRIMARY KEY, request TEXT NOT NULL, reply TEXT)"
            )
            self.ledger.commit()
            self._exchange("get_state")
            if self.state.get("run_state") == "idle":
                self._exchange("_clock", [int(time.time())])
            self.connected.set()
            next_beat = 0
            while not self.closed.is_set():
                if self.auto_heartbeat and time.monotonic() >= next_beat:
                    self._exchange("heartbeat")
                    next_beat = time.monotonic() + self.heartbeat_ms / 1000
                try:
                    cmd, reply = self.inbox.get_nowait()
                except queue.Empty:
                    for _ in self._next():
                        pass
                else:
                    if isinstance(cmd, tuple):
                        peer, keys = cmd
                        reply.put(self._exchange("_enroll", [peer], keys))
                    else:
                        reply.put(self._dispatch(cmd))
        except Exception as exc:
            if not self.closed.is_set():
                self.problem = f"{type(exc).__name__}: {exc}"
                try:
                    self._host("fault", {"reason": "transport_lost", "detail": self.problem})
                except OSError:
                    pass
        finally:
            self.connected.set()
            if self.ledger is not None:
                self.ledger.close()
            self.serial.close()

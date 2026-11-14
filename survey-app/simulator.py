"""Deterministic v1 adapter. RF scheduling exists only inside the simulated client."""

import math
import time
import uuid
from collections import OrderedDict, deque


def number(default, minimum, maximum, unit):
    return {
        "type": "integer",
        "default": default,
        "min": minimum,
        "max": maximum,
        "unit": unit,
    }


SETTINGS = {
    "profile": {
        "type": "enum",
        "choices": ["LONG_FAST", "FAST (experimental)"],
        "default": "LONG_FAST",
    },
    "min_interval_ms": number(3000, 500, 60000, "ms"),
    "response_timeout_ms": number(1200, 100, 10000, "ms"),
    "adaptive": {"type": "boolean", "default": True},
    "max_interval_ms": number(12000, 500, 120000, "ms"),
    "util_target_pct": number(12, 1, 75, "%"),
    "backdown_pct": number(25, 2, 90, "%"),
    "gps_interval_ms": number(1000, 250, 5000, "ms"),
    "gps_max_age_ms": number(2000, 500, 30000, "ms"),
    "heartbeat_interval_ms": number(1000, 250, 5000, "ms"),
    "heartbeat_timeout_ms": number(5000, 1000, 30000, "ms"),
    "quiet_duration_s": number(900, 1, 1800, "s"),
}
COMMANDS = [
    "hello",
    "get_state",
    "configure",
    "start",
    "pause",
    "resume",
    "stop",
    "set_target",
    "heartbeat",
]
SCENARIOS = [
    "Mixed route",
    "Strong link",
    "Weak link",
    "Asymmetric link",
    "Timeouts",
    "Busy channel",
    "No GPS",
    "Stale GPS",
    "Heartbeat loss",
    "USB loss",
    "Late / duplicate",
    "Queue pressure",
    "Map outage",
]
TARGETS = {
    "SIM-R01": {"lat_deg": 36.283, "lon_deg": -115.633},
    "SIM-R02": {"lat_deg": 36.294, "lon_deg": -115.652},
}
EMPTY_GPS = {
    "valid": False,
    "lat_deg": None,
    "lon_deg": None,
    "altitude_m": None,
    "fix_utc_ms": None,
    "fix_age_ms": None,
    "quality": None,
    "satellites": None,
}


class Simulator:
    source = "simulation"

    def __init__(self):
        self.boot_id = "sim-" + uuid.uuid4().hex[:12]
        self.seq = self.fix_index = self.attempt_index = 0
        self.events = deque()
        self.acks = OrderedDict()
        self.last_tx = None
        self.last_gps_report = None
        self.scenario = "Mixed route"
        self.last_fix = self.next_attempt = self.last_heartbeat = self.quiet_until = (
            None
        )
        self.gps = EMPTY_GPS.copy()
        self.pending = None
        self.settings = {k: s["default"] for k, s in SETTINGS.items()}
        self.state = {
            "run_state": "idle",
            "mode": "survey",
            "session_id": None,
            "segment_id": 0,
            "target_id": "SIM-R01",
            "settings": self.settings,
            "gps": self.gps,
            "counts": {"attempts": 0, "success": 0},
            "transport": "connected",
            "heartbeat_ok": False,
            "cadence_ms": None,
            "backdown": False,
            "queue_dropped": 0,
            "queue_depth": 0,
            "queue_capacity": 512,
            "measured_interval_ms": None,
            "quiet_remaining_s": 0,
            "scenario": self.scenario,
            "fault": None,
        }
        self.hello = {
            "build": "sim-1",
            "protocol": 1,
            "hardware": "Virtual Heltec + RAK",
            "commands": COMMANDS,
            "settings": SETTINGS,
            "targets": TARGETS,
            "scenarios": SCENARIOS,
            "capabilities": ["direct_hop", "independent_gps", "bench", "target_lock"],
            "profile": self.settings["profile"],
        }

    def emit(self, name, data):
        from copy import deepcopy

        self.seq += 1
        self.events.append(
            {
                "v": 1,
                "kind": "event",
                "boot_id": self.boot_id,
                "seq": self.seq,
                "name": name,
                "data_source": self.source,
                "data": deepcopy(data),
            }
        )

    def change_scenario(self, value, now):
        if value not in SCENARIOS:
            raise ValueError("Unknown simulation scenario")
        previous = self.scenario
        self.scenario = self.state["scenario"] = value
        self.state["queue_depth"] = 500 if value == "Queue pressure" else 0
        if value == "Queue pressure" and previous != value:
            self.state["queue_dropped"] += 3
        if value == "USB loss":
            self.state["transport"] = "disconnected"
            self.fault("Adapter disconnected", now, "transport_lost")
        elif previous == "USB loss":
            self.state["transport"] = "connected"
            self.emit("hello", self.hello)
        self.emit("state", self.state)

    def finish(self, now, status, **extra):
        if self.pending:
            self.emit(
                "result",
                dict(
                    self.pending,
                    status=status,
                    receive_mono_ms=now,
                    uplink=None,
                    downlink=None,
                )
                | extra,
            )
            self.pending = None

    def fault(self, reason, now, status="cancelled"):
        self.finish(now, status, reason=reason)
        if self.state["run_state"] == "running":
            self.state["run_state"] = "paused"
        self.state["fault"] = reason
        self.emit("fault", {"reason": reason, "session_id": self.state["session_id"]})
        self.emit("state", self.state)

    def apply(self, cmd, now):
        name, p = cmd["name"], cmd["params"]
        s = self.state
        if name not in COMMANDS:
            raise ValueError("Unsupported command")
        allowed = {
            "configure": SETTINGS,
            "set_target": {"target_id"},
            "start": {"mode", "target_id"},
        }
        if set(p) - set(allowed.get(name, ())):
            raise ValueError("Unknown command parameter")
        if s["transport"] != "connected" and name != "stop":
            raise ValueError("USB disconnected")
        if name == "heartbeat":
            if self.scenario != "Heartbeat loss":
                self.last_heartbeat = now
                s["heartbeat_ok"] = True
        elif name == "hello":
            self.emit("hello", self.hello)
        elif name == "get_state":
            self.emit("state", s)
        elif name in ("configure", "set_target"):
            if s["run_state"] == "running":
                raise ValueError("Pause before changing the survey configuration")
            if name == "configure":
                settings = self.settings | p
                for k, v in p.items():
                    spec = SETTINGS.get(k)
                    if not spec or not (
                        spec["type"] == "integer"
                        and type(v) is int
                        and spec["min"] <= v <= spec["max"]
                        or spec["type"] == "enum"
                        and v in spec["choices"]
                        or spec["type"] == "boolean"
                        and type(v) is bool
                    ):
                        raise ValueError("Unsupported or out-of-range setting: " + k)
                for lo, hi in [
                    ("response_timeout_ms", "min_interval_ms"),
                    ("min_interval_ms", "max_interval_ms"),
                    ("gps_interval_ms", "gps_max_age_ms"),
                    ("heartbeat_interval_ms", "heartbeat_timeout_ms"),
                    ("util_target_pct", "backdown_pct"),
                ]:
                    if (
                        settings[lo] > settings[hi]
                        or lo in ("heartbeat_interval_ms", "util_target_pct")
                        and settings[lo] == settings[hi]
                    ):
                        raise ValueError(f"{hi} must cover {lo}")
                self.settings.update(p)
                self.hello["profile"] = settings["profile"]
            else:
                if p.get("target_id") not in TARGETS:
                    raise ValueError("Unknown target")
                s["target_id"] = p["target_id"]
            s["segment_id"] += 1
        elif name in ("start", "resume"):
            if name == "start" and s["run_state"] in ("paused", "running"):
                raise ValueError("Stop the current run before starting another")
            if name == "resume" and s["run_state"] != "paused":
                raise ValueError("Only a paused session can resume")
            mode = p.get("mode") if name == "start" else s["mode"]
            target = p.get("target_id", s["target_id"])
            if mode not in ("survey", "bench") or target not in TARGETS:
                raise ValueError("Select a supported mode and target")
            if not s["heartbeat_ok"] or mode == "survey" and not self.gps["valid"]:
                raise ValueError("Start requires host heartbeat and a fresh survey fix")
            if name == "start":
                self.last_tx = None
                s.update(
                    session_id="sim-" + uuid.uuid4().hex[:12],
                    segment_id=1,
                    mode=mode,
                    counts={"attempts": 0, "success": 0},
                    target_id=target,
                    measured_interval_ms=None,
                )
            s.update(run_state="running", fault=None)
            self.next_attempt = now
        elif name in ("pause", "stop"):
            if name == "pause" and s["run_state"] != "running":
                raise ValueError("Pause requires a running session")
            self.finish(now, "cancelled", reason=name)
            s["run_state"] = "stopped" if name == "stop" else "paused"
        if name not in ("hello", "get_state", "heartbeat"):
            self.emit("state", s)
        return (
            dict(self.settings)
            if name == "configure"
            else {
                k: s[k]
                for k in ("run_state", "session_id", "segment_id", "target_id", "mode")
            }
        )

    def send(self, cmd):
        now = int(time.monotonic() * 1000)
        cid = cmd.get("id")
        if isinstance(cid, str) and cid in self.acks:
            previous, ack = self.acks[cid]
            self.emit(
                "ack",
                ack
                if cmd == previous
                else {
                    "command_id": cid,
                    "ok": False,
                    "applied": {},
                    "error": "Command ID collision",
                },
            )
            return
        try:
            if (
                cmd.get("v") != 1
                or cmd.get("kind") != "command"
                or not isinstance(cid, str)
                or not isinstance(cmd.get("params"), dict)
                or not isinstance(cmd.get("name"), str)
            ):
                raise ValueError("Invalid v1 command envelope")
            applied = self.apply(cmd, now)
            error = None
        except ValueError as e:
            applied, error = {}, str(e)
        ack = {
            "command_id": cid,
            "ok": error is None,
            "applied": applied,
            "error": error,
        }
        if isinstance(cid, str) and cmd.get("name") != "heartbeat":
            self.acks[cid] = (cmd.copy(), ack)
            if len(self.acks) > 512:
                self.acks.popitem(last=False)
        self.emit("ack", ack)

    def poll(self, now):
        s, cfg = self.state, self.settings
        if s["transport"] == "connected":
            stale = (
                self.last_heartbeat is None
                or now - self.last_heartbeat >= cfg["heartbeat_timeout_ms"]
            )
            if stale and s["heartbeat_ok"]:
                s["heartbeat_ok"] = False
                self.fault("Host heartbeat expired", now)
            if (
                self.last_gps_report is None
                or now - self.last_gps_report >= cfg["gps_interval_ms"]
            ):
                self.last_gps_report = now
                if self.scenario not in ("No GPS", "Stale GPS"):
                    self.fix_index += 1
                    t = self.fix_index * 0.024
                    self.gps = {
                        "valid": True,
                        "lat_deg": 36.28 + 0.009 * math.sin(t),
                        "lon_deg": -115.642 + 0.013 * math.sin(t * 0.61),
                        "altitude_m": 2210 + round(20 * math.sin(t)),
                        "fix_age_ms": 0,
                        "fix_utc_ms": int(time.time() * 1000),
                        "satellites": 9,
                        "quality": 1,
                    }
                    self.last_fix = now
                elif (
                    self.scenario == "No GPS"
                    or self.last_fix is None
                    or now - self.last_fix > cfg["gps_max_age_ms"]
                ):
                    self.gps = EMPTY_GPS | {
                        "fix_age_ms": None
                        if self.last_fix is None
                        else now - self.last_fix
                    }
                else:
                    self.gps["fix_age_ms"] = now - self.last_fix
                s["gps"] = self.gps
                self.emit(
                    "gps",
                    self.gps
                    | {"session_id": s["session_id"], "segment_id": s["segment_id"]},
                )
                if (
                    s["mode"] == "survey"
                    and s["run_state"] == "running"
                    and not self.gps["valid"]
                ):
                    self.fault(
                        "Stale survey GPS fix"
                        if self.scenario == "Stale GPS"
                        else "Survey GPS fix unavailable",
                        now,
                    )
            if self.gps["valid"]:
                self.gps["fix_age_ms"] = now - self.last_fix
                if self.gps["fix_age_ms"] > cfg["gps_max_age_ms"]:
                    self.gps = s["gps"] = EMPTY_GPS | {
                        "fix_age_ms": now - self.last_fix
                    }
                    if s["run_state"] == "running" and s["mode"] == "survey":
                        self.fault("Stale survey GPS fix", now)
            if s["run_state"] == "running":
                self.rf_tick(now)
            s["quiet_remaining_s"] = max(
                0, math.ceil(((self.quiet_until or now) - now) / 1000)
            )
            if now - getattr(self, "last_state", -100000) >= 1000:
                self.emit("state", s)
                self.last_state = now
        events = list(self.events)
        self.events.clear()
        return events

    def rf_tick(self, now):
        s, cfg = self.state, self.settings
        if self.pending and now >= self.reply_time:
            status = self.outcome
            travel = self.reply_time - self.pending["tx_mono_ms"]
            up, down = self.signals

            def reading(pair):
                return {"rssi_dbm": pair[0], "snr_db": pair[1]}

            detail = (
                {"uplink": reading(up), "downlink": reading(down), "rtt_ms": travel}
                if status == "success"
                else {}
            )
            original = self.pending.copy()
            self.finish(now, status, **detail)
            s["counts"]["success"] += int(status == "success")
            if self.scenario == "Late / duplicate":
                self.emit(
                    "result",
                    original
                    | dict(
                        status="late",
                        duplicate_of=original["attempt_id"],
                        reason="additional reply",
                        receive_mono_ms=now + 1,
                        **detail,
                    ),
                )
            self.emit(
                "statistics", {"counts": s["counts"], "session_id": s["session_id"]}
            )
        if self.pending or now < self.next_attempt:
            return
        self.attempt_index += 1
        s["measured_interval_ms"] = None if self.last_tx is None else now - self.last_tx
        self.last_tx = now
        i = self.attempt_index
        scenario = self.scenario
        if scenario == "Mixed route":
            scenario = [
                "Strong link",
                "Asymmetric link",
                "Weak link",
                "Timeouts",
                "Busy channel",
            ][(i - 1) % 5]
        util = 39 if scenario == "Busy channel" else 9
        s["backdown"] = cfg["adaptive"] and util >= cfg["backdown_pct"]
        s["cadence_ms"] = (
            min(cfg["max_interval_ms"], cfg["min_interval_ms"] * 2)
            if s["backdown"]
            else cfg["min_interval_ms"]
        )
        self.next_attempt = now + s["cadence_ms"]
        self.outcome = "timeout" if scenario == "Timeouts" else "success"
        self.reply_time = now + (
            cfg["response_timeout_ms"]
            if self.outcome == "timeout"
            else min(640, cfg["response_timeout_ms"] - 10)
        )
        self.signals = {
            "Weak link": ((-119, -15), (-118, -13)),
            "Asymmetric link": ((-118, -12), (-89, 7)),
        }.get(scenario, ((-84, 9), (-88, 7)))
        self.pending = {
            k: s[k] for k in ("mode", "segment_id", "session_id", "target_id")
        }
        self.pending.update(
            attempt_id=f"{s['session_id']}-{i}",
            sequence=i,
            gps=self.gps.copy(),
            profile=cfg["profile"],
            build=self.hello["build"],
            radio="simulated LoRa",
            target_location=TARGETS[s["target_id"]],
            enqueue_mono_ms=now,
            tx_mono_ms=now,
            local_util_pct=util,
            remote_util_pct=None,
            predicted_airtime_ms=600,
            measured_airtime_ms=None,
            direct_path="simulated zero-hop",
            provenance="simulation",
            status="pending",
        )
        s["counts"]["attempts"] += 1
        self.emit("attempt", self.pending)
        self.quiet_until = now + cfg["quiet_duration_s"] * 1000
        self.emit(
            "quiet",
            {"session_id": s["session_id"], "quiet_until_mono_ms": self.quiet_until},
        )

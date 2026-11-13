"""Read-only archive sampler, sent over SSH by scripts/watch-nodes.py.

Only sanitized measurements leave the server. Uses its existing MQTT runtime;
does not subscribe, publish, authenticate to the portal, or write server files.
"""

import base64
from collections import OrderedDict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import struct
import sys
import time


def epoch(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None


def utc(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat(timespec="milliseconds")


def reading(value, received, measured=None, sample=""):
    stamp = epoch(measured)
    arrival = epoch(received)
    quality = "unknown" if stamp is None else "future" if arrival is not None and stamp > arrival else "valid"
    return {"value": value, "receivedAt": received, "measuredAt": measured,
            "quality": quality, "sample": sample or received}


class Measurements:
    def __init__(self, nodes):
        self.nodes = {n["radio"]: {**n, "lastContactAt": None, "readings": {}} for n in nodes}
        self.seen = OrderedDict()
        self.rejected = 0

    def put(self, radio, metric, value, received, measured=None, sample=""):
        if radio not in self.nodes or epoch(received) is None:
            return
        if isinstance(value, float) and not math.isfinite(value):
            return
        new = reading(value, received, measured, sample)
        old = self.nodes[radio]["readings"].get(metric)
        # Source clock orders clocked reports; duplicate transport copies cannot
        # renew a sample. Unknown clocks use receipt, never for GPS freshness.
        if old:
            if old["sample"] == new["sample"]:
                return
            old_at = epoch(old["measuredAt"]) if old["quality"] == "valid" else epoch(old["receivedAt"])
            new_at = epoch(new["measuredAt"]) if new["quality"] == "valid" else epoch(new["receivedAt"])
            if new_at < old_at or new_at == old_at and new["receivedAt"] <= old["receivedAt"]:
                return
        self.nodes[radio]["readings"][metric] = new

    def contact(self, radio, received):
        node = self.nodes[radio]
        if epoch(received) is not None and (not node["lastContactAt"] or epoch(received) > epoch(node["lastContactAt"])):
            node["lastContactAt"] = received

    def unique(self, fingerprint):
        if fingerprint in self.seen:
            return False
        self.seen[fingerprint] = None
        if len(self.seen) > 100000:
            self.seen.popitem(last=False)
        return True

    def seed(self, db, mappings):
        for key, last, raw, position in db.execute("SELECT key,lastContactAt,readings,latestPosition FROM devices"):
            radio = mappings.get(key)
            if radio not in self.nodes:
                continue
            if last:
                self.contact(radio, last)
            data = json.loads(raw or "{}")
            for metric, item in data.items():
                if not isinstance(item, dict) or not item.get("receivedAt"):
                    continue
                name = {"battery": "voltage", "temperature": "temperature", "humidity": "humidity",
                        "power1Voltage": "inaVoltage", "power1CurrentMa": "inaCurrent",
                        "sensorVoltage": "envVoltage", "sensorCurrentMa": "envCurrent",
                        "wifiSignal": "wifi", "gatewayHealth": "gateway", "sdHealth": "sd"}.get(metric)
                if name:
                    value = item.get("value") if "value" in item else item
                    self.put(radio, name, value, item["receivedAt"], item.get("measuredAt"))
            pos = json.loads(position or "{}")
            if pos.get("receivedAt"):
                # Deliberately exclude coordinates and member assignments.
                value = {k: pos.get(k) for k in ("satellites", "pdop", "altitude") if pos.get(k) is not None}
                self.put(radio, "gps", value, pos["receivedAt"], pos.get("measuredAt"))


RANGES = {
    "battery_level": ("charge", 0, 101), "voltage": ("voltage", 0, 100),
    "channel_utilization": ("busy", 0, 100), "air_util_tx": ("tx", 0, 100),
    "uptime_seconds": ("uptime", 0, 4294967295),
}
ENVIRONMENT = {"temperature": ("temperature", -100, 150), "relative_humidity": ("humidity", 0, 100),
               "voltage": ("envVoltage", 0, 100), "current": ("envCurrent", -100000, 100000)}
POWER = {"ch1_voltage": ("inaVoltage", 0, 100), "ch1_current": ("inaCurrent", -100000, 100000)}


def telemetry_values(data):
    for group, fields in (("device_metrics", RANGES), ("environment_metrics", ENVIRONMENT), ("power_metrics", POWER)):
        for field, value in data.get(group, {}).items():
            rule = fields.get(field)
            if rule and isinstance(value, (int, float)) and math.isfinite(value) and rule[1] <= value <= rule[2]:
                yield rule[0], value


class Decoder:
    def __init__(self, cfg, state, backend):
        sys.path.insert(0, backend)
        from mqtt_adapter import Adapter
        from meshtastic.protobuf import mqtt_pb2, mesh_pb2, telemetry_pb2, portnums_pb2
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from google.protobuf.json_format import MessageToDict
        self.pb = (mqtt_pb2, mesh_pb2, telemetry_pb2, portnums_pb2)
        self.crypto = (Cipher, algorithms, modes)
        self.to_dict = MessageToDict
        # Add selected physical radios to a private, in-memory decoding map only.
        config = {**cfg, "infrastructure": dict(cfg.get("infrastructure", {}))}
        for radio, node in state.nodes.items():
            if radio not in config["members"]:
                config["infrastructure"].setdefault(radio, node["label"])
        self.adapter = Adapter(config)
        self.key = base64.b64decode(cfg["channelKey"], validate=True)
        self.cfg = cfg
        self.state = state

    def consume(self, at, raw, topic):
        mqtt, mesh, telem, ports = self.pb
        e = json.loads(raw)
        if e.get("retained") or e.get("payloadBytes", 0) > 4096:
            return
        prefix = f'{self.cfg["root"].rstrip("/")}/2/e/{self.cfg["channel"]}/'
        if not topic.startswith(prefix) or topic[len(prefix):] not in self.cfg["gateways"]:
            return
        binary = base64.b64decode(e["payloadBase64"], validate=True)
        env = mqtt.ServiceEnvelope.FromString(binary)
        p = env.packet
        radio = f'!{getattr(p, "from"):08x}'
        if (radio not in self.state.nodes or not p.id or p.via_mqtt or p.pki_encrypted
                or env.gateway_id != topic[len(prefix):] or env.channel_id != self.cfg["channel"]
                or p.WhichOneof("payload_variant") != "encrypted"):
            return
        Cipher, algorithms, modes = self.crypto
        nonce = struct.pack("<QI", p.id, getattr(p, "from")) + b"\0" * 4
        d = mesh.Data.FromString(Cipher(algorithms.AES(self.key), modes.CTR(nonce)).decryptor().update(p.encrypted))
        fingerprint = f"{radio}:{p.id}:{hashlib.sha256(p.encrypted).hexdigest()}"
        if not self.state.unique(fingerprint):
            return
        self.state.contact(radio, at)
        if d.portnum == ports.TELEMETRY_APP:
            t = telem.Telemetry.FromString(d.payload)
            data = self.to_dict(t, preserving_proto_field_name=True)
            measured = utc(t.time) if t.time >= 1577836800 else None
            for metric, value in telemetry_values(data):
                self.state.put(radio, metric, value, at, measured, fingerprint)
        elif d.portnum == ports.POSITION_APP:
            p = mesh.Position.FromString(d.payload)
            if not p.HasField("latitude_i") or not p.HasField("longitude_i"):
                return
            if abs(p.timestamp_millis_adjust) > 999:
                return
            measured = utc(p.timestamp + p.timestamp_millis_adjust / 1000) if p.timestamp else None
            data = {"satellites": p.sats_in_view or None, "pdop": p.PDOP / 100 if p.PDOP else None}
            if p.HasField("altitude"):
                data["altitude"] = p.altitude
            self.state.put(radio, "gps", data, at, measured, fingerprint)
        elif d.portnum in (ports.PRIVATE_APP, ports.NEIGHBORINFO_APP):
            report = self.adapter.decode(topic, binary, epoch(at))
            if not report:
                return
            kind, data = report["kind"], report["data"]
            measured = report.get("measuredAt")
            if kind == "neighbors":
                self.state.put(radio, "neighbors", data.get("totalNeighbors", len(data.get("rows", []))),
                               at, measured, fingerprint)
            elif kind in ("gateway-health", "sd-health"):
                # Re-sent SD generations keep their original clock/receipt.
                metric = "gateway" if kind == "gateway-health" else "sd"
                prior = self.state.nodes[radio]["readings"].get(metric)
                if prior and isinstance(prior["value"], dict):
                    old = prior["value"]
                    if old.get("bootId") == data["bootId"] and old.get("sequence", -1) >= data["sequence"]:
                        return
                self.state.put(radio, metric, data, at, measured, fingerprint)


def configured_nodes(cfg, roster):
    nodes = {radio: {"radio": radio, "label": label, "kind": "repeater"} for radio, label in roster.items()}
    for group, kind in (("members", "member"), ("infrastructure", "infrastructure")):
        for radio, key in cfg.get(group, {}).items():
            if radio not in nodes:
                nodes[radio] = {"radio": radio, "label": "Legacy V3" if key.startswith("legacy-v3-") else key.upper(),
                                "kind": "gateway" if radio in cfg["gateways"] else kind}
    registered = {**cfg.get("members", {}), **cfg.get("infrastructure", {})}
    for radio, node in nodes.items():
        node["registered"] = radio in registered
    return list(nodes.values())


def feed_status(db):
    row = db.execute("SELECT connected,forcedOffline,heartbeatAt FROM feed WHERE key='worker'").fetchone()
    if not row:
        return {"connected": False, "heartbeatAt": None}
    return {"connected": bool(row[0]) and not bool(row[1]), "heartbeatAt": row[2] or None}


def run(settings):
    """One incremental reader per SSH session; archive cursor avoids full rescans."""
    try:
        cfg = json.loads(Path(settings["config"]).read_text())
        state = Measurements(configured_nodes(cfg, settings["roster"]))
        decoder = Decoder(cfg, state, settings["backend"])
        mappings = {v: k for k, v in {**cfg["members"], **cfg.get("infrastructure", {})}.items()}
        database = Path(settings["database"]).as_uri() + "?mode=ro"
        with sqlite3.connect(database, uri=True, timeout=2) as db:
            db.execute("PRAGMA query_only=ON")
            # One consistent startup snapshot, then short incremental reads.
            db.execute("BEGIN")
            cursor = db.execute("SELECT COALESCE(MAX(rowid),0) FROM mqtt_archive").fetchone()[0]
            state.seed(db, mappings)
            cutoff = utc(time.time() - settings["hours"] * 3600)
            rows = db.execute("SELECT receivedAt,envelope,topic FROM mqtt_archive WHERE receivedAt>=? AND rowid<=? ORDER BY rowid",
                              (cutoff, cursor)).fetchall()
            db.commit()
            consume_rows(decoder, rows)
            while True:
                try:
                    # Includes gateway Wi-Fi reports and old member battery
                    # readings that are outside the bounded archive bootstrap.
                    state.seed(db, mappings)
                    rows = db.execute("SELECT rowid,receivedAt,envelope,topic FROM mqtt_archive WHERE rowid>? ORDER BY rowid LIMIT 2000",
                                      (cursor,)).fetchall()
                    if rows:
                        consume_rows(decoder, [r[1:] for r in rows])
                        cursor = rows[-1][0]
                    payload = {"schema": 1, "at": utc(time.time()), "feed": feed_status(db),
                               "nodes": sorted(state.nodes.values(), key=lambda n: n["label"]),
                               "skipped": state.rejected, "catchingUp": len(rows) == 2000}
                    print(json.dumps(payload, allow_nan=False), flush=True)
                except sqlite3.Error:
                    print(json.dumps({"error": "Database read unavailable", "at": utc(time.time())}), flush=True)
                if settings.get("once"):
                    break
                time.sleep(settings["interval"])
    except (BrokenPipeError, KeyboardInterrupt):
        return
    except Exception as error:
        # Exception messages can contain configuration or raw packet contents.
        print(json.dumps({"error": "Sampler failed: " + type(error).__name__, "at": utc(time.time())}), flush=True)
        raise SystemExit(1)


def consume_rows(decoder, rows):
    for at, raw, topic in rows:
        try:
            decoder.consume(at, raw, topic)
        except Exception:
            decoder.state.rejected += 1

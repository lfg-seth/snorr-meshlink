"""Read-only archive sampler, sent over SSH by scripts/watch-nodes.py.

Only sanitized measurements leave the server. Uses its existing MQTT runtime;
does not subscribe, publish, authenticate to the portal, or write server files.
"""

import base64
from bisect import insort
from collections import defaultdict, OrderedDict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from contextlib import closing
import re
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


METRIC_STREAM = {
    "voltage": "device", "charge": "device", "busy": "device", "tx": "device", "uptime": "device",
    "temperature": "environment", "humidity": "environment", "envVoltage": "environment", "envCurrent": "environment",
    "inaVoltage": "power", "inaCurrent": "power", "neighbors": "snns", "standardNeighbors": "neighbor_info",
    "gps": "position", "gateway": "gateway", "wifi": "wifi", "sd": "sd",
}


class Measurements:
    def __init__(self, nodes, cadences=None, gateway_names=None):
        cadences = cadences or {}
        self.gateway_names = gateway_names or {}
        self.nodes = {n["radio"]: {**n, "lastContactAt": None, "readings": {}, "watchdogs": {
            stream: {"cadenceSeconds": period, "lastReceivedAt": None, "sample": None, "basis": "saved-profile"}
            for stream, period in cadences.get(n["radio"], {}).items() if period is not None}} for n in nodes}
        self.seen = OrderedDict()
        self.packets = []
        self.rejected = 0

    def record_packet(self, radio, stream, at, fingerprint, gateway=None, route=None):
        received = epoch(at)
        if received is None:
            return
        packet = {"id": hashlib.sha256(fingerprint.encode()).hexdigest()[:24],
                  "radio": radio, "stream": stream, "received": received,
                  "heardThroughRadio": gateway, "heardThrough": self.gateway_names.get(gateway, gateway),
                  "route": route}
        # Keep the newest receipts even when archive rows arrive out of time order.
        insort(self.packets, packet, key=lambda item: item["received"])
        if len(self.packets) > 48:
            self.packets.pop(0)

    def recent_packets(self, now):
        return [p for p in reversed(self.packets) if 0 <= now - p["received"] <= 3600]

    def put(self, radio, metric, value, received, measured=None, sample=""):
        if radio not in self.nodes or epoch(received) is None:
            return
        if isinstance(value, float) and not math.isfinite(value):
            return
        new = reading(value, received, measured, sample)
        new["stream"] = METRIC_STREAM.get(metric)
        old = self.nodes[radio]["readings"].get(metric)
        # Source clock orders clocked reports; duplicate transport copies cannot
        # renew a sample. Unknown clocks use receipt, never for GPS freshness.
        if old:
            if old["sample"] == new["sample"]:
                return
            old_at = epoch(old["measuredAt"]) if old["quality"] == "valid" else epoch(old["receivedAt"])
            new_at = epoch(new["measuredAt"]) if new["quality"] == "valid" else epoch(new["receivedAt"])
            # The persisted fix omits altitude. Enrich that same receipt on archive replay.
            if (metric == "gps" and sample and old["sample"] == old["receivedAt"]
                    and epoch(old["receivedAt"]) == epoch(received) and old_at == new_at):
                old["value"].update({k: v for k, v in value.items() if v is not None})
            if new_at < old_at or new_at == old_at and new["receivedAt"] <= old["receivedAt"]:
                return
        self.nodes[radio]["readings"][metric] = new

    def watch(self, radio, stream, received, sample, measured=None, cadence=None):
        """Each validated packet type has its own arrival timer, separate from fix age."""
        if radio not in self.nodes or epoch(received) is None:
            return
        watches = self.nodes[radio]["watchdogs"]
        item = watches.setdefault(stream, {"cadenceSeconds": None, "lastReceivedAt": None,
                                            "sample": None, "basis": "event"})
        if isinstance(cadence, (int, float)) and not isinstance(cadence, bool) and math.isfinite(cadence) and 0 < cadence <= 604800:
            item.update(cadenceSeconds=cadence, basis="reported-interval")
        if item["sample"] == sample or item["lastReceivedAt"] and epoch(received) <= epoch(item["lastReceivedAt"]):
            return
        item.update(lastReceivedAt=received, measuredAt=measured, sample=sample)

    def contact(self, radio, received, gateway=None, route=None):
        node = self.nodes[radio]
        timestamp = epoch(received)
        previous = epoch(node["lastContactAt"])
        if timestamp is None:
            return
        if previous is not None and timestamp < previous:
            return
        if timestamp == previous:
            if not gateway or node.get("heardThrough"):
                return
            received = node["lastContactAt"]
        node.update(lastContactAt=received, heardThrough=gateway,
                    heardThroughName=self.gateway_names.get(gateway, gateway),
                    route={"reception": "local"} if radio == gateway else route)

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
                    stream = METRIC_STREAM[name]
                    generation = (f"{stream}:{value['bootId']}:{value['sequence']}"
                                  if isinstance(value, dict) and "bootId" in value and "sequence" in value else item["receivedAt"])
                    self.watch(radio, stream, item["receivedAt"], generation, item.get("measuredAt"),
                               value.get("intervalSeconds") if isinstance(value, dict) else None)
            pos = json.loads(position or "{}")
            if pos.get("receivedAt"):
                # Deliberately exclude coordinates and member assignments.
                value = {k: pos.get(k) for k in ("satellites", "pdop", "altitude") if pos.get(k) is not None}
                self.put(radio, "gps", value, pos["receivedAt"], pos.get("measuredAt"))
                self.watch(radio, "position", pos["receivedAt"], pos["receivedAt"], pos.get("measuredAt"))


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


def relay_index(names):
    by_byte = defaultdict(list)
    for radio, name in names.items():
        if not re.fullmatch(r"![0-9a-fA-F]{8}", radio):
            continue
        # NodeDB::getLastByteOfNodeNum reserves zero and encodes both 00 and ff as ff.
        suffix = int(radio[-2:], 16) or 0xff
        by_byte[suffix].append((radio, name))
    return by_byte


def packet_route(packet, radio, gateway, by_byte, has_bitfield=False):
    if radio == gateway:
        return {"reception": "local"}
    transport = getattr(packet, "transport_mechanism", 0)
    start, limit = getattr(packet, "hop_start", 0), getattr(packet, "hop_limit", -1)
    # Zero is internal/unspecified; 1–4 are the protobuf LoRa transports.
    if transport not in (0, 1, 2, 3, 4) or not 0 <= limit <= start <= 7:
        return None
    # getHopsAway accepts zero start only when the decoded Data bitfield proves origin support.
    if start == 0 and not has_bitfield:
        return None
    # With a supported start, an omitted proto3 limit is a valid exhausted budget.
    hops = start - limit
    route = {"reception": "unknown", "reportedHops": hops}
    # The receive driver discards the relay byte at zero start. The count can still be known.
    has_signal = packet.rx_rssi < 0 or (math.isfinite(packet.rx_snr) and packet.rx_snr != 0)
    if start == 0 or (not transport and not has_signal):
        return route
    matches = by_byte.get(getattr(packet, "relay_node", 0), [])
    if hops:
        route["reception"] = "relayed"
        if len(matches) == 1:
            candidate, name = matches[0]
            if candidate not in (radio, gateway):
                route["lastRelayRadio"] = candidate
                if name:
                    route["lastRelayCandidate"] = name
    elif len(matches) == 1 and matches[0][0] == radio:
        route["reception"] = "direct"
    return route


class Decoder:
    def __init__(self, cfg, state, backend, by_byte):
        if backend not in sys.path:
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
        self.by_byte = by_byte

    def packet_data(self, packet):
        Cipher, algorithms, modes = self.crypto
        nonce = struct.pack("<QI", packet.id, getattr(packet, "from")) + b"\0" * 4
        plaintext = Cipher(algorithms.AES(self.key), modes.CTR(nonce)).decryptor().update(packet.encrypted)
        return self.pb[1].Data.FromString(plaintext)

    def persisted_route(self, db, radio, gateway, at, packet_key):
        """Match the saved receipt to one archive envelope, even outside the replay window."""
        topic = f'{self.adapter.root}/2/e/{self.adapter.channel}/{gateway}'
        rows = db.execute("SELECT envelope FROM mqtt_archive WHERE receivedAt=? AND topic=?", (at, topic))
        found = None
        for (raw,) in rows:
            try:
                record = json.loads(raw)
                if record.get("retained") or record.get("payloadBytes", 0) > 4096:
                    continue
                binary = base64.b64decode(record["payloadBase64"], validate=True)
                normalized = self.adapter.decode(topic, binary, epoch(at))
                if not normalized or packet_key != "{kind}:{deviceId}:{packetId}".format(**normalized):
                    continue
                packet = self.pb[0].ServiceEnvelope.FromString(binary).packet
                if radio != f'!{getattr(packet, "from"):08x}':
                    continue
                if found is not None:
                    return None  # Same time, gateway and content can still have two RF headers.
                found = packet
            except (ValueError, KeyError):
                continue
        if found is None:
            return None
        has_bitfield = found.hop_start == 0 and self.packet_data(found).HasField("bitfield")
        return packet_route(found, radio, gateway, self.by_byte, has_bitfield)

    def consume(self, at, raw, topic):
        mqtt = self.pb[0]
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
        d = self.packet_data(p)
        fingerprint = f"{radio}:{p.id}:{hashlib.sha256(p.encrypted).hexdigest()}"
        unique = self.state.unique(fingerprint)
        # A persisted device contact may correspond to this transport copy.
        if unique or epoch(at) == epoch(self.state.nodes[radio]["lastContactAt"]):
            route = packet_route(p, radio, env.gateway_id, self.by_byte, d.HasField("bitfield"))
            self.state.contact(radio, at, env.gateway_id, route)
        if not unique:
            return
        stream = self.apply_readings(d, radio, at, fingerprint, topic, binary)
        self.state.record_packet(radio, stream, at, fingerprint, env.gateway_id, route)

    def apply_readings(self, d, radio, at, fingerprint, topic, binary):
        """Update measurements and identify the stream of this original transmission."""
        _, mesh, telem, ports = self.pb
        if d.portnum == ports.TELEMETRY_APP:
            t = telem.Telemetry.FromString(d.payload)
            data = self.to_dict(t, preserving_proto_field_name=True)
            measured = utc(t.time) if t.time >= 1577836800 else None
            group = next((k for k, value in data.items() if isinstance(value, dict)), None)
            if group:
                stream = {"device_metrics": "device", "environment_metrics": "environment",
                          "power_metrics": "power"}.get(group, "telemetry:" + group)
                self.state.watch(radio, stream, at, fingerprint, measured)
            for metric, value in telemetry_values(data):
                self.state.put(radio, metric, value, at, measured, fingerprint)
            return stream if group else "telemetry"
        elif d.portnum == ports.POSITION_APP:
            p = mesh.Position.FromString(d.payload)
            if not p.HasField("latitude_i") or not p.HasField("longitude_i"):
                return "position"
            if (abs(p.latitude_i) > 900000000 or abs(p.longitude_i) > 1800000000
                    or abs(p.timestamp_millis_adjust) > 999):
                return "position"
            measured = utc(p.timestamp + p.timestamp_millis_adjust / 1000) if p.timestamp else None
            data = {"satellites": p.sats_in_view or None, "pdop": p.PDOP / 100 if p.PDOP else None}
            if p.HasField("altitude"):
                data["altitude"] = p.altitude
            self.state.put(radio, "gps", data, at, measured, fingerprint)
            self.state.watch(radio, "position", at, fingerprint, measured)
            return "position"
        elif d.portnum in (ports.PRIVATE_APP, ports.NEIGHBORINFO_APP):
            report = self.adapter.decode(topic, binary, epoch(at))
            if not report:
                self.state.watch(radio, "private-other", at, fingerprint)
                return "private-other"
            kind, data = report["kind"], report["data"]
            measured = report.get("measuredAt")
            if kind == "neighbors":
                standard = data.get("reportType") == "neighbor-info"
                stream = "neighbor_info" if standard else "snns"
                generation = f"snns:{data['bootId']}:{data['sequence']}" if not standard else fingerprint
                self.state.watch(radio, stream, at, generation, measured)
                self.state.put(radio, "standardNeighbors" if standard else "neighbors", data.get("totalNeighbors", len(data.get("rows", []))),
                               at, measured, fingerprint)
                return stream
            elif kind in ("gateway-health", "sd-health"):
                # Re-sent SD generations keep their original clock/receipt.
                metric = "gateway" if kind == "gateway-health" else "sd"
                prior = self.state.nodes[radio]["readings"].get(metric)
                if prior and isinstance(prior["value"], dict):
                    old = prior["value"]
                    if old.get("bootId") == data["bootId"] and old.get("sequence", -1) >= data["sequence"]:
                        return metric
                self.state.put(radio, metric, data, at, measured, fingerprint)
                self.state.watch(radio, metric, at, f"{metric}:{data['bootId']}:{data['sequence']}",
                                 measured, data.get("intervalSeconds"))
                return metric
            elif kind in ("wifi", "wifi-signal"):
                self.state.put(radio, "wifi", data, at, measured, fingerprint)
                self.state.watch(radio, "wifi", at, f"wifi:{data['bootId']}:{data['sequence']}",
                                 measured, data.get("intervalSeconds"))
                return "wifi"
            else:
                self.state.watch(radio, "private-other", at, fingerprint)
                return "private-other"
        else:
            # Event-driven packet types get an age timer but no invented deadline.
            try:
                packet_type = ports.PortNum.Name(d.portnum).lower()
            except ValueError:
                packet_type = str(d.portnum)
            stream = "nodeinfo" if d.portnum == ports.NODEINFO_APP else "packet:" + packet_type
            self.state.watch(radio, stream, at, fingerprint)
            return stream


def configured_nodes(cfg, roster):
    nodes = {radio: {"radio": radio, "label": label, "kind": "repeater"} for radio, label in roster.items()}
    for group, kind in (("members", "member"), ("infrastructure", "infrastructure")):
        for radio, key in cfg.get(group, {}).items():
            if radio not in nodes:
                legacy = key.startswith("legacy-v3-")
                nodes[radio] = {"radio": radio, "label": f"V3-{radio[1:]}" if legacy else key.upper(),
                                "kind": "legacy" if legacy else "gateway" if radio in cfg["gateways"] else kind}
    registered = {**cfg.get("members", {}), **cfg.get("infrastructure", {})}
    for radio, node in nodes.items():
        node["registered"] = radio in registered
    return list(nodes.values())


def seed_gateway_receipts(db, state, mappings, gateways, decoder):
    """Recover the route of a persisted contact even outside the archive replay window."""
    radios = {key: radio for radio, key in gateways.items()}
    rows = db.execute("""
        SELECT r.deviceId, r.receivedAt, r.gatewayId, r.packetKey FROM packet_receipts r
        JOIN devices d ON d.key = r.deviceId AND d.lastContactAt = r.receivedAt
        WHERE r.outcome IN ('accepted', 'duplicate') ORDER BY r.rowid
    """)
    for key, received, gateway, packet_key in rows:
        radio = mappings.get(key)
        if radio in state.nodes and gateway in radios and not state.nodes[radio].get("heardThrough"):
            gateway_radio = radios[gateway]
            route = None
            if radio != gateway_radio:
                route = decoder.persisted_route(db, radio, gateway_radio, received, packet_key)
            state.contact(radio, received, gateway_radio, route)


def feed_status(db):
    row = db.execute("SELECT connected,forcedOffline,heartbeatAt FROM feed WHERE key='worker'").fetchone()
    if not row:
        return {"connected": False, "heartbeatAt": None}
    return {"connected": bool(row[0]) and not bool(row[1]), "heartbeatAt": row[2] or None}


def run(settings, publish=None):
    """One incremental reader per SSH session; archive cursor avoids full rescans."""
    try:
        cfg = json.loads(Path(settings["config"]).read_text())
        nodes = configured_nodes(cfg, settings["roster"])
        site_names = settings.get("siteNames", {})
        # Count collisions across the fleet, including radios without a displayed card or name.
        names = dict.fromkeys(settings.get("cadences", {}))
        identities = {**cfg["members"], **cfg.get("infrastructure", {}), **cfg["gateways"]}
        names.update(dict.fromkeys(identities))
        if "selected" in settings:
            nodes = [node for node in nodes if node["radio"] in settings["selected"]]
        mappings = {v: k for k, v in {**cfg["members"], **cfg.get("infrastructure", {})}.items()}
        database = Path(settings["database"]).as_uri() + "?mode=ro"
        with closing(sqlite3.connect(database, uri=True, timeout=2)) as db:
            db.execute("PRAGMA query_only=ON")
            # One consistent startup snapshot, then short incremental reads.
            db.execute("BEGIN")
            cursor = db.execute("SELECT COALESCE(MAX(rowid),0) FROM mqtt_archive").fetchone()[0]
            registered_names = {
                key: (name or "").strip()
                for key, name in db.execute(
                    "SELECT key, json_extract(configuration, '$.name') FROM devices")
            }
            names.update({radio: site_names.get(radio) or registered_names.get(key)
                          for radio, key in identities.items()})
            names.update({radio: name for radio, name in site_names.items() if name})
            gateway_names = {radio: names.get(radio) or radio for radio in cfg["gateways"]}
            state = Measurements(nodes, settings.get("cadences"), gateway_names)
            decoder = Decoder(cfg, state, settings["backend"], relay_index(names))
            state.seed(db, mappings)
            seed_gateway_receipts(db, state, mappings, cfg["gateways"], decoder)
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
                    if publish is None:
                        print(json.dumps(payload, allow_nan=False), flush=True)
                    else:
                        payload["packets"] = state.recent_packets(epoch(payload["at"]))
                        if publish(payload) is False:
                            return True  # Caller requested a new selection.
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

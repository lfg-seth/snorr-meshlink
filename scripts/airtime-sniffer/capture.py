"""Receive-only SNORR wire capture, optional channel decoding, and airtime accounting."""
from __future__ import annotations

import base64
from collections import Counter, OrderedDict, deque
from datetime import datetime, timezone
import functools
import json
import math
from pathlib import Path
import re
import struct
import zlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import DecodeError
from meshtastic.protobuf import mesh_pb2, portnums_pb2, telemetry_pb2

PUBLIC_KEY = bytes.fromhex("d4f1bb3a20290759f0bcffabcf4e6901")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
MARKER = re.compile(r"SNORR_(RX|DATA|END|CFG) (.*)")


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def xor_hash(data):
    return functools.reduce(int.__xor__, data, 0)


def expand_key(key):
    if len(key) == 1:
        if key[0] == 0:
            return b""
        return PUBLIC_KEY[:-1] + bytes([(PUBLIC_KEY[-1] + key[0] - 1) & 255])
    if 1 < len(key) < 16:
        return key.ljust(16, b"\0")
    if 16 < len(key) < 32:
        return key.ljust(32, b"\0")
    if len(key) not in (0, 16, 32):
        raise ValueError("Channel keys must be 0–32 bytes")
    return key


class Decoder:
    def __init__(self, channels=()):
        self.channels = []
        self.names = {}
        for name, key in channels:
            key = expand_key(key)
            self.channels.append((name, xor_hash(name.encode()) ^ xor_hash(key), key))
        # Public default keys for the documented standard modem channel names.
        for name in ("LongFast", "LongSlow", "LongMod", "MediumSlow", "MediumFast", "ShortSlow", "ShortFast", "ShortTurbo", "VLongSlow"):
            self.channels.append((name, xor_hash(name.encode()) ^ xor_hash(PUBLIC_KEY), PUBLIC_KEY))

    @classmethod
    def from_file(cls, path):
        if not path:
            return cls()
        obj = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        decoder = cls([(c["name"], base64.b64decode(c["psk"], validate=True)) for c in obj["channels"]])
        decoder.names.update(obj.get("names", {}))
        return decoder

    def decode(self, raw, state=0):
        result = {"raw_hex": raw.hex(), "length": len(raw)}
        if state != 0:
            return {**result, "decode_status": "radio_error", "summary": f"Radio read error {state}; bytes untrusted"}
        if len(raw) < 16:
            return {**result, "decode_status": "short_frame", "summary": "Short/non-Meshtastic frame"}
        to, sender, packet_id, flags, channel, next_hop, relay = struct.unpack("<IIIBBBB", raw[:16])
        result.update(sender=f"!{sender:08x}", to=f"!{to:08x}", packet_id=f"{packet_id:08x}",
                      channel_hash=channel, hop_limit=flags & 7, hop_start=flags >> 5,
                      want_ack=bool(flags & 8), via_mqtt=bool(flags & 16), next_hop=next_hop, relay=relay)
        result["sender_name"] = self.names.get(result["sender"], "")
        payload = raw[16:]
        result["encrypted_hex"] = payload.hex()
        for name, channel_hash, key in self.channels:
            if channel_hash != channel:
                continue
            plain = payload
            if key:
                decryptor = Cipher(algorithms.AES(key), modes.CTR(struct.pack("<QII", packet_id, sender, 0))).decryptor()
                plain = decryptor.update(payload) + decryptor.finalize()
            data = mesh_pb2.Data()
            try:
                data.ParseFromString(plain)
                # AES-CTR has no authentication; this is only structural validation.
                if not data.portnum:
                    continue
            except (DecodeError, ValueError, struct.error, OverflowError):
                continue
            try:
                content = self.content(data.portnum, data.payload, sender)
            except (DecodeError, ValueError, struct.error, OverflowError):
                content = {"decode_error": "Invalid application payload", "payload_hex": data.payload.hex()}
            try:
                port = portnums_pb2.PortNum.Name(data.portnum)
            except ValueError:
                port = f"PORT_{data.portnum}"
            result.update(decode_status="decoded_candidate", channel_name=name, port=port,
                          port_number=data.portnum, decoded=MessageToDict(data), content=content,
                          summary=self.describe(port, content), authentication="unauthenticated channel AES-CTR/cleartext")
            if data.portnum == portnums_pb2.NODEINFO_APP:
                self.names[result["sender"]] = content.get("short_name") or content.get("long_name") or result["sender"]
                result["sender_name"] = self.names[result["sender"]]
            return result
        result.update(decode_status="encrypted_or_unknown", summary="Encrypted/unknown key, PKI, or invalid Data protobuf")
        return result

    @staticmethod
    def content(port, payload, sender):
        if port == portnums_pb2.TEXT_MESSAGE_APP:
            return {"text": payload.decode("utf-8", errors="replace")}
        classes = {portnums_pb2.POSITION_APP: mesh_pb2.Position, portnums_pb2.NODEINFO_APP: mesh_pb2.User,
                   portnums_pb2.TELEMETRY_APP: telemetry_pb2.Telemetry, portnums_pb2.NEIGHBORINFO_APP: mesh_pb2.NeighborInfo,
                   portnums_pb2.ROUTING_APP: mesh_pb2.Routing, portnums_pb2.TRACEROUTE_APP: mesh_pb2.RouteDiscovery,
                   portnums_pb2.WAYPOINT_APP: mesh_pb2.Waypoint}
        if port == 256 and payload.startswith(b"SNNS"):
            return decode_snns(payload, sender)
        if port in classes:
            msg = classes[port]()
            msg.ParseFromString(payload)
            content = MessageToDict(msg, preserving_proto_field_name=True)
            if port == portnums_pb2.POSITION_APP:
                for field in ("latitude", "longitude"):
                    if f"{field}_i" in content:
                        content[f"{field}_degrees"] = content[f"{field}_i"] / 1e7
            return content
        return {"payload_hex": payload.hex(), "payload_bytes": len(payload)}

    @staticmethod
    def describe(port, content):
        if "text" in content:
            return "Text: " + content["text"]
        return port + " " + json.dumps(content, ensure_ascii=False, separators=(",", ":"))


def decode_snns(payload, sender):
    if len(payload) < 24:
        raise ValueError("Truncated SNNS")
    magic, version, flags, count, total, observer, boot, sequence, uptime = struct.unpack_from("<4sBBBBIIII", payload)
    if (version != 1 or observer != sender or not boot or not sequence or not 1 <= count <= 8
            or flags & ~3 or not count <= total <= 255 or bool(flags & 1) != (total > count)
            or len(payload) != 24 + 16 * count):
        raise ValueError("Invalid SNNS")
    rows = []
    for offset in range(24, len(payload), 16):
        node, age, rssi, snr, observations = struct.unpack_from("<IIhhI", payload, offset)
        if not node or node == sender or age >= 1800 or not -200 <= rssi < 0 or not -400 <= snr <= 400 or not observations:
            raise ValueError("Invalid SNNS row")
        rows.append({"node_id": f"!{node:08x}", "hearing_age_seconds": age, "observations": observations,
                     "rssi_dbm": rssi, "snr_db": snr / 4})
    return {"type": "SNNS_v1", "observer": f"!{observer:08x}", "boot": boot, "uptime_seconds": uptime,
            "sequence": sequence, "flags": flags, "total_neighbors": total, "neighbors": rows}


class WireParser:
    """Reassemble every raw reception, reporting serial loss instead of hiding it."""
    def __init__(self):
        self.pending = None
        self.previous = None
        self.config = {}

    def finish(self):
        if self.pending is not None:
            seq = self.pending["seq"]
            self.pending = None
            return [{"type": "capture_gap", "reason": "Incomplete reception at disconnect/end", "sequence": seq}]
        return []

    def feed(self, line):
        match = MARKER.search(ANSI.sub("", line))
        if not match:
            return []
        kind, text = match.groups()
        events = []
        try:
            values = dict(part.split("=", 1) for part in text.strip().split())
            if kind == "CFG":
                if values.get("v") != "1":
                    raise ValueError("Unsupported sniffer version")
                self.config = values
                return [{"type": "radio_config", **values}]
            sequence = int(values["seq"])
            if kind == "RX":
                events.extend(self.finish())
                boot = values["boot"]
                if self.previous and self.previous[0] == boot and sequence != (self.previous[1] + 1) & 0xffffffff:
                    events.append({"type": "capture_gap", "reason": "Reception sequence gap", "previous": self.previous[1], "next": sequence})
                self.previous = (boot, sequence)
                length = int(values["len"])
                if values.get("v") != "1" or not 0 <= length <= 255:
                    raise ValueError("Invalid version/length")
                self.pending = {"seq": sequence, "boot": boot, "device_ms": int(values["ms"]), "length": length,
                                "radio_state": int(values["state"]), "rssi_dbm": int(values["rssi"]),
                                "snr_db": float(values["snr"]), "airtime_ms": int(values["toa"]), "bytes": bytearray(),
                                "radio_config": self.config.copy()}
                if not math.isfinite(self.pending["snr_db"]) or self.pending["airtime_ms"] < 0:
                    raise ValueError("Invalid RF metadata")
            elif self.pending is None or sequence != self.pending["seq"]:
                raise ValueError("Orphan packet chunk/end")
            elif kind == "DATA":
                data = self.pending["bytes"]
                if int(values["off"]) != len(data):
                    raise ValueError("Missing/reordered packet chunk")
                data.extend(bytes.fromhex(values["hex"]))
                if len(data) > self.pending["length"]:
                    raise ValueError("Packet exceeds advertised length")
            elif kind == "END":
                data = bytes(self.pending["bytes"])
                if len(data) != self.pending["length"] or zlib.crc32(data) != int(values["crc"], 16):
                    raise ValueError("Incomplete/corrupt serial packet")
                self.pending.pop("bytes")
                events.append({"type": "reception", **self.pending, "raw": data})
                self.pending = None
        except (KeyError, ValueError, OverflowError) as exc:
            self.pending = None
            events.append({"type": "capture_gap", "reason": str(exc)})
        return events


class AirtimeStats:
    def __init__(self):
        self.counts = Counter()
        self.senders = {}
        self.relays = {}
        self.recent = deque()
        self.seen = OrderedDict()
        self.peak = 0.0

    def add(self, event, now):
        if event["type"] != "reception":
            if event["type"] == "capture_gap":
                self.counts["gaps"] += 1
            return
        self.counts["packets"] += 1
        status = event["decode_status"]
        self.counts["decoded" if status == "decoded_candidate" else "opaque"] += 1
        if event["radio_state"]:
            self.counts["radio_errors"] += 1
        key = (event.get("sender"), event.get("packet_id"), event.get("channel_hash"), event.get("encrypted_hex"))
        duplicate = False
        if event["radio_state"] == 0 and event.get("packet_id"):
            # Preserve every copy; duplicate is just an annotation within ten minutes.
            previous = self.seen.pop(key, None)
            duplicate = previous is not None and now - previous <= 600
            self.seen[key] = now
            while self.seen and (len(self.seen) > 10000 or now - next(iter(self.seen.values())) > 600):
                self.seen.popitem(last=False)
        event["duplicate"] = duplicate
        self.counts["duplicates"] += int(duplicate)
        source = event.get("sender", "unknown/error")
        sender = self.senders.setdefault(source, Counter())
        sender.update(packets=1, airtime_ms=event["airtime_ms"], duplicates=int(duplicate))
        relay = f"0x{event['relay']:02x}" if event.get("hop_start") else "unknown/legacy"
        self.relays.setdefault(relay, Counter()).update(packets=1, airtime_ms=event["airtime_ms"], duplicates=int(duplicate))
        self.recent.append((now, event["airtime_ms"], source))
        self.prune(now)
        self.peak = max(self.peak, sum(ms for _, ms, _ in self.recent) / 600)

    def prune(self, now):
        while self.recent and now - self.recent[0][0] >= 60:
            self.recent.popleft()

    def snapshot(self, now):
        self.prune(now)
        per_source = Counter()
        for _, ms, source in self.recent:
            per_source[source] += ms
        return {**self.counts, "rx_airtime_60s_percent": sum(per_source.values()) / 600,
                "peak_rx_airtime_60s_percent": self.peak,
                "relay_hints": [{"relay_hint": relay, **counts} for relay, counts in
                                sorted(self.relays.items(), key=lambda x: -x[1]["airtime_ms"])],
                "senders": [{"sender": source, **counts, "rx_airtime_60s_percent": per_source[source] / 600}
                            for source, counts in sorted(self.senders.items(), key=lambda x: -x[1]["airtime_ms"])]}


def packet_line(event):
    if event["type"] != "reception":
        return event["type"].upper() + " " + json.dumps({k: v for k, v in event.items() if k != "type"}, ensure_ascii=False)
    duplicate = " DUP" if event.get("duplicate") else ""
    opaque = " raw=" + event["raw_hex"] if event["decode_status"] != "decoded_candidate" else ""
    name = f" ({event['sender_name']})" if event.get("sender_name") else ""
    relay = f"0x{event['relay']:02x}" if event.get("hop_start") else "unknown"
    channel = f"0x{event['channel_hash']:02x}" if "channel_hash" in event else "unknown"
    mqtt = " MQTT-flag" if event.get("via_mqtt") else ""
    return (f"{event.get('received_at', '')} #{event['seq']}{duplicate} {event.get('sender', '?')}{name} → {event.get('to', '?')} "
            f"id={event.get('packet_id', '?')} hash={channel} relay={relay}{mqtt} "
            f"hop={event.get('hop_limit', '?')}/{event.get('hop_start', '?')} "
            f"RSSI={event['rssi_dbm']} SNR={event['snr_db']} {event['airtime_ms']}ms "
            f"{event['summary']}{opaque}")

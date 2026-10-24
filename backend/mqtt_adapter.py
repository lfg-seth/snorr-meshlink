"""Receive-only adapter for encrypted member positions and device telemetry."""
import base64
from datetime import datetime, timezone
import hashlib
import math
import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from google.protobuf.message import DecodeError
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2, telemetry_pb2


class PacketRejected(ValueError):
    """Bounded reason only: never include packet contents or key material."""


def at(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


class Adapter:
    def __init__(self, config):
        self.root = config['root'].rstrip('/')
        self.channel = config['channel']
        self.members = config['members']
        self.infrastructure = config.get('infrastructure', {})
        if set(self.members) & set(self.infrastructure):
            raise ValueError('Member and infrastructure mappings must be disjoint.')
        self.gateways = config['gateways']
        self.key = base64.b64decode(config['channelKey'], validate=True)
        if len(self.key) not in (16, 32):
            raise ValueError('A full private AES-128/256 channel key is required.')
        if not self.channel or '/' in self.channel or any(x in self.channel for x in '#+'):
            raise ValueError('Invalid channel topic segment.')
        if not self.members or not self.gateways:
            raise ValueError('Verified member and gateway mappings are required.')

    def decode(self, topic, payload, received_at, retained=False):
        if retained:
            raise PacketRejected('retained packet')
        if len(payload) > 4096:
            raise PacketRejected('oversize envelope')
        prefix = f'{self.root}/2/e/{self.channel}/'
        if not topic.startswith(prefix) or topic[len(prefix):] not in self.gateways:
            raise PacketRejected('unknown topic/gateway')
        gateway = topic[len(prefix):]
        try:
            envelope = mqtt_pb2.ServiceEnvelope.FromString(payload)
            packet = envelope.packet
            if (not envelope.HasField('packet') or envelope.gateway_id != gateway
                    or envelope.channel_id != self.channel):
                raise PacketRejected('envelope/topic mismatch')
            source = f'!{getattr(packet, "from"):08x}'
            if source not in self.members and source not in self.infrastructure:
                raise PacketRejected('unknown source')
            if not packet.id or packet.pki_encrypted or packet.via_mqtt:
                raise PacketRejected('unsupported packet flags/ID')
            if packet.WhichOneof('payload_variant') != 'encrypted':
                raise PacketRejected('expected channel-encrypted packet')
            nonce = struct.pack('<QI', packet.id, getattr(packet, 'from')) + b'\0' * 4
            plaintext = Cipher(algorithms.AES(self.key), modes.CTR(nonce)).decryptor().update(packet.encrypted)
            data = mesh_pb2.Data.FromString(plaintext)
            if not math.isfinite(received_at):
                raise PacketRejected('invalid receipt time')
            digest = hashlib.sha256(self.channel.encode() + b'\0' + data.SerializeToString()).hexdigest()[:32]
            common = {'gatewayId': self.gateways[gateway], 'packetId': f'{packet.id:08x}:{digest}',
                      'receivedAt': at(received_at)}
            device_id = (self.infrastructure if source in self.infrastructure else self.members)[source]
            if data.portnum == portnums_pb2.PRIVATE_APP:
                if data.payload.startswith(b'SNGH'):
                    if source not in self.gateways or source not in self.infrastructure or len(data.payload) != 32:
                        raise PacketRejected('invalid gateway health provenance/size')
                    magic, version, flags, reserved, observer, boot, sequence, uptime, clock, interval = struct.unpack('<4sBBHIIIIII', data.payload)
                    if version != 1 or flags & ~3 or flags == 2 or reserved or observer != getattr(packet, 'from') or not boot or not sequence or not 180 <= interval <= 2147468:
                        raise PacketRejected('invalid gateway health report')
                    return {**common, 'deviceId': device_id, 'kind': 'gateway-health',
                            'measuredAt': at(clock) if clock >= 1577836800 else None,
                            'data': {'bootId': boot, 'sequence': sequence, 'uptimeSeconds': uptime,
                                     'intervalSeconds': interval, 'wifiConnected': bool(flags & 1),
                                     'mqttConnected': bool(flags & 2)}}
                if not data.payload.startswith(b'SNNS'):
                    return None
                report = self.neighbor_signals(data.payload, getattr(packet, 'from'))
                return {**common, 'deviceId': device_id, 'kind': 'neighbors',
                        'measuredAt': None, 'data': report}
            if data.portnum == portnums_pb2.NEIGHBORINFO_APP:
                report = mesh_pb2.NeighborInfo.FromString(data.payload)
                if report.node_id != getattr(packet, 'from') or len(report.neighbors) > 32:
                    raise PacketRejected('invalid neighbor report provenance/size')
                rows = []
                seen = set()
                for neighbor in report.neighbors:
                    if not neighbor.node_id or neighbor.node_id == report.node_id or neighbor.node_id in seen:
                        raise PacketRejected('invalid neighbor identity')
                    seen.add(neighbor.node_id)
                    if not math.isfinite(neighbor.snr) or not -100 <= neighbor.snr <= 100:
                        raise PacketRejected('invalid neighbor signal')
                    # Scalar SNR is not optional: absent wire zero is ambiguous.
                    present = any(field.name == 'snr' for field, _ in neighbor.ListFields())
                    rows.append(self.neighbor_row(neighbor.node_id, neighbor.snr if present else None, None))
                return {**common, 'deviceId': device_id, 'kind': 'neighbors', 'measuredAt': None,
                        'data': {'reportType': 'neighbor-info', 'observerNodeId': source, 'rows': rows}}
            if data.portnum == portnums_pb2.TELEMETRY_APP:
                telemetry = telemetry_pb2.Telemetry.FromString(data.payload)
                metrics = {}
                if telemetry.HasField('device_metrics') and telemetry.device_metrics.HasField('voltage'):
                    voltage = telemetry.device_metrics.voltage
                    if not math.isfinite(voltage) or not 0 <= voltage <= 100:
                        raise PacketRejected('invalid battery voltage')
                    if voltage > 0:
                        metrics['battery'] = voltage
                if source in self.infrastructure and telemetry.HasField('environment_metrics'):
                    for field, key, low, high in [('temperature', 'temperature', -100, 150),
                                                  ('relative_humidity', 'humidity', 0, 100)]:
                        environment = telemetry.environment_metrics
                        if environment.HasField(field):
                            value = getattr(environment, field)
                            if not math.isfinite(value) or not low <= value <= high:
                                raise PacketRejected('invalid environmental metric')
                            metrics[key] = value
                    for field, key, low, high in [('voltage', 'sensorVoltage', 0, 100),
                                                  ('current', 'sensorCurrentMa', -100000, 100000)]:
                        if environment.HasField(field):
                            value = getattr(environment, field)
                            if not math.isfinite(value) or not low <= value <= high:
                                raise PacketRejected('invalid sensor power metric')
                            metrics[key] = value
                if source in self.infrastructure and telemetry.HasField('power_metrics'):
                    for channel in range(1, 9):
                        for field, suffix, low, high in [('voltage', 'Voltage', 0, 100),
                                                         ('current', 'CurrentMa', -100000, 100000)]:
                            name = f'ch{channel}_{field}'
                            if telemetry.power_metrics.HasField(name):
                                value = getattr(telemetry.power_metrics, name)
                                if not math.isfinite(value) or not low <= value <= high:
                                    raise PacketRejected('invalid channel power metric')
                                metrics[f'power{channel}{suffix}'] = value
                if not metrics:
                    return None
                # Small values observed on R003 are uptime, not Unix timestamps.
                measured = at(telemetry.time) if telemetry.time >= 1577836800 else None
                return {**common, 'deviceId': (self.infrastructure if source in self.infrastructure else self.members)[source], 'kind': 'telemetry',
                        'measuredAt': measured, 'data': metrics}
            if data.portnum != portnums_pb2.POSITION_APP or source not in self.members:
                return None
            position = mesh_pb2.Position.FromString(data.payload)
            if not position.HasField('latitude_i') or not position.HasField('longitude_i'):
                raise PacketRejected('position lacks coordinates')
            latitude, longitude = position.latitude_i / 1e7, position.longitude_i / 1e7
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                raise PacketRejected('invalid coordinates')
            # Position.time is a device/transmit clock. Only timestamp names the
            # GPS solution; never substitute a recent clock for an old fix.
            if abs(position.timestamp_millis_adjust) > 999:
                raise PacketRejected('invalid GPS millisecond adjustment')
            measured = (at(position.timestamp + position.timestamp_millis_adjust / 1000)
                        if position.timestamp else None)
            quality = {}
            # Non-optional protobuf scalars default to zero when absent. Neither
            # absent nor zero means perfect quality or a known satellite count.
            if position.PDOP:
                quality['pdop'] = position.PDOP / 100
            if position.sats_in_view:
                quality['satellites'] = position.sats_in_view
            # Gateway-independent content identity prevents packet-ID reuse from
            # silently discarding a new fix after reboot; exact replays deduplicate.
            return {**common, 'deviceId': self.members[source], 'kind': 'position', 'measuredAt': measured,
                    'data': {'latitude': latitude, 'longitude': longitude, **quality}}
        except (DecodeError, OverflowError, OSError):
            raise PacketRejected('malformed packet') from None

    def neighbor_row(self, node, snr, rssi, **details):
        node_id = f'!{node:08x}'
        mapped = {**self.members, **self.infrastructure, **self.gateways}
        return {'heardDeviceId': mapped.get(node_id), 'heardNodeId': node_id,
                'snrDb': snr, 'rssiDbm': rssi, **details}

    def neighbor_signals(self, payload, sender):
        if len(payload) < 24:
            raise PacketRejected('truncated SNNS header')
        magic, version, flags, count, total, observer, boot, sequence, uptime = struct.unpack_from('<4sBBBBIIII', payload)
        if (version != 1 or flags & ~3 or not 1 <= count <= 8 or not count <= total <= 255
                or len(payload) != 24 + count * 16 or bool(flags & 1) != (total > count)):
            raise PacketRejected('invalid SNNS version/size/flags')
        if observer != sender or not boot or not sequence:
            raise PacketRejected('invalid SNNS provenance')
        rows, seen = [], set()
        for offset in range(24, len(payload), 16):
            node, age, rssi, snr, observations = struct.unpack_from('<IIhhI', payload, offset)
            if not node or node == observer or node in seen:
                raise PacketRejected('invalid SNNS neighbor identity')
            if not 0 <= age < 1800 or not -200 <= rssi < 0 or not -400 <= snr <= 400 or not observations:
                raise PacketRejected('invalid SNNS observation')
            seen.add(node)
            rows.append(self.neighbor_row(node, snr / 4, rssi, hearingAgeSeconds=age,
                                          observationCount=observations))
        return {'reportType': 'snns-v1', 'observerNodeId': f'!{observer:08x}',
                'bootId': boot, 'sequence': sequence, 'reportUptimeSeconds': uptime,
                'subset': bool(flags & 1), 'capacityEvicted': bool(flags & 2),
                'totalNeighbors': total, 'rows': rows}

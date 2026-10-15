"""Receive-only adapter for pinned stock Meshtastic channel-encrypted positions."""
import base64
from datetime import datetime, timezone
import hashlib
import math
import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from google.protobuf.message import DecodeError
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2


class PacketRejected(ValueError):
    """Bounded reason only: never include packet contents or key material."""


def at(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


class Adapter:
    def __init__(self, config):
        self.root = config['root'].rstrip('/')
        self.channel = config['channel']
        self.members = config['members']
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
            if source not in self.members:
                raise PacketRejected('unknown source')
            if not packet.id or packet.pki_encrypted or packet.via_mqtt:
                raise PacketRejected('unsupported packet flags/ID')
            if packet.WhichOneof('payload_variant') != 'encrypted':
                raise PacketRejected('expected channel-encrypted packet')
            nonce = struct.pack('<QI', packet.id, getattr(packet, 'from')) + b'\0' * 4
            plaintext = Cipher(algorithms.AES(self.key), modes.CTR(nonce)).decryptor().update(packet.encrypted)
            data = mesh_pb2.Data.FromString(plaintext)
            if data.portnum != portnums_pb2.POSITION_APP:
                return None  # Other packet kinds are deliberately deferred.
            position = mesh_pb2.Position.FromString(data.payload)
            if not position.HasField('latitude_i') or not position.HasField('longitude_i'):
                raise PacketRejected('position lacks coordinates')
            latitude, longitude = position.latitude_i / 1e7, position.longitude_i / 1e7
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                raise PacketRejected('invalid coordinates')
            if not math.isfinite(received_at):
                raise PacketRejected('invalid receipt time')
            # Position.time is a device/transmit clock. Only timestamp names the
            # GPS solution; never substitute a recent clock for an old fix.
            if abs(position.timestamp_millis_adjust) > 999:
                raise PacketRejected('invalid GPS millisecond adjustment')
            measured = (at(position.timestamp + position.timestamp_millis_adjust / 1000)
                        if position.timestamp else None)
            # Gateway-independent content identity prevents packet-ID reuse from
            # silently discarding a new fix after reboot; exact replays deduplicate.
            digest = hashlib.sha256(self.channel.encode() + b'\0' + data.SerializeToString()).hexdigest()[:32]
            return {'deviceId': self.members[source], 'gatewayId': self.gateways[gateway],
                    'packetId': f'{packet.id:08x}:{digest}', 'kind': 'position',
                    'measuredAt': measured, 'receivedAt': at(received_at),
                    'data': {'latitude': latitude, 'longitude': longitude}}
        except (DecodeError, OverflowError, OSError):
            raise PacketRejected('malformed packet') from None

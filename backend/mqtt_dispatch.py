"""One manual publish on a fresh MQTT 5 session. Never reconnect or queue replies."""
import base64
import json
import os
from pathlib import Path
import ssl
import sys
import time

import paho.mqtt.client as mqtt
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2

from mqtt_adapter import DISPATCH_NODE, TEXT_LIMIT, channel_cipher, channel_hash

HOST = 'mqtt.spp.lol'
ROOT = 'snorr/pilot'
CHANNEL = 'SNORRbench'
TOPIC = f'{ROOT}/2/e/{CHANNEL}/dispatch'


def credentials():
    path = Path(os.environ['CREDENTIALS_DIRECTORY']) / 'dispatch.json'
    return json.loads(path.read_bytes())


def publisher(config, client_id='', reconnect=False):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id,
                         protocol=mqtt.MQTTv5, reconnect_on_failure=reconnect)
    client.username_pw_set('meshlink-dispatch', config['password'])
    client.tls_set_context(ssl.create_default_context())
    client.connect_timeout = 3
    return client


def envelope(key, packet_id, text):
    payload = text.encode('utf-8')
    if not text.strip() or len(payload) > TEXT_LIMIT or '\0' in text:
        raise ValueError('Invalid attributed text.')
    if not 0 < packet_id <= 0xffffffff or len(key) not in (16, 32):
        raise ValueError('Invalid envelope parameters.')
    service = mqtt_pb2.ServiceEnvelope(channel_id=CHANNEL, gateway_id='dispatch')
    packet = service.packet
    setattr(packet, 'from', DISPATCH_NODE)
    packet.to, packet.id = 0xffffffff, packet_id
    packet.hop_limit = packet.hop_start = 1
    packet.channel = channel_hash(CHANNEL, key)
    data = mesh_pb2.Data(portnum=portnums_pb2.TEXT_MESSAGE_APP, payload=payload)
    packet.encrypted = channel_cipher(key, packet).encryptor().update(data.SerializeToString())
    return service.SerializeToString()


def publish(config, request):
    wire = envelope(base64.b64decode(config['channelKey'], validate=True),
                    int(request['packetId'], 16), request['text'])
    expires = request['expiresAt'] / 1000
    if not time.time() < expires <= time.time() + 12:
        return 'not_sent'
    client = publisher(config)
    outcome = 'not_sent'
    acknowledged = False

    def connected(client, userdata, flags, reason, properties):
        nonlocal outcome
        if reason.is_failure or time.time() >= expires:
            client.disconnect()
            return
        # Once publish is attempted, only the matching broker PUBACK can resolve uncertainty.
        outcome = 'unknown'
        props = mqtt.Properties(mqtt.PacketTypes.PUBLISH)
        props.MessageExpiryInterval = max(1, int(expires - time.time()))
        client.publish(TOPIC, wire, qos=1, retain=False, properties=props)

    def puback(client, userdata, mid, reason, properties):
        nonlocal outcome, acknowledged
        outcome = 'rejected' if reason.is_failure else 'broker_accepted'
        acknowledged = True

    client.on_connect, client.on_publish = connected, puback
    try:
        client.connect(HOST, 8883, keepalive=15)
        # Manual loop on this one socket. No background loop, reconnect or replay.
        while not acknowledged and time.time() < expires:
            if client.loop(timeout=.2) != mqtt.MQTT_ERR_SUCCESS:
                break
    except OSError:
        pass
    finally:
        client.disconnect()
    return outcome


if __name__ == '__main__':
    print(publish(credentials(), json.load(sys.stdin)))

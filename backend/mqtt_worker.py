"""Persistent TLS MQTT subscriber. Never publishes or performs radio administration."""
import argparse
import base64
import json
import os
from pathlib import Path
import signal
import sqlite3
import ssl
import threading
import time
import uuid

import paho.mqtt.client as mqtt

from client import ApiError, Client
from mqtt_adapter import Adapter, PacketRejected, at
from mqtt_adapter import G008
import mqtt_dispatch


class Spool:
    """Private durable receipt queue; acknowledge only after the API stores it."""
    def __init__(self, path):
        self.lock = threading.Lock()
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute('CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)')
        self.db.commit()

    def put(self, payload):
        with self.lock, self.db:
            self.db.execute('INSERT INTO queue(payload) VALUES (?)', (json.dumps(payload),))

    def first(self):
        with self.lock:
            row = self.db.execute('SELECT id,payload FROM queue ORDER BY id LIMIT 1').fetchone()
            return (row[0], json.loads(row[1])) if row else None

    def ack(self, receipt_id):
        with self.lock, self.db:
            self.db.execute('DELETE FROM queue WHERE id=?', (receipt_id,))

    def close(self):
        self.db.close()


class Worker:
    def __init__(self, config, api_credentials, spool, dispatch=None):
        self.config, self.secret, self.spool = config, api_credentials, spool
        self.adapter = Adapter(config)
        self.api = Client(config.get('apiUrl', 'http://127.0.0.1:8090'))
        self.authenticated_at = 0
        self.connected = threading.Event()
        self.stopping = threading.Event()
        self.fatal = threading.Event()
        self.counts = {'queued': 0, 'unsupported': 0, 'rejected': 0, 'saved': 0}
        self.dispatch_probe = None
        self.dispatch_connected = threading.Event()
        self.gateway_seen = None
        if dispatch is not None:
            if (config['root'], config['channel'], config['channelKey']) != (
                    mqtt_dispatch.ROOT, mqtt_dispatch.CHANNEL, dispatch['channelKey']):
                raise ValueError('Dispatch channel differs from receiver configuration.')
            self.gateway_key = self.adapter.gateways[G008]
            self.dispatch_probe = mqtt_dispatch.publisher(dispatch, 'meshlink-dispatch-health', reconnect=True)
            self.dispatch_probe.on_connect = self.on_dispatch_connect
            self.dispatch_probe.on_disconnect = lambda *_: self.dispatch_connected.clear()
        self.mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                client_id='meshlink-channel-ingest' if dispatch else 'meshlink-pilot-gps',
                                clean_session=True, manual_ack=True)
        self.mqtt.username_pw_set(config['username'], config['password'])
        self.mqtt.tls_set_context(ssl.create_default_context())
        self.mqtt.reconnect_delay_set(1, 30)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_subscribe = self.on_subscribe
        self.mqtt.on_disconnect = self.on_disconnect
        self.mqtt.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason, properties):
        self.connected.clear()
        if not reason.is_failure:
            client.subscribe(f'{self.adapter.root}/#', qos=1)

    def on_subscribe(self, client, userdata, mid, reasons, properties):
        if reasons and all(not reason.is_failure for reason in reasons):
            self.connected.set()

    def on_disconnect(self, client, userdata, flags, reason, properties):
        self.connected.clear()
        self.gateway_seen = None

    def on_dispatch_connect(self, client, userdata, flags, reason, properties):
        if not reason.is_failure:
            self.dispatch_connected.set()

    def on_message(self, client, userdata, message):
        try:
            received = time.time()
            # Preserve the wire bytes before any filtering or interpretation.
            archive = {
                'receiptId': str(uuid.uuid4()), 'topic': message.topic,
                'receivedAt': at(received), 'qos': int(message.qos),
                'retained': bool(message.retain), 'duplicate': bool(message.dup),
                'payloadBase64': base64.b64encode(message.payload).decode('ascii'),
                'payloadBytes': len(message.payload),
            }
            packet = None
            try:
                packet = self.adapter.decode(message.topic, message.payload, received, message.retain)
                if self.dispatch_probe and packet and packet['gatewayId'] == self.gateway_key:
                    self.gateway_seen = time.monotonic()
                archive['decodeOutcome'] = 'normalized' if packet else 'unsupported'
                if packet is None:
                    self.counts['unsupported'] += 1
            except PacketRejected as error:
                archive['decodeOutcome'] = 'rejected'
                archive['decodeReason'] = str(error)
                self.counts['rejected'] += 1
            except Exception:
                # An unexpected decoder failure must not discard the original.
                archive['decodeOutcome'] = 'error'
                archive['decodeReason'] = 'decoder error'
                self.counts['rejected'] += 1
            if self.dispatch_probe:
                archive['broker'] = mqtt_dispatch.HOST
            self.spool.put({'archive': archive, 'normalized': packet})
            self.counts['queued'] += 1
            # QoS 1/2 acknowledgement follows durable local persistence.
            if message.qos:
                client.ack(message.mid, message.qos)
        except Exception:
            self.connected.clear()
            self.fatal.set()
            client.disconnect()

    def request(self, path, body):
        if time.monotonic() - self.authenticated_at > 2400 or not self.api.token:
            self.api.login(self.secret['username'], self.secret['password'])
            self.authenticated_at = time.monotonic()
        try:
            return self.api.request('POST', path, body)
        except ApiError as error:
            if error.status == 401:
                self.api.token = ''
            raise

    def heartbeat(self):
        connected = self.connected.is_set()
        if self.dispatch_probe:
            seen = self.gateway_seen
            self.request('/api/meshlink/worker/channel-heartbeat', {
                'connected': connected, 'gatewayId': self.gateway_key,
                'ready': connected and self.dispatch_connected.is_set()
                         and seen is not None and time.monotonic() - seen < 420,
            })
        else:
            self.request('/api/meshlink/worker/heartbeat', {'connected': connected})

    def tick(self):
        self.heartbeat()
        # Bound each batch so heartbeats and stop requests remain responsive.
        deadline = time.monotonic() + 5
        for _ in range(20):
            if self.stopping.is_set() or time.monotonic() >= deadline:
                break
            item = self.spool.first()
            if not item:
                break
            queued = item[1]
            if 'archive' in queued:
                # Stable receipt ID makes retries after API commit idempotent.
                self.request('/api/meshlink/worker/archive', queued['archive'])
                packet = queued.get('normalized')
            else:
                packet = queued  # Drain receipts queued by the previous release.
            if packet:
                try:
                    self.request('/api/meshlink/worker/ingest', packet)
                except ApiError as error:
                    # Ingest commits a rejection receipt before returning 400.
                    if error.status != 400:
                        raise
            self.spool.ack(item[0])
            self.counts['saved'] += 1

    def run(self):
        self.mqtt.connect_async(self.config['host'], self.config.get('port', 8883), keepalive=15)
        self.mqtt.loop_start()
        if self.dispatch_probe:
            self.dispatch_probe.connect_async(mqtt_dispatch.HOST, 8883, keepalive=15)
            self.dispatch_probe.loop_start()
        last_report = 0
        try:
            while not self.stopping.is_set():
                if self.fatal.is_set():
                    raise RuntimeError('Private receipt queue failed; worker stopped.')
                try:
                    self.tick()
                except (ApiError, OSError, ValueError):
                    print('API unavailable; queued receipts retained.', flush=True)
                if time.monotonic() - last_report >= 60:
                    print('MQTT subscribed:', self.connected.is_set(), 'counts:', self.counts, flush=True)
                    last_report = time.monotonic()
                self.stopping.wait(3)
        finally:
            self.connected.clear()
            self.mqtt.disconnect()
            self.mqtt.loop_stop()
            if self.dispatch_probe:
                self.dispatch_probe.disconnect()
                self.dispatch_probe.loop_stop()
            try:
                self.heartbeat()
            except Exception:
                pass
            self.spool.close()


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, default=os.environ.get('MESHLINK_MQTT_CONFIG', '/etc/meshlink/mqtt.json'))
    parser.add_argument('--spool', type=Path, default=os.environ.get('MESHLINK_MQTT_SPOOL', '/var/lib/meshlink-worker/receipts.sqlite'))
    parser.add_argument('--channel-overlap', action='store_true')
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    secret = json.loads(Path(os.environ['MESHLINK_WORKER_CREDENTIALS']).read_text())
    dispatch = None
    if args.channel_overlap:
        dispatch = mqtt_dispatch.credentials()
        config.update(host=mqtt_dispatch.HOST, port=8883, sharedMessages=True)
    worker = Worker(config, secret, Spool(args.spool), dispatch)
    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, lambda *_: worker.stopping.set())
    worker.run()


if __name__ == '__main__':
    main()

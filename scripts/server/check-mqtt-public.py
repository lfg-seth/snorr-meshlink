#!/usr/bin/env python3
"""Check public TLS MQTT delivery using server-private credentials, without reset."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import secrets
import socket
import ssl

HOST = 'mqtt.snorr.org'
PORT = 8883
CONNECT_HOST = HOST
CONNECT_PORT = PORT
CREDENTIALS = Path('/root/meshlink-private/mqtt-credentials.json')

# Import only the existing protocol/access-test helpers; its main/reset never runs.
spec = importlib.util.spec_from_file_location(
    'pilot_mqtt_helpers', Path(__file__).with_name('reset-mqtt-pilot.py'))
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
tls_context = ssl.create_default_context()


def connect(username=None, password=None):
    raw = socket.create_connection((CONNECT_HOST, CONNECT_PORT), timeout=10)
    try:
        conn = tls_context.wrap_socket(raw, server_hostname=HOST)
    except Exception:
        raw.close()
        raise
    try:
        flags = 2 if username is None else 0xc2
        body = (helpers.field('MQTT') + bytes([5, flags]) + b'\x00\x1e\x00'
                + helpers.field('snorr-public-check-' + secrets.token_hex(6)))
        if username is not None:
            body += helpers.field(username) + helpers.field(password)
        conn.sendall(helpers.packet(0x10, body))
        kind, reply = helpers.receive(conn)
        if kind != 0x20 or len(reply) < 3:
            raise RuntimeError('Invalid MQTT 5 CONNACK')
        return conn, reply[1]
    except Exception:
        conn.close()
        raise


def main():
    global CONNECT_HOST, CONNECT_PORT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe-only', action='store_true', help='Check TLS/anonymous rejection without credentials')
    parser.add_argument('--connect-host', default=HOST, help='TCP destination, e.g. loopback SSH relay; TLS identity stays mqtt.snorr.org')
    parser.add_argument('--connect-port', type=int, default=PORT)
    args = parser.parse_args()
    CONNECT_HOST, CONNECT_PORT = args.connect_host, args.connect_port
    print('Target: mqtt.snorr.org:8883; TLS certificate/hostname verification enabled.')
    print('TCP connection:', CONNECT_HOST, CONNECT_PORT)
    if args.probe_only:
        conn, code = connect()
        conn.close()
        if code not in (0x86, 0x87):
            raise RuntimeError('Expected MQTT authorization rejection')
        print('PASS: public TLS and anonymous rejection (no credentials read).')
        return
    if os.geteuid() != 0:
        raise RuntimeError('Run with sudo on the broker to read its private credential file')
    credentials = json.loads(CREDENTIALS.read_text())
    users = credentials['accounts']
    if set(users) != {'pilot-v3-uplink-1', 'pilot-v3-uplink-2', 'pilot-worker'}:
        raise RuntimeError('Unexpected pilot account set; no authenticated tests sent')
    if credentials['root'] != 'snorr/pilot':
        raise RuntimeError('Unexpected pilot topic root')
    helpers.connect = connect
    helpers.verify(users, set())
    print('PASS: each V3 account publishes a non-retained synthetic message through public TLS; worker receives it.')
    print('PASS: worker writes, gateway reads, JSON and unrelated-topic writes are denied.')
    print('No broker configuration changed; no passwords printed or retained messages created.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL:', type(error).__name__, str(error))
        raise SystemExit(1)

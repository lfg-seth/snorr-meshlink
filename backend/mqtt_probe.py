"""Read-only live adapter preflight; prints counts and fix ages, never coordinates."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import ssl
import threading
import time

import paho.mqtt.client as mqtt
from mqtt_adapter import Adapter, PacketRejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=150)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    adapter = Adapter(config)
    ready = threading.Event()
    counts, ages = {}, []
    fresh_members = set()
    rejected = 0
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(config['username'], config['password'])
    client.tls_set_context(ssl.create_default_context())

    def connect(client, userdata, flags, reason, properties):
        if not reason.is_failure:
            client.subscribe(f'{adapter.root}/2/e/{adapter.channel}/+', qos=1)

    def subscribed(client, userdata, mid, reasons, properties):
        if reasons and all(not reason.is_failure for reason in reasons):
            ready.set()

    def message(client, userdata, message):
        nonlocal rejected
        try:
            packet = adapter.decode(message.topic, message.payload, time.time(), message.retain)
            if packet and packet['kind'] == 'position':
                pair = packet['deviceId'] + '/' + packet['gatewayId']
                counts[pair] = counts.get(pair, 0) + 1
                if packet['measuredAt']:
                    age = round(time.time() - datetime.fromisoformat(packet['measuredAt']).timestamp(), 2)
                    ages.append(age)
                    if 0 <= age < 900:
                        fresh_members.add(packet['deviceId'])
        except PacketRejected:
            rejected += 1

    client.on_connect, client.on_subscribe, client.on_message = connect, subscribed, message
    client.connect(config['host'], config.get('port', 8883), 15)
    client.loop_start()
    try:
        ready.wait(10)
        print('TLS subscription accepted:', ready.is_set(), flush=True)
        for second in range(args.seconds):
            time.sleep(1)
            if (second + 1) % 30 == 0:
                print('Observed GPS pairs:', counts, 'decode rejections:', rejected, flush=True)
    finally:
        client.disconnect()
        client.loop_stop()
    print(json.dumps({'positionReceiptsByPair': counts, 'fixAgeSeconds': ages,
                      'rejected': rejected, 'seconds': args.seconds}), flush=True)
    expected = {member + '/' + gateway for member in adapter.members.values()
                for gateway in adapter.gateways.values()}
    all_paths = set(counts) == expected and fresh_members == set(adapter.members.values())
    if not all_paths:
        print('Preflight requires fresh GPS from both trackers through both gateways.', flush=True)
        raise SystemExit(2)
    print('Fresh GPS feed verified. Full bench paths verified:', all_paths, flush=True)


if __name__ == '__main__':
    main()

"""Authenticated normalized replay/simulation boundary. No MQTT/radio connection yet."""
import argparse
import json
import time
from pathlib import Path

from client import ApiError, Client
from fixtures import packet
from manage import credentials


def run(once=False, replay=None, interval=5):
    secret = credentials()['worker']
    client = Client()
    client.login(secret['username'], secret['password'])
    authenticated_at = time.monotonic()
    if replay:
        client.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
        # Caller supplies normalized JSONL from ignored local-data/, not raw firmware packets.
        with Path(replay).open() as stream:
            for line in stream:
                if line.strip():
                    client.request('POST', '/api/meshlink/worker/ingest', json.loads(line))
        return
    try:
        tick = 0
        while True:
            if time.monotonic() - authenticated_at > 2400:
                client.login(secret['username'], secret['password'])
                authenticated_at = time.monotonic()
            heartbeat = client.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
            if not heartbeat['feedOnline']:
                if once:
                    print('Simulated feed outage: observations left unchanged.')
                    return
                time.sleep(interval)
                continue
            # Only demo trackers 1–3 progress; others retain stale/unknown/never-seen states.
            for i, longitude, latitude in [(1, -115.633, 36.265), (2, -115.650, 36.274), (3, -115.662, 36.281)]:
                client.request('POST', '/api/meshlink/worker/ingest', packet(f'd{i}', 'position', {
                    'longitude': longitude + (tick % 20) * .0001, 'latitude': latitude,
                    'battery': 80 - i * 5,
                }))
            client.request('POST', '/api/meshlink/worker/ingest', packet('r1', 'telemetry', {
                'battery': 3.58, 'temperature': 8.4, 'solar': 1.2, 'intrusion': False,
            }))
            print('Simulation heartbeat and 4 normalized observations saved.', flush=True)
            if once:
                return
            tick += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        client.request('POST', '/api/meshlink/worker/heartbeat', {'connected': False})
    except ApiError as error:
        if error.status == 401:
            print('Worker token expired. Restart to authenticate again; no unsent radio actions exist.')
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--replay', help='Normalized packet JSONL file in private/local-data storage')
    args = parser.parse_args()
    run(args.once, args.replay)

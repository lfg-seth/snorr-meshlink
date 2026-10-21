"""Authenticated normalized replay/simulation boundary. No MQTT/radio connection yet."""
import argparse
import json
import os
import time
from datetime import datetime, timezone
from contextlib import closing
import sqlite3
from pathlib import Path

from client import ApiError, Client
from fixtures import packet
from demo_scenario import telemetry
from manage import credentials


def run(once=False, replay=None, interval=5):
    # Hosted workers receive only their own credential, under a separate OS user.
    credential_file = os.environ.get('MESHLINK_WORKER_CREDENTIALS')
    secret = (json.loads(Path(credential_file).read_text()) if credential_file
              else credentials()['worker'])
    client = Client(os.environ.get('MESHLINK_API_URL', 'http://127.0.0.1:8090'))
    client.login(secret['username'], secret['password'])
    # Read only the explicitly marked, local demo's saved scenario clock. This
    # does not touch a live database, and survives demo-worker restarts.
    reference = datetime.now(timezone.utc)
    demo_data = Path(credential_file).parent / 'pb_data' / 'data.db' if credential_file else None
    if demo_data and demo_data.is_file():
        with closing(sqlite3.connect(f'{demo_data.resolve().as_uri()}?mode=ro', uri=True)) as database:
            marker = database.execute("SELECT name FROM sqlite_master WHERE name='meshlink_demo_marker'").fetchone()
            if marker and database.execute('SELECT kind FROM meshlink_demo_marker').fetchall() == [('synthetic-only',)]:
                row = database.execute("SELECT configuration FROM devices WHERE key='r1'").fetchone()
                saved = json.loads(row[0]).get('demoBatteryReference') if row else None
                if saved:
                    reference = datetime.fromisoformat(saved)
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
                    'battery': 100 if i == 1 else 80 - i * 5,
                    'pdop': [1.5, 3.5, 7][i - 1], 'satellites': [12, 8, 5][i - 1],
                }))
            measured = datetime.now(timezone.utc)
            for device_id in ['d1', 'd2', 'd3', 'r1', 'r2', 'b1']:
                data = telemetry(device_id, measured, reference)
                client.request('POST', '/api/meshlink/worker/ingest', packet(device_id, 'telemetry', data))
            print('Simulation heartbeat and 9 normalized observations saved.', flush=True)
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

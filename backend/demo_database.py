"""Build a synthetic Git checkpoint, then run a separate writable demo copy."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import sqlite3
import subprocess
import tempfile

import manage as backend_manage
from client import Client
from fixtures import DEVICES, initial_packets, provision, at, packet
from demo_power import seed_history
from demo_scenario import configurations, telemetry, neighbor_packets

ROOT, BACKEND, BINARY = backend_manage.ROOT, backend_manage.BACKEND, backend_manage.BINARY
SEED = BACKEND / 'demo'
LOCAL = ROOT / 'local-data' / 'demo'
CREDENTIALS = LOCAL / 'credentials.json'
API_PORT = 8092
DEMO_PASSWORD = 'fictional-demo-only-password'


def demo_credentials():
    # Deliberately public, synthetic accounts; never reuse these on production.
    return {key: {'username': f'meshlink-{key}', 'password': DEMO_PASSWORD}
            for key in ['admin', 'member', 'member2', 'worker', 'superuser']}


def command(data_dir=None):
    return backend_manage.command(data_dir or LOCAL / 'pb_data')


def links():
    """Illustrative directional observations, including missing and zero values."""
    for observer, heard, origin, source, path, snr, rssi, received_age, observed_age in [
        ('b1', 'd1', 'd1', 'gateway', 'direct', 9.5, -88, 1, 1),
        ('b2', 'd1', 'd1', 'gateway', 'direct', 4.25, -103, 1, 1),
        ('b1', 'r1', 'd2', 'gateway', 'relayed', 7.0, -94, 2, 2),
        ('b2', None, 'd3', 'gateway', 'relayed', -4.5, -119, 3, 3),
        ('b1', 'd4', 'd4', 'gateway', 'direct', 0, -112, 24, 24),
        ('b2', 'd2', 'd2', 'gateway', 'direct', None, None, 5, None),
        ('r1', 'd1', None, 'neighbor', 'direct', 8.0, None, 8, None),
        ('r1', 'r2', None, 'neighbor', 'direct', -1.75, None, 8, None),
        ('r2', 'r1', None, 'neighbor', 'direct', 2.5, None, 75, None),
        ('r2', 'd3', None, 'neighbor', 'direct', 0, None, 75, None),
    ]:
        yield {'observerDeviceId': observer, 'heardDeviceId': heard,
               'originalSourceDeviceId': origin, 'source': source, 'path': path,
               'signal': {'snrDb': snr, 'rssiDbm': rssi},
               'receivedAt': at(received_age),
               'observedAt': at(observed_age) if observed_age is not None else None}


def build():
    """Generate only from fictional fixtures in a new disposable database."""
    reference = datetime.now(timezone.utc)
    with tempfile.TemporaryDirectory(prefix='meshlink-demo-seed-') as temporary:
        directory = Path(temporary)
        data = directory / 'pb_data'
        credentials = demo_credentials()
        subprocess.run(command(data) + ['migrate', 'up'], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(command(data) + ['superuser', 'upsert', '--',
            'demo-admin@example.invalid', DEMO_PASSWORD], check=True, stdout=subprocess.DEVNULL)
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        with (directory / 'build.log').open('w') as log:
            process = backend_manage.start(data, port, log)
            try:
                url = f'http://127.0.0.1:{port}'
                backend_manage.wait_ready(url, process)
                owner = Client(url)
                owner.login('demo-admin@example.invalid', DEMO_PASSWORD, '_superusers')
                provision(owner, credentials)
                devices = owner.request('GET', '/api/collections/devices/records')['items']
                for key, config in configurations():
                    device = next(d for d in devices if d['key'] == key)
                    owner.request('PATCH', f'/api/collections/devices/records/{device["id"]}',
                                  {'configuration': {**device['configuration'], **config}})
                # Match the original browser demo's member map labels. Radio
                # short names remain device identities (S001, S002, ...).
                for member in owner.request('GET', '/api/collections/members/records')['items']:
                    short_name = {'m1': 'AVERY', 'm2': 'JORD', 'm3': 'MORG',
                                  'm4': 'RILEY', 'm5': 'CASEY'}[member['key']]
                    owner.request('PATCH', f'/api/collections/members/records/{member["id"]}',
                                  {'shortName': short_name})
                # The seed is visibly identified independently of any environment flag.
                with closing(sqlite3.connect(data / 'data.db')) as database:
                    database.execute('CREATE TABLE meshlink_demo_marker (kind TEXT NOT NULL)')
                    database.execute("INSERT INTO meshlink_demo_marker VALUES ('synthetic-only')")
                    database.commit()
                worker = Client(url)
                worker.login(credentials['worker']['username'], DEMO_PASSWORD)
                worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
                for item in initial_packets():
                    if item['kind'] == 'position':
                        index = int(item['deviceId'][1:])
                        if index <= 3:
                            item['data'].update(pdop=[1.5, 3.5, 7][index - 1], satellites=[12, 8, 5][index - 1])
                        if index == 1:
                            item['data']['battery'] = 100
                    worker.request('POST', '/api/meshlink/worker/ingest', item)
                for key, age in [('d1', 1), ('d2', 3), ('d3', 8), ('d4', 17),
                                 ('r1', 2), ('r2', 22), ('b1', 1)]:
                    worker.request('POST', '/api/meshlink/worker/ingest',
                                   packet(key, 'telemetry', telemetry(key, reference, reference), age))
                for row in links():
                    owner.request('POST', '/api/collections/link_observations/records', row)
                for item in neighbor_packets():
                    worker.request('POST', '/api/meshlink/worker/ingest', item)
            finally:
                process.terminate()
                process.wait(timeout=10)
        SEED.mkdir(parents=True, exist_ok=True)
        seed_history(data / 'data.db', reference)
        target = SEED / 'data.db'
        with closing(sqlite3.connect(data / 'data.db')) as source, closing(sqlite3.connect(directory / 'checkpoint.db')) as checkpoint:
            source.backup(checkpoint)
            checkpoint.execute('PRAGMA journal_mode=DELETE')
            checkpoint.execute('VACUUM')
        staged = SEED / 'data.db.tmp'
        shutil.copyfile(directory / 'checkpoint.db', staged)
        os.replace(staged, target)
        manifest = {'format': 1, 'kind': 'synthetic-only', 'referenceTime': reference.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
                    'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                    'pocketbaseVersion': json.loads((BACKEND / 'pocketbase-release.json').read_text())['version']}
        (SEED / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Built backend/demo/data.db using fictional fixtures only.')


def initialize(local=None):
    destination = local or LOCAL
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Existing demo runtime found; kept its database and saved edits. Use a new --dir for a fresh copy.')
    manifest = json.loads((SEED / 'manifest.json').read_text())
    seed = SEED / 'data.db'
    if manifest['kind'] != 'synthetic-only' or hashlib.sha256(seed.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Demo seed verification failed; no runtime was initialized.')
    with closing(sqlite3.connect(f'{seed.as_uri()}?mode=ro', uri=True)) as source:
        if source.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('Demo database integrity check failed.')
        if source.execute('SELECT kind FROM meshlink_demo_marker').fetchall() != [('synthetic-only',)]:
            raise ValueError('The source is not a synthetic demo checkpoint.')
        if set(row[0] for row in source.execute('SELECT key FROM devices')) != {d['key'] for d in DEVICES}:
            raise ValueError('Unexpected devices in demo checkpoint.')
        destination.mkdir(parents=True, mode=0o700, exist_ok=True)
        (destination / 'pb_data').mkdir()
        with closing(sqlite3.connect(destination / 'pb_data' / 'data.db')) as runtime:
            source.backup(runtime)
            # Rebase the saved scenario once, in the DB; browser values are never fabricated.
            delta = datetime.now(timezone.utc) - datetime.fromisoformat(manifest['referenceTime'])
            pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z')
            tables = ['devices', 'assignments', 'positions', 'packet_receipts', 'observations',
                      'messages', 'send_attempts', 'name_jobs', 'incidents', 'warnings', 'events', 'feed', 'link_observations']
            for table in tables:
                columns = [row[1] for row in runtime.execute(f'PRAGMA table_info("{table}")')]
                for row in runtime.execute(f'SELECT * FROM "{table}"').fetchall():
                    updates = {}
                    for column, value in zip(columns, row):
                        if isinstance(value, str) and pattern.search(value):
                            updates[column] = pattern.sub(lambda m: (datetime.fromisoformat(m[0]) + delta)
                                .isoformat(timespec='milliseconds').replace('+00:00', 'Z'), value)
                    if updates:
                        runtime.execute(f'UPDATE "{table}" SET ' + ','.join(f'"{key}"=?' for key in updates) + ' WHERE id=?',
                                        [*updates.values(), row[columns.index('id')]])
            runtime.commit()
            runtime.execute('PRAGMA journal_mode=DELETE')
    (destination / 'credentials.json').write_text(json.dumps(demo_credentials(), indent=2) + '\n')
    (destination / 'worker.json').write_text(json.dumps(demo_credentials()['worker']) + '\n')
    for file in ['credentials.json', 'worker.json']:
        (destination / file).chmod(0o600)
    print(f'Initialized separate synthetic demo at {destination}. Production was not accessed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'init', 'serve'])
    parser.add_argument('--dir', type=Path, help='New demo runtime directory for init only')
    args = parser.parse_args()
    if args.action == 'build':
        build()
    elif args.action == 'init':
        initialize(args.dir)
    else:
        if not (LOCAL / 'pb_data' / 'data.db').exists():
            raise ValueError('Run python3 backend/demo_database.py init first.')
        process = backend_manage.start(LOCAL / 'pb_data', API_PORT)
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            process.wait(timeout=10)


if __name__ == '__main__':
    main()

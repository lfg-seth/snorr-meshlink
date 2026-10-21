#!/usr/bin/env python3
"""Verify hosted demo separation and restore its latest backup in isolation."""
import hashlib
from contextlib import closing
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request

sys.path.insert(0, '/opt/meshlink/backend')
from client import Client

PASSWORD = 'fictional-demo-only-password'


def status(client, path):
    request = urllib.request.Request(client.url + path,
        headers={'Authorization': client.token} if client.token else {})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def main():
    proxy = Client('http://127.0.0.1:8080/demo-api')
    assert status(proxy, '/api/health') == 200
    assert status(proxy, '/api/meshlink/state') == 401
    for path in ['/_/', '/api/settings', '/api/collections/devices/records',
                 '/api/collections/_superusers/auth-with-password',
                 '/api/meshlink/worker/heartbeat', '/api/meshlink/worker/ingest']:
        assert status(proxy, path) == 404, path
    proxy.login('meshlink-admin', PASSWORD)
    state = proxy.request('GET', '/api/meshlink/state')
    assert state['simulation'] is True and state['feedOnline'] is True
    assert len(state['trackers']) == 6 and len(state['infrastructure']) == 4
    assert len(state['links']) >= 10  # Saved workspaces may retain older examples or add reports.
    for hours in [24, 168, 720]:
        history = proxy.request('GET', f'/api/meshlink/battery-history/r1?hours={hours}')
        assert history['samples'] and history['truncated'] is False
    # Tokens are signed by separate databases, even for matching account names.
    live = Client('http://127.0.0.1:8080')
    live.token = proxy.token
    assert status(live, '/api/meshlink/state') == 401
    for path in ['/var/lib/meshlink/pb_data/data.db', '/etc/meshlink/mqtt.json',
                 '/etc/meshlink/worker.json']:
        assert subprocess.run(['runuser', '-u', 'meshlink-demo', '--', 'test', '-r', path]).returncode != 0
    print('Separate demo proxy, authentication, history, feed and live-state isolation: PASS')

    backup = sorted(Path('/var/backups/meshlink').glob('meshlink-*.tar.gz'))[-1]
    with backup.open('rb') as file:
        assert hashlib.file_digest(file, 'sha256').hexdigest() == backup.with_suffix('.sha256').read_text().split()[0]
    with tempfile.TemporaryDirectory(prefix='meshlink-demo-restore-', dir='/root') as temporary:
        root = Path(temporary)
        with tarfile.open(backup) as archive:
            members = [item for item in archive.getmembers() if any(
                item.name == prefix or item.name.startswith(prefix + '/')
                for prefix in ['demo-state', 'demo-bin', 'release/backend'])]
            archive.extractall(root, members=members, filter='data')
        data = root / 'demo-state/pb_data'
        with closing(sqlite3.connect(data / 'data.db')) as database:
            assert database.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
            assert database.execute('SELECT kind FROM meshlink_demo_marker').fetchall() == [('synthetic-only',)]
            counts = {name: database.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0]
                      for name in ['accounts', 'members', 'assignments', 'devices', 'link_observations', 'observations']}
            assert counts['observations'] > 17000 and counts['link_observations'] >= 10
        backend = root / 'release/backend'
        with (root / 'restore.log').open('w') as log:
            process = subprocess.Popen([
                str(root / 'demo-bin/pocketbase'), f'--dir={data}',
                f'--hooksDir={backend / "pb_hooks"}', f'--migrationsDir={backend / "pb_migrations"}',
                '--automigrate=false', '--hooksWatch=false', 'serve', '--http=127.0.0.1:18092'],
                env={**os.environ, 'MESHLINK_SIMULATION': '1'}, stdout=log, stderr=log)
            try:
                restored = Client('http://127.0.0.1:18092')
                for _ in range(100):
                    if process.poll() is not None:
                        raise RuntimeError('Restored demo API failed; inspect restore privately.')
                    try:
                        if status(restored, '/api/health') == 200:
                            break
                    except urllib.error.URLError:
                        pass
                    time.sleep(.1)
                else:
                    raise RuntimeError('Restored demo API did not become ready.')
                restored.login('meshlink-admin', PASSWORD)
                snapshot = restored.request('GET', '/api/meshlink/state')
                assert snapshot['simulation'] is True
                assert len(snapshot['trackers']) + len(snapshot['infrastructure']) == counts['devices']
                assert len(snapshot['members']) == counts['members']
                assert len(snapshot['links']) == counts['link_observations']
                history = restored.request('GET', '/api/meshlink/battery-history/r1?hours=720')
                end = datetime.now(timezone.utc)
                cutoff = (end - timedelta(hours=720)).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
                with closing(sqlite3.connect(data / 'data.db')) as database:
                    expected = [{'at': at, 'volts': volts} for at, volts in database.execute(
                        "SELECT measuredAt, json_extract(payload, '$.battery') FROM observations "
                        "WHERE deviceId='r1' AND measuredAt >= ? AND measuredAt <= ? "
                        "AND json_extract(payload, '$.battery') > 0 ORDER BY measuredAt, id",
                        (cutoff, end.isoformat(timespec='milliseconds').replace('+00:00', 'Z')))]
                assert expected and history['samples'] == expected and history['truncated'] is False
            finally:
                process.terminate()
                process.wait(timeout=10)
    print('Synthetic database checksum/integrity, saved history and isolated demo API recovery: PASS')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Check deployment boundaries and restore the latest backup into an isolated API."""
import json
import hashlib
import argparse
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


def status(base, path):
    try:
        with urllib.request.urlopen(base + path, timeout=10) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--public', action='store_true', help='Also test HTTPS through Cloudflare using public DNS')
    args = parser.parse_args()
    proxy = 'http://127.0.0.1:8080'
    # systemd start confirms process launch, not HTTP readiness after a backup.
    for attempt in range(100):
        try:
            if status(proxy, '/api/health') == 200:
                break
        except urllib.error.URLError:
            pass
        time.sleep(.1)
    else:
        raise RuntimeError('API did not become ready after service restart.')
    for path, expected in [('/', 200), ('/map', 200), ('/api/health', 200),
                           ('/api/meshlink/state', 401), ('/_/', 404),
                           ('/api/settings', 404),
                           ('/api/collections/_superusers/auth-with-password', 404),
                           ('/api/collections/devices/records', 404),
                           ('/api/meshlink/worker/heartbeat', 404)]:
        assert status(proxy, path) == expected, path
    secrets = json.loads(Path('/var/lib/meshlink/credentials.json').read_text())
    client = Client(proxy)
    client.login(secrets['admin']['username'], secrets['admin']['password'])
    live = client.request('GET', '/api/meshlink/state')
    simulation = live['simulation']
    if not simulation:
        with urllib.request.urlopen(proxy + '/', timeout=10) as response:
            html = response.read().decode()
        assert '<meta name="meshlink-portal-mode" content="live">' in html, 'Live backend is serving a frontend without verified live mode'
        print('Hosted frontend declares live mode: PASS')
    assert len(live['trackers']) == (6 if simulation else 2)
    # Respect the enabled 2-auth-requests/3-second policy; the worker can log in too.
    time.sleep(3.1)
    if simulation:
        member = Client(proxy)
        member.login(secrets['member']['username'], secrets['member']['password'])
        assert member.request('GET', '/api/meshlink/state')['account']['role'] == 'member'
    else:
        assert {d['id'] for d in live['trackers']} == {'b001', 'b002'}
        infrastructure = {'g001', 'g002'}
        repeaters = Path('/etc/meshlink/repeaters.json')
        if repeaters.exists():
            infrastructure.update(d['key'] for d in json.loads(repeaters.read_text())['devices'])
        assert {d['id'] for d in live['infrastructure']} == infrastructure
        assert not live['members']
    print('Proxy, protected routes and sign-in: PASS')

    # The loopback proxy trusts only CF-Connecting-IP. Public callers cannot
    # supply this header themselves because Cloudflare replaces it.
    def bad_login(ip):
        request = urllib.request.Request(proxy + '/api/collections/accounts/auth-with-password',
            data=json.dumps({'identity': 'nonexistent-verification-user', 'password': 'invalid'}).encode(),
            headers={'Content-Type': 'application/json', 'CF-Connecting-IP': ip})
        try:
            urllib.request.urlopen(request, timeout=10).close()
            return 200
        except urllib.error.HTTPError as error:
            return error.code
    assert [bad_login('198.51.100.12') for _ in range(3)] == [400, 400, 429]
    assert bad_login('198.51.100.13') == 400
    print('Per-client authentication throttling through the trusted proxy: PASS')

    if args.public:
        # Keep TLS hostname/certificate verification intact. Resolve just this
        # hostname through public DNS while the LAN resolver caches an old NXDOMAIN.
        dns_request = urllib.request.Request(
            'https://cloudflare-dns.com/dns-query?name=meshlink.spp.lol&type=A',
            headers={'Accept': 'application/dns-json'})
        with urllib.request.urlopen(dns_request, timeout=10) as response:
            answers = json.load(response)['Answer']
        address = next(item['data'] for item in answers if item['type'] == 1)
        # Cloudflare currently blocks Python's default user-agent. Use curl for
        # these ordinary probes; do not change edge protections. No credentials.
        for path, expected in [('/', 200), ('/api/health', 200),
                               ('/api/meshlink/state', 401), ('/_/', 404)]:
            result = subprocess.check_output([
                'curl', '--resolve', f'meshlink.spp.lol:443:{address}',
                '--silent', '--show-error', '--output', '/dev/null',
                '--write-out', '%{http_code}', 'https://meshlink.spp.lol' + path], text=True)
            assert int(result) == expected, (path, result)
        print('Cloudflare HTTPS, certificate verification and protected public routes: PASS')

    backup = sorted(Path('/var/backups/meshlink').glob('meshlink-*.tar.gz'))[-1]
    expected_digest = backup.with_suffix('.sha256').read_text().split()[0]
    with backup.open('rb') as file:
        assert hashlib.file_digest(file, 'sha256').hexdigest() == expected_digest
    with tempfile.TemporaryDirectory(prefix='meshlink-restore-', dir='/root') as temporary:
        root = Path(temporary)
        with tarfile.open(backup) as archive:
            archive.extractall(root, filter='data')
        state = root / 'state'
        with sqlite3.connect(state / 'pb_data/data.db') as database:
            assert database.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
            # Preserve complete histories and account/assignment records, not just pins.
            counts = {table: database.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                      for table in ['accounts', 'devices', 'members', 'assignments',
                                    'positions', 'observations', 'packet_receipts',
                                    'messages', 'incidents', 'events']}
            if database.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='mqtt_archive'").fetchone():
                counts['mqtt_archive'] = database.execute('SELECT COUNT(*) FROM mqtt_archive').fetchone()[0]
            if database.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='link_observations'").fetchone():
                counts['link_observations'] = database.execute('SELECT COUNT(*) FROM link_observations').fetchone()[0]
            with sqlite3.connect('file:/var/lib/meshlink/pb_data/data.db?mode=ro', uri=True) as current:
                account_count = current.execute('SELECT COUNT(*) FROM accounts').fetchone()[0]
            assert counts['accounts'] == account_count
            assert counts['devices'] == len(live['trackers']) + len(live['infrastructure'])
            assert counts['positions'] > 0 and counts['packet_receipts'] > 0
        restored_secret = json.loads((state / 'credentials.json').read_text())
        assert restored_secret == secrets
        backend = root / 'release/backend'
        with (root / 'restore.log').open('w') as log:
            process = subprocess.Popen([
                str(state / 'bin/pocketbase'), f'--dir={state / "pb_data"}',
                f'--hooksDir={backend / "pb_hooks"}',
                f'--migrationsDir={backend / "pb_migrations"}',
                '--automigrate=false', '--hooksWatch=false',
                'serve', '--http=127.0.0.1:18090'],
                env={**os.environ, 'MESHLINK_SIMULATION': '1' if simulation else '0'}, stdout=log, stderr=log)
            try:
                restored = Client('http://127.0.0.1:18090')
                for _ in range(100):
                    if process.poll() is not None:
                        raise RuntimeError('Restored API failed; inspect restore privately.')
                    try:
                        restored.request('GET', '/api/health')
                        break
                    except urllib.error.URLError:
                        time.sleep(.1)
                else:
                    raise RuntimeError('Restored API did not become ready.')
                restored.login(restored_secret['admin']['username'], restored_secret['admin']['password'])
                snapshot = restored.request('GET', '/api/meshlink/state')
                assert snapshot['simulation'] == simulation
                assert snapshot['trackers'] and snapshot['members'] == live['members']
                assert snapshot['assignments'] == live['assignments']
                assert snapshot['messages'] == live['messages']
                assert snapshot['incidents'] == live['incidents']
                assert snapshot['events'] == live['events']
                print('Isolated database integrity, credentials, assignments, history and API restore: PASS')
                print(json.dumps({'restoredRecordCounts': counts}))
            finally:
                process.terminate()
                process.wait(timeout=20)


if __name__ == '__main__':
    main()

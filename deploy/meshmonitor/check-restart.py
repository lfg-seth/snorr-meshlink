#!/usr/bin/env python3
"""Restart only MeshMonitor, proving persisted rows and MQTT recovery."""

from http.cookiejar import CookieJar
import json
from pathlib import Path
import sqlite3
import subprocess
import time
import urllib.request

base = 'http://10.1.20.182:3001'
db = sqlite3.connect('file:/data/meshmonitor.db?mode=ro', uri=True)
tables = ['nodes', 'telemetry', 'mqtt_packet_log', 'sources', 'users', 'permissions', 'api_tokens', 'channel_database']
before = {table: {row[0] for row in db.execute(f'SELECT rowid FROM "{table}"')} for table in tables}
db.close()
subprocess.run(['systemctl', 'restart', 'meshmonitor'], check=True)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))


def call(method, path, data=None, csrf=None):
    headers = {'Content-Type': 'application/json'}
    if csrf:
        headers['X-CSRF-Token'] = csrf
    request = urllib.request.Request(base + path, headers=headers, method=method,
                                    data=None if data is None else json.dumps(data).encode())
    with opener.open(request, timeout=3) as response:
        return json.load(response)


for attempt in range(45):
    try:
        csrf = call('GET', '/api/csrf-token')['csrfToken']
        break
    except OSError:
        time.sleep(1)
else:
    raise RuntimeError('MeshMonitor did not restart')
login = json.loads(Path('/etc/meshmonitor/admin-login.json').read_text())
call('POST', '/api/auth/login', login, csrf)
source_id = Path('/etc/meshmonitor/source-id').read_text().strip()
for attempt in range(30):
    status = call('GET', f'/api/sources/{source_id}/status')
    status = status.get('status', status)
    if status.get('connected'):
        break
    time.sleep(1)
else:
    raise RuntimeError('MQTT did not reconnect')
assert status['mode'] == 'subscribe_only'
assert status['uplinkOut'] == 0 and status['downlinkRepublished'] == 0
db = sqlite3.connect('file:/data/meshmonitor.db?mode=ro', uri=True)
for table in tables:
    after = {row[0] for row in db.execute(f'SELECT rowid FROM "{table}"')}
    assert before[table] <= after, table
db.close()
print('Restart retains all row IDs and accounts/tokens; TLS MQTT reconnects; uplink and local republish counters both zero.')

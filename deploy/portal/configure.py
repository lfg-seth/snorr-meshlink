#!/usr/bin/env python3
"""Configure proxy handling privately via the loopback superuser API."""
import json
import grp
import os
from pathlib import Path
import sys

sys.path.insert(0, '/opt/meshlink/backend')
from client import Client

secrets = json.loads(Path('/var/lib/meshlink/credentials.json').read_text())
secret = secrets['superuser']
client = Client()
client.login('bootstrap@example.invalid', secret['password'], '_superusers')
settings = client.request('GET', '/api/settings')
meta = {**settings['meta'], 'appURL': 'https://meshlink.spp.lol'}
client.request('PATCH', '/api/settings', {
    'trustedProxy': {'headers': ['X-Real-IP'], 'useLeftmostIP': False},
    'meta': meta,
})
worker_path = Path('/etc/meshlink/worker.json')
# Write the credential privately before granting the worker group read access.
with os.fdopen(os.open(worker_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), 'w') as file:
    os.fchmod(file.fileno(), 0o600)
    json.dump(secrets['worker'], file)
os.chown(worker_path, 0, grp.getgrnam('meshlink-worker').gr_gid)
worker_path.chmod(0o640)
print('Public app URL and trusted proxy client IP configured; rate limits remain enabled.')

#!/usr/bin/env python3
"""Restore a private backup, compare retained rows, and boot with all sources disabled."""

import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
import time
import urllib.request

tables = ['nodes', 'telemetry', 'mqtt_packet_log', 'sources', 'users', 'permissions', 'api_tokens', 'settings', 'channel_database']
subprocess.run(['systemctl', 'start', 'meshmonitor-backup'], check=True)
archive = sorted(Path('/var/backups/meshmonitor').glob('meshmonitor-*.tar.gz'))[-1]
with tempfile.TemporaryDirectory(prefix='meshmonitor-restore-', dir='/data') as temporary:
    root = Path(temporary)
    with tarfile.open(archive) as backup:
        backup.extractall(root, filter='data')
        original = backup.extractfile('data/meshmonitor.db').read()
    restored = root / 'data/meshmonitor.db'
    assert hashlib.sha256(original).digest() == hashlib.sha256(restored.read_bytes()).digest()
    db = sqlite3.connect(restored)
    assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    counts = {table: db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] for table in tables}
    assert counts['nodes'] > 0 and counts['mqtt_packet_log'] > 0
    # Preserve a pre-boot restore digest; disable only the disposable copy's sources.
    db.execute('UPDATE sources SET enabled=0')
    db.commit()
    db.close()
    account = pwd.getpwnam('meshmonitor')
    for path in [root, *root.rglob('*')]:
        os.chown(path, account.pw_uid, account.pw_gid)
    env = dict(os.environ)
    env.update(dict(line.split('=', 1) for line in (root / 'etc/meshmonitor/meshmonitor.env').read_text().splitlines() if '=' in line))
    env.update(DATABASE_PATH=str(restored), PORT='3002', MESHLINK_BIND_ADDRESS='127.0.0.1')
    log = open('/root/meshmonitor-install/restore-check.log', 'wb')
    process = subprocess.Popen(['/opt/meshmonitor-runtime/node', 'dist/server/server.js'],
                               cwd='/opt/meshmonitor', env=env, stdout=log, stderr=log,
                               user=account.pw_uid, group=account.pw_gid)
    try:
        for attempt in range(45):
            if process.poll() is not None:
                raise RuntimeError('Isolated restore process exited; inspect private log')
            try:
                with urllib.request.urlopen('http://127.0.0.1:3002/api/auth/status', timeout=2) as response:
                    status = json.load(response)
                assert status['anonymousDisabled'] is True
                break
            except OSError:
                time.sleep(1)
        else:
            raise RuntimeError('Isolated restore never became ready')
        db = sqlite3.connect(restored)
        for table in ['nodes', 'telemetry', 'mqtt_packet_log', 'users', 'permissions', 'api_tokens', 'channel_database']:
            assert db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] == counts[table]
        assert db.execute('SELECT count(*) FROM sources WHERE enabled=1').fetchone()[0] == 0
        db.close()
        print('Isolated restored application boots with zero enabled sources; retained row counts match:', counts)
    finally:
        process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        log.close()

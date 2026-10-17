#!/usr/bin/env python3
"""Consistent root-private SQLite/config backup; no automatic history pruning."""

from datetime import datetime, timezone
from pathlib import Path
import os
import sqlite3
import tarfile
import tempfile

os.umask(0o077)
destination = Path('/var/backups/meshmonitor')
destination.mkdir(parents=True, exist_ok=True, mode=0o700)
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
with tempfile.TemporaryDirectory(prefix='meshmonitor-backup-') as directory:
    snapshot = Path(directory) / 'meshmonitor.db'
    with sqlite3.connect('file:/data/meshmonitor.db?mode=ro', uri=True) as source:
        with sqlite3.connect(snapshot) as target:
            source.backup(target)
            assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    output = destination / f'meshmonitor-{stamp}.tar.gz'
    with tarfile.open(output, 'w:gz') as archive:
        archive.add(snapshot, arcname='data/meshmonitor.db')
        archive.add('/etc/meshmonitor', arcname='etc/meshmonitor')
        archive.add('/etc/systemd/system/meshmonitor.service', arcname='meshmonitor.service')
        archive.add('/root/meshmonitor-install/config', arcname='deployment')
# Archive rotation only. Never deletes MeshMonitor observations or portal data.
for old in sorted(destination.glob('meshmonitor-*.tar.gz'))[:-14]:
    old.unlink()
print(f'Consistent private backup: {output.name}')

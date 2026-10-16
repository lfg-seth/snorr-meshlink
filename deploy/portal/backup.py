#!/usr/bin/env python3
"""Quiesce the pilot, archive its complete private state, then restart it."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

DESTINATION = Path('/var/backups/meshlink')
SERVICES = ['meshlink-demo-worker.service', 'meshlink-demo-api.service',
            'meshlink-worker.service', 'meshlink-api.service']


def main():
    if os.geteuid() != 0:
        raise SystemExit('Run as root; backup contains private provisioning credentials.')
    DESTINATION.mkdir(mode=0o700, parents=True, exist_ok=True)
    active = [name for name in SERVICES if subprocess.run(
        ['systemctl', 'is-active', '--quiet', name]).returncode == 0]
    temporary = None
    try:
        for name in active:
            subprocess.run(['systemctl', 'stop', name], check=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        target = DESTINATION / f'meshlink-{stamp}.tar.gz'
        with tempfile.NamedTemporaryFile(dir=DESTINATION, delete=False) as file:
            temporary = Path(file.name)
        with tarfile.open(temporary, 'w:gz') as archive:
            for source, name in [
                ('/var/lib/meshlink', 'state'),
                ('/opt/meshlink/backend', 'release/backend'),
                ('/opt/meshlink/deploy/portal', 'release/deploy/portal'),
                ('/var/www/meshlink', 'release/portal-dist'),
            ]:
                archive.add(source, arcname=name, filter=lambda info: None
                            if '__pycache__' in Path(info.name).parts else info)
            # Live adapter configuration/key and buffered receipts are private
            # recovery state too. Worker has already stopped before archiving.
            for source, name in [('/etc/meshlink', 'worker-config'),
                                 ('/var/lib/meshlink-demo', 'demo-state'),
                                 ('/opt/meshlink-demo/bin', 'demo-bin'),
                                 ('/etc/nginx/sites-available/meshlink', 'services/nginx.conf'),
                                 ('/etc/systemd/system/meshlink-demo-api.service', 'services/meshlink-demo-api.service'),
                                 ('/etc/systemd/system/meshlink-demo-worker.service', 'services/meshlink-demo-worker.service'),
                                 ('/var/lib/meshlink-worker', 'worker-state'),
                                 ('/etc/systemd/system/meshlink-api.service', 'services/meshlink-api.service'),
                                 ('/etc/systemd/system/meshlink-api.service.d', 'services/meshlink-api.service.d'),
                                 ('/etc/systemd/system/meshlink-worker.service', 'services/meshlink-worker.service')]:
                if Path(source).exists():
                    archive.add(source, arcname=name)
        with tarfile.open(temporary) as archive:
            names = set(archive.getnames())
            if not {'state/pb_data/data.db', 'state/credentials.json'} <= names:
                raise RuntimeError('Incomplete backup; existing backups retained.')
        temporary.chmod(0o600)
        os.replace(temporary, target)
        temporary = None
        with target.open('rb') as file:
            digest = hashlib.file_digest(file, 'sha256').hexdigest()
        target.with_suffix('.sha256').write_text(f'{digest}  {target.name}\n')
        # Retain 14 complete local archives. No source/pilot data is removed.
        for old in sorted(DESTINATION.glob('meshlink-*.tar.gz'))[:-14]:
            old.unlink()
            old.with_suffix('.sha256').unlink(missing_ok=True)
        print(json.dumps({'backup': target.name, 'bytes': target.stat().st_size,
                          'sha256': digest}))
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        for name in reversed(active):
            subprocess.run(['systemctl', 'start', name], check=True)


if __name__ == '__main__':
    main()

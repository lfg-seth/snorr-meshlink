#!/usr/bin/env python3
"""Provision a separate hosted synthetic demo; preserve any existing demo edits."""
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import sys

sys.path.insert(0, '/opt/meshlink/backend')
from demo_database import initialize


def main():
    if os.geteuid() != 0:
        raise SystemExit('Run as root on the portal LXC.')
    try:
        account = pwd.getpwnam('meshlink-demo')
    except KeyError:
        subprocess.run(['useradd', '--system', '--user-group', '--home-dir',
                        '/var/lib/meshlink-demo', '--shell', '/usr/sbin/nologin',
                        'meshlink-demo'], check=True)
        account = pwd.getpwnam('meshlink-demo')
    state = Path('/var/lib/meshlink-demo')
    if not (state / 'pb_data/data.db').exists():
        initialize(state)
    else:
        print('Existing hosted demo retained; checkpoint was not reapplied.')
    state.chmod(0o700)
    for path in [state, *state.rglob('*')]:
        os.chown(path, account.pw_uid, account.pw_gid)
    binary = Path('/opt/meshlink-demo/bin/pocketbase')
    binary.parent.mkdir(parents=True, exist_ok=True)
    staged = binary.with_suffix('.new')
    shutil.copy2('/var/lib/meshlink/bin/pocketbase', staged)
    staged.chmod(0o755)
    os.replace(staged, binary)
    for name in ['meshlink-demo-api.service', 'meshlink-demo-worker.service']:
        shutil.copy2(Path('/opt/meshlink/deploy/portal') / name,
                     Path('/etc/systemd/system') / name)
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', '--now', 'meshlink-demo-api.service',
                    'meshlink-demo-worker.service'], check=True)
    print('Hosted demo enabled on loopback 8092; live provisioning was not changed.')


if __name__ == '__main__':
    main()

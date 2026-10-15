#!/usr/bin/env python3
"""Owner-run private credential export for bench gateways and subscriber; no broker changes."""
import json
import os
from pathlib import Path
import pwd
import stat


def main():
    if os.geteuid() != 0:
        raise RuntimeError('Run with sudo on the MQTT broker')
    os.umask(0o077)
    source = Path('/root/meshlink-private/mqtt-credentials.json')
    state = json.loads(source.read_text())
    if (state.get('host'), state.get('port'), state.get('tls'), state.get('root')) != (
            'mqtt.snorr.org', 8883, True, 'snorr/pilot'):
        raise RuntimeError('Unexpected broker endpoint/root; refusing export')
    names = ('pilot-v3-uplink-1', 'pilot-v3-uplink-2', 'pilot-worker')
    accounts = state.get('accounts', {})
    if any(not isinstance(accounts.get(name), str) or not accounts[name] for name in names):
        raise RuntimeError('Expected pilot accounts missing; refusing export')
    owner = pwd.getpwnam('setheth')
    directory = Path(owner.pw_dir) / '.meshlink-bench'
    if directory.is_symlink():
        raise RuntimeError('Refusing symlink export directory')
    if directory.exists():
        info = directory.stat()
        if not directory.is_dir() or info.st_uid != owner.pw_uid or stat.S_IMODE(info.st_mode) != 0o700:
            raise RuntimeError('Existing export directory must be owner-private mode 0700')
    else:
        directory.mkdir(mode=0o700)
        os.chown(directory, owner.pw_uid, owner.pw_gid)
    destination = directory / 'mqtt-credentials.json'
    payload = json.dumps({
        'host': state['host'], 'port': state['port'], 'tls': state['tls'], 'root': state['root'],
        'accounts': {name: accounts[name] for name in names},
    }, sort_keys=True, indent=2) + '\n'
    if destination.exists() or destination.is_symlink():
        info = destination.lstat()
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != owner.pw_uid
                or stat.S_IMODE(info.st_mode) != 0o600 or destination.read_text() != payload):
            raise RuntimeError('Existing export differs or has unsafe permissions; refusing overwrite')
    else:
        descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, 'w') as output:
            output.write(payload)
            output.flush()
            os.fsync(output.fileno())
            os.fchown(output.fileno(), owner.pw_uid, owner.pw_gid)
    print('Private bench export ready:', destination)
    print('Broker accounts/configuration unchanged; no credentials printed. Remove export after retrieval.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL:', type(error).__name__, str(error))
        raise SystemExit(1)

#!/usr/bin/env python3
"""Fit only existing V3 account passwords to stock Meshtastic; preserve broker ACLs and worker."""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import pwd
import secrets
import stat
import subprocess
import tempfile
import time

GATEWAYS = ('pilot-v3-uplink-1', 'pilot-v3-uplink-2')
ACCOUNTS = set(GATEWAYS) | {'pilot-worker'}


def atomic_write(path, data, original):
    descriptor, temporary = tempfile.mkstemp(prefix='.meshlink-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
            os.fchmod(output.fileno(), stat.S_IMODE(original.st_mode))
            os.fchown(output.fileno(), original.st_uid, original.st_gid)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def fit(credentials, password_file, acl_file, backup_parent, reload_broker, verify, export):
    state = json.loads(credentials.read_text())
    if (state.get('host'), state.get('port'), state.get('tls'), state.get('root')) != (
            'mqtt.snorr.org', 8883, True, 'snorr/pilot') or set(state.get('accounts', {})) != ACCOUNTS:
        raise RuntimeError('Unexpected pilot credentials; refusing changes')
    users = state['accounts']
    if any(not isinstance(v, str) or not v for v in users.values()):
        raise RuntimeError('Invalid existing account values')
    if all(len(users[name].encode()) <= 31 for name in GATEWAYS):
        verify(users)
        export(state)
        print('PASS: gateway credentials already fit; no account changes')
        return
    old_credentials, old_passwords, old_acl = credentials.read_bytes(), password_file.read_bytes(), acl_file.read_bytes()
    credential_info, password_info = credentials.stat(), password_file.stat()
    lines = old_passwords.decode().splitlines()
    if len(lines) != len(ACCOUNTS) or set(line.split(':', 1)[0] for line in lines) != ACCOUNTS:
        raise RuntimeError('Unexpected password-file accounts; refusing changes')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    backup = backup_parent / ('mqtt-v3-password-fit-' + stamp)
    backup.mkdir(mode=0o700, parents=True)
    for name, data in [('credentials-before.json', old_credentials), ('passwd-before', old_passwords), ('acl-before', old_acl)]:
        (backup / name).write_bytes(data)
        (backup / name).chmod(0o600)
    updated = dict(users)
    for name in GATEWAYS:
        updated[name] = secrets.token_urlsafe(22)
        assert len(updated[name].encode()) <= 31
    staged = backup / 'gateway-hashes'
    staged.write_text(''.join(name + ':' + updated[name] + '\n' for name in GATEWAYS))
    staged.chmod(0o600)
    subprocess.run(['mosquitto_passwd', '-U', str(staged)], check=True, capture_output=True)
    hashes = {line.split(':', 1)[0]: line for line in staged.read_text().splitlines()}
    if set(hashes) != set(GATEWAYS):
        raise RuntimeError('Unexpected generated gateway hashes')
    merged = ''.join(hashes.get(line.split(':', 1)[0], line) + '\n' for line in old_passwords.decode().splitlines())
    state['accounts'] = updated
    try:
        atomic_write(password_file, merged.encode(), password_info)
        atomic_write(credentials, (json.dumps(state, indent=2) + '\n').encode(), credential_info)
        reload_broker()
        verify(updated)
        if acl_file.read_bytes() != old_acl:
            raise RuntimeError('ACL changed unexpectedly')
        if updated['pilot-worker'] != users['pilot-worker']:
            raise RuntimeError('Worker credential changed unexpectedly')
        export(state)
    except Exception:
        atomic_write(password_file, old_passwords, password_info)
        atomic_write(credentials, old_credentials, credential_info)
        reload_broker()
        raise
    print('PASS: only two V3 passwords replaced with 30-character values; worker and ACL unchanged')
    print('Private rollback backup:', backup)


def export_private(state):
    owner = pwd.getpwnam('setheth')
    directory = Path(owner.pw_dir) / '.meshlink-bench'
    if directory.is_symlink():
        raise RuntimeError('Refusing symlink export directory')
    if not directory.exists():
        directory.mkdir(mode=0o700)
        os.chown(directory, owner.pw_uid, owner.pw_gid)
    info = directory.stat()
    if info.st_uid != owner.pw_uid or stat.S_IMODE(info.st_mode) != 0o700:
        raise RuntimeError('Export directory is not owner-private')
    destination = directory / 'mqtt-credentials.json'
    if destination.is_symlink():
        raise RuntimeError('Refusing symlink export file')
    if destination.exists():
        info = destination.stat()
        if info.st_uid != owner.pw_uid or stat.S_IMODE(info.st_mode) != 0o600:
            raise RuntimeError('Export file is not owner-private')
    else:
        destination.touch(mode=0o600)
        os.chown(destination, owner.pw_uid, owner.pw_gid)
    payload = {key: state[key] for key in ('host', 'port', 'tls', 'root', 'accounts')}
    atomic_write(destination, (json.dumps(payload, indent=2) + '\n').encode(), destination.stat())
    print('Private bench export ready:', destination)


def main():
    if os.geteuid() != 0:
        raise RuntimeError('Run with sudo on the broker')
    os.umask(0o077)
    for path in (Path('/root/meshlink-private/mqtt-credentials.json'), Path('/etc/mosquitto/passwd'), Path('/etc/mosquitto/acl')):
        if path.is_symlink() or not path.is_file() or path.stat().st_uid != 0:
            raise RuntimeError('Expected root-owned regular pilot files')
    subprocess.run(['systemctl', 'is-active', '--quiet', 'mosquitto'], check=True)
    spec = importlib.util.spec_from_file_location('pilot_helpers', Path(__file__).with_name('reset-mqtt-pilot.py'))
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)
    def verify_ready(users):
        for _ in range(20):
            ready = True
            for name in GATEWAYS:
                conn, code = helpers.connect(name, users[name])
                conn.close()
                ready = ready and code == 0
            if ready:
                helpers.verify(users, set())
                return
            time.sleep(.1)
        raise RuntimeError('Reload did not activate gateway credentials')
    fit(Path('/root/meshlink-private/mqtt-credentials.json'), Path('/etc/mosquitto/passwd'),
        Path('/etc/mosquitto/acl'), Path('/root/meshlink-maintenance'),
        lambda: subprocess.run(['systemctl', 'reload', 'mosquitto'], check=True),
        verify_ready, export_private)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL:', type(error).__name__, str(error))
        raise SystemExit(1)

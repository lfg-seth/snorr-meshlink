#!/usr/bin/env python3
"""Run with sudo on the broker host. Archive legacy MQTT and provision uplink-only pilot."""
import argparse
import datetime
import ipaddress
import json
import os
from pathlib import Path
import pwd
import secrets
import select
import shutil
import socket
import struct
import subprocess
import sys
import time

HOST = 'mqtt.snorr.org'
BACKEND_ADDRESS = '127.0.0.1'
BACKEND_PORT = 1883
ROOT = 'snorr/pilot'
CREDS = Path('/root/meshlink-private/mqtt-credentials.json')
TREES = [Path('/etc/mosquitto'), Path('/var/lib/mosquitto'), Path('/var/log/mosquitto')]


def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def write(path, content, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    path.chmod(mode)


def field(data):
    if isinstance(data, str):
        data = data.encode()
    return struct.pack('!H', len(data)) + data


def packet(kind, body):
    length = len(body)
    prefix = bytearray([kind])
    while True:
        digit = length % 128
        length //= 128
        prefix.append(digit | (128 if length else 0))
        if not length:
            return bytes(prefix) + body


def receive(conn):
    def exact(n):
        result = b''
        while len(result) < n:
            chunk = conn.recv(n - len(result))
            if not chunk:
                raise RuntimeError('Broker closed test connection')
            result += chunk
        return result
    kind = exact(1)[0]
    length = 0
    factor = 1
    for _ in range(4):
        digit = exact(1)[0]
        length += (digit & 127) * factor
        if not digit & 128:
            return kind, exact(length)
        factor *= 128
    raise RuntimeError('Invalid MQTT length')


def connect(username=None, password=None):
    conn = socket.create_connection((BACKEND_ADDRESS, BACKEND_PORT), timeout=5)
    flags = 2 if username is None else 0xc2
    body = field('MQTT') + bytes([5, flags]) + b'\x00\x1e\x00' + field('meshlink-test-' + secrets.token_hex(6))
    if username is not None:
        body += field(username) + field(password)
    conn.sendall(packet(0x10, body))
    kind, reply = receive(conn)
    if kind != 0x20 or len(reply) < 3:
        conn.close()
        raise RuntimeError('Invalid CONNACK')
    return conn, reply[1]


def verify(users, legacy):
    for name, password in [(None, None), ('invalid-account', secrets.token_urlsafe(24))]:
        conn, code = connect(name, password)
        conn.close()
        if code == 0:
            raise RuntimeError('Unauthorized login accepted')
    topic = ROOT + '/2/e/__audit__/fixture'
    listeners = {}
    try:
        for name, password in users.items():
            conn, code = connect(name, password)
            if code != 0:
                conn.close()
                raise RuntimeError('Pilot credential rejected: ' + name)
            listeners[name] = conn
            conn.sendall(packet(0x82, b'\x00\x01\x00' + field(topic) + b'\x00'))
            kind, body = receive(conn)
            # Mosquitto can accept subscriptions and filter delivery using ACLs.
            if kind != 0x90 or body[-1] not in (0, 0x87):
                raise RuntimeError('Unexpected SUBACK for ' + name)
            if name == 'pilot-worker' and body[-1] != 0:
                raise RuntimeError('Worker subscription rejected')
        for name, password in users.items():
            conn, code = connect(name, password)
            with conn:
                if code != 0:
                    raise RuntimeError('Pilot credential rejected: ' + name)
                conn.sendall(packet(0x32, field(topic) + b'\x00\x02\x00' + b'synthetic-access-check'))
                kind, body = receive(conn)
                allowed_write = kind == 0x40 and (len(body) == 2 or body[2] in (0, 0x10))
                if allowed_write != (name != 'pilot-worker'):
                    raise RuntimeError('Unexpected publish permission for ' + name)
                if name != 'pilot-worker':
                    kind, body = receive(listeners['pilot-worker'])
                    if kind != 0x30 or not body.endswith(b'synthetic-access-check'):
                        raise RuntimeError('Worker did not receive synthetic fixture')
                for denied_topic in (ROOT + '/2/json/mqtt/audit', 'unrelated/access-check'):
                    conn.sendall(packet(0x32, field(denied_topic) + b'\x00\x03\x00' + b'synthetic-denied'))
                    kind, body = receive(conn)
                    if kind != 0x40 or len(body) < 3 or body[2] != 0x87:
                        raise RuntimeError('Unauthorized namespace was not denied')
        for name, conn in listeners.items():
            if name != 'pilot-worker' and (getattr(conn, 'pending', lambda: 0)() or select.select([conn], [], [], 0.5)[0]):
                raise RuntimeError('Uplink-only gateway received broker topic data')
    finally:
        for conn in listeners.values():
            conn.close()
    actual = {line.split(':', 1)[0] for line in Path('/etc/mosquitto/passwd').read_text().splitlines()}
    if actual != set(users) or actual.intersection(legacy):
        raise RuntimeError('Legacy credential reset verification failed')
    print('PASS: pilot credentials, anonymous/invalid rejection, read/write delivery ACLs and command/unrelated-topic denial.')


def main():
    if os.geteuid() != 0:
        raise RuntimeError('Run with sudo on the MQTT server')
    os.umask(0o077)
    global BACKEND_ADDRESS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bind-address', default='127.0.0.1', help='Loopback by default; LAN binding requires an already-active restricted UFW rule')
    parser.add_argument('--proxy-address', help='Private IPv4 source of Nginx, needed for LAN listener')
    parser.add_argument('--verify', action='store_true', help='Test an existing fresh pilot without resetting it')
    args = parser.parse_args()
    if args.verify:
        state = json.loads(CREDS.read_text())
        BACKEND_ADDRESS = state['backend_address']
        verify(state['accounts'], set())
        run('systemctl', 'is-active', '--quiet', 'mosquitto')
        return
    BACKEND_ADDRESS = str(ipaddress.IPv4Address(args.bind_address))
    bind = ipaddress.IPv4Address(BACKEND_ADDRESS)
    if not bind.is_loopback:
        if not bind.is_private or bind.is_unspecified or bind.is_link_local:
            raise RuntimeError('Backend must bind a private IPv4 address')
        if not args.proxy_address:
            raise RuntimeError('LAN binding requires --proxy-address and verified firewall restriction')
        proxy = ipaddress.IPv4Address(args.proxy_address)
        if not proxy.is_private or proxy.is_loopback or proxy.is_unspecified:
            raise RuntimeError('Use the actual private Nginx source address')
        # Do not expose plaintext credentials before the firewall is restricted.
        # Require a first allow rule for this proxy, followed by deny for all others.
        status = run('ufw', 'status', 'numbered', capture_output=True, text=True).stdout
        rows = [line.strip() for line in status.splitlines() if line.strip().startswith('[')]
        if 'Status: active' not in status or len(rows) < 2:
            raise RuntimeError('Enable and restrict UFW before LAN binding; see handoff')
        first = rows[0].split(']', 1)[1].strip()
        second = rows[1].split(']', 1)[1].strip()
        if (f'{BACKEND_ADDRESS} 1883/tcp' not in first or 'ALLOW IN' not in first
                or str(proxy) not in first or '1883/tcp' not in second or 'DENY IN' not in second
                or 'Anywhere' not in second):
            raise RuntimeError('First UFW rules must allow proxy to backend:1883, then deny other 1883 connections')
    if Path('/etc/mosquitto/MESHLINK_FRESH_PILOT').exists() or CREDS.exists():
        raise RuntimeError('Fresh-pilot marker or credentials already exist; refusing another reset')
    if run('systemctl', 'show', 'mosquitto', '-p', 'DropInPaths', '--value', capture_output=True, text=True).stdout.strip():
        raise RuntimeError('Custom service overrides require review before reset')
    account = pwd.getpwnam('mosquitto')
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    archive = Path('/root/meshlink-archive') / ('mqtt-legacy-' + timestamp)
    archive.mkdir(parents=True, mode=0o700)
    with (archive / 'service-before.txt').open('w') as service_record:
        run('systemctl', 'cat', 'mosquitto', stdout=service_record)
    legacy_file = Path('/etc/mosquitto/passwd')
    legacy = {line.split(':', 1)[0] for line in legacy_file.read_text().splitlines()} if legacy_file.exists() else set()
    # Stock Meshtastic's 32-byte password field needs room for a terminator.
    users = {name: secrets.token_urlsafe(36 if name == 'pilot-worker' else 22)
             for name in ('pilot-v3-uplink-1', 'pilot-v3-uplink-2', 'pilot-worker')}
    moved = []
    run('systemctl', 'stop', 'mosquitto')  # flush persistence before archiving
    try:
        legacy_paths = TREES + [
            Path('/etc/letsencrypt/renewal/mqtt.spp.lol.conf'),
            Path('/etc/letsencrypt/renewal-hooks/deploy/meshlink-mqtt'),
            Path('/usr/local/libexec/meshlink-mqtt-maintenance.py'),
        ]
        for path in legacy_paths:
            if path.exists():
                dest = archive / path.relative_to('/')
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path), str(dest))
                moved.append((path, dest))
        for path in TREES:
            path.mkdir(parents=True, mode=0o750)
            path.chmod(0o750)
        os.chown('/etc/mosquitto', 0, account.pw_gid)
        conf_dir = Path('/etc/mosquitto/conf.d')
        conf_dir.mkdir(mode=0o750)
        conf_dir.chmod(0o750)
        os.chown(conf_dir, 0, account.pw_gid)
        for path in TREES[1:]:
            os.chown(path, account.pw_uid, account.pw_gid)
        write('/etc/mosquitto/mosquitto.conf', f'''user mosquitto
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
include_dir /etc/mosquitto/conf.d
''', 0o644)
        write('/etc/mosquitto/conf.d/pilot.conf', f"""listener {BACKEND_PORT} {BACKEND_ADDRESS}
protocol mqtt
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl
""", 0o644)
        # Hash root-private plaintext in place; no passwords in argv or output.
        write('/etc/mosquitto/passwd', ''.join(f'{name}:{password}\n' for name, password in users.items()))
        run('mosquitto_passwd', '-U', '/etc/mosquitto/passwd')
        os.chown('/etc/mosquitto/passwd', 0, account.pw_gid)
        Path('/etc/mosquitto/passwd').chmod(0o640)
        acl = ''.join(f'user {name}\ntopic write {ROOT}/2/e/#\n\n' for name in users if name != 'pilot-worker')
        acl += f'user pilot-worker\ntopic read {ROOT}/2/e/#\n'
        write('/etc/mosquitto/acl', acl, 0o640)
        os.chown('/etc/mosquitto/acl', 0, account.pw_gid)
        run('systemctl', 'start', 'mosquitto')
        for _ in range(20):
            try:
                with socket.create_connection((BACKEND_ADDRESS, BACKEND_PORT), timeout=1):
                    break
            except OSError:
                time.sleep(0.25)
        verify(users, legacy)
        CREDS.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        CREDS.parent.chmod(0o700)
        write(CREDS, json.dumps({'host': HOST, 'port': 8883, 'tls': True, 'root': ROOT, 'backend_address': BACKEND_ADDRESS, 'backend_port': BACKEND_PORT, 'accounts': users}, indent=2) + '\n')
        write('/etc/mosquitto/MESHLINK_FRESH_PILOT', timestamp + '\n')
    except Exception:
        subprocess.run(['systemctl', 'stop', 'mosquitto'], check=False)
        for path, dest in moved:
            if path.exists():
                failed = archive / 'failed-fresh' / path.relative_to('/')
                failed.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path), str(failed))
            shutil.move(str(dest), str(path))
        subprocess.run(['systemctl', 'start', 'mosquitto'], check=False)
        print('Reset failed; original trees restored. Private attempt evidence:', archive, file=sys.stderr)
        raise
    print('Legacy archive:', archive)
    print('Private new credentials:', CREDS, '(do not paste or commit)')
    print(f'Fresh broker: {BACKEND_ADDRESS}:{BACKEND_PORT}; protobuf uplink root: {ROOT}')
    print(f'Intended public endpoint: {HOST}:8883 with TLS handled by Mike/Nginx.')
    print('Broker has no TLS/certificate dependency; old broker-specific renewal config archived.')
    print('Dispatch/JSON commands denied; gateway/worker integration still to verify.')
    if bind.is_loopback:
        print('Loopback-only: separate-host Nginx access awaits its private IP/firewall rule.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('ERROR:', type(exc).__name__, str(exc), file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Enable the confirmed private Nginx backend without resetting pilot accounts."""
import datetime
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time

BIND = '192.168.12.51'
PROXY = '192.168.12.254'
CONFIG = Path('/etc/mosquitto/conf.d/pilot.conf')


def run(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True).stdout


def probe(address):
    cid = b'snorr-backend-check'
    body = b'\x00\x04MQTT\x04\x02\x00\x3c' + len(cid).to_bytes(2, 'big') + cid
    with socket.create_connection((address, 1883), timeout=3) as conn:
        conn.sendall(b'\x10' + bytes([len(body)]) + body)
        reply = b''
        while len(reply) < 4:
            chunk = conn.recv(4 - len(reply))
            if not chunk:
                raise RuntimeError('Broker closed before CONNACK')
            reply += chunk
        if reply != b'\x20\x02\x00\x05':
            raise RuntimeError('Expected anonymous access rejection')


def main():
    if os.geteuid() != 0:
        raise RuntimeError('Run with sudo on the broker host')
    status = run('ufw', 'status', 'verbose')
    if 'Status: active' not in status or 'Default: deny (incoming)' not in status:
        raise RuntimeError('Requires active UFW with default deny incoming; no changes made')
    if '22/tcp' not in status or 'ALLOW IN' not in status:
        raise RuntimeError('Verify existing SSH firewall access first')
    with socket.socket() as test:
        test.bind((BIND, 0))
    original = CONFIG.read_text()
    expected = ('listener 1883 127.0.0.1\nprotocol mqtt\nallow_anonymous false\n'
                'password_file /etc/mosquitto/passwd\nacl_file /etc/mosquitto/acl\n')
    if original != expected:
        raise RuntimeError('Pilot configuration differs from verified reset template; no changes made')
    for path in [Path('/etc/mosquitto/mosquitto.conf'), *CONFIG.parent.glob('*.conf')]:
        for line in path.read_text().splitlines():
            line = line.strip()
            if line.startswith('per_listener_settings') and line.split()[-1] == 'true':
                raise RuntimeError('Per-listener authentication requires separate review')
            if path != CONFIG and line.startswith(('listener ', 'include_dir ')):
                if path.name == 'mosquitto.conf' and line == 'include_dir /etc/mosquitto/conf.d':
                    continue
                raise RuntimeError('Additional listeners/includes require review')
    probe('127.0.0.1')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    archive = Path('/root/meshlink-maintenance') / ('nginx-backend-' + stamp)
    archive.mkdir(parents=True, mode=0o700)
    archive.chmod(0o700)
    shutil.copy2(CONFIG, archive / 'pilot.conf')
    shutil.copytree('/etc/ufw', archive / 'ufw')
    # Insert deny first so the backend is never opened without source restriction.
    run('ufw', 'insert', '1', 'deny', 'in', 'proto', 'tcp', 'from', 'any', 'to', 'any', 'port', '1883')
    run('ufw', 'insert', '1', 'allow', 'in', 'proto', 'tcp', 'from', PROXY, 'to', BIND, 'port', '1883')
    try:
        CONFIG.write_text(original + '\nlistener 1883 ' + BIND + '\nprotocol mqtt\n')
        run('systemctl', 'restart', 'mosquitto')
        for attempt in range(20):
            try:
                probe('127.0.0.1')
                probe(BIND)
                break
            except OSError:
                if attempt == 19:
                    raise
                time.sleep(0.25)
        if run('systemctl', 'is-active', 'mosquitto').strip() != 'active':
            raise RuntimeError('Broker is not active')
    except Exception:
        shutil.copy2(archive / 'pilot.conf', CONFIG)
        run('systemctl', 'restart', 'mosquitto')
        print('Restored original loopback broker configuration; restrictive 1883 rules retained.')
        raise
    print('PASS: loopback and private LAN MQTT respond and reject anonymous access.')
    print('Nginx upstream must be 192.168.12.51:1883, plain MQTT TCP; TLS terminates at Nginx.')
    print('Firewall permits only 192.168.12.254 to this private listener; SSH rules preserved.')
    print('Private configuration/firewall backup:', archive)
    print(run('ufw', 'status', 'numbered'))
    print('Public TLS authentication/ACLs still require end-to-end verification.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAILED:', type(error).__name__, str(error))
        raise SystemExit(1)

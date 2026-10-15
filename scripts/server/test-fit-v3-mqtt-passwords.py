#!/usr/bin/env python3
"""Exercise password compatibility, preservation, idempotence and rollback on an isolated broker."""
import importlib.util
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import tempfile
import time


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    if os.geteuid() == 0:
        raise RuntimeError('Run unprivileged; this test uses only temporary files and a loopback broker')
    os.umask(0o077)
    fitter = load('fitter', 'fit-v3-mqtt-passwords.py')
    helpers = load('helpers', 'reset-mqtt-pilot.py')
    with tempfile.TemporaryDirectory(prefix='meshlink-password-fit-') as temporary:
        directory = Path(temporary)
        credentials, passwords, acl = [directory / name for name in ('credentials.json', 'passwd', 'acl')]
        old_users = {name: secrets.token_urlsafe(36) for name in sorted(fitter.ACCOUNTS)}
        state = {'host': 'mqtt.snorr.org', 'port': 8883, 'tls': True, 'root': 'snorr/pilot', 'accounts': old_users}
        credentials.write_text(json.dumps(state, indent=2) + '\n')
        passwords.write_text(''.join(name + ':' + value + '\n' for name, value in old_users.items()))
        subprocess.run(['mosquitto_passwd', '-U', str(passwords)], check=True, capture_output=True)
        acl.write_text(''.join('user ' + name + '\ntopic write snorr/pilot/2/e/#\n\n' for name in fitter.GATEWAYS)
                       + 'user pilot-worker\ntopic read snorr/pilot/2/e/#\n')
        credentials.chmod(0o600)
        passwords.chmod(0o640)
        original_credentials, original_passwords, original_acl = credentials.read_bytes(), passwords.read_bytes(), acl.read_bytes()
        worker_hash = next(line for line in original_passwords.splitlines() if line.startswith(b'pilot-worker:'))
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        config = directory / 'broker.conf'
        config.write_text(f'listener {port} 127.0.0.1\nallow_anonymous false\npassword_file {passwords}\nacl_file {acl}\npersistence false\n')
        log = (directory / 'broker.log').open('w')
        broker = subprocess.Popen(['mosquitto', '-c', str(config)], stdout=log, stderr=subprocess.STDOUT)
        helpers.BACKEND_ADDRESS, helpers.BACKEND_PORT = '127.0.0.1', port

        def reload_broker():
            broker.send_signal(signal.SIGHUP)
            time.sleep(.2)

        def authenticate(users):
            for name, password in users.items():
                conn, code = helpers.connect(name, password)
                conn.close()
                if code != 0:
                    raise RuntimeError('Isolated account authentication failed')

        try:
            for _ in range(30):
                if broker.poll() is not None:
                    raise RuntimeError('Isolated broker failed to start')
                try:
                    authenticate(old_users)
                    break
                except (OSError, RuntimeError):
                    time.sleep(.1)
            else:
                raise RuntimeError('Isolated broker did not become ready')
            exported = []
            fitter.fit(credentials, passwords, acl, directory / 'backups', reload_broker, authenticate, exported.append)
            updated = json.loads(credentials.read_text())['accounts']
            assert all(len(updated[name].encode()) == 30 for name in fitter.GATEWAYS)
            assert updated['pilot-worker'] == old_users['pilot-worker']
            assert worker_hash in passwords.read_bytes().splitlines() and acl.read_bytes() == original_acl
            assert exported[-1]['accounts'] == updated
            for name in fitter.GATEWAYS:
                conn, code = helpers.connect(name, old_users[name])
                conn.close()
                assert code != 0
            before_idempotent = credentials.read_bytes(), passwords.read_bytes()
            fitter.fit(credentials, passwords, acl, directory / 'backups', reload_broker, authenticate, exported.append)
            assert before_idempotent == (credentials.read_bytes(), passwords.read_bytes())
            print('PASS: 30-byte gateway passwords authenticate; old gateway values fail; worker/ACL preserved; rerun idempotent')
            fitter.atomic_write(credentials, original_credentials, credentials.stat())
            fitter.atomic_write(passwords, original_passwords, passwords.stat())
            reload_broker()
            def fail_verification(users):
                raise RuntimeError('Injected verification failure')
            try:
                fitter.fit(credentials, passwords, acl, directory / 'backups', reload_broker, fail_verification, exported.append)
            except RuntimeError as error:
                assert str(error) == 'Injected verification failure'
            else:
                raise AssertionError('Injected failure did not fail')
            assert credentials.read_bytes() == original_credentials and passwords.read_bytes() == original_passwords
            assert acl.read_bytes() == original_acl
            authenticate(old_users)
            print('PASS: failed verification restores original credential/hash files and working broker authentication')
        finally:
            broker.terminate()
            broker.wait(timeout=5)
            log.close()


if __name__ == '__main__':
    main()

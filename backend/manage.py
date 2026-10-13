"""Local native backend commands; binaries, databases and credentials stay ignored."""
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import platform
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile

from client import Client
from fixtures import initial_packets, provision

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / 'backend'
LOCAL = ROOT / 'local-data' / 'backend'
BINARY = LOCAL / 'bin' / ('pocketbase.exe' if os.name == 'nt' else 'pocketbase')
CREDENTIALS = LOCAL / 'credentials.json'


def command(data_dir=None):
    return [str(BINARY), f'--dir={data_dir or LOCAL / "pb_data"}',
            f'--hooksDir={BACKEND / "pb_hooks"}', f'--migrationsDir={BACKEND / "pb_migrations"}', '--automigrate=false', '--hooksWatch=false']


def install_receipt_path():
    return BINARY.with_name('pocketbase-install.json')


def save_install_receipt(receipt):
    target = install_receipt_path()
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=target.parent, delete=False) as file:
            temporary = Path(file.name)
            json.dump(receipt, file, indent=2)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def install():
    manifest = json.loads((BACKEND / 'pocketbase-release.json').read_text())
    machine = {'x86_64': 'amd64', 'AMD64': 'amd64', 'aarch64': 'arm64', 'arm64': 'arm64'}.get(platform.machine())
    system = {'Linux': 'linux', 'Darwin': 'darwin', 'Windows': 'windows'}.get(platform.system())
    filename = f'pocketbase_{manifest["version"]}_{system}_{machine}.zip'
    expected = manifest['sha256'].get(filename)
    if not expected:
        raise ValueError('Unsupported platform for the pinned release.')
    # A verified installation can be reused offline, including while it runs.
    try:
        receipt = json.loads(install_receipt_path().read_text())
    except (FileNotFoundError, ValueError):
        receipt = {}
    if (receipt.get('version') == manifest['version']
            and receipt.get('archive') == filename
            and receipt.get('archiveSha256') == expected
            and BINARY.is_file()
            and hashlib.sha256(BINARY.read_bytes()).hexdigest() == receipt.get('binarySha256')):
        print(f'PocketBase {manifest["version"]} is already installed and verified; kept the existing binary.')
        return

    url = f'https://github.com/pocketbase/pocketbase/releases/download/v{manifest["version"]}/{filename}'
    with urllib.request.urlopen(url, timeout=60) as response:
        archive = response.read()
    if hashlib.sha256(archive).hexdigest() != expected:
        raise ValueError('PocketBase archive checksum does not match the pinned official release.')
    import io
    with zipfile.ZipFile(io.BytesIO(archive)) as archive:
        binary = archive.read(BINARY.name)
    digest = hashlib.sha256(binary).hexdigest()
    receipt = {'version': manifest['version'], 'archive': filename,
               'archiveSha256': expected, 'binarySha256': digest}
    BINARY.parent.mkdir(parents=True, exist_ok=True)
    # Installations created before receipts existed need one verification download.
    if BINARY.is_file() and hashlib.sha256(BINARY.read_bytes()).hexdigest() == digest:
        save_install_receipt(receipt)
        print(f'PocketBase {manifest["version"]} is already installed and verified; kept the existing binary.')
        return

    # Never truncate an executable. Stage a complete file on the same filesystem.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=BINARY.parent, delete=False) as file:
            temporary = Path(file.name)
            file.write(binary)
            file.flush()
            os.fsync(file.fileno())
        temporary.chmod(0o755)
        try:
            os.replace(temporary, BINARY)
        except PermissionError as error:
            raise RuntimeError('PocketBase could not be replaced. Stop the backend with Ctrl+C, rerun install, then restart it.') from error
        except OSError as error:
            if error.errno == errno.ETXTBSY:
                raise RuntimeError('PocketBase is running and cannot be replaced. Stop the backend with Ctrl+C, rerun install, then restart it.') from error
            raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    save_install_receipt(receipt)
    print(f'Installed verified PocketBase {manifest["version"]} in local-data/backend/bin.')


def credentials():
    return json.loads(CREDENTIALS.read_text())


def make_credentials():
    return {key: {'username': f'meshlink-{key}', 'password': secrets.token_urlsafe(24)}
            for key in ['admin', 'member', 'member2', 'worker', 'superuser']}


def start(data_dir=None, port=8090, log=None):
    environment = {**os.environ, 'MESHLINK_SIMULATION': '1'}
    return subprocess.Popen(command(data_dir) + ['serve', f'--http=127.0.0.1:{port}', '--origins=http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:4173,http://localhost:4173'],
                            env=environment, stdout=log, stderr=log)


def wait_ready(url, process):
    for _ in range(100):
        if process.poll() is not None:
            raise RuntimeError('PocketBase exited during startup; inspect the private server log.')
        try:
            Client(url).request('GET', '/api/health')
            return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(.1)
    raise RuntimeError('PocketBase did not become ready.')


def initialize():
    if CREDENTIALS.exists() or (LOCAL / 'pb_data' / 'data.db').exists():
        raise ValueError('Existing local backend found. Initialization does not overwrite credentials or pilot data.')
    # Fail before creating a database if the temporary setup port is unavailable.
    with socket.socket() as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        probe.bind(('127.0.0.1', 8091))
    LOCAL.mkdir(parents=True, exist_ok=True)
    LOCAL.chmod(0o700)
    data = make_credentials()
    with CREDENTIALS.open('x') as file:
        os.chmod(CREDENTIALS, 0o600)
        json.dump(data, file, indent=2)
    # Run setup commands without logging their generated password arguments.
    subprocess.run(command() + ['migrate', 'up'], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(command() + ['superuser', 'upsert', 'bootstrap@example.invalid', data['superuser']['password']], check=True, stdout=subprocess.DEVNULL)
    with (LOCAL / 'setup.log').open('w') as log:
        process = start(port=8091, log=log)
        try:
            url = 'http://127.0.0.1:8091'
            wait_ready(url, process)
            admin = Client(url)
            admin.login('bootstrap@example.invalid', data['superuser']['password'], '_superusers')
            provision(admin, data)
            worker = Client(url)
            worker.login(data['worker']['username'], data['worker']['password'])
            worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
            for packet in initial_packets():
                worker.request('POST', '/api/meshlink/worker/ingest', packet)
        finally:
            process.terminate()
            process.wait(timeout=10)
    print('Initialized fictional scenario. Credentials and data are in ignored local-data/backend/.')
    print('Run `python3 backend/manage.py credentials` privately to view portal login details.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['install', 'init-demo', 'serve', 'credentials', 'worker', 'check'])
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()
    if args.action == 'install':
        install()
    elif args.action == 'init-demo':
        initialize()
    elif args.action == 'credentials':
        # Deliberate owner-facing command; never run in CI or paste output into Git.
        data = credentials()
        for key in ['admin', 'member']:
            print(f'{key}: username={data[key]["username"]} password={data[key]["password"]}')
    elif args.action == 'serve':
        process = start()
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            process.wait(timeout=10)
    elif args.action == 'worker':
        from worker import run
        run(once=args.once)
    elif args.action == 'check':
        subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(BACKEND / 'tests'), '-v'], check=True, cwd=ROOT)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, urllib.error.URLError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

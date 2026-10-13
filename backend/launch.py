"""Supervise the three local development processes on Linux, macOS or WSL."""
from contextlib import ExitStack
from datetime import datetime
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

import manage

PORTAL = manage.ROOT / 'portal'
API_PORT = 8090
PORTAL_PORT = 5173


def preflight():
    if os.name != 'posix':
        raise RuntimeError('Use this launcher in Linux, macOS or WSL. Native Windows is not supported.')
    required = [
        (manage.BINARY, 'Run python3 backend/manage.py install first.'),
        (manage.CREDENTIALS, 'Run python3 backend/manage.py init-demo once for a new local backend.'),
        (manage.LOCAL / 'pb_data' / 'data.db', 'Backend initialization is incomplete; inspect the private setup log.'),
        (PORTAL / 'node_modules' / 'vite' / 'bin' / 'vite.js', 'Run npm ci from portal/ first.'),
    ]
    for path, instruction in required:
        if not path.is_file():
            raise RuntimeError(instruction)
    node = shutil.which('node')
    if not node:
        raise RuntimeError('Node is missing. Activate the version in .nvmrc first.')
    version = subprocess.check_output([node, '--version'], text=True).strip()
    parts = tuple(int(part) for part in version.lstrip('v').split('.'))
    if not (22, 23, 1) <= parts < (23, 0, 0):
        raise RuntimeError(f'Node {version} is unsupported. Activate the version in .nvmrc first.')
    for port in (API_PORT, PORTAL_PORT):
        with socket.socket() as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(('127.0.0.1', port))
            except OSError as error:
                raise RuntimeError(f'Port {port} is occupied. Stop the existing process before launching; nothing was stopped.') from error
    return node


def wait_http(url, process, timeout=15):
    deadline = time.monotonic() + timeout
    # Ignore machine proxy settings for these localhost readiness checks.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError('A service exited during startup. Inspect its private log.')
        try:
            with opener.open(url, timeout=.5) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(.1)
    raise RuntimeError(f'Service did not become ready at {url}. Inspect its private log.')


def stop_group(process):
    # Each child owns a separate session. Never signal an unrelated port owner.
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            break
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            process.poll()  # Reap the group leader, including after an early exit.
            try:
                os.killpg(process.pid, 0)
            except ProcessLookupError:
                return
            time.sleep(.05)
    process.wait()


def supervise(node, logs):
    processes = {}
    print(f'Starting local MeshLink. Private logs: {logs}', flush=True)
    with ExitStack() as files:
        def spawn(name, argv, cwd):
            log = files.enter_context((logs / f'{name}.log').open('x'))
            processes[name] = subprocess.Popen(
                argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                env={**os.environ, 'MESHLINK_SIMULATION': '1', 'PYTHONUNBUFFERED': '1'},
                start_new_session=True,
            )
            return processes[name]

        try:
            backend = spawn('backend', manage.command() + [
                'serve', f'--http=127.0.0.1:{API_PORT}',
                f'--origins=http://127.0.0.1:{PORTAL_PORT},http://localhost:{PORTAL_PORT}',
            ], manage.ROOT)
            wait_http(f'http://127.0.0.1:{API_PORT}/api/health', backend)
            spawn('worker', [sys.executable, str(manage.BACKEND / 'worker.py')], manage.ROOT)
            portal = spawn('portal', [node, str(PORTAL / 'node_modules' / 'vite' / 'bin' / 'vite.js'),
                                    '--host', '127.0.0.1', '--port', str(PORTAL_PORT), '--strictPort'], PORTAL)
            wait_http(f'http://127.0.0.1:{PORTAL_PORT}/', portal)
            print(f'Portal: http://127.0.0.1:{PORTAL_PORT} — choose Backend sign in.', flush=True)
            print('Ctrl+C stops all three processes. Simulation is enabled.', flush=True)
            while True:
                for name, process in processes.items():
                    code = process.poll()
                    if code is not None:
                        raise RuntimeError(f'{name} exited (code {code}); stopping the other services. Inspect {logs / (name + ".log")}.')
                time.sleep(.2)
        finally:
            # Let the worker record its disconnected heartbeat while the API lives.
            previous_int = signal.signal(signal.SIGINT, signal.SIG_IGN)
            previous_term = signal.signal(signal.SIGTERM, signal.SIG_IGN)
            try:
                for name in ('worker', 'portal', 'backend'):
                    if name in processes:
                        stop_group(processes[name])
            finally:
                signal.signal(signal.SIGINT, previous_int)
                signal.signal(signal.SIGTERM, previous_term)


def main():
    if os.name != 'posix':
        raise RuntimeError('Use this launcher in Linux, macOS or WSL. Native Windows is not supported.')
    import fcntl
    manage.LOCAL.mkdir(parents=True, exist_ok=True)
    # Lock stays held for the whole run and releases even if the launcher dies.
    with (manage.LOCAL / 'launch.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError('A MeshLink launcher is already running. Stop it before starting another.') from error
        node = preflight()
        logs = manage.LOCAL / 'logs' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        logs.mkdir(parents=True, mode=0o700)
        def interrupt(*_):
            raise KeyboardInterrupt

        previous = signal.signal(signal.SIGTERM, interrupt)
        try:
            supervise(node, logs)
        finally:
            signal.signal(signal.SIGTERM, previous)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nMeshLink stopped. Saved backend data is preserved.')
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

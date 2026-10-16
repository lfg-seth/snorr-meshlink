"""Launcher safety checks with disposable real child processes."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import launch
import demo_database as manage


@unittest.skipUnless(sys.platform != 'win32', 'POSIX process groups required')
class LauncherTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='meshlink-launch-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.addCleanup(patch.stopall)

    def requirements(self):
        patch.object(manage, 'LOCAL', self.root).start()
        patch.object(manage, 'BINARY', self.root / 'pocketbase').start()
        patch.object(manage, 'CREDENTIALS', self.root / 'credentials.json').start()
        patch.object(launch, 'PORTAL', self.root / 'portal').start()
        for path in (manage.BINARY, manage.CREDENTIALS, self.root / 'pb_data' / 'data.db',
                     launch.PORTAL / 'node_modules' / 'vite' / 'bin' / 'vite.js'):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        patch.object(launch.shutil, 'which', return_value='/node').start()
        patch.object(launch.subprocess, 'check_output', return_value='v22.23.1').start()

    def test_missing_setup_does_not_initialize_data(self):
        self.requirements()
        manage.CREDENTIALS.unlink()
        with self.assertRaisesRegex(RuntimeError, 'demo_database.py init'):
            launch.preflight()
        self.assertFalse(manage.CREDENTIALS.exists())

    def test_occupied_port_does_not_stop_existing_service(self):
        self.requirements()
        with socket.socket() as existing:
            existing.bind(('127.0.0.1', 0))
            port = existing.getsockname()[1]
            patch.object(launch, 'API_PORT', port).start()
            existing.listen()
            with self.assertRaisesRegex(RuntimeError, f'Port {port} is occupied'):
                launch.preflight()
            self.assertEqual(existing.getsockname()[1], port)

    def test_second_launcher_refuses_before_preflight(self):
        import fcntl
        patch.object(manage, 'LOCAL', self.root).start()
        with (self.root / 'launch.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with patch.object(launch, 'preflight', side_effect=AssertionError('Must not start')):
                with self.assertRaisesRegex(RuntimeError, 'already running'):
                    launch.main()

    def lifecycle(self, startup_failure=False, worker_exits=False):
        real_popen = subprocess.Popen
        children = []
        names = []

        def spawn(argv, **kwargs):
            name = ('backend', 'worker', 'portal')[len(children)]
            names.append(name)
            code = 'pass' if worker_exits and name == 'worker' else 'import time; time.sleep(60)'
            kwargs['cwd'] = self.root
            child = real_popen([sys.executable, '-c', code], **kwargs)
            children.append(child)
            return child

        def ready(url, process):
            if startup_failure:
                raise RuntimeError('not ready')
            if len(children) == 3:
                if worker_exits:
                    children[1].wait(timeout=5)
                else:
                    raise KeyboardInterrupt

        with patch.object(launch.subprocess, 'Popen', side_effect=spawn), \
                patch.object(launch, 'wait_http', side_effect=ready), redirect_stdout(io.StringIO()):
            with self.assertRaises(RuntimeError if startup_failure or worker_exits else KeyboardInterrupt):
                launch.supervise('/node', self.root)
        self.assertTrue(all(child.poll() is not None for child in children))
        return names

    def test_ctrl_c_stops_all_three_real_processes(self):
        self.assertEqual(self.lifecycle(), ['backend', 'worker', 'portal'])

    def test_child_exit_stops_other_processes(self):
        self.assertEqual(self.lifecycle(worker_exits=True), ['backend', 'worker', 'portal'])

    def test_failed_api_start_never_starts_worker_or_portal(self):
        self.assertEqual(self.lifecycle(startup_failure=True), ['backend'])

    def test_unresponsive_process_is_killed(self):
        child = subprocess.Popen([sys.executable, '-c',
            'import signal,time; signal.signal(signal.SIGINT,signal.SIG_IGN); '
            'signal.signal(signal.SIGTERM,signal.SIG_IGN); print("ready",flush=True); time.sleep(60)'],
            start_new_session=True, stdout=subprocess.PIPE, text=True)
        self.addCleanup(child.stdout.close)
        self.assertEqual(child.stdout.readline().strip(), 'ready')
        launch.stop_group(child)
        self.assertEqual(child.returncode, -signal.SIGKILL)


if __name__ == '__main__':
    unittest.main()

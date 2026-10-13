"""Installer regression tests, including reinstalling a running real executable."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import manage

REAL_BINARY = manage.BINARY


class InstallerTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='meshlink-install-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.binary = self.root / 'bin' / REAL_BINARY.name
        self.binary.parent.mkdir()
        self.addCleanup(patch.stopall)
        patch.object(manage, 'BINARY', self.binary).start()
        patch.object(manage, 'BACKEND', self.root).start()
        patch.object(manage.platform, 'machine', return_value='x86_64').start()
        patch.object(manage.platform, 'system', return_value='Linux').start()

    def archive(self, contents):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            archive.writestr(self.binary.name, contents)
        data = stream.getvalue()
        manifest = {'version': '0.40.5', 'sha256': {
            'pocketbase_0.40.5_linux_amd64.zip': hashlib.sha256(data).hexdigest(),
        }}
        (self.root / 'pocketbase-release.json').write_text(json.dumps(manifest))
        return data

    def install(self, archive):
        with patch.object(manage.urllib.request, 'urlopen', return_value=io.BytesIO(archive)), redirect_stdout(io.StringIO()):
            manage.install()

    def test_verified_repeat_is_offline_and_keeps_existing_executable(self):
        archive = self.archive(b'verified executable')
        self.install(archive)
        previous = self.binary.stat()
        with patch.object(manage.urllib.request, 'urlopen', side_effect=AssertionError('Repeat must not download')), redirect_stdout(io.StringIO()):
            manage.install()
        self.assertEqual(self.binary.read_bytes(), b'verified executable')
        self.assertEqual(self.binary.stat().st_ino, previous.st_ino)
        self.assertEqual(self.binary.stat().st_mtime_ns, previous.st_mtime_ns)

    def test_missing_receipt_verifies_identical_binary_without_replacing_it(self):
        contents = b'existing executable'
        archive = self.archive(contents)
        self.binary.write_bytes(contents)
        previous = self.binary.stat()
        self.install(archive)
        self.assertEqual(self.binary.stat().st_ino, previous.st_ino)
        self.assertEqual(self.binary.stat().st_mtime_ns, previous.st_mtime_ns)
        self.assertTrue(manage.install_receipt_path().is_file())

    def test_checksum_failure_leaves_existing_binary_untouched(self):
        self.archive(b'new executable')
        self.binary.write_bytes(b'old executable')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.install(b'corrupted download')
        self.assertEqual(self.binary.read_bytes(), b'old executable')
        self.assertFalse(manage.install_receipt_path().exists())

    def test_locked_replacement_preserves_existing_binary_and_cleans_staging_file(self):
        archive = self.archive(b'new executable')
        self.binary.write_bytes(b'old executable')
        with patch.object(manage.os, 'replace', side_effect=PermissionError('Executable locked')):
            with self.assertRaisesRegex(RuntimeError, 'Stop the backend'):
                self.install(archive)
        self.assertEqual(self.binary.read_bytes(), b'old executable')
        self.assertEqual(list(self.binary.parent.iterdir()), [self.binary])

    def test_tampered_binary_is_replaced_from_verified_archive(self):
        archive = self.archive(b'verified executable')
        self.install(archive)
        self.binary.write_bytes(b'changed executable')
        self.install(archive)
        self.assertEqual(self.binary.read_bytes(), b'verified executable')
        if sys.platform != 'win32':
            self.assertEqual(self.binary.stat().st_mode & 0o777, 0o755)

    def test_reinstall_while_actual_pocketbase_is_running(self):
        # This would raise ETXTBSY with the old write_bytes installer on Linux.
        contents = REAL_BINARY.read_bytes()
        archive = self.archive(contents)
        shutil.copy2(REAL_BINARY, self.binary)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        process = subprocess.Popen([str(self.binary), 'serve', f'--http=127.0.0.1:{port}',
                                    f'--dir={self.root / "data"}', '--hooksWatch=false'],
                                   cwd=self.root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            manage.wait_ready(f'http://127.0.0.1:{port}', process)
            inode = self.binary.stat().st_ino
            self.install(archive)
            self.assertIsNone(process.poll())
            self.assertEqual(self.binary.stat().st_ino, inode)
            manage.Client(f'http://127.0.0.1:{port}').request('GET', '/api/health')
        finally:
            process.terminate()
            process.wait(timeout=10)


if __name__ == '__main__':
    unittest.main()

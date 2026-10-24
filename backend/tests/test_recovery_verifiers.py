"""Recovery assertions must accept provisioned fleets and bounded saved history."""
from contextlib import closing, ExitStack, redirect_stdout
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
import sqlite3
import tempfile
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend'))
sys.path.insert(0, str(ROOT / 'deploy/portal'))


def load_script(filename):
    spec = importlib.util.spec_from_file_location(filename.replace('-', '_'), ROOT / 'deploy/portal' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReachedNextCheck(Exception):
    pass


class VerifierCallSiteTests(unittest.TestCase):
    def test_live_accepts_the_one_member_provisioned_fleet(self):
        module = load_script('verify.py')
        state = {'simulation': False, 'trackers': [{'id': 'b002'}],
                 'infrastructure': [{'id': 'g003'}], 'members': []}
        client = Mock()
        client.request.return_value = state
        def urlopen(request, **kwargs):
            if isinstance(request, str):
                return io.BytesIO(b'<meta name="meshlink-portal-mode" content="live">')
            raise ReachedNextCheck('device checks reached authentication isolation')
        statuses = {'/': 200, '/map': 200, '/api/health': 200, '/api/meshlink/state': 401}
        with ExitStack() as stack:
            stack.enter_context(patch.object(sys, 'argv', ['verify.py']))
            stack.enter_context(patch.object(module, 'status', side_effect=lambda base, path: statuses.get(path, 404)))
            stack.enter_context(patch.object(module, 'Client', return_value=client))
            stack.enter_context(patch.object(Path, 'read_text', return_value=json.dumps({'admin': {'username': 'fixture', 'password': 'fixture'}})))
            stack.enter_context(patch.object(module.urllib.request, 'urlopen', side_effect=urlopen))
            stack.enter_context(patch.object(module.time, 'sleep'))
            stack.enter_context(patch.object(module, 'device_ids', create=True,
                return_value={'trackers': {'b002'}, 'infrastructure': {'g003'}}))
            stack.enter_context(patch.object(module, 'expected_infrastructure', create=True, return_value={'g003', 'retired'}))
            stack.enter_context(redirect_stdout(io.StringIO()))
            with self.assertRaises(ReachedNextCheck):
                module.main()

    def test_demo_accepts_a_full_bounded_window_before_isolation_checks(self):
        module = load_script('verify-demo.py')
        at = datetime(2026, 10, 24, tzinfo=timezone.utc)
        samples = [{'at': (at + timedelta(seconds=i)).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
                    'volts': 3.7} for i in range(50000)]
        state = {'simulation': True, 'feedOnline': True, 'trackers': [{}] * 6,
                 'infrastructure': [{}] * 4, 'links': [{}] * 10}
        state['trackers'] = [{'id': f'd{i}'} for i in range(6)]
        state['infrastructure'] = [{'id': f'r{i}'} for i in range(4)]
        client = Mock()
        client.request.side_effect = lambda method, path: state if path.endswith('/state') else {'samples': samples, 'truncated': True}
        def status(value, path):
            if path == '/api/health': return 200
            if path == '/api/meshlink/state':
                if getattr(value, 'token', None) is not None:
                    raise ReachedNextCheck('bounded history reached live-token isolation')
                return 401
            return 404
        client.token = None
        with patch.object(module, 'Client', return_value=client), patch.object(module, 'status', side_effect=status), \
             patch.object(module, 'device_ids', return_value={key: {d['id'] for d in state[key]} for key in ('trackers', 'infrastructure')}), \
             redirect_stdout(io.StringIO()):
            # The second Client is assigned the demo token before this check.
            client.login.side_effect = lambda *args: setattr(client, 'token', 'fixture-token')
            with self.assertRaises(ReachedNextCheck):
                module.main()


from recovery_checks import assert_device_ids, assert_history_shape, assert_saved_history, device_ids


class RecoveryAssertionsTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.execute('CREATE TABLE observations (id TEXT, deviceId TEXT, measuredAt TEXT, receivedAt TEXT, timestampQuality TEXT, payload TEXT)')
        self.end = datetime(2026, 10, 24, tzinfo=timezone.utc)

    def insert(self, number, at=None, measured=True, voltage=3.7, device='r1'):
        at = at or self.end - timedelta(seconds=number)
        stamp = at.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        row = (f'{number:08}', device, stamp if measured else '', stamp, 'valid' if measured else 'unknown', json.dumps({'battery': voltage}))
        self.db.execute('INSERT INTO observations VALUES (?,?,?,?,?,?)', row)
        return {'at': stamp, 'volts': voltage, 'measuredAt': row[2] or None,
                'receivedAt': stamp, 'timestampQuality': row[4]}

    def check(self, samples, truncated=False, hours=24, started=None, finished=None):
        return assert_saved_history({'samples': samples, 'truncated': truncated}, self.db, 'r1', hours,
                                    started or self.end, finished or self.end)

    def test_device_inventory_is_read_only_and_all_counts_are_valid(self):
        (ROOT / 'local-data').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / 'local-data') as tmp:
            path = Path(tmp) / 'data.db'
            with closing(sqlite3.connect(path)) as db:
                db.execute('CREATE TABLE devices (key TEXT, kind TEXT)')
                db.executemany('INSERT INTO devices VALUES (?,?)', [('b002', 'member'), ('g003', 'gateway'), ('r006', 'repeater')])
                db.commit()
            before = path.read_bytes()
            expected = device_ids(path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(expected, {'trackers': {'b002'}, 'infrastructure': {'g003', 'r006'}})
            snapshot = {key: [{'id': value} for value in values] for key, values in expected.items()}
            assert_device_ids(snapshot, expected)
            for bad in [[], [{'id': 'retired'}], snapshot['trackers'] * 2]:
                with self.assertRaises(AssertionError):
                    assert_device_ids({**snapshot, 'trackers': bad}, expected)
            assert_device_ids({'trackers': [], 'infrastructure': []}, {'trackers': set(), 'infrastructure': set()})
            with self.assertRaises(sqlite3.OperationalError):
                device_ids(Path(tmp) / 'missing.db')
            self.assertFalse((Path(tmp) / 'missing.db').exists())

    def test_exact_cap_and_over_cap_select_newest_rows_with_correct_flag(self):
        rows = [self.insert(i) for i in range(50000)]
        expected = list(reversed(rows))
        self.assertEqual(self.check(expected), 50000)
        with self.assertRaises(AssertionError):
            self.check(expected, True)
        self.insert(50000)
        self.assertEqual(self.check(expected, True), 50001)
        for wrong, flag in [(expected, False), (list(reversed(expected)), True),
                            (expected[:-1], True), ([{**expected[0], 'volts': 4.2}, *expected[1:]], True),
                            ([expected[0], *expected], True)]:
            with self.assertRaises(AssertionError):
                self.check(wrong, flag)

    def test_small_history_all_windows_and_missing_history(self):
        rows = [self.insert(0), self.insert(1), self.insert(2)]
        for hours in (24, 168, 720):
            self.assertEqual(self.check(list(reversed(rows)), hours=hours), 3)
        for bad in [[], rows, [rows[0]], [{**rows[0], 'volts': 0}], [{**rows[0], 'volts': float('nan')}]]:
            with self.assertRaises(AssertionError):
                self.check(bad)

    def test_receipt_fallback_ties_and_metadata_match_saved_values(self):
        measured = self.insert(1, at=self.end)
        receipt = self.insert(2, at=self.end, measured=False)
        # Stable API merge puts measured before receipt in descending order;
        # reversing for display therefore puts the receipt-only row first.
        expected = [receipt, measured]
        self.assertEqual(self.check(expected), 2)
        with self.assertRaises(AssertionError):
            self.check(list(reversed(expected)))
        with self.assertRaises(AssertionError):
            self.check([{**receipt, 'timestampQuality': 'valid'}, measured])

    def test_request_boundary_uses_exact_possible_window_without_tolerance(self):
        edge = self.insert(1, at=self.end - timedelta(hours=24))
        middle = self.insert(2, at=self.end - timedelta(hours=1))
        future = self.insert(3, at=self.end + timedelta(milliseconds=1))
        self.insert(4, at=self.end - timedelta(hours=25))
        self.insert(5, voltage=0)
        self.insert(6, device='other')
        self.assertEqual(self.check([edge, middle]), 2)
        after = self.end + timedelta(milliseconds=2)
        self.assertEqual(self.check([middle, future], started=self.end, finished=after), 2)
        with self.assertRaises(AssertionError):
            self.check([edge, middle, future], started=after, finished=after)

    def test_legacy_measured_only_backup_and_shape_validation(self):
        saved = self.insert(1)
        self.insert(2, measured=False)
        legacy = {key: saved[key] for key in ('at', 'volts')}
        self.assertEqual(self.check([legacy]), 1)
        for response in [{'samples': [legacy], 'truncated': 1},
                         {'samples': [legacy], 'truncated': True},
                         {'samples': [], 'truncated': False}]:
            with self.assertRaises(AssertionError):
                assert_history_shape(response)

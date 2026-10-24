"""The tracked synthetic DB must be inspectable, persistent and isolated."""
import hashlib
from contextlib import closing
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import demo_database as demo
import manage
from client import ApiError, Client


class DemoDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='meshlink-demo-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.runtime = self.root / 'runtime'
        demo.initialize(self.runtime)
        self.data = self.runtime / 'pb_data'
        self.log = (self.root / 'server.log').open('w')
        self.addCleanup(self.log.close)
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            self.port = probe.getsockname()[1]
        self.process = manage.start(self.data, self.port, self.log)
        self.addCleanup(self.stop)
        self.url = f'http://127.0.0.1:{self.port}'
        manage.wait_ready(self.url, self.process)
        self.admin = Client(self.url)
        self.admin.login('meshlink-admin', demo.DEMO_PASSWORD)
        self.owner = Client(self.url)
        self.owner.login('demo-admin@example.invalid', demo.DEMO_PASSWORD, '_superusers')
        self.owner.request('PATCH', '/api/settings', {'rateLimits': {'enabled': False}})

    def stop(self):
        if self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=10)

    def assert_feature_examples(self):
        state = self.admin.request('GET', '/api/meshlink/state')
        trackers = {row['id']: row for row in state['trackers']}
        infra = {row['id']: row for row in state['infrastructure']}
        with self.subTest(feature='member battery voltage and configured pack'):
            self.assertEqual(trackers['d1']['batteryProfile'], 'lipo-1s')
            self.assertEqual(trackers['d1']['batteryCapacityMah'], 3000)
            self.assertGreater(trackers['d1']['batteryVoltage'], 3)
            self.assertEqual(trackers['d1']['batteryTimestampQuality'], 'valid')
            self.assertIsNone(trackers['d6']['batteryVoltage'])
        with self.subTest(feature='infrastructure charge estimate'):
            self.assertEqual(infra['r1']['batteryProfile'], 'eve-26v-1s')
        with self.subTest(feature='weather humidity'):
            self.assertEqual(infra['r1']['humidity'], 42)
            self.assertIsNone(infra['r2']['humidity'])
        with self.subTest(feature='signed sensor power and channel identity'):
            readings = {r['metric']: r for r in infra['r1']['powerReadings']}
            self.assertLess(readings['power1CurrentMa']['value'], 0)
            self.assertGreater(readings['power1CurrentMa']['rawValue'], 0)
            self.assertGreater(readings['power3CurrentMa']['value'], 0)
            self.assertLess(readings['power3CurrentMa']['rawValue'], 0)
            self.assertEqual(readings['sensorCurrentMa']['value'], 0)
            self.assertTrue(all(r['timestampQuality'] == 'valid' for r in readings.values()))
            self.assertEqual(infra['b2']['powerReadings'], [])
        with self.subTest(feature='SNNS hearing age, counts and report coverage'):
            rows = [r for r in state['links'] if r.get('reportType') == 'snns-v1']
            self.assertGreaterEqual(len(rows), 3)
            self.assertEqual({r['subset'] for r in rows}, {True, False})
            self.assertTrue(any(r['capacityEvicted'] for r in rows))
            self.assertTrue(any(r['snrDb'] == 0 for r in rows))
            for row in rows:
                self.assertIsNotNone(row['rssiDbm'])
                self.assertIsNone(row['observedAt'])
                self.assertGreater(row['observationCount'], 0)
                self.assertGreaterEqual(row['hearingAgeSeconds'], 0)
                self.assertIn(row['transportGatewayId'], ['b1', 'b2'])

    def test_checkpoint_has_examples_for_current_portal_features(self):
        self.assert_feature_examples()

    def test_simulation_keeps_new_telemetry_fresh(self):
        before = self.admin.request('GET', '/api/meshlink/state')
        subprocess.run([sys.executable, str(demo.BACKEND / 'worker.py'), '--once'], check=True,
                       env={**os.environ, 'MESHLINK_API_URL': self.url,
                            'MESHLINK_WORKER_CREDENTIALS': str(self.runtime / 'worker.json')},
                       stdout=subprocess.DEVNULL)
        self.assert_feature_examples()
        state = self.admin.request('GET', '/api/meshlink/state')
        self.assertEqual(len(state['links']), 13)  # Worker must not duplicate saved reports.
        for key in ['d1', 'd2', 'd3']:
            old = next(t for t in before['trackers'] if t['id'] == key)
            new = next(t for t in state['trackers'] if t['id'] == key)
            self.assertGreater(new['batteryMeasuredAt'], old['batteryMeasuredAt'])
        old = next(d for d in before['infrastructure'] if d['id'] == 'r1')
        new = next(d for d in state['infrastructure'] if d['id'] == 'r1')
        for metric in ['humidity', 'power1CurrentMa', 'power3CurrentMa', 'sensorCurrentMa']:
            self.assertGreater(new['readingTimes'][metric], old['readingTimes'][metric])

    def test_frontend_snapshot_reads_saved_links_and_dashboard_edits_survive_restart(self):
        seed_digest = hashlib.sha256((demo.SEED / 'data.db').read_bytes()).hexdigest()
        state = self.admin.request('GET', '/api/meshlink/state')
        self.assertTrue(state['simulation'])
        self.assertEqual(len(state['links']), 13)
        self.assertEqual(len(state['trackers']), 6)
        self.assertEqual(len(state['infrastructure']), 4)
        self.assertTrue(any(row['snrDb'] == 0 for row in state['links']))
        self.assertTrue(any(row['heardDeviceId'] is None and row['path'] == 'relayed' for row in state['links']))
        self.assertTrue(all(row['rssiDbm'] is None and row['observedAt'] is None
                            for row in state['links'] if row['source'] == 'neighbor' and row.get('reportType') != 'snns-v1'))
        self.assertEqual(next(t for t in state['trackers'] if t['id'] == 'd1')['battery'], 100)
        row = state['links'][0]
        self.owner.request('PATCH', f'/api/collections/link_observations/records/{row["id"]}',
                           {'signal': {'snrDb': 3.25, 'rssiDbm': -101}})
        self.admin.request('POST', '/api/meshlink/assign', {'deviceId': 'd6', 'memberId': 'm5'})
        self.stop()
        self.process = manage.start(self.data, self.port, self.log)
        manage.wait_ready(self.url, self.process)
        restored = self.admin.request('GET', '/api/meshlink/state')
        self.assertEqual(next(r for r in restored['links'] if r['id'] == row['id'])['snrDb'], 3.25)
        self.assertTrue(any(a['deviceId'] == 'd6' and a['memberId'] == 'm5' and not a['endedAt']
                            for a in restored['assignments']))
        with closing(sqlite3.connect(self.data / 'data.db')) as database:
            self.assertEqual(json.loads(database.execute('SELECT signal FROM link_observations WHERE id=?',
                                                       (row['id'],)).fetchone()[0])['rssiDbm'], -101)
        self.assertEqual(hashlib.sha256((demo.SEED / 'data.db').read_bytes()).hexdigest(), seed_digest)

    def test_link_access_is_authenticated_and_collection_writes_stay_locked(self):
        for client in [Client(self.url), self.admin]:
            with self.assertRaises(ApiError):
                client.request('GET', '/api/collections/link_observations/records')
            with self.assertRaises(ApiError):
                client.request('POST', '/api/collections/link_observations/records', next(demo.links()))
        with self.assertRaises(ApiError):
            Client(self.url).request('GET', '/api/meshlink/state')
        member = Client(self.url)
        member.login('meshlink-member', demo.DEMO_PASSWORD)
        self.assertEqual(len(member.request('GET', '/api/meshlink/state')['links']), 13)
        worker = Client(self.url)
        worker.login('meshlink-worker', demo.DEMO_PASSWORD)
        with self.assertRaises(ApiError):
            worker.request('GET', '/api/meshlink/state')

    def test_battery_history_has_solar_cycles_decline_and_authenticated_time_windows(self):
        from datetime import datetime
        history = {}
        for device in ['r1', 'r2', 'b1']:
            lengths = []
            for hours in [24, 168, 720]:
                result = self.admin.request('GET', f'/api/meshlink/battery-history/{device}?hours={hours}')
                self.assertFalse(result['truncated'])
                samples = result['samples']
                lengths.append(len(samples))
                self.assertGreater(len(samples), hours * 5)
                self.assertEqual(samples, sorted(samples, key=lambda s: s['at']))
                history[device] = samples
            self.assertLess(lengths[0], lengths[1])
            self.assertLess(lengths[1], lengths[2])
        healthy, deficit = history['r1'], history['r2']
        for samples in [healthy, deficit]:
            deltas = [b['volts'] - a['volts'] for a, b in zip(samples, samples[1:])]
            self.assertTrue(any(d > 0 for d in deltas), 'daytime charging')
            self.assertTrue(any(d < 0 for d in deltas), 'overnight drain')
            self.assertGreater((datetime.fromisoformat(samples[-1]['at']) -
                                datetime.fromisoformat(samples[0]['at'])).total_seconds(), 29 * 86400)
        self.assertLess(abs(healthy[-1]['volts'] - healthy[0]['volts']), .02)
        self.assertLess(deficit[-1]['volts'] - deficit[0]['volts'], -.45)
        for suffix in ['r1?hours=1', 'd1?hours=24', 'missing?hours=24']:
            with self.assertRaises(ApiError):
                self.admin.request('GET', '/api/meshlink/battery-history/' + suffix)
        worker = Client(self.url)
        worker.login('meshlink-worker', demo.DEMO_PASSWORD)
        for client in [Client(self.url), worker]:
            with self.assertRaises(ApiError):
                client.request('GET', '/api/meshlink/battery-history/r1?hours=24')
        member = Client(self.url)
        member.login('meshlink-member', demo.DEMO_PASSWORD)
        self.assertGreater(len(member.request('GET', '/api/meshlink/battery-history/r1')['samples']), 100)

    def test_init_preserves_existing_runtime_and_unseeded_schema_has_no_samples(self):
        with self.assertRaisesRegex(ValueError, 'Existing demo runtime'):
            demo.initialize(self.runtime)
        empty = self.root / 'unseeded'
        subprocess.run(manage.command(empty) + ['migrate', 'up'], check=True, stdout=subprocess.DEVNULL)
        with closing(sqlite3.connect(empty / 'data.db')) as database:
            self.assertEqual(database.execute('SELECT COUNT(*) FROM link_observations').fetchone()[0], 0)
            self.assertEqual(database.execute('SELECT COUNT(*) FROM devices').fetchone()[0], 0)
            self.assertEqual(database.execute('SELECT COUNT(*) FROM accounts').fetchone()[0], 0)
        self.assertEqual(json.loads((demo.SEED / 'manifest.json').read_text())['sha256'],
                         hashlib.sha256((demo.SEED / 'data.db').read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()

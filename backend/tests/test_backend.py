"""Integration tests against the actual pinned PocketBase binary and fresh databases."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import socket
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from client import ApiError, Client
from fixtures import at, initial_packets, packet, provision
from manage import BINARY, command, make_credentials, start, wait_ready


class BackendTests(unittest.TestCase):
    def test_unknown_clock_humidity_updates_without_replacing_known_measurements(self):
        first = packet('r1', 'telemetry', {'temperature': 23, 'humidity': 35}, gateway='b1')
        first['measuredAt'] = None
        self.assertEqual(self.ingest(first)['outcome'], 'accepted')
        later = {**packet('r1', 'telemetry', {'humidity': 36}, gateway='b1'), 'measuredAt': None}
        self.assertEqual(self.ingest(later)['outcome'], 'accepted')
        row = next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')
        self.assertEqual(row['humidity'], 36)
        self.assertIsNone(row['readingTimes']['humidity'])
        self.assertTrue(row['lastContactAt'])
        known = packet('r1', 'telemetry', {'humidity': 40}, gateway='b1')
        self.assertEqual(self.ingest(known)['outcome'], 'accepted')
        self.assertEqual(self.ingest({**later, 'packetId': 'unknown-late'})['outcome'], 'accepted')
        self.assertEqual(next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')['humidity'], 40)
        with self.assertRaises(ApiError):
            self.ingest(packet('r1', 'telemetry', {'humidity': 101}, gateway='b1'))

    def test_live_cutover_transaction_and_real_gps_receipts(self):
        import json
        migrations = self.data / 'cutover-migrations'
        migrations.mkdir()
        source = Path(__file__).resolve().parents[2] / 'deploy/portal/live-cutover.js'
        shutil.copyfile(source, migrations / '1792010000_live_cutover.js')
        config = {'members': {'!699c2ed8': 'b001', '!699ca878': 'b002'},
                  'gateways': {'!9ea13cc0': 'g001', '!849ad7a0': 'g002'},
                  'identities': {}}
        settings = self.data / 'mqtt.json'
        settings.write_text(json.dumps(config))
        self.stop()
        cmd = [x for x in command(self.data) if not x.startswith('--migrationsDir=')]
        cmd += [f'--migrationsDir={migrations}', 'migrate', 'up']
        env = {**os.environ, 'MESHLINK_MQTT_CONFIG': str(settings)}
        failed = subprocess.run(cmd, env=env, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        # Missing physical identity is discovered after deletes; transaction must
        # restore the complete fictional input, including accounts/members.
        import sqlite3
        with sqlite3.connect(self.data / 'data.db') as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM devices').fetchone()[0], 10)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM members').fetchone()[0], 5)
        for node_id, key in {**config['members'], **config['gateways']}.items():
            config['identities'][key] = {'hardwareId': f'test-{key}', 'nodeId': node_id,
                                         'shortName': key.upper()}
        settings.write_text(json.dumps(config))
        subprocess.run(cmd, env=env, check=True, stdout=subprocess.DEVNULL)
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.assertEqual({d['key'] for d in self.records('devices')}, {'b001', 'b002', 'g001', 'g002'})
        self.assertFalse(self.records('members'))
        self.assertEqual(len([a for a in self.records('accounts') if a['role'] == 'disabled']), 2)
        # The ordinary normalized boundary now stores real mapped device keys.
        item = packet('b001', 'position', {'latitude': 36.2, 'longitude': -115.6}, gateway='g001')
        self.assertEqual(self.ingest(item)['outcome'], 'accepted')
        self.assertEqual(self.ingest({**item, 'gatewayId': 'g002'})['outcome'], 'duplicate')
        self.assertEqual(len(self.records('positions')), 1)
        self.assertEqual(len(self.records('packet_receipts')), 2)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='meshlink-test-')
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.credentials = make_credentials()
        subprocess.run(command(self.data) + ['migrate', 'up'], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(command(self.data) + ['superuser', 'upsert', '--', 'bootstrap@example.invalid', self.credentials['superuser']['password']], check=True, stdout=subprocess.DEVNULL)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        self.log = (self.data / 'server.log').open('w')
        self.addCleanup(self.log.close)
        self.process = start(self.data, port, self.log)
        self.addCleanup(self.stop)
        self.url = f'http://127.0.0.1:{port}'
        wait_ready(self.url, self.process)
        self.superuser = Client(self.url)
        self.superuser.login('bootstrap@example.invalid', self.credentials['superuser']['password'], '_superusers')
        # Disable rate throttling only in disposable test DBs, so rapid role logins do not mask authorization results.
        self.superuser.request('PATCH', '/api/settings', {'rateLimits': {'enabled': False}})
        provision(self.superuser, self.credentials)
        self.admin = self.login('admin')
        self.member = self.login('member')
        self.member2 = self.login('member2')
        self.worker = self.login('worker')
        self.worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})

    def stop(self):
        if self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=10)

    def login(self, key):
        client = Client(self.url)
        data = self.credentials[key]
        client.login(data['username'], data['password'])
        return client

    def state(self):
        return self.admin.request('GET', '/api/meshlink/state')

    def ingest(self, item):
        return self.worker.request('POST', '/api/meshlink/worker/ingest', item)

    def records(self, collection):
        return self.superuser.request('GET', f'/api/collections/{collection}/records?perPage=500')['items']

    def denied(self, status, client, method, path, body=None):
        with self.assertRaises(ApiError) as raised:
            client.request(method, path, body)
        self.assertEqual(raised.exception.status, status)

    def test_roles_and_collection_bypass(self):
        self.denied(401, Client(self.url), 'GET', '/api/meshlink/state')
        self.denied(403, self.worker, 'GET', '/api/meshlink/state')
        self.denied(403, self.member, 'POST', '/api/meshlink/rules', {'deviceId': 'r1', 'trigger': 3.5, 'recovery': 3.7})
        self.denied(403, self.admin, 'POST', '/api/meshlink/worker/ingest', {})
        self.denied(403, self.admin, 'POST', '/api/collections/devices/records', {'key': 'intruder', 'kind': 'member'})
        self.denied(403, self.member, 'POST', '/api/meshlink/assign', {'deviceId': 'd5', 'memberId': 'm1'})
        member = next(a for a in self.records('accounts') if a['memberId'] == 'm5')
        self.denied(403, self.member, 'PATCH', f'/api/collections/accounts/records/{member["id"]}', {'role': 'admin'})
        self.assertFalse(self.records('packet_receipts'))

    def test_duplicate_receipts_delayed_fixes_and_unknown_timestamp(self):
        newest = packet('d1', 'position', {'latitude': 36.2, 'longitude': -115.6}, 1, 'same-packet')
        self.ingest(newest)
        duplicate = {**newest, 'gatewayId': 'b2', 'receivedAt': at()}
        self.assertEqual(self.ingest(duplicate)['outcome'], 'duplicate')
        delayed = packet('d1', 'position', {'latitude': 36.8, 'longitude': -115.9}, 25)
        self.ingest(delayed)
        self.ingest(packet('d1', 'position', {'latitude': 36.9, 'longitude': -115.9}, None))
        tracker = self.state()['trackers'][0]
        self.assertEqual(tracker['position']['latitude'], 36.2)
        self.assertEqual(tracker['position']['measuredAt'], newest['measuredAt'])
        self.assertEqual(len(self.records('positions')), 3)
        self.assertEqual(len(self.records('packet_receipts')), 4)
        self.assertEqual(tracker['lastContactAt'], self.records('devices')[0].get('lastContactAt', tracker['lastContactAt']))

    def test_rejected_packets_retain_receipt_without_poisoning_position(self):
        self.denied(400, self.worker, 'POST', '/api/meshlink/worker/ingest', packet('d1', 'position', {'latitude': 400, 'longitude': 0}))
        self.assertEqual(self.records('packet_receipts')[0]['outcome'], 'rejected')
        self.assertFalse(self.records('positions'))
        unknown = packet('d5', 'position', {'latitude': 36.2, 'longitude': -115.6}, None)
        unknown['measuredAt'] = 'not-a-timestamp'
        self.ingest(unknown)
        p = next(t for t in self.state()['trackers'] if t['id'] == 'd5')['position']
        self.assertIsNone(p['measuredAt'])
        self.assertEqual(p['timestampQuality'], 'invalid')
        self.assertTrue(self.state()['trackers'][-1]['position'] is None)

    def test_transactional_transfer_and_historical_attribution(self):
        before = packet('d1', 'position', {'latitude': 36.2, 'longitude': -115.6}, 1)
        self.ingest(before)
        self.admin.request('POST', '/api/meshlink/assign', {'deviceId': 'd1', 'memberId': 'm2'})
        state = self.state()
        active = [a for a in state['assignments'] if not a['endedAt']]
        self.assertEqual(len([a for a in active if a['memberId'] == 'm2']), 1)
        self.assertEqual(next(a for a in active if a['deviceId'] == 'd1')['memberId'], 'm2')
        self.assertFalse(any(a['deviceId'] == 'd2' for a in active))
        self.assertEqual(self.records('positions')[0]['memberId'], 'm1')
        self.assertEqual(state['trackers'][0]['shortName'], 'S001')
        self.assertEqual(len(state['nameJobs']), 2)
        self.assertTrue(next(a for a in state['assignments'] if a['memberId'] == 'm1')['endedAt'])

    def test_two_members_cannot_claim_one_tracker_concurrently(self):
        self.member2.request('POST', '/api/meshlink/release', {'deviceId': 'd2'})
        barrier = threading.Barrier(2)
        def claim(client, member_id):
            barrier.wait()
            try:
                client.request('POST', '/api/meshlink/assign', {'deviceId': 'd5', 'memberId': member_id})
                return 200
            except ApiError as error:
                return error.status
        with ThreadPoolExecutor(max_workers=2) as pool:
            a = pool.submit(claim, self.member, 'm5')
            b = pool.submit(claim, self.member2, 'm2')
            outcomes = sorted([a.result(), b.result()])
        self.assertEqual(outcomes, [200, 409])
        self.assertEqual(len([a for a in self.state()['assignments'] if a['deviceId'] == 'd5' and not a['endedAt']]), 1)

    def test_outage_never_submits_message_and_uses_single_gateway(self):
        self.admin.request('POST', '/api/meshlink/demo/feed', {'online': False})
        self.denied(409, self.member, 'POST', '/api/meshlink/messages', {'text': 'Unsent draft'})
        self.assertFalse(self.records('send_attempts'))
        self.admin.request('POST', '/api/meshlink/demo/feed', {'online': True})
        self.assertFalse(self.state()['messages'])
        self.member.request('POST', '/api/meshlink/messages', {'text': 'Manual send'})
        message = self.state()['messages'][0]
        self.assertEqual(message['text'], 'Demo Casey: Manual send')
        self.assertIn('unconfirmed', message['evidence'])
        self.assertEqual(self.records('send_attempts')[0]['gatewayId'], 'b1')

    def test_intrusion_latches_normal_ack_resolution_and_grouping(self):
        item = packet('r1', 'telemetry', {'intrusion': True}, 1, 'intrusion')
        self.ingest(item); self.ingest(item)
        self.ingest(packet('r1', 'telemetry', {'intrusion': True}, .8))
        self.ingest(packet('r1', 'telemetry', {'intrusion': False}, .5))
        self.assertEqual(len(self.state()['incidents']), 1)
        incident = self.state()['incidents'][0]
        self.member.request('POST', f'/api/meshlink/incidents/{incident["id"]}', {'action': 'acknowledge'})
        self.assertIsNone(self.state()['incidents'][0]['resolvedAt'])
        self.denied(403, self.member, 'POST', f'/api/meshlink/incidents/{incident["id"]}', {'action': 'resolve', 'note': 'Unauthorized'})
        self.denied(400, self.admin, 'POST', f'/api/meshlink/incidents/{incident["id"]}', {'action': 'resolve', 'note': ''})
        self.admin.request('POST', f'/api/meshlink/incidents/{incident["id"]}', {'action': 'resolve', 'note': 'Training inspection complete'})
        self.ingest(packet('r1', 'telemetry', {'intrusion': True}, .1))
        self.assertEqual(len(self.state()['incidents']), 2)
        self.ingest(packet('r2', 'telemetry', {'intrusion': True}, .1))
        self.assertEqual(len(self.state()['incidents']), 2)  # r2 is not equipped.

    def test_low_battery_requires_fresh_recovery_not_replay_or_ack(self):
        self.admin.request('POST', '/api/meshlink/rules', {'deviceId': 'r1', 'trigger': 3.6, 'recovery': 3.8})
        self.ingest(packet('r1', 'telemetry', {'battery': 3.5}, 1))
        warning = next(w for w in self.state()['warnings'] if w['kind'] == 'battery')
        self.member.request('POST', f'/api/meshlink/warnings/{warning["id"]}/ack', {})
        self.ingest(packet('r1', 'telemetry', {'battery': 4.1}, 20))
        self.assertIsNone(next(w for w in self.state()['warnings'] if w['id'] == warning['id'])['recoveredAt'])
        self.admin.request('POST', '/api/meshlink/demo/feed', {'online': False})
        self.worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
        self.assertIsNone(self.state()['warnings'][0]['recoveredAt'])
        self.admin.request('POST', '/api/meshlink/demo/feed', {'online': True})
        self.ingest(packet('r1', 'telemetry', {'battery': 3.9}, .1))
        self.assertTrue(next(w for w in self.state()['warnings'] if w['id'] == warning['id'])['recoveredAt'])

    def test_cadence_missing_capabilities_feed_suppression_and_reconnect_grace(self):
        # Move only monitoring/restore clocks in this isolated test DB; routes never accept a client clock.
        for device in self.records('devices'):
            self.superuser.request('PATCH', f'/api/collections/devices/records/{device["id"]}', {'monitoringStartedAt': at(60)})
        feed = self.records('feed')[0]
        self.superuser.request('PATCH', f'/api/collections/feed/records/{feed["id"]}', {'restoredAt': at(60)})
        self.worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
        warnings = self.state()['warnings']
        self.assertEqual({w['kind'] for w in warnings if w['deviceId'] == 'r2'}, {'missing:battery', 'missing:solar'})
        self.assertEqual({w['kind'] for w in warnings if w['deviceId'] == 'b2'}, {'missing:battery'})
        count = len(warnings)
        self.admin.request('POST', '/api/meshlink/demo/feed', {'online': False})
        self.worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
        self.assertEqual(len(self.state()['warnings']), count)
        self.admin.request('POST', '/api/meshlink/demo/feed', {'online': True})
        self.worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
        self.assertTrue(all(not w['recoveredAt'] for w in self.state()['warnings']))
        self.ingest(packet('r2', 'telemetry', {'battery': 3.9}, .1))
        warning = next(w for w in self.state()['warnings'] if w['deviceId'] == 'r2' and w['kind'] == 'missing:battery')
        self.assertTrue(warning['recoveredAt'])
        self.assertTrue(next(w for w in self.state()['warnings'] if w['deviceId'] == 'r2' and w['kind'] == 'missing:solar')['recoveredAt'] is None)

    def test_stale_name_job_cannot_confirm_after_reassignment(self):
        self.admin.request('POST', '/api/meshlink/assign', {'deviceId': 'd5', 'memberId': 'm5'})
        old = self.state()['nameJobs'][0]
        self.admin.request('POST', '/api/meshlink/assign', {'deviceId': 'd5', 'memberId': 'm2'})
        self.denied(409, self.admin, 'POST', '/api/meshlink/demo/name-job', {'deviceId': 'd5', 'jobId': old['id'], 'status': 'confirmed'})
        latest = [j for j in self.state()['nameJobs'] if j['deviceId'] == 'd5'][-1]
        self.admin.request('POST', '/api/meshlink/demo/name-job', {'deviceId': 'd5', 'jobId': latest['id'], 'status': 'confirmed'})
        self.assertEqual([j for j in self.state()['nameJobs'] if j['deviceId'] == 'd5'][-1]['status'], 'confirmed')

    def test_admin_accounts_and_reporting_configuration(self):
        body = {'username': 'new-member', 'name': 'Demo New Member', 'memberId': 'm1', 'role': 'member', 'password': self.credentials['member']['password']}
        self.denied(403, self.member, 'POST', '/api/meshlink/accounts', body)
        self.denied(400, self.admin, 'POST', '/api/meshlink/accounts', {**body, 'role': 'worker'})
        account = self.admin.request('POST', '/api/meshlink/accounts', body)
        other = Client(self.url); other.login('new-member', body['password'])
        self.admin.request('POST', f'/api/meshlink/accounts/{account["id"]}', {'action': 'reset-password', 'password': self.credentials['member2']['password']})
        with self.assertRaises(ApiError):
            other.request('GET', '/api/meshlink/state')
        other.login('new-member', self.credentials['member2']['password'])
        self.admin.request('POST', f'/api/meshlink/accounts/{account["id"]}', {'action': 'disable'})
        with self.assertRaises(ApiError):
            other.request('GET', '/api/meshlink/state')
        self.denied(400, self.admin, 'POST', f'/api/meshlink/accounts/{self.state()["account"]["id"]}', {'action': 'disable'})
        self.denied(403, self.member, 'POST', '/api/meshlink/configuration', {'deviceId': 'r1', 'configuration': {'cadenceMinutes': 2}})
        self.denied(400, self.admin, 'POST', '/api/meshlink/configuration', {'deviceId': 'r1', 'configuration': {'cadenceMinutes': -2}})
        self.admin.request('POST', '/api/meshlink/configuration', {'deviceId': 'r1', 'configuration': {'reportCadenceMinutes': {'solar': 2}, 'missingTimeoutMinutes': {'solar': 10}, 'disabledMonitoring': ['temperature']}})
        self.admin.request('POST', '/api/meshlink/rules', {'deviceId': '*', 'trigger': 3.6, 'recovery': 3.8})
        self.ingest(packet('r1', 'telemetry', {'battery': 3.5}, 1))
        self.assertTrue(any(w['kind'] == 'battery' for w in self.state()['warnings']))
        self.admin.request('POST', '/api/meshlink/rules', {'deviceId': 'r1', 'trigger': 3.6, 'recovery': 3.8, 'enabled': False})
        self.ingest(packet('r1', 'telemetry', {'battery': 4.1}, .1))
        self.assertTrue(all(not w['recoveredAt'] for w in self.state()['warnings']))

    def test_future_measurement_and_disabled_simulation_controls(self):
        future = packet('d5', 'position', {'latitude': 36.2, 'longitude': -115.6}, -5)
        self.ingest(future)
        position = next(t for t in self.state()['trackers'] if t['id'] == 'd5')['position']
        self.assertIsNone(position['measuredAt'])
        self.assertEqual(position['timestampQuality'], 'future')
        # Run the same persisted DB with simulation controls explicitly off.
        self.stop()
        environment = {**os.environ, 'MESHLINK_SIMULATION': '0'}
        port = int(self.url.rsplit(':', 1)[1])
        self.process = subprocess.Popen(command(self.data) + ['serve', f'--http=127.0.0.1:{port}'], env=environment, stdout=self.log, stderr=self.log)
        wait_ready(self.url, self.process)
        self.assertFalse(self.state()['simulation'])
        self.denied(403, self.admin, 'POST', '/api/meshlink/demo/feed', {'online': False})
        self.denied(403, self.admin, 'POST', '/api/meshlink/messages', {'text': 'Must not publish to radio'})
        self.assertFalse(self.records('send_attempts'))

    def test_snapshot_history_order_and_unique_records(self):
        for i in range(5):
            self.ingest(packet('d1', 'message', {'author': 'Demo Avery', 'text': f'Ordered message {i}'}, 10 - i))
            self.ingest(packet('d1', 'position', {'latitude': 36.2 + i * .001, 'longitude': -115.6}, 10 - i))
        state = self.state()
        self.assertEqual([m['text'] for m in state['messages']], [f'Ordered message {i}' for i in range(5)])
        self.assertEqual(len({m['id'] for m in state['messages']}), 5)
        self.assertEqual([p['latitude'] for p in state['trackers'][0]['history']], [36.2 + i * .001 for i in range(5)])
        self.assertEqual([m['text'] for m in self.state()['messages']], [f'Ordered message {i}' for i in range(5)])

    def test_restart_preserves_observations_and_incidents(self):
        self.ingest(packet('d1', 'position', {'latitude': 36.2, 'longitude': -115.6}, 1))
        self.ingest(packet('r1', 'telemetry', {'intrusion': True}, 1))
        self.stop()
        port = int(self.url.rsplit(':', 1)[1])
        self.process = start(self.data, port, self.log)
        wait_ready(self.url, self.process)
        self.assertEqual(self.state()['trackers'][0]['position']['latitude'], 36.2)
        self.assertEqual(len(self.state()['incidents']), 1)


if __name__ == '__main__':
    unittest.main()

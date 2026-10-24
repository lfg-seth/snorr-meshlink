"""Integration tests against the actual pinned PocketBase binary and fresh databases."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack, closing
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
    def test_telemetry_calendar_time_then_receipt_fallback_across_clock_loss(self):
        known = packet('r1', 'telemetry', {'battery': 4.19, 'temperature': 20}, 300)
        known['receivedAt'] = at(299)
        self.ingest(known)
        unknown = packet('r1', 'telemetry', {'battery': 4.05, 'temperature': 0}, None)
        unknown['receivedAt'] = at(2)
        self.ingest(unknown)
        row = lambda: next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')
        self.assertEqual(row()['battery'], 4.05)
        self.assertEqual(row()['temperature'], 0)
        self.assertIsNone(row()['readingTimes']['battery'])
        self.assertEqual(row()['readingReceivedTimes']['battery'], unknown['receivedAt'])
        self.assertEqual(row()['reportedAt'], unknown['receivedAt'])
        saved = next(o for o in self.records('observations') if o['packetKey'].startswith('telemetry:r1:' + unknown['packetId']))
        self.assertEqual(saved['measuredAt'], '')
        self.assertEqual(saved['timestampQuality'], 'unknown')
        # Late calendar-time and delayed receipt-time packets cannot replace it.
        for measured, received in [(10, 1), (None, 3)]:
            delayed = packet('r1', 'telemetry', {'battery': 3.5}, measured)
            delayed['receivedAt'] = at(received)
            self.ingest(delayed)
            self.assertEqual(row()['battery'], 4.05)
        self.assertEqual(self.ingest({**unknown, 'gatewayId': 'b2', 'receivedAt': at(1)})['outcome'], 'duplicate')
        self.assertEqual(row()['readingReceivedTimes']['battery'], unknown['receivedAt'])
        # Recovery uses measurement time, rather than the later arrival time.
        recovered = packet('r1', 'telemetry', {'battery': 4.1}, 1)
        self.ingest(recovered)
        self.assertEqual(row()['battery'], 4.1)
        self.assertEqual(row()['readingTimes']['battery'], recovered['measuredAt'])
        history = self.admin.request('GET', '/api/meshlink/battery-history/r1?hours=24')['samples']
        self.assertTrue(any(s['at'] == unknown['receivedAt'] and s['volts'] == 4.05 for s in history))
        self.assertTrue(any(s['at'] == recovered['measuredAt'] and s['volts'] == 4.1 for s in history))
        self.assertEqual([s['at'] for s in history], sorted(s['at'] for s in history))
        self.assertTrue(any(s['at'] == unknown['receivedAt'] for s in row()['samples']))

    def test_invalid_telemetry_clocks_fall_back_without_changing_gps_freshness(self):
        fix = packet('d1', 'position', {'latitude': 36.2, 'longitude': -115.6}, 30)
        self.ingest(fix)
        for clock, quality in [('not-a-time', 'invalid'), (at(-10), 'future'), (None, 'unknown')]:
            reading = packet('d1', 'telemetry', {'battery': 3.9}, None)
            reading['measuredAt'] = clock
            self.ingest(reading)
            row = next(d for d in self.state()['trackers'] if d['id'] == 'd1')
            self.assertIsNone(row['batteryMeasuredAt'])
            self.assertEqual(row['batteryReceivedAt'], reading['receivedAt'])
            self.assertEqual(row['batteryTimestampQuality'], quality)
            self.assertEqual(row['position']['measuredAt'], fix['measuredAt'])

    def test_battery_history_merges_both_clocks_before_limiting_and_preserves_provenance(self):
        reference = datetime.now(timezone.utc)
        stamp = lambda minutes: (reference - timedelta(minutes=minutes)).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        for minute in range(44):
            measured = stamp(minute + 1) if minute % 2 else ''
            self.superuser.request('POST', '/api/collections/observations/records', {
                'deviceId': 'r1', 'packetKey': f'history-{minute}', 'measuredAt': measured,
                'receivedAt': stamp(minute + .5), 'timestampQuality': 'valid' if measured else 'unknown',
                'payload': {'battery': 3.5 + minute / 1000}})
        for key, measured, received in [('old-known', stamp(1500), stamp(1)), ('old-unknown', '', stamp(1500))]:
            self.superuser.request('POST', '/api/collections/observations/records', {
                'deviceId': 'r1', 'packetKey': key, 'measuredAt': measured, 'receivedAt': received,
                'timestampQuality': 'valid' if measured else 'unknown', 'payload': {'battery': 4.2}})
        samples = next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')['samples']
        self.assertEqual(len(samples), 40)
        self.assertEqual(samples[0]['volts'], 3.539)
        self.assertEqual(samples[-1]['volts'], 3.5)
        for sample in samples:
            self.assertEqual(sample['at'], sample['measuredAt'] or sample['receivedAt'])
        history = self.admin.request('GET', '/api/meshlink/battery-history/r1?hours=24')['samples']
        self.assertEqual(len(history), 44)
        self.assertEqual([s['at'] for s in history], sorted(s['at'] for s in history))
        for client in [self.worker, Client(self.url)]:
            with self.assertRaises(ApiError):
                client.request('GET', '/api/meshlink/battery-history/r1?hours=24')

    def test_telemetry_receipt_fallback_drives_health_without_duplicate_refresh(self):
        self.admin.request('POST', '/api/meshlink/rules', {'deviceId': 'r1', 'trigger': 3.5, 'recovery': 3.8})
        low = packet('r1', 'telemetry', {'battery': 3.4}, None)
        self.ingest(low)
        warnings = lambda: [w for w in self.state()['warnings'] if w['deviceId'] == 'r1' and w['kind'] == 'battery']
        self.assertIsNone(warnings()[0]['recoveredAt'])
        self.ingest(packet('r1', 'telemetry', {'battery': 4.0}, 20))
        self.assertIsNone(warnings()[0]['recoveredAt'])
        good = packet('r1', 'telemetry', {'battery': 3.9}, None)
        self.ingest(good)
        self.assertTrue(warnings()[0]['recoveredAt'])
        stale = packet('r2', 'telemetry', {'battery': 3.9}, None)
        stale['receivedAt'] = at(30)
        self.ingest(stale)
        self.ingest({**stale, 'gatewayId': 'b2', 'receivedAt': at()})
        r2 = next(d for d in self.state()['infrastructure'] if d['id'] == 'r2')
        self.assertEqual(r2['readingReceivedTimes']['battery'], stale['receivedAt'])
        # A new source reading, not a duplicate or neighboring-node mention, recovers missing health.
        device = next(d for d in self.records('devices') if d['key'] == 'r2')
        self.superuser.request('PATCH', '/api/collections/devices/records/' + device['id'], {'monitoringStartedAt': at(60)})
        feed = self.records('feed')[0]
        self.superuser.request('PATCH', '/api/collections/feed/records/' + feed['id'], {'restoredAt': at(60)})
        self.worker.request('POST', '/api/meshlink/worker/heartbeat', {'connected': True})
        missing = lambda: [w for w in self.state()['warnings'] if w['deviceId'] == 'r2' and w['kind'] == 'missing:battery']
        self.assertIsNone(missing()[0]['recoveredAt'])
        self.ingest(packet('r2', 'telemetry', {'battery': 3.95}, None))
        self.assertTrue(missing()[0]['recoveredAt'])

    def test_neighbor_reports_atomic_dedup_private_storage_and_clock_semantics(self):
        data = {'reportType': 'snns-v1', 'observerNodeId': '!05237743', 'bootId': 42,
                'sequence': 7, 'reportUptimeSeconds': 100, 'subset': False,
                'capacityEvicted': True, 'totalNeighbors': 2, 'rows': [
                    {'heardDeviceId': 'd1', 'heardNodeId': '!699c2ed8', 'snrDb': 0,
                     'rssiDbm': -80, 'hearingAgeSeconds': 12, 'observationCount': 10},
                    {'heardDeviceId': None, 'heardNodeId': '!00000123', 'snrDb': -3.25,
                     'rssiDbm': -120, 'hearingAgeSeconds': 1799, 'observationCount': 1}]}
        item = packet('r1', 'neighbors', data, None)
        before = self.state()
        self.assertEqual(self.ingest(item)['outcome'], 'accepted')
        self.assertEqual(self.ingest({**item, 'gatewayId': 'b2'})['outcome'], 'duplicate')
        rows = self.state()['links']
        self.assertEqual(len(rows), 2)
        self.assertEqual({r['heardNodeId'] for r in rows}, {'!699c2ed8', '!00000123'})
        self.assertTrue(all(r['observerDeviceId'] == 'r1' and r['observedAt'] is None for r in rows))
        self.assertTrue(all(r['transportGatewayId'] == 'b1' for r in rows))
        self.assertEqual(len(self.records('neighbor_reports')), 1)
        self.assertEqual(len(self.records('packet_receipts')), 2)
        self.assertEqual(self.state()['trackers'], before['trackers'])
        for bad in [{**data, 'rows': [data['rows'][0], {**data['rows'][1], 'rssiDbm': 0}]},
                    {**data, 'bootId': 0}, {**data, 'subset': True},
                    {**data, 'rows': [data['rows'][0], data['rows'][0]]}]:
            self.denied(400, self.worker, 'POST', '/api/meshlink/worker/ingest', packet('r1', 'neighbors', bad))
        self.assertEqual(len(self.records('neighbor_reports')), 1)
        self.assertEqual(len(self.state()['links']), 2)
        for client in [self.admin, self.member, self.worker, Client(self.url)]:
            with self.assertRaises(ApiError):
                client.request('GET', '/api/collections/neighbor_reports/records')
        empty = packet('r1', 'neighbors', {'reportType': 'neighbor-info', 'observerNodeId': '!05237743', 'rows': []}, None)
        self.assertEqual(self.ingest(empty)['outcome'], 'accepted')
        self.assertEqual(self.ingest(empty)['outcome'], 'duplicate')
        self.assertEqual(len(self.state()['links']), 2)  # No omission-driven deletion.
        self.stop()
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.assertEqual(len(self.state()['links']), 2)
        self.assertEqual(self.ingest(item)['outcome'], 'duplicate')

    def test_sensor_current_signed_channels_and_latest_reading_independent_of_battery(self):
        before = self.state()
        item = packet('r1', 'telemetry', {'power3Voltage': 4.2, 'power3CurrentMa': -323.1,
                                        'power1CurrentMa': 0}, 1)
        self.assertEqual(self.ingest(item)['outcome'], 'accepted')
        self.assertEqual(self.ingest({**item, 'gatewayId': 'b2'})['outcome'], 'duplicate')
        current = next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')
        self.assertIsNone(current['battery'])
        readings = {r['metric']: r for r in current['powerReadings']}
        self.assertEqual(readings['power3CurrentMa']['value'], -323.1)
        self.assertEqual(readings['power1CurrentMa']['value'], 0)
        self.assertNotIn('batteryCurrentMa', current)
        for minutes in [20, None, -10]:
            self.ingest(packet('r1', 'telemetry', {'power3CurrentMa': 100}, minutes))
        replay_future = packet('r1', 'telemetry', {'power3CurrentMa': 100}, 2)
        replay_future['receivedAt'] = at(10)
        self.ingest(replay_future)  # Future when received remains future on replay.
        latest = {r['metric']: r for r in next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')['powerReadings']}
        self.assertEqual(latest['power3CurrentMa']['value'], 100)
        self.assertIsNone(latest['power3CurrentMa']['measuredAt'])
        self.assertEqual(latest['power3CurrentMa']['timestampQuality'], 'future')
        self.assertGreater(latest['power3CurrentMa']['receivedAt'], replay_future['receivedAt'])
        self.assertEqual(latest['power1CurrentMa'], readings['power1CurrentMa'])
        self.ingest(packet('r1', 'telemetry', {'sensorVoltage': 0.008, 'sensorCurrentMa': -0.4}, None))
        self.assertEqual(len(next(d for d in self.state()['infrastructure'] if d['id'] == 'r1')['powerReadings']), 5)
        for data in [{'power9CurrentMa': 1}, {'power3CurrentMa': -100001}, {'sensorVoltage': -1}, {'power1CurrentMa': True}]:
            self.denied(400, self.worker, 'POST', '/api/meshlink/worker/ingest', packet('r1', 'telemetry', data))
        self.denied(400, self.worker, 'POST', '/api/meshlink/worker/ingest', packet('d1', 'telemetry', {'sensorCurrentMa': 1}))
        self.assertEqual(before['trackers'], self.state()['trackers'])

    def test_position_quality_stays_with_its_fix_across_duplicates_delay_and_restart(self):
        coordinates = {'latitude': 36.2, 'longitude': -115.6}
        newest = packet('d1', 'position', {**coordinates, 'pdop': 1.83, 'satellites': 9}, 1)
        self.assertEqual(self.ingest(newest)['outcome'], 'accepted')
        first = self.state()['trackers'][0]['position']
        self.assertEqual(first['pdop'], 1.83)
        self.assertEqual(first['satellites'], 9)
        self.assertEqual(self.ingest({**newest, 'gatewayId': 'b2', 'receivedAt': at()})['outcome'], 'duplicate')
        for minutes in [25, None, -5]:
            self.ingest(packet('d1', 'position', {**coordinates, 'pdop': 8, 'satellites': 5}, minutes))
            self.assertEqual(self.state()['trackers'][0]['position'], first)
        history = self.state()['trackers'][0]['history']
        self.assertEqual([(p['pdop'], p['satellites']) for p in history], [(8, 5), (1.83, 9)])
        for data in [{'pdop': -1}, {'pdop': '1.83'}, {'pdop': True}, {'pdop': 42949673},
                     {'satellites': -1}, {'satellites': 1.5}, {'satellites': '9'},
                     {'satellites': 4294967296}]:
            self.denied(400, self.worker, 'POST', '/api/meshlink/worker/ingest',
                        packet('d1', 'position', {**coordinates, **data}))
        self.assertEqual(self.state()['trackers'][0]['position'], first)
        self.stop()
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.assertEqual(self.state()['trackers'][0]['position'], first)
        self.assertEqual(self.state()['trackers'][0]['history'], history)
        for quality in [{}, {'pdop': None, 'satellites': None}, {'pdop': 0, 'satellites': 0}]:
            item = packet('d1', 'position', {**coordinates, **quality})
            self.assertEqual(self.ingest(item)['outcome'], 'accepted')
            current = self.state()['trackers'][0]['position']
            self.assertEqual(current['measuredAt'], item['measuredAt'])
            self.assertIsNone(current['pdop'])
            self.assertIsNone(current['satellites'])

    def test_member_map_shortname_is_validated_persisted_and_only_changes_self(self):
        route = '/api/meshlink/profile'
        for client in [Client(self.url), self.worker]:
            with self.assertRaises(ApiError):
                client.request('POST', route, {'shortName': 'CASEY'})
        self.denied(400, self.admin, 'POST', route, {'shortName': 'ADMIN'})
        before = self.state()
        for value in ['', '123456', 'a b', '<b>', 123, None]:
            self.denied(400, self.member, 'POST', route, {'shortName': value})
        self.denied(400, self.member, 'POST', route, {'shortName': 'OTHER', 'memberId': 'm2'})
        self.denied(400, self.member, 'POST', route, {'shortName': 'OTHER', 'role': 'admin'})
        self.member.request('POST', route, {'shortName': 'CJ_5'})
        state = self.state()
        self.assertEqual(next(m for m in state['members'] if m['id'] == 'm5')['shortName'], 'CJ_5')
        self.assertEqual(next(m for m in state['members'] if m['id'] == 'm2')['shortName'], '')
        self.assertEqual(state['assignments'], before['assignments'])
        self.assertEqual(state['trackers'], before['trackers'])
        self.stop()
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.assertEqual(next(m for m in self.state()['members'] if m['id'] == 'm5')['shortName'], 'CJ_5')

    def test_account_setup_saves_member_chosen_shortname_atomically(self):
        body = {'username': 'alias-member', 'name': 'Demo Alias', 'memberId': 'm1',
                'role': 'member', 'shortName': 'ONE', 'password': self.credentials['member']['password']}
        self.denied(400, self.admin, 'POST', '/api/meshlink/accounts', {**body, 'shortName': 'TOOLONG'})
        self.assertEqual(next(m for m in self.state()['members'] if m['id'] == 'm1')['shortName'], '')
        self.admin.request('POST', '/api/meshlink/accounts', body)
        self.assertEqual(next(m for m in self.state()['members'] if m['id'] == 'm1')['shortName'], 'ONE')
        # A duplicate account cannot partially replace the other member's label.
        with self.assertRaises(ApiError):
            self.admin.request('POST', '/api/meshlink/accounts', {**body, 'memberId': 'm3', 'shortName': 'THREE'})
        self.assertEqual(next(m for m in self.state()['members'] if m['id'] == 'm3')['shortName'], '')
        self.assertEqual(self.state()['trackers'][0]['deviceType'], 'Heltec V4')

    def test_member_voltage_config_and_gps_clocks_are_independent(self):
        fix = packet('d1', 'position', {'latitude': 36.2, 'longitude': -115.6, 'battery': 42})
        self.ingest(fix)
        before = next(d for d in self.state()['trackers'] if d['id'] == 'd1')
        reading = packet('d1', 'telemetry', {'battery': 3.8}, 1)
        self.assertEqual(self.ingest(reading)['outcome'], 'accepted')
        self.assertEqual(self.ingest({**reading, 'gatewayId': 'b2'})['outcome'], 'duplicate')
        configured = {'deviceId': 'd1', 'configuration': {'batteryProfile': 'lipo-1s', 'batteryCapacityMah': 3000}}
        with self.assertRaises(ApiError):
            self.member.request('POST', '/api/meshlink/configuration', configured)
        self.admin.request('POST', '/api/meshlink/configuration', configured)
        row = next(d for d in self.state()['trackers'] if d['id'] == 'd1')
        self.assertEqual(row['position'], before['position'])
        self.assertEqual(row['battery'], 42)  # Reported percent retains its original meaning.
        self.assertEqual(row['batteryVoltage'], 3.8)
        self.assertEqual(row['batteryMeasuredAt'], reading['measuredAt'])
        self.assertEqual(row['batteryCapacityMah'], 3000)
        self.assertEqual(row['batteryProfile'], 'lipo-1s')
        for config in [{'batteryProfile': 'lipo-2s'}, {'batteryCapacityMah': -1},
                       {'batteryCapacityMah': 1.5}, {'batteryCapacityMah': '1000'},
                       {'cadenceMinutes': 1}]:
            with self.assertRaises(ApiError):
                self.admin.request('POST', '/api/meshlink/configuration', {'deviceId': 'd1', 'configuration': config})
        reference = datetime.now(timezone.utc)
        for index, item in enumerate([packet('d1', 'telemetry', {'battery': 3.7}, minutes=-10),
                     {**packet('d1', 'telemetry', {'battery': 3.6}), 'measuredAt': None},
                     packet('d1', 'telemetry', {'battery': 4.1}, minutes=10)]):
            item['receivedAt'] = (reference - timedelta(seconds=3 - index)).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
            self.ingest(item)
        row = next(d for d in self.state()['trackers'] if d['id'] == 'd1')
        self.assertEqual(row['batteryVoltage'], 3.6)
        self.assertIsNone(row['batteryMeasuredAt'])
        self.assertEqual(row['position'], before['position'])
        with self.assertRaises(ApiError):
            self.ingest(packet('d1', 'telemetry', {'temperature': 20}))
        self.admin.request('POST', '/api/meshlink/configuration', {'deviceId': 'd1',
            'configuration': {'batteryProfile': 'unknown', 'batteryCapacityMah': None}})
        self.assertIsNone(next(d for d in self.state()['trackers'] if d['id'] == 'd1')['batteryCapacityMah'])

    def test_raw_mqtt_archive_is_lossless_private_and_idempotent(self):
        import base64
        import uuid
        item = {'receiptId': str(uuid.uuid4()), 'topic': 'snorr/pilot/unknown',
                'receivedAt': at(), 'qos': 1, 'retained': True, 'duplicate': True,
                'payloadBase64': base64.b64encode(b'\x00\xff').decode(),
                'payloadBytes': 2, 'decodeOutcome': 'rejected', 'decodeReason': 'retained packet'}
        path = '/api/meshlink/worker/archive'
        before = self.state()
        for client in [Client(self.url), self.admin, self.member]:
            with self.assertRaises(ApiError):
                client.request('POST', path, item)
        self.assertEqual(self.worker.request('POST', path, item)['outcome'], 'saved')
        # JSON object order can change during durable queue/API serialization.
        retry = dict(reversed(list(item.items())))
        self.assertEqual(self.worker.request('POST', path, retry)['outcome'], 'duplicate')
        with self.assertRaises(ApiError):
            self.worker.request('POST', path, {**item, 'topic': 'changed'})
        rows = self.records('mqtt_archive')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['envelope'], item)
        for client in [Client(self.url), self.admin, self.member, self.worker]:
            # Locked collection list queries cannot reveal archived payloads.
            with self.assertRaises(ApiError):
                client.request('GET', '/api/collections/mqtt_archive/records')
        self.assertEqual(before['trackers'], self.state()['trackers'])
        self.assertEqual(before['infrastructure'], self.state()['infrastructure'])
        for value in ['', 'AA=', '!!!!']:
            with self.assertRaises(ApiError):
                self.worker.request('POST', path, {**item, 'receiptId': str(uuid.uuid4()),
                    'payloadBase64': value})
        self.stop()
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.assertEqual(self.records('mqtt_archive')[0]['envelope'], item)

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
        with closing(sqlite3.connect(self.data / 'data.db')) as db:
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
        self.assertTrue(all(t['deviceType'] == 'Heltec V4' for t in self.state()['trackers']))
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

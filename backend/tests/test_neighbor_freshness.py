"""Current neighbor evidence against the actual pinned PocketBase binary."""
from copy import deepcopy
from contextlib import closing
import sqlite3
import subprocess
import unittest

import test_backend
from fixtures import at, packet
from manage import command, start, wait_ready


class NeighborFreshnessTests(unittest.TestCase):
    # Share the disposable actual-binary fixture, not its unrelated test cases.
    setUp = test_backend.BackendTests.setUp
    stop = test_backend.BackendTests.stop
    login = test_backend.BackendTests.login
    state = test_backend.BackendTests.state
    ingest = test_backend.BackendTests.ingest
    records = test_backend.BackendTests.records

    def report(self, sequence=1, uptime=100, age=10, count=1, boot=42, received=None, **changes):
        data = {'reportType': 'snns-v1', 'observerNodeId': '!05237743', 'bootId': boot,
                'sequence': sequence, 'reportUptimeSeconds': uptime, 'subset': False,
                'capacityEvicted': False, 'totalNeighbors': 1, 'rows': [
                    {'heardDeviceId': 'd1', 'heardNodeId': '!699c2ed8', 'snrDb': 0,
                     'rssiDbm': -80, 'hearingAgeSeconds': age, 'observationCount': count}]}
        data.update(changes)
        item = packet('r1', 'neighbors', data, None)
        item['receivedAt'] = received or at()
        self.ingest(item)
        return item

    def test_standard_table_is_archive_only_and_relative_evidence_expires(self):
        first = self.report(age=30, received=at(119))
        rows = self.state()['currentLinks']
        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0]['observedAt'])
        self.assertEqual(rows[0]['freshness'], {
            'basis': 'relative', 'anchorReceivedAt': first['receivedAt'], 'ageAtAnchorSeconds': 30})
        standard = deepcopy(first)
        standard['packetId'] = 'standard-table'
        standard['receivedAt'] = at()
        standard['data'] = {'reportType': 'neighbor-info', 'observerNodeId': '!05237743',
                            'rows': [{'heardDeviceId': 'd1', 'heardNodeId': '!699c2ed8',
                                      'snrDb': 8, 'rssiDbm': None}]}
        self.ingest(standard)
        self.assertEqual(self.state()['currentLinks'], rows)
        self.assertEqual(len(self.state()['links']), 2)
        # A duplicate via a new gateway retains its original relative anchor.
        self.ingest({**first, 'gatewayId': 'b2', 'receivedAt': at()})
        self.assertEqual(self.state()['currentLinks'], rows)
        current = self.records('neighbor_current')[0]
        self.superuser.request('PATCH', '/api/collections/neighbor_current/records/' + current['id'],
                               {'anchorReceivedAt': at(120)})
        self.assertEqual(self.state()['currentLinks'], [])
        self.assertEqual(len(self.state()['links']), 2)

    def test_unchanged_hearing_new_packet_ids_and_ordering_cannot_renew_anchor(self):
        original = self.report(uptime=100, age=10, count=5, received=at(20))
        selected = self.state()['currentLinks'][0]
        self.report(sequence=2, uptime=200, age=110, count=5)
        # One-second source rounding jitter must not move the selected reading.
        self.report(sequence=3, uptime=201, age=110, count=5)
        self.assertEqual(self.state()['currentLinks'], [selected])
        # Different normalized packet IDs still share the same SNNS generation.
        self.report(sequence=3, uptime=202, age=0, count=8)
        self.report(sequence=2, uptime=202, age=0, count=8)
        self.assertEqual(self.state()['currentLinks'], [selected])
        self.assertEqual(len(self.records('neighbor_frontiers')), 1)
        self.assertEqual(len(self.records('neighbor_current')), 1)
        self.assertEqual(len(self.state()['links']), 5)
        self.assertEqual(selected['freshness']['anchorReceivedAt'], original['receivedAt'])

    def test_new_counts_reset_counts_saturation_and_older_hearing(self):
        self.report(uptime=100, age=10, count=5, received=at(20))
        old = self.state()['currentLinks'][0]
        # Same-second new reception is proved by an increasing collector count.
        increased = self.report(sequence=2, uptime=100, age=10, count=6, received=at(19))
        self.assertEqual(self.state()['currentLinks'][0]['receivedAt'], increased['receivedAt'])
        newer = self.state()['currentLinks'][0]
        self.assertNotEqual(old['id'], newer['id'])
        self.report(sequence=3, uptime=110, age=40, count=7)
        self.report(sequence=4, uptime=111, age=21, count=1)
        self.assertEqual(self.state()['currentLinks'], [newer])
        # Expiry/capacity eviction legitimately resets count; newer hearing wins.
        reset = self.report(sequence=5, uptime=120, age=0, count=1, received=at(18))
        self.assertEqual(self.state()['currentLinks'][0]['receivedAt'], reset['receivedAt'])
        self.report(sequence=6, uptime=130, age=0, count=4294967295, received=at(17))
        saturated = self.state()['currentLinks'][0]
        self.report(sequence=7, uptime=140, age=10, count=4294967295)
        self.assertEqual(self.state()['currentLinks'], [saturated])
        fresh = self.report(sequence=8, uptime=150, age=0, count=4294967295)
        self.assertEqual(self.state()['currentLinks'][0]['receivedAt'], fresh['receivedAt'])

    def test_subset_omission_does_not_erase_or_refresh_other_pair(self):
        row1 = self.report(subset=True, totalNeighbors=2)
        selected1 = self.state()['currentLinks'][0]
        second = deepcopy(row1['data']['rows'][0])
        second.update(heardNodeId='!00000123', heardDeviceId=None)
        self.report(sequence=2, uptime=150, age=10, rows=[second], subset=True, totalNeighbors=2)
        self.assertEqual(len(self.state()['currentLinks']), 2)
        self.assertIn(selected1, self.state()['currentLinks'])
        self.report(sequence=3, uptime=160, age=70, count=1)
        self.assertEqual(len(self.state()['currentLinks']), 2)
        self.assertIn(selected1, self.state()['currentLinks'])

    def test_old_original_receipt_expiry_and_tombstone_survive_restart(self):
        old = self.report(received=at(180))
        self.assertEqual(self.state()['currentLinks'], [])
        self.assertEqual(len(self.records('neighbor_current')), 1)
        self.report(sequence=2, uptime=200, age=110, count=1)
        self.assertEqual(self.state()['currentLinks'], [])
        self.stop()
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.ingest({**old, 'gatewayId': 'b2', 'receivedAt': at()})
        self.report(sequence=2, uptime=200, age=0, count=2)
        self.report(sequence=3, uptime=201, age=111, count=1)
        self.assertEqual(self.state()['currentLinks'], [])
        self.assertEqual(len(self.records('neighbor_current')), 1)
        self.report(sequence=4, uptime=250, age=0, count=2)
        self.assertEqual(len(self.state()['currentLinks']), 1)

    def test_boot_transition_and_repeated_retired_boot_are_archive_only(self):
        self.report(boot=42, sequence=50, uptime=300)
        self.report(boot=43, sequence=1, uptime=20)
        selected = self.state()['currentLinks']
        self.report(boot=42, sequence=51, uptime=400, age=0, count=10)
        self.report(boot=42, sequence=52, uptime=450, age=0, count=11)
        self.assertEqual(self.state()['currentLinks'], selected)
        self.report(boot=44, received=at(120))  # Novel older-received boot is also conservative.
        self.assertEqual(self.state()['currentLinks'], selected)
        self.assertEqual(len(self.records('neighbor_current')), 1)
        self.assertEqual(len(self.state()['links']), 5)

    def test_millis_rollover_and_sequence_rollback_remain_conservative(self):
        self.report(uptime=4294967, age=7, count=4294967295, received=at(20))
        selected = self.state()['currentLinks']
        self.report(sequence=2, uptime=0, age=7, count=4294967295)
        self.assertEqual(self.state()['currentLinks'], selected)
        self.report(sequence=3, uptime=1, age=8, count=4294967295)
        self.assertEqual(self.state()['currentLinks'], selected)
        self.report(sequence=4, uptime=10, age=0, count=4294967295)
        self.assertNotEqual(self.state()['currentLinks'], selected)
        selected = self.state()['currentLinks']
        self.report(sequence=5, uptime=9, age=0, count=4294967295)
        self.assertEqual(self.state()['currentLinks'], selected)
        self.report(sequence=4294967295, uptime=20, age=0, count=4294967295)
        selected = self.state()['currentLinks']
        self.report(sequence=1, uptime=21, age=0, count=4294967295)
        self.assertEqual(self.state()['currentLinks'], selected)

    def test_bootstrap_uses_historical_order_without_promoting_historical_hearings(self):
        def historical(boot, sequence, uptime, received):
            item = {'reportType': 'snns-v1', 'observerNodeId': '!05237743', 'bootId': boot,
                    'sequence': sequence, 'reportUptimeSeconds': uptime}
            self.superuser.request('POST', '/api/collections/neighbor_reports/records', {
                'packetKey': f'historical-{boot}-{sequence}', 'deviceId': 'r1',
                'receivedAt': received, 'payload': item})
        historical(42, 10, 100, at(30))
        historical(43, 20, 200, at(20))
        historical(43, 19, 190, at(10))  # Late lower sequence cannot lower baseline.
        self.assertEqual(self.state()['currentLinks'], [])
        self.report(boot=42, sequence=30, uptime=300, age=0)
        self.report(boot=42, sequence=31, uptime=301, age=0)
        self.assertEqual(self.state()['currentLinks'], [])
        self.assertEqual(self.records('neighbor_frontiers')[0]['payload']['bootId'], 43)
        self.report(boot=43, sequence=20, uptime=250, age=0)
        self.report(boot=43, sequence=21, uptime=250, age=50)
        self.assertEqual(self.state()['currentLinks'], [])
        self.report(boot=43, sequence=22, uptime=260, age=1)
        self.assertEqual(len(self.state()['currentLinks']), 1)

    def test_absolute_evidence_requires_consistent_clocks_and_standard_tables_stay_archived(self):
        created = []
        for observed, received, details in [(at(1), at(), {}), (at(121), at(), {}),
                                            (at(1), at(), {'reportType': 'neighbor-info'}),
                                            (at(1), at(2), {}), (at(1), at(-1), {}),
                                            ('bad-clock', at(), {}), (at(1)[:-1], at(), {})]:
            created.append(self.superuser.request('POST', '/api/collections/link_observations/records', {
                'observerDeviceId': 'b1', 'heardDeviceId': 'd1', 'source': 'gateway',
                'path': 'direct', 'signal': {'snrDb': 0, 'rssiDbm': -80}, 'details': details,
                'receivedAt': received, 'observedAt': observed}))
        current = self.state()['currentLinks']
        self.assertEqual([row['id'] for row in current], [created[0]['id']])
        self.assertNotIn('freshness', current[0])
        self.assertEqual(len(self.state()['links']), len(created))
        for collection in ['neighbor_current', 'neighbor_frontiers']:
            rules = self.superuser.request('GET', '/api/collections/' + collection)
            for rule in ['listRule', 'viewRule', 'createRule', 'updateRule', 'deleteRule']:
                self.assertIsNone(rules[rule])

    def test_current_snapshot_is_bounded_independently_of_complete_archive(self):
        # Bulk fictional history keeps this API-boundary regression fast and
        # avoids conflating the2000-row snapshot limit with API write throttles.
        with closing(sqlite3.connect(self.data / 'data.db')) as database:
            database.executemany('INSERT INTO link_observations '
                '(id, observerDeviceId, heardDeviceId, source, path, signal, receivedAt, observedAt) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [
                    (f'fictional{i:06}', 'b1', 'd1', 'gateway', 'direct', '{"snrDb":0}', at(), at(1))
                    for i in range(2005)])
            database.commit()
        self.assertEqual(len(self.state()['currentLinks']), 2000)
        self.assertEqual(len(self.state()['links']), 2000)
        with closing(sqlite3.connect(self.data / 'data.db')) as database:
            self.assertEqual(database.execute('SELECT count(*) FROM link_observations').fetchone()[0], 2005)

    def test_migration_down_up_preserves_history_and_does_not_backfill_current_state(self):
        self.report()
        self.stop()
        reverted = subprocess.run(command(self.data) + ['migrate', 'down', '1'],
                                  input='y\n', text=True, capture_output=True)
        self.assertEqual(reverted.returncode, 0, reverted.stdout + reverted.stderr)
        with closing(sqlite3.connect(self.data / 'data.db')) as database:
            self.assertEqual(database.execute('SELECT count(*) FROM link_observations').fetchone()[0], 1)
            names = {r[0] for r in database.execute('SELECT name FROM sqlite_master')}
            self.assertNotIn('neighbor_current', names)
            self.assertNotIn('neighbor_frontiers', names)
            self.assertNotIn('idx_links_observed_at', names)
        reapplied = subprocess.run(command(self.data) + ['migrate', 'up'], capture_output=True, text=True)
        self.assertEqual(reapplied.returncode, 0, reapplied.stdout + reapplied.stderr)
        self.process = start(self.data, int(self.url.rsplit(':', 1)[1]), self.log)
        wait_ready(self.url, self.process)
        self.assertEqual(len(self.state()['links']), 1)
        self.assertEqual(self.state()['currentLinks'], [])


if __name__ == '__main__':
    unittest.main()

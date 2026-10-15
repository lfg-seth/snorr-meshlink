"""Verify stored real positions and two-gateway deduplication without printing tracks."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import sys
import time

sys.path.insert(0, '/opt/meshlink/backend')
from client import Client


def main():
    secret = json.loads(Path('/var/lib/meshlink/credentials.json').read_text())['admin']
    client = Client('http://127.0.0.1:8080')
    client.login(secret['username'], secret['password'])
    deadline = time.monotonic() + 300
    while True:
        state = client.request('GET', '/api/meshlink/state')
        assert state['simulation'] is False
        assert {d['id'] for d in state['trackers']} == {'b001', 'b002'}
        assert {d['id'] for d in state['infrastructure']} == {'g001', 'g002'}
        assert not state['members'] and not state['assignments'] and not state['messages']
        if not state['feedOnline']:
            if time.monotonic() >= deadline:
                raise RuntimeError('Live worker heartbeat unavailable')
            time.sleep(3)
            continue
        with sqlite3.connect('file:/var/lib/meshlink/pb_data/data.db?mode=ro', uri=True) as db:
            counts = {table: db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                      for table in ('positions', 'packet_receipts')}
            pairs = db.execute('SELECT deviceId,gatewayId,COUNT(*) FROM packet_receipts '
                               'WHERE outcome IN ("accepted","duplicate") GROUP BY deviceId,gatewayId').fetchall()
            duplicated = db.execute('SELECT deviceId,packetKey FROM packet_receipts '
                                    'WHERE outcome IN ("accepted","duplicate") '
                                    'GROUP BY deviceId,packetKey HAVING COUNT(DISTINCT gatewayId)=2').fetchall()
            outcomes = dict(db.execute('SELECT outcome,COUNT(*) FROM packet_receipts GROUP BY outcome').fetchall())
        observed = {(device, gateway) for device, gateway, count in pairs}
        complete = observed == {(device, gateway) for device in ('b001', 'b002') for gateway in ('g001', 'g002')}
        if complete and {device for device, key in duplicated} == {'b001', 'b002'}:
            break
        if time.monotonic() >= deadline:
            raise RuntimeError('Both trackers/two-gateway stored receipts not yet verified.')
        time.sleep(3)
    now = datetime.now(timezone.utc).timestamp()
    ages = {}
    for tracker in state['trackers']:
        position = tracker['position']
        assert position and position['timestampQuality'] == 'valid' and position['measuredAt']
        age = now - datetime.fromisoformat(position['measuredAt']).timestamp()
        assert 0 <= age < 900, 'GPS solution is not fresh under the pilot threshold'
        ages[tracker['id']] = round(age, 2)
    print(json.dumps({'live': True, 'counts': counts, 'receiptOutcomes': outcomes,
                      'receiptsByPair': pairs, 'latestFixAgeSeconds': ages,
                      'twoGatewayDeduplicationForBothTrackers': True}))


if __name__ == '__main__':
    main()

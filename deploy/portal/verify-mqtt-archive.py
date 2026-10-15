"""Verify live raw MQTT capture without printing packet contents or locations."""
import argparse
import base64
import json
from pathlib import Path
import sqlite3
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wait', type=int, default=60)
    args = parser.parse_args()
    deadline = time.monotonic() + args.wait
    with sqlite3.connect('file:/var/lib/meshlink/pb_data/data.db?mode=ro', uri=True) as db:
        initial = db.execute('SELECT COUNT(*) FROM mqtt_archive').fetchone()[0]
        while True:
            count = db.execute('SELECT COUNT(*) FROM mqtt_archive').fetchone()[0]
            if count > initial:
                break
            if time.monotonic() >= deadline:
                raise RuntimeError('No new MQTT archive receipts during verification window.')
            time.sleep(1)
        rows = db.execute('SELECT receiptId,topic,receivedAt,envelope FROM mqtt_archive '
                          'ORDER BY receivedAt DESC LIMIT 200').fetchall()
        outcomes = {}
        for receipt_id, topic, received, serialized in rows:
            envelope = json.loads(serialized)
            assert envelope['receiptId'] == receipt_id
            assert envelope['topic'] == topic and envelope['receivedAt'] == received
            assert len(base64.b64decode(envelope['payloadBase64'], validate=True)) == envelope['payloadBytes']
            outcome = envelope['decodeOutcome']
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    with sqlite3.connect('file:/var/lib/meshlink-worker/receipts.sqlite?mode=ro', uri=True) as queue:
        pending = queue.execute('SELECT COUNT(*) FROM queue').fetchone()[0]
    print(json.dumps({'archiveRecords': count, 'newDuringCheck': count - initial,
                      'verifiedRecentRecords': len(rows), 'decodeOutcomes': outcomes,
                      'pendingQueue': pending}))


if __name__ == '__main__':
    main()

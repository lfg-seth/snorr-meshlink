"""Replay newly supported radio data from a private archive, without changing it.

Run against an isolated copy first. Dry-run is the default; --apply requires
worker credentials and uses the ordinary validated ingestion route.
"""
import argparse
import base64
from datetime import datetime
import json
from pathlib import Path
import re
import sqlite3

from client import Client
from mqtt_adapter import Adapter, PacketRejected


def replay(database, config, through, api=None):
    cutoff = datetime.fromisoformat(through.replace('Z', '+00:00'))
    if cutoff.utcoffset() is None:
        raise ValueError('The replay cutoff must include a timezone.')
    adapter = Adapter(config)
    counts = dict(scanned=0, unsupported=0, rejected=0, neighbors=0, power=0, accepted=0, duplicate=0)
    with sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True) as db:
        # A fixed cutoff and SQLite read snapshot bound a replay while MQTT runs.
        rows = db.execute('SELECT envelope FROM mqtt_archive WHERE receivedAt <= ? ORDER BY receivedAt,id', (through,))
        for (raw,) in rows:
            counts['scanned'] += 1
            item = json.loads(raw)
            try:
                received = datetime.fromisoformat(item['receivedAt'].replace('Z', '+00:00')).timestamp()
                packet = adapter.decode(item['topic'], base64.b64decode(item['payloadBase64'], validate=True),
                                        received, item['retained'])
            except (PacketRejected, ValueError):
                counts['rejected'] += 1
                continue
            if packet and packet['kind'] == 'neighbors':
                counts['neighbors'] += 1
            elif packet and packet['kind'] == 'telemetry':
                power = {key: value for key, value in packet['data'].items()
                         if re.fullmatch(r'(sensor|power[1-8])(Voltage|CurrentMa)', key)}
                if not power:
                    counts['unsupported'] += 1
                    continue
                # Older environment observations already occupy the original key.
                # Add an idempotent power-only supplement; never overwrite history.
                packet = {**packet, 'packetId': packet['packetId'] + ':power-v1', 'data': power}
                counts['power'] += 1
            else:
                counts['unsupported'] += 1
                continue
            if api:
                result = api.request('POST', '/api/meshlink/worker/ingest', packet)
                counts[result['outcome']] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--through', required=True, help='Inclusive original receipt UTC timestamp, ending in Z')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--credentials', type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z', args.through):
        parser.error('--through must be an ISO UTC timestamp with milliseconds')
    config = json.loads(args.config.read_text())
    api = None
    if args.apply:
        if not args.credentials:
            parser.error('--apply requires worker credentials')
        secret = json.loads(args.credentials.read_text())
        api = Client(config.get('apiUrl', 'http://127.0.0.1:8090'))
        api.login(secret['username'], secret['password'])
    print(json.dumps(replay(args.database, config, args.through, api), sort_keys=True))


if __name__ == '__main__':
    main()

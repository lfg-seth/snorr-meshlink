"""Combine private readbacks with worker-only export; no secrets on stdout."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('readbacks', type=Path)
    parser.add_argument('worker_export', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    os.umask(0o077)
    rows = json.loads(args.readbacks.read_text())
    labels = {row['shortName']: row for row in rows}
    expected = {'B001': '!699c2ed8', 'B002': '!699ca878',
                'G001': '!9ea13cc0', 'G002': '!849ad7a0'}
    if set(labels) != set(expected) or any(labels[k]['nodeId'] != v for k, v in expected.items()):
        raise ValueError('Unexpected physical device mapping.')
    if len({r['channelKey'] for r in rows}) != 1 or len({r['channel'] for r in rows}) != 1:
        raise ValueError('Bench channels do not match.')
    if any(not r['hardwareId'] for r in rows):
        raise ValueError('Physical device identity missing.')
    if len({r['hardwareId'] for r in rows}) != 4:
        raise ValueError('Physical device identities must be distinct.')
    config = json.loads(args.worker_export.read_text())
    config.update(channel=rows[0]['channel'], channelKey=rows[0]['channelKey'],
                  members={v: k.lower() for k, v in expected.items() if k.startswith('B')},
                  gateways={v: k.lower() for k, v in expected.items() if k.startswith('G')},
                  identities={k.lower(): {field: labels[k][field]
                             for field in ('nodeId', 'hardwareId', 'shortName')} for k in expected})
    with args.destination.open('x') as file:
        os.chmod(args.destination, 0o600)
        json.dump(config, file)
    print('Private portal MQTT config ready with four verified device mappings.')


if __name__ == '__main__':
    main()

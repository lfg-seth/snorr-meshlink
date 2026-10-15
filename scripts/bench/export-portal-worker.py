"""Export only the existing read-only worker credential for portal provisioning."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    os.umask(0o077)
    source = json.loads(args.source.read_text())
    if (source['host'], source['port'], source['tls'], source['root']) != (
            'mqtt.snorr.org', 8883, True, 'snorr/pilot'):
        raise ValueError('Unexpected broker configuration.')
    data = {key: source[key] for key in ('host', 'port', 'root')}
    data.update(username='pilot-worker', password=source['accounts']['pilot-worker'])
    # Refuse replacing any existing file/symlink; never rotate working credentials.
    with args.destination.open('x') as file:
        os.chmod(args.destination, 0o600)
        json.dump(data, file)
    print('Worker-only private export ready; broker accounts unchanged.')


if __name__ == '__main__':
    main()

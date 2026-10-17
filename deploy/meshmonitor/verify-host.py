#!/usr/bin/env python3
"""Read-only integration evidence, without printing tokens, node IDs or payloads."""

from collections import Counter
import json
from pathlib import Path
import sqlite3
import sys
import urllib.parse
import urllib.request


def get(url, token=None):
    request = urllib.request.Request(url, headers={} if token is None else {'Authorization': 'Bearer ' + token})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


if sys.argv[1] == 'grafana':
    live = sqlite3.connect('file:/var/lib/grafana/grafana.db?mode=ro', uri=True)
    before = sqlite3.connect('file:/root/meshmonitor-integration/grafana-before.db?mode=ro', uri=True)
    query = "SELECT name,value FROM resource WHERE resource='dashboards'"
    old = {row[0]: json.loads(row[1]).get('spec') for row in before.execute(query)}
    current = {row[0]: json.loads(row[1]).get('spec') for row in live.execute(query)}
    assert old.keys() <= current.keys()
    assert all(current[key] == value for key, value in old.items())
    assert 'snorr-meshmonitor' in current
    print('Existing dashboard specifications preserved:', len(old), '; added:', len(current) - len(old))
    dashboard = json.loads(Path('/var/lib/grafana/dashboards/snorr-meshmonitor/dashboard.json').read_text())
    for panel in dashboard['panels']:
        for target in panel.get('targets', []):
            result = get('http://prometheus.int.spp.lol:9090/api/v1/query?' + urllib.parse.urlencode({'query': target['expr']}))
            assert result['status'] == 'success'
    print('All dashboard expressions query successfully from the Grafana host.')
elif sys.argv[1] == 'prometheus':
    base = 'http://127.0.0.1:9090'
    flags = get(base + '/api/v1/status/flags')['data']
    assert flags['storage.tsdb.retention.time'] == '30d'
    targets = get(base + '/api/v1/targets')['data']['activeTargets']
    target = next(target for target in targets if target['labels']['job'] == 'snorr-meshmonitor')
    assert target['health'] == 'up' and not target['lastError']
    print('Prometheus retention 30d; MeshMonitor scrape up; sample count:', get(base + '/api/v1/query?' + urllib.parse.urlencode({'query': 'scrape_samples_scraped{job="snorr-meshmonitor"}'}))['data']['result'][0]['value'][1])
    print('Target health by job:', dict(Counter((target['labels']['job'], target['health']) for target in targets)))
    status = get(base + '/api/v1/query?' + urllib.parse.urlencode({'query': 'meshmonitor_source_connected{job="snorr-meshmonitor"}'}))
    assert status['data']['result'][0]['value'][1] == '1'
    print('Live MQTT connection metric is 1.')
elif sys.argv[1] == 'meshmonitor':
    db = sqlite3.connect('file:/data/meshmonitor.db?mode=ro', uri=True)
    print('Stored counts:', {table: db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] for table in ['nodes', 'telemetry', 'mqtt_packet_log']})
    print('Telemetry types/counts:', db.execute('SELECT telemetryType,count(*) FROM telemetry GROUP BY telemetryType').fetchall())
    print('Gateway groups represented:', db.execute('SELECT count(DISTINCT gatewayId) FROM mqtt_packet_log').fetchone()[0])
    print('Packet outcomes:', db.execute('SELECT ingestOutcome,count(*) FROM mqtt_packet_log GROUP BY ingestOutcome').fetchall())
    for source_type, enabled, raw_config in db.execute('SELECT type,enabled,config FROM sources'):
        if enabled:
            config = json.loads(raw_config)
            assert source_type == 'mqtt_bridge' and config['mode'] == 'subscribe_only'
            assert not config.get('brokerSourceId')
            assert config['upstream']['url'].startswith('mqtts://')
    print('Only standalone certificate-verified subscribe-only MQTT source enabled.')
else:
    raise SystemExit('Choose grafana, prometheus or meshmonitor')

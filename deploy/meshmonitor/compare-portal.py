#!/usr/bin/env python3
"""On the portal host, compare private MeshMonitor values against archived bytes."""

import base64
from datetime import datetime
import json
import math
from pathlib import Path
import sqlite3
import sys

sys.path.insert(0, '/opt/meshlink/backend')
from mqtt_adapter import Adapter, PacketRejected

config = json.loads(Path('/etc/meshlink/mqtt.json').read_text())
adapter = Adapter(config)
rows = json.loads(Path('/root/meshmonitor-compare-input.json').read_text())
db = sqlite3.connect('file:/var/lib/meshlink/pb_data/data.db?mode=ro', uri=True)
decoded = {}
for raw, in db.execute('SELECT envelope FROM mqtt_archive ORDER BY receivedAt DESC LIMIT 1000'):
    envelope = json.loads(raw)
    try:
        packet = adapter.decode(envelope['topic'], base64.b64decode(envelope['payloadBase64']),
                                datetime.fromisoformat(envelope['receivedAt'].replace('Z', '+00:00')).timestamp(), envelope.get('retained', False))
    except PacketRejected:
        continue
    if packet and packet['kind'] == 'telemetry':
        decoded[(packet['deviceId'], int(packet['packetId'].split(':')[0], 16))] = packet
matched = 0
for node_num, packet_id, metric, value in rows:
    node_id = f'!{node_num:08x}'
    device = {**config['members'], **config.get('infrastructure', {})}.get(node_id)
    packet = decoded.get((device, packet_id))
    if packet is None:
        continue
    key = 'battery' if metric == 'voltage' else metric
    if key not in packet['data']:
        continue
    assert math.isclose(packet['data'][key], value, rel_tol=1e-5, abs_tol=1e-5)
    # Also confirm the same normalized value was actually persisted by the portal.
    stored = db.execute('SELECT payload FROM observations WHERE deviceId=? AND packetKey LIKE ?',
                        (device, '%' + packet['packetId'] + '%')).fetchall()
    assert any(math.isclose(json.loads(raw).get(key, float('nan')), value, rel_tol=1e-5, abs_tol=1e-5) for raw, in stored)
    matched += 1
assert matched > 0
print('MeshMonitor telemetry matches archived-byte decoding AND stored portal observations:', matched, 'values; comparison rows:', len(rows))

"""Synthetic voltage examples only: daily solar recovery and a solar deficit."""
from datetime import datetime, timedelta, timezone
import json
import math
import sqlite3
from contextlib import closing
from zoneinfo import ZoneInfo


def voltage(device_id, measured_at, reference):
    local = measured_at.astimezone(ZoneInfo('America/Los_Angeles'))
    hour = local.hour + local.minute / 60 + local.second / 3600
    # Charge 06:00–16:00, then drain overnight; curved joins at dawn/dusk.
    cycle = (-math.cos(math.pi * (hour - 6) / 10) if 6 <= hour < 16
             else math.cos(math.pi * ((hour - 16) % 24) / 14))
    if device_id == 'r1':
        value = 3.93 + .18 * cycle
    elif device_id == 'r2':
        elapsed_days = (measured_at - reference).total_seconds() / 86400 + 30
        value = 4.0 - .017 * elapsed_days + .105 * cycle
    else:
        value = 4.05 + .008 * math.sin(hour * math.pi / 12)
    return round(value, 4)


def seed_history(path, reference):
    """Add reproducible history only to an explicitly marked synthetic DB."""
    with closing(sqlite3.connect(path)) as database:
        if database.execute('SELECT kind FROM meshlink_demo_marker').fetchall() != [('synthetic-only',)]:
            raise ValueError('Battery examples require a synthetic demo database.')
        # Preserve other telemetry and edits while bringing existing voltage rows
        # onto the same illustrative curves (including old worker readings).
        for record_id, device_id, measured_at, payload in database.execute(
                "SELECT id, deviceId, measuredAt, payload FROM observations WHERE deviceId IN ('r1','r2','b1')").fetchall():
            data = json.loads(payload)
            if measured_at and 'battery' in data:
                data['battery'] = voltage(device_id, datetime.fromisoformat(measured_at), reference)
                database.execute('UPDATE observations SET payload=? WHERE id=?', (json.dumps(data), record_id))
        for device_id, interval, age in [('r1', 10, 2), ('r2', 10, 22), ('b1', 5, 1)]:
            end = reference - timedelta(minutes=age)
            rows = []
            for minutes in range(30 * 24 * 60, -1, -interval):
                measured = end - timedelta(minutes=minutes)
                stamp = measured.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
                rows.append((device_id, stamp, f'demo-power-v1:{device_id}:{stamp}',
                             json.dumps({'battery': voltage(device_id, measured, reference)}), stamp, 'valid'))
            database.executemany('INSERT OR IGNORE INTO observations '
                '(deviceId,measuredAt,packetKey,payload,receivedAt,timestampQuality) VALUES (?,?,?,?,?,?)', rows)
            record_id, readings, config = database.execute(
                'SELECT id, readings, configuration FROM devices WHERE key=?', (device_id,)).fetchone()
            readings, config = json.loads(readings), json.loads(config)
            if 'battery' in readings:
                readings['battery']['value'] = voltage(device_id,
                    datetime.fromisoformat(readings['battery']['measuredAt']), reference)
            config['demoBatteryReference'] = reference.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
            database.execute('UPDATE devices SET readings=?, configuration=? WHERE id=?',
                             (json.dumps(readings), json.dumps(config), record_id))
        database.commit()

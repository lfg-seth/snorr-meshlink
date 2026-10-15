"""Fictional scenario only; these are not inventory or deployed-site records."""
from datetime import datetime, timedelta, timezone
import uuid


def at(minutes=0):
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


MEMBERS = [
    {'key': f'm{i}', 'name': name, 'initials': initials}
    for i, (name, initials) in enumerate([
        ('Demo Avery', 'DA'), ('Demo Jordan', 'DJ'), ('Demo Morgan', 'DM'),
        ('Demo Riley', 'DR'), ('Demo Casey', 'DC'),
    ], 1)
]
DEVICES = [
    {'key': f'd{i}', 'kind': 'member', 'number': f'{i:03}', 'shortName': f'S{i:03}', 'configuration': {'deviceType': 'Heltec V4'}}
    for i in range(1, 7)
]
for key, name, kind, longitude, latitude, cadence, equipped in [
    ('r1', 'Demo ridge relay', 'repeater', -115.680, 36.310, 5, {'solar': True, 'weather': True, 'intrusion': True}),
    ('r2', 'Demo canyon relay', 'repeater', -115.617, 36.279, 5, {'solar': True, 'weather': False, 'intrusion': False}),
    ('b1', 'Demo dispatch gateway', 'backhaul', -115.640, 36.250, 2, {'solar': False, 'weather': False, 'intrusion': False}),
    ('b2', 'Demo uplink gateway', 'backhaul', -115.657, 36.303, 2, {'solar': False, 'weather': False, 'intrusion': False}),
]:
    DEVICES.append({'key': key, 'kind': kind, 'configuration': {
        'name': name, 'longitude': longitude, 'latitude': latitude, 'cadenceMinutes': cadence,
        'equipped': equipped, 'downlink': key == 'b1',
        'batterySetup': 'Illustrative battery configuration · chemistry/cell count/capacity unverified',
        'solarSetup': 'Demo panel configuration unknown' if equipped['solar'] else 'Not configured',
        'antenna': 'Fiberglass (demo)' if kind == 'repeater' else 'Muzi whip (demo)',
    }})


def provision(superuser, credentials):
    """Only seed an empty database; repeated init never relabels prior records."""
    existing = superuser.request('GET', '/api/collections/devices/records?perPage=1')
    if existing['totalItems']:
        raise ValueError('Database already has devices. Demo initialization stopped without replacing records.')
    for member in MEMBERS:
        superuser.request('POST', '/api/collections/members/records', member)
    for device in DEVICES:
        superuser.request('POST', '/api/collections/devices/records', {**device, 'monitoringStartedAt': at()})
    for key, role, member_id, name in [
        ('admin', 'admin', '', 'Demo Dispatch'), ('member', 'member', 'm5', 'Demo Casey'),
        ('member2', 'member', 'm2', 'Demo Jordan'), ('worker', 'worker', '', 'Simulation worker'),
    ]:
        item = credentials[key]
        superuser.request('POST', '/api/collections/accounts/records', {
            'username': item['username'], 'name': name, 'role': role, 'memberId': member_id,
            'password': item['password'], 'passwordConfirm': item['password'],
        })
    for i in range(1, 5):
        superuser.request('POST', '/api/collections/assignments/records', {
            'deviceId': f'd{i}', 'memberId': f'm{i}', 'startedAt': at(110),
        })


def packet(device_id, kind, data, minutes=0, packet_id=None, gateway='b1'):
    return {'packetId': packet_id or uuid.uuid4().hex, 'deviceId': device_id,
            'gatewayId': gateway, 'kind': kind, 'measuredAt': at(minutes) if minutes is not None else None,
            'receivedAt': at(), 'data': data}


def initial_packets():
    coordinates = [(-115.633, 36.265), (-115.650, 36.274), (-115.662, 36.281), (-115.684, 36.270), (-115.674, 36.293)]
    for i, (coordinate, minutes) in enumerate(zip(coordinates, [1, 3, 8, 17, None]), 1):
        longitude, latitude = coordinate
        if minutes is not None:
            for step, age in enumerate([95, 90, 85, 42, 37, 32]):
                yield packet(f'd{i}', 'position', {'longitude': longitude - .002 * (6 - step), 'latitude': latitude - .001 * (6 - step), 'battery': 80 - i * 5}, age)
        yield packet(f'd{i}', 'position', {'longitude': longitude, 'latitude': latitude, 'battery': 80 - i * 5}, minutes)
    yield packet('r1', 'telemetry', {'battery': 3.58, 'temperature': 8.4, 'solar': 1.2, 'intrusion': True}, 12)
    yield packet('r1', 'telemetry', {'battery': 3.58, 'temperature': 8.4, 'solar': 1.2, 'intrusion': False}, 2)
    yield packet('r2', 'telemetry', {'battery': 3.9}, 22)
    yield packet('b1', 'telemetry', {'battery': 4.05}, 1)
    yield packet('d1', 'message', {'author': 'Demo Avery', 'text': 'Training scenario: simulated worker connected.'}, 1)

"""Fictional examples for the portal's battery, weather and radio details."""
from demo_power import voltage
from fixtures import packet


MEMBER_BATTERIES = {
    'd1': (3000, 4.15), 'd2': (1100, 3.92),
    'd3': (1000, 3.78), 'd4': (3000, 3.60),
}


def configurations():
    for key, (capacity, _) in MEMBER_BATTERIES.items():
        yield key, {'batteryProfile': 'lipo-1s', 'batteryCapacityMah': capacity}
    for key, cells in [('r1', 2), ('r2', 4)]:
        yield key, {
            'batteryProfile': 'eve-26v-1s',
            'batterySetup': f'EVE 26V · {cells} × 2550 mAh · 1S{cells}P (demo)',
            'solarSetup': '6 W panel (demo configuration)',
        }
    yield 'b1', {'batteryProfile': 'lipo-1s',
                 'batterySetup': 'LiPo · 1 cell · 1100 mAh whole pack · 1S (demo)'}


def telemetry(device_id, measured, reference):
    if device_id in MEMBER_BATTERIES:
        return {'battery': MEMBER_BATTERIES[device_id][1]}
    battery = voltage(device_id, measured, reference)
    data = {'battery': battery}
    if device_id == 'r1':
        # Channel signs are illustrative sensor values, not battery charge state.
        data.update(temperature=8.4, humidity=42, solar=1.2, intrusion=False,
                    sensorVoltage=0, sensorCurrentMa=0,
                    power1Voltage=battery, power1CurrentMa=45,
                    power3Voltage=5, power3CurrentMa=-18)
    elif device_id == 'r2':
        data.update(sensorVoltage=battery, sensorCurrentMa=-30)
    return data


def neighbor_packets():
    # Synthetic node IDs deliberately unrelated to inventoried hardware.
    for device_id, observer, heard, sequence, partial in [
        ('r1', '!de000001', [('d1', '!de000011', 8, -92, 12, 34),
                             ('r2', '!de000002', 0, -112, 120, 7)], 5, False),
        ('r2', '!de000002', [('r1', '!de000001', -2.5, -118, 1799, 1)], 9, True),
    ]:
        yield packet(device_id, 'neighbors', {
            'reportType': 'snns-v1', 'observerNodeId': observer,
            'bootId': 42, 'sequence': sequence, 'reportUptimeSeconds': 3600,
            'totalNeighbors': len(heard) + (2 if partial else 0),
            'subset': partial, 'capacityEvicted': partial,
            'rows': [{'heardDeviceId': key, 'heardNodeId': node,
                      'snrDb': snr, 'rssiDbm': rssi, 'hearingAgeSeconds': age,
                      'observationCount': count}
                     for key, node, snr, rssi, age, count in heard],
        }, None)

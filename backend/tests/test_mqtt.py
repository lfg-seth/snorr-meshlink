"""Synthetic encrypted wire fixtures, durable retries, and broker outage semantics."""
from datetime import datetime
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import Mock
import base64


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2, telemetry_pb2
from client import ApiError
from mqtt_adapter import Adapter, PacketRejected
from mqtt_worker import Spool, Worker

CONFIG = {'host': 'mqtt.example.invalid', 'username': 'worker', 'password': 'fictional',
          'root': 'snorr/pilot', 'channel': 'Test', 'channelKey': 'AAAAAAAAAAAAAAAAAAAAAA==',
          'members': {'!699c2ed8': 'b001'},
          'gateways': {'!9ea13cc0': 'g001', '!849ad7a0': 'g002'}}
NOW = 1792010000


def fixture(gateway='!9ea13cc0', measured=NOW - 30, packet_id=123, source=0x699c2ed8,
            port=portnums_pb2.POSITION_APP, coordinates=True, quality=None):
    position = mesh_pb2.Position(time=NOW, timestamp=measured)
    for key, value in (quality or {}).items():
        setattr(position, key, value)
    if coordinates:
        position.latitude_i, position.longitude_i = 362000000, -1156000000
    data = mesh_pb2.Data(portnum=port, payload=position.SerializeToString())
    packet = mesh_pb2.MeshPacket(id=packet_id)
    setattr(packet, 'from', source)
    # Known wire nonce: ID occupies 8 little-endian bytes, sender 4, counter 4.
    nonce = struct.pack('<QI', packet_id, source) + b'\0' * 4
    packet.encrypted = Cipher(algorithms.AES(b'\0' * 16), modes.CTR(nonce)).encryptor().update(data.SerializeToString())
    envelope = mqtt_pb2.ServiceEnvelope(packet=packet, channel_id='Test', gateway_id=gateway)
    return f'snorr/pilot/2/e/Test/{gateway}', envelope.SerializeToString()


class AdapterTests(unittest.TestCase):
    def test_gateway_health_wire_provenance_flags_clock_and_peer_route(self):
        config = {**CONFIG, 'infrastructure': {'!9ea13cc0': 'g001', '!849ad7a0': 'g002'}}
        def decode(payload, gateway='!849ad7a0', source=0x9ea13cc0):
            data = mesh_pb2.Data(portnum=portnums_pb2.PRIVATE_APP, payload=payload)
            p = mesh_pb2.MeshPacket(id=19)
            setattr(p, 'from', source)
            nonce = struct.pack('<QI', 19, source) + b'\0' * 4
            p.encrypted = Cipher(algorithms.AES(b'\0' * 16), modes.CTR(nonce)).encryptor().update(data.SerializeToString())
            wire = mqtt_pb2.ServiceEnvelope(packet=p, channel_id='Test', gateway_id=gateway)
            return Adapter(config).decode(f'snorr/pilot/2/e/Test/{gateway}', wire.SerializeToString(), NOW)
        payload = struct.pack('<4sBBHIIIIII', b'SNGH', 1, 0, 0, 0x9ea13cc0, 42, 7, 100, NOW-1, 180)
        actual = decode(payload)
        self.assertEqual(actual['kind'], 'gateway-health')
        self.assertEqual(actual['deviceId'], 'g001')
        self.assertEqual(actual['gatewayId'], CONFIG['gateways']['!849ad7a0'])
        self.assertFalse(actual['data']['wifiConnected'])
        self.assertFalse(actual['data']['mqttConnected'])
        for offset, value in [(4, 2), (5, 2), (5, 4), (6, 1), (8, 1), (12, 0), (16, 0), (28, 1)]:
            bad = bytearray(payload)
            bad[offset] = value
            with self.assertRaises(PacketRejected): decode(bytes(bad))
        with self.assertRaises(PacketRejected): decode(payload[:-1])
        with self.assertRaises(PacketRejected): decode(payload + b'\0')

    def wire_report(self, payload, port=portnums_pb2.PRIVATE_APP, gateway='!9ea13cc0'):
        source = 0x05237743
        data = mesh_pb2.Data(portnum=port, payload=payload)
        packet = mesh_pb2.MeshPacket(id=17)
        setattr(packet, 'from', source)
        packet.encrypted = Cipher(algorithms.AES(b'\0' * 16), modes.CTR(struct.pack('<QI', 17, source) + b'\0' * 4)).encryptor().update(data.SerializeToString())
        wire = mqtt_pb2.ServiceEnvelope(packet=packet, channel_id='Test', gateway_id=gateway)
        return Adapter({**CONFIG, 'infrastructure': {'!05237743': 'r003'}}).decode(
            f'snorr/pilot/2/e/Test/{gateway}', wire.SerializeToString(), NOW)

    def test_snns_wire_values_unknown_nodes_gateway_dedup_and_missing_absolute_time(self):
        header = struct.pack('<4sBBBBIIII', b'SNNS', 1, 3, 2, 9, 0x05237743, 42, 7, 100)
        rows = struct.pack('<IIhhI', 0x699c2ed8, 0, -80, 0, 15) + struct.pack('<IIhhI', 1234, 1799, -140, -13, 1)
        first = self.wire_report(header + rows)
        second = self.wire_report(header + rows, gateway='!849ad7a0')
        self.assertEqual(first['kind'], 'neighbors')
        self.assertEqual(first['packetId'], second['packetId'])
        self.assertEqual(first['data'], second['data'])
        self.assertIsNone(first['measuredAt'])
        report = first['data']
        self.assertTrue(report['subset'])
        self.assertTrue(report['capacityEvicted'])
        self.assertEqual(report['rows'][0], {'heardDeviceId': 'b001', 'heardNodeId': '!699c2ed8',
            'snrDb': 0, 'rssiDbm': -80, 'hearingAgeSeconds': 0, 'observationCount': 15})
        self.assertIsNone(report['rows'][1]['heardDeviceId'])
        self.assertEqual(report['rows'][1]['snrDb'], -3.25)
        for offset, value in [(4, 2), (5, 4), (6, 9), (7, 1), (8, 0), (12, 0), (16, 0)]:
            bad = bytearray(header + rows)
            bad[offset] = value
            with self.assertRaises(PacketRejected):
                self.wire_report(bytes(bad))
        for bad in [b'SNNS', header + rows[:-1], header + rows + b'\0',
                    header + rows[:16] * 2]:
            with self.assertRaises(PacketRejected):
                self.wire_report(bad)
        valid_header = struct.pack('<4sBBBBIIII', b'SNNS', 1, 0, 1, 1, 0x05237743, 42, 7, 100)
        for node, age, rssi, snr, count in [(0, 0, -80, 0, 1), (0x05237743, 0, -80, 0, 1),
                (123, 1800, -80, 0, 1), (123, 0, 0, 0, 1), (123, 0, -80, 401, 1), (123, 0, -80, 0, 0)]:
            with self.assertRaises(PacketRejected):
                self.wire_report(valid_header + struct.pack('<IIhhI', node, age, rssi, snr, count))
        self.assertIsNone(self.wire_report(b'other private application'))

    def test_standard_neighbor_unknown_scalar_zero_and_provenance(self):
        report = mesh_pb2.NeighborInfo(node_id=0x05237743)
        report.neighbors.add(node_id=0x699c2ed8, snr=5.5, last_rx_time=NOW)
        report.neighbors.add(node_id=123, snr=0)
        decoded = self.wire_report(report.SerializeToString(), portnums_pb2.NEIGHBORINFO_APP)
        self.assertEqual(decoded['data']['rows'][0]['snrDb'], 5.5)
        self.assertIsNone(decoded['data']['rows'][0]['rssiDbm'])
        self.assertIsNone(decoded['data']['rows'][1]['snrDb'])
        self.assertIsNone(decoded['measuredAt'])
        report.node_id = 123
        with self.assertRaises(PacketRejected):
            self.wire_report(report.SerializeToString(), portnums_pb2.NEIGHBORINFO_APP)

    def test_signed_power_metrics_preserve_channels_zero_presence_and_clocks(self):
        t = telemetry_pb2.Telemetry(time=NOW - 60)
        t.power_metrics.ch3_voltage = 4.2
        t.power_metrics.ch3_current = -323.1
        t.power_metrics.ch1_current = 0
        result = self.telemetry(t)
        self.assertAlmostEqual(result['data']['power3Voltage'], 4.2, places=5)
        self.assertAlmostEqual(result['data']['power3CurrentMa'], -323.1, places=4)
        self.assertEqual(result['data']['power1CurrentMa'], 0)
        self.assertNotIn('power1Voltage', result['data'])
        self.assertNotIn('battery', result['data'])
        self.assertEqual(result['packetId'], self.telemetry(t, '!849ad7a0')['packetId'])
        t.environment_metrics.voltage = 0.008
        t.environment_metrics.current = -0.4
        result = self.telemetry(t)
        self.assertAlmostEqual(result['data']['sensorCurrentMa'], -0.4)
        self.assertNotIn('power3CurrentMa', result['data'])
        t.environment_metrics.current = float('nan')
        with self.assertRaises(PacketRejected):
            self.telemetry(t)

    def telemetry(self, telemetry, gateway='!9ea13cc0'):
        source = 0x05237743
        data = mesh_pb2.Data(portnum=portnums_pb2.TELEMETRY_APP, payload=telemetry.SerializeToString())
        packet = mesh_pb2.MeshPacket(id=17)
        setattr(packet, 'from', source)
        packet.encrypted = Cipher(algorithms.AES(b'\0' * 16), modes.CTR(struct.pack('<QI', 17, source) + b'\0' * 4)).encryptor().update(data.SerializeToString())
        wire = mqtt_pb2.ServiceEnvelope(packet=packet, channel_id='Test', gateway_id=gateway)
        adapter = Adapter({**CONFIG, 'infrastructure': {'!05237743': 'r003'}})
        return adapter.decode(f'snorr/pilot/2/e/Test/{gateway}', wire.SerializeToString(), NOW)

    def test_environment_zero_values_unknown_clock_and_gateway_deduplication(self):
        t = telemetry_pb2.Telemetry(time=91)
        t.environment_metrics.temperature = 0
        t.environment_metrics.relative_humidity = 0
        first, second = self.telemetry(t), self.telemetry(t, '!849ad7a0')
        self.assertEqual(first['data'], {'temperature': 0, 'humidity': 0})
        self.assertEqual(first['deviceId'], 'r003')
        self.assertIsNone(first['measuredAt'])
        self.assertEqual(first['packetId'], second['packetId'])
        t.time = NOW - 60
        self.assertEqual(datetime.fromisoformat(self.telemetry(t)['measuredAt']).timestamp(), NOW - 60)
        t.time = NOW + 60
        self.assertGreater(self.telemetry(t)['measuredAt'], self.telemetry(t)['receivedAt'])

    def test_member_voltage_telemetry_preserves_measurement_and_deduplicates(self):
        telemetry = telemetry_pb2.Telemetry(time=NOW - 90)
        telemetry.device_metrics.voltage = 3.8
        data = mesh_pb2.Data(portnum=portnums_pb2.TELEMETRY_APP, payload=telemetry.SerializeToString())
        packet = mesh_pb2.MeshPacket(id=99)
        setattr(packet, 'from', 0x699c2ed8)
        packet.encrypted = Cipher(algorithms.AES(b'\0' * 16), modes.CTR(
            struct.pack('<QI', 99, 0x699c2ed8) + b'\0' * 4)).encryptor().update(data.SerializeToString())
        results = []
        for gateway in CONFIG['gateways']:
            wire = mqtt_pb2.ServiceEnvelope(packet=packet, channel_id='Test', gateway_id=gateway)
            results.append(self.adapter.decode(f'snorr/pilot/2/e/Test/{gateway}', wire.SerializeToString(), NOW))
        self.assertEqual(results[0]['deviceId'], 'b001')
        self.assertAlmostEqual(results[0]['data']['battery'], 3.8, places=5)
        self.assertEqual(datetime.fromisoformat(results[0]['measuredAt']).timestamp(), NOW - 90)
        self.assertEqual(results[0]['packetId'], results[1]['packetId'])

    def test_voltage_presence_and_invalid_environment(self):
        t = telemetry_pb2.Telemetry(time=NOW)
        t.device_metrics.battery_level = 101
        self.assertIsNone(self.telemetry(t))
        t.device_metrics.voltage = 4.1
        self.assertAlmostEqual(self.telemetry(t)['data']['battery'], 4.1, places=5)
        t.environment_metrics.relative_humidity = 101
        with self.assertRaises(PacketRejected):
            self.telemetry(t)
        t.environment_metrics.relative_humidity = float('nan')
        with self.assertRaises(PacketRejected):
            self.telemetry(t)

    def setUp(self):
        self.adapter = Adapter(CONFIG)

    def decode(self, **kwargs):
        topic, wire = fixture(**kwargs)
        return self.adapter.decode(topic, wire, NOW)

    def test_measurement_clock_and_gateway_independent_identity(self):
        first, second = self.decode(), self.decode(gateway='!849ad7a0')
        self.assertEqual(first['packetId'], second['packetId'])
        self.assertEqual(first['gatewayId'], 'g001')
        self.assertEqual(second['gatewayId'], 'g002')
        self.assertEqual(first['data'], {'latitude': 36.2, 'longitude': -115.6})
        self.assertEqual(datetime.fromisoformat(first['measuredAt']).timestamp(), NOW - 30)
        self.assertEqual(datetime.fromisoformat(first['receivedAt']).timestamp(), NOW)

    def test_reused_id_with_new_fix_and_zero_clock(self):
        self.assertNotEqual(self.decode()['packetId'], self.decode(measured=NOW - 20)['packetId'])
        self.assertIsNone(self.decode(measured=0)['measuredAt'])
        # Future clocks stay future for ingestion validation, never become receipt clocks.
        self.assertGreater(self.decode(measured=NOW + 60)['measuredAt'], self.decode()['receivedAt'])

    def test_position_quality_scaling_absence_and_gateway_duplicates(self):
        for raw, expected in [(183, 1.83), (282, 2.82), (300, 3), (601, 6.01)]:
            quality = {'PDOP': raw, 'sats_in_view': 9}
            first = self.decode(quality=quality)
            second = self.decode(quality=quality, gateway='!849ad7a0')
            self.assertEqual(first['data'], {'latitude': 36.2, 'longitude': -115.6,
                                            'pdop': expected, 'satellites': 9})
            self.assertEqual(first['data'], second['data'])
            self.assertEqual(first['packetId'], second['packetId'])
            self.assertEqual(first['measuredAt'], self.decode()['measuredAt'])
        for quality in [None, {'PDOP': 0, 'sats_in_view': 0}, {'HDOP': 150}]:
            self.assertEqual(self.decode(quality=quality)['data'],
                             {'latitude': 36.2, 'longitude': -115.6})
        self.assertNotEqual(self.decode(quality={'PDOP': 183})['packetId'],
                            self.decode(quality={'PDOP': 282})['packetId'])

    def test_recent_transmit_clock_never_refreshes_old_gps_solution(self):
        packet = self.decode(measured=NOW - 3600)
        self.assertEqual(datetime.fromisoformat(packet['measuredAt']).timestamp(), NOW - 3600)
        self.assertIsNone(self.decode(measured=0)['measuredAt'])

    def test_reject_unknown_retained_plaintext_and_topic_mismatch(self):
        with self.assertRaises(PacketRejected):
            self.decode(source=42)
        topic, wire = fixture()
        with self.assertRaises(PacketRejected):
            self.adapter.decode(topic, wire, NOW, retained=True)
        with self.assertRaises(PacketRejected):
            self.adapter.decode(topic.replace('Test', 'Other'), wire, NOW)
        with self.assertRaises(PacketRejected):
            self.adapter.decode(topic.replace('!9ea13cc0', '!849ad7a0'), wire, NOW)
        envelope = mqtt_pb2.ServiceEnvelope.FromString(wire)
        envelope.packet.decoded.portnum = portnums_pb2.POSITION_APP
        with self.assertRaises(PacketRejected):
            self.adapter.decode(topic, envelope.SerializeToString(), NOW)

    def test_missing_coordinates_malformed_and_other_kind(self):
        with self.assertRaises(PacketRejected):
            self.decode(coordinates=False)
        topic, _ = fixture()
        with self.assertRaises(PacketRejected):
            self.adapter.decode(topic, b'\xff', NOW)
        self.assertIsNone(self.decode(port=portnums_pb2.TEXT_MESSAGE_APP))


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'queue.sqlite'
        self.spool = Spool(self.path)
        self.addCleanup(lambda: self.spool.close())
        self.worker = Worker(CONFIG, {'username': 'worker', 'password': 'fictional'}, self.spool)
        self.worker.request = Mock(return_value={'outcome': 'accepted'})

    def test_restart_preserves_receipts_and_failed_api_does_not_ack(self):
        packet = Adapter(CONFIG).decode(*fixture(), NOW)
        self.spool.put(packet)
        self.spool.close()
        self.spool = Spool(self.path)
        self.worker.spool = self.spool
        self.assertEqual(self.spool.first()[1], packet)
        self.worker.request.side_effect = [None, OSError('API down')]
        with self.assertRaises(OSError):
            self.worker.tick()
        self.assertIsNotNone(self.spool.first())
        self.worker.request.side_effect = None
        self.worker.tick()
        self.assertIsNone(self.spool.first())

    def test_subscription_and_disconnect_heartbeat(self):
        success, failure = Mock(is_failure=False), Mock(is_failure=True)
        client = Mock()
        self.worker.on_connect(client, None, None, success, None)
        client.subscribe.assert_called_once_with('snorr/pilot/#', qos=1)
        self.worker.on_subscribe(None, None, 1, [failure], None)
        self.assertFalse(self.worker.connected.is_set())
        self.worker.on_subscribe(None, None, 1, [success], None)
        self.assertTrue(self.worker.connected.is_set())
        self.worker.on_disconnect(None, None, None, success, None)
        self.worker.tick()
        self.worker.request.assert_called_with('/api/meshlink/worker/heartbeat', {'connected': False})

    def test_archive_all_traffic_before_normalization_and_ack(self):
        for topic, payload, retained in [
            (*fixture(port=portnums_pb2.TEXT_MESSAGE_APP), False),
            (*fixture(source=42), False),
            ('snorr/pilot/arbitrary', b'\xff\x00', False),
            (*fixture(), True),
            ('snorr/pilot/empty', b'', False),
        ]:
            with self.subTest(topic=topic, retained=retained):
                client = Mock()
                message = Mock(topic=topic, payload=payload, retain=retained,
                               qos=1, dup=True, mid=7)
                self.worker.on_message(client, None, message)
                queued = self.spool.first()[1]
                self.assertEqual(base64.b64decode(queued['archive']['payloadBase64']), payload)
                self.assertEqual(queued['archive']['topic'], topic)
                self.assertTrue(queued['archive']['duplicate'])
                self.assertIsNone(queued['normalized'])
                client.ack.assert_called_once_with(7, 1)
                self.worker.tick()
                self.assertIsNone(self.spool.first())
                self.worker.request.assert_called_with('/api/meshlink/worker/archive', queued['archive'])

    def test_archive_retry_keeps_identity_and_normalized_rejection_can_drain(self):
        topic, payload = fixture()
        self.worker.on_message(Mock(), None, Mock(topic=topic, payload=payload,
            retain=False, qos=0, dup=False, mid=0))
        queued = self.spool.first()[1]
        self.worker.request.side_effect = [None, OSError('API unavailable')]
        with self.assertRaises(OSError):
            self.worker.tick()
        self.assertEqual(self.spool.first()[1], queued)
        self.worker.request.side_effect = [None, {}, ApiError(400, 'rejected')]
        self.worker.tick()
        self.assertIsNone(self.spool.first())

    def test_message_rejection_and_storage_failure(self):
        topic, payload = fixture()
        message = Mock(topic=topic, payload=payload, retain=False, qos=1, dup=False, mid=7)
        self.worker.on_message(Mock(), None, message)
        self.assertIsNotNone(self.spool.first())
        self.worker.spool.put = Mock(side_effect=OSError('disk full'))
        client = Mock()
        self.worker.on_message(client, None, message)
        self.assertTrue(self.worker.fatal.is_set())
        client.disconnect.assert_called_once()


if __name__ == '__main__':
    unittest.main()

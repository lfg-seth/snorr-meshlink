"""Shared-channel wire filtering, one-shot publication and overlap backup invariants."""
import base64
from contextlib import closing
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import sys
import tarfile
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mqtt_dispatch as dispatch
from mqtt_adapter import Adapter, channel_cipher, channel_hash, DISPATCH_NODE, G008, PacketRejected
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from mqtt_worker import Spool, Worker

KEY = bytes(range(16))
CONFIG = {'host':dispatch.HOST, 'port':8883, 'root':dispatch.ROOT, 'channel':dispatch.CHANNEL,
          'channelKey':base64.b64encode(KEY).decode(), 'members':{'!12345678':'b004'},
          'gateways':{G008:'gateway-a','!11223344':'gateway-b'}, 'sharedMessages':True,
          'username':'reader','password':'fictional'}
NOW = time.time()


def uplink(source=0x12345678, gateway=G008, text=b'hello', **fields):
    e = mqtt_pb2.ServiceEnvelope(channel_id=dispatch.CHANNEL, gateway_id=gateway)
    p = e.packet
    setattr(p, 'from', source)
    p.id, p.to, p.channel = 42, 0xffffffff, channel_hash(dispatch.CHANNEL, KEY)
    p.encrypted = channel_cipher(KEY, p).encryptor().update(
        mesh_pb2.Data(portnum=portnums_pb2.TEXT_MESSAGE_APP, payload=text).SerializeToString())
    for k,v in fields.items():
        setattr(p,k,v)
    return f'{dispatch.ROOT}/2/e/{dispatch.CHANNEL}/{gateway}', e.SerializeToString()


class ChannelTests(unittest.TestCase):
    def test_only_eligible_shared_texts(self):
        a = Adapter(CONFIG)
        first = a.decode(*uplink(), NOW)
        self.assertEqual(first['data'], {'text':'hello','source':'!12345678'})
        second = a.decode(*uplink(gateway='!11223344'), NOW + 6)
        self.assertEqual(first['packetId'], second['packetId'])
        self.assertNotEqual(first['gatewayId'], second['gatewayId'])
        self.assertEqual(a.decode(*uplink(source=17), NOW)['deviceId'],'!00000011')
        for fields in ({'to':0x11223344},{'channel':255 - channel_hash(dispatch.CHANNEL,KEY)},
                       {'source':DISPATCH_NODE}):
            self.assertIsNone(a.decode(*uplink(**fields), NOW))
        for fields in ({'pki_encrypted':True},{'via_mqtt':True},{'text':b'\xff'},{'text':b'x'*234}):
            with self.assertRaises(PacketRejected):
                a.decode(*uplink(**fields), NOW)
        with self.assertRaises(PacketRejected):
            a.decode(*uplink(), NOW, True)
        self.assertIsNone(a.decode(dispatch.TOPIC, dispatch.envelope(KEY, 42, 'dispatch echo'), NOW))

    def test_publish_envelope_and_multibyte_ceiling(self):
        text = 'D: ' + 'é' * 115
        e = mqtt_pb2.ServiceEnvelope.FromString(dispatch.envelope(KEY, 39, text))
        p = e.packet
        self.assertEqual((e.gateway_id,e.channel_id,p.id,getattr(p,'from'),p.to),
                         ('dispatch','SNORRbench',39,DISPATCH_NODE,0xffffffff))
        self.assertEqual((p.channel,p.hop_start,p.hop_limit),(channel_hash('SNORRbench',KEY),1,1))
        data = mesh_pb2.Data.FromString(channel_cipher(KEY,p).decryptor().update(p.encrypted))
        self.assertEqual((data.portnum,data.payload),(portnums_pb2.TEXT_MESSAGE_APP,text.encode()))
        with self.assertRaises(ValueError):
            dispatch.envelope(KEY,39,text+'x')

    def test_publish_once_even_if_ack_lost_or_denied(self):
        request = {'text':'D: test','packetId':'00112233','expiresAt':int((time.time()+9)*1000)}
        for ack,expected in [('accepted','broker_accepted'),('denied','rejected'),('lost','unknown')]:
            client = Mock()
            def loop(timeout):
                client.on_connect(client,None,None,Mock(is_failure=False),None)
                if ack != 'lost':
                    client.on_publish(client,None,1,Mock(is_failure=ack=='denied'),None)
                return 1
            client.loop.side_effect = loop
            with patch.object(dispatch,'publisher',return_value=client):
                self.assertEqual(dispatch.publish(CONFIG,request),expected)
            self.assertEqual(client.publish.call_count,1)
            args,kwargs = client.publish.call_args
            self.assertEqual(args[0],dispatch.TOPIC)
            self.assertEqual((kwargs['qos'],kwargs['retain']),(1,False))
            client.reconnect.assert_not_called()
        with patch.object(dispatch,'publisher') as make:
            self.assertEqual(dispatch.publish(CONFIG,{**request,'expiresAt':1}),'not_sent')
            make.assert_not_called()

    def test_overlap_health_independent_of_legacy_and_archive_has_broker(self):
        with tempfile.TemporaryDirectory() as tmp, closing(Spool(Path(tmp)/'q.sqlite')) as spool:
            w = Worker(CONFIG, {}, spool, CONFIG)
            w.request = Mock()
            w.connected.set()
            w.dispatch_connected.set()
            w.heartbeat()
            self.assertFalse(w.request.call_args.args[1]['ready'])
            topic,payload = uplink()
            w.on_message(Mock(), None, Mock(topic=topic,payload=payload,retain=False,qos=1,dup=False))
            self.assertEqual(spool.first()[1]['archive']['broker'],dispatch.HOST)
            w.heartbeat()
            self.assertEqual(w.request.call_args.args,('/api/meshlink/worker/channel-heartbeat',
                {'connected':True,'ready':True,'gatewayId':'gateway-a'}))
            w.on_disconnect(None,None,None,None,None)
            w.connected.set()
            w.heartbeat()
            self.assertFalse(w.request.call_args.args[1]['ready'])

    def test_online_queue_snapshot_includes_committed_wal(self):
        path = Path(__file__).resolve().parents[2] / 'deploy/portal/backup.py'
        spec = importlib.util.spec_from_file_location('backup',path)
        backup = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(backup)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with closing(sqlite3.connect(root/'receipts.sqlite')) as db:
                db.execute('pragma journal_mode=wal')
                db.execute('create table queue (id integer)')
                db.execute('insert into queue values (42)')
                db.commit()
                buf = io.BytesIO()
                with tarfile.open(fileobj=buf,mode='w:') as tar:
                    backup.add_worker_state(tar,root,'worker-state')
                buf.seek(0)
                with tarfile.open(fileobj=buf) as tar:
                    self.assertFalse(any(n.endswith(('-shm','-wal','-journal')) for n in tar.getnames()))
                    snapshot = root/'restored'
                    snapshot.write_bytes(tar.extractfile('worker-state/receipts.sqlite').read())
                with closing(sqlite3.connect(snapshot)) as restored:
                    self.assertEqual(restored.execute('select * from queue').fetchall(),[(42,)])

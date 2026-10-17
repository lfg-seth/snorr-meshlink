import argparse
import contextlib
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from capture import AirtimeStats, Decoder, WireParser, decode_snns
from meshtastic.protobuf import mesh_pb2, telemetry_pb2
from sniffer import CaptureSession, SnifferWindow

KEY = bytes(range(16))
HEADER = struct.pack("<IIIBBBB", 0xffffffff, 0x01020304, 0x11223344, 0x63, 54, 0, 0x04)
GOLDEN = HEADER + bytes.fromhex("7381dddc1af0b70bfdc1327e98c33262718cf43e95bd")


def temp_dir():
    root = Path(__file__).resolve().parents[3] / "local-data/sniffer-tests"
    root.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=root)


def wire(raw=GOLDEN, seq=1, ms=1000, state=0, boot="deadbeef"):
    lines = ["INFO | SNORR_CFG v=1 fw=test freq=910.000000 bw=250.000 sf=11 cr=5 tx=0",
             f"INFO | SNORR_RX v=1 boot={boot} seq={seq} ms={ms} len={len(raw)} state={state} rssi=-50 snr=6.25 toa=722"]
    lines.extend(f"INFO | SNORR_DATA seq={seq} off={off} hex={raw[off:off+40].hex()}" for off in range(0, len(raw), 40))
    lines.append(f"INFO | SNORR_END seq={seq} crc={zlib.crc32(raw):08x}")
    return "\n".join(lines) + "\n"


def parse(text):
    parser = WireParser()
    events = []
    for line in text.splitlines():
        events.extend(parser.feed(line))
    events.extend(parser.finish())
    return events


class DecodeTests(unittest.TestCase):
    def test_known_ciphertext_header_and_text(self):
        event = Decoder([("Test", KEY)]).decode(GOLDEN)
        self.assertEqual(event["content"]["text"], "SNORR sniffer test")
        self.assertEqual(event["sender"], "!01020304")
        self.assertEqual(event["packet_id"], "11223344")
        self.assertEqual((event["hop_limit"], event["hop_start"]), (3, 3))
        self.assertEqual(event["decode_status"], "decoded_candidate")

    def test_unknown_key_and_pki_keep_bytes(self):
        event = Decoder().decode(GOLDEN)
        self.assertEqual(event["decode_status"], "encrypted_or_unknown")
        self.assertEqual(event["raw_hex"], GOLDEN.hex())
        self.assertEqual(event["relay"], 4)
        pki = bytearray(GOLDEN)
        pki[13] = 0
        self.assertEqual(Decoder().decode(pki)["decode_status"], "encrypted_or_unknown")

    def test_bad_radio_and_short_frames_never_decoded(self):
        self.assertEqual(Decoder([("Test", KEY)]).decode(GOLDEN, -7)["decode_status"], "radio_error")
        self.assertEqual(Decoder().decode(b"abc")["decode_status"], "short_frame")

    def test_empty_and_invalid_application_data_keep_the_port(self):
        # A zero-byte PSK channel sends the Data protobuf unchanged.
        name = "Plain"
        header = bytearray(HEADER)
        from capture import xor_hash
        header[13] = xor_hash(name.encode())
        decoder = Decoder([(name, b"")])
        empty = mesh_pb2.Data(portnum=1)
        self.assertEqual(decoder.decode(header + empty.SerializeToString())["content"]["text"], "")
        bad = mesh_pb2.Data(portnum=67, payload=b"\xff")
        result = decoder.decode(header + bad.SerializeToString())
        self.assertEqual(result["port"], "TELEMETRY_APP")
        self.assertEqual(result["content"]["payload_hex"], "ff")
        self.assertIn("decode_error", result["content"])

    def test_zero_gps_and_negative_power_fields_retained(self):
        telemetry = telemetry_pb2.Telemetry(time=123)
        telemetry.power_metrics.ch3_voltage = 4.2
        telemetry.power_metrics.ch3_current = -323.1
        decoded = Decoder.content(67, telemetry.SerializeToString(), 1)
        self.assertAlmostEqual(decoded["power_metrics"]["ch3_current"], -323.1, places=3)
        position = mesh_pb2.Position(latitude_i=0, longitude_i=0, sats_in_view=7)
        decoded = Decoder.content(3, position.SerializeToString(), 1)
        self.assertEqual(decoded["latitude_i"], 0)
        self.assertEqual(decoded["longitude_i"], 0)

    def test_private_neighbor_contract(self):
        payload = struct.pack("<4sBBBBIIII", b"SNNS", 1, 0, 1, 1, 1, 7, 9, 300)
        payload += struct.pack("<IIhhI", 2, 42, -91, -10, 8)
        decoded = decode_snns(payload, 1)
        self.assertEqual(decoded["sequence"], 9)
        self.assertEqual(decoded["neighbors"][0]["snr_db"], -2.5)
        self.assertEqual(decoded["neighbors"][0]["observations"], 8)
        with self.assertRaises(ValueError):
            decode_snns(payload[:-1], 1)


class CaptureTests(unittest.TestCase):
    def test_all_lengths_and_byte_values(self):
        for length in (0, 1, 16, 40, 41, 255):
            raw = bytes(range(length))
            events = parse(wire(raw))
            self.assertFalse(any(e["type"] == "capture_gap" for e in events))
            self.assertEqual([e["raw"] for e in events if e["type"] == "reception"], [raw])

    def test_duplicates_and_foreign_packets_never_dropped(self):
        events = parse(wire() + wire(seq=2, ms=2000) + wire(raw=b"foreign frame contents", seq=3, ms=3000))
        receptions = [e for e in events if e["type"] == "reception"]
        stats = AirtimeStats()
        for now, event in enumerate(receptions):
            event.update(Decoder().decode(event.pop("raw")))
            stats.add(event, now)
        self.assertEqual(len(receptions), 3)
        self.assertTrue(receptions[1]["duplicate"])
        self.assertEqual(stats.snapshot(2)["packets"], 3)
        self.assertAlmostEqual(stats.snapshot(2)["rx_airtime_60s_percent"], 3 * 722 / 600)
        self.assertEqual(stats.snapshot(63)["rx_airtime_60s_percent"], 0)
        self.assertAlmostEqual(stats.snapshot(63)["peak_rx_airtime_60s_percent"], 3 * 722 / 600)

    def test_serial_corruption_and_sequence_loss_are_visible(self):
        for text in (wire().replace("hex=", "hex=ff", 1), wire().replace("off=0", "off=1", 1),
                     wire().replace("SNORR_END", "MISSING_END") + wire(seq=3),
                     wire() + wire(seq=4)):
            self.assertTrue(any(e["type"] == "capture_gap" for e in parse(text)))
        self.assertEqual(len([e for e in parse(wire() + wire(seq=1, boot="newboot")) if e["type"] == "reception"]), 2)

    def test_replay_files_are_unique_and_complete(self):
        with temp_dir() as temp:
            fixture = Path(temp) / "input.raw"
            fixture.write_bytes((wire() + wire(seq=2, ms=61000) + wire(b"bad", seq=3, ms=62000, state=-7)).encode())
            captures = []
            for _ in range(2):
                session = CaptureSession(None, Decoder([("Test", KEY)]), temp, replay=fixture)
                with contextlib.redirect_stdout(io.StringIO()):
                    session.run()
                self.assertIsNone(session.error)
                events = [json.loads(x) for x in (session.directory / "events.jsonl").read_text(encoding="utf8").splitlines()]
                captures.append(session.directory)
                self.assertEqual(len([e for e in events if e["type"] == "reception"]), 3)
                self.assertEqual((session.directory / "serial.raw").read_bytes(), fixture.read_bytes())
                self.assertIn("SNORR sniffer test", (session.directory / "messages.log").read_text(encoding="utf8"))
                self.assertNotIn("AAECAwQFBgcICQoLDA0ODw==", (session.directory / "events.jsonl").read_text(encoding="utf8"))
                summary = json.loads((session.directory / "summary.json").read_text())
                self.assertEqual(summary["radio_errors"], 1)
                self.assertAlmostEqual(summary["rx_airtime_60s_percent"], 2 * 722 / 600)
            self.assertNotEqual(*captures)

    def test_receive_only_serial_partial_reads_and_close(self):
        fixture = wire().encode()
        class FakeSerial:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
                self.chunks = [fixture[i:i+7] for i in range(0, len(fixture), 7)]
                self.closed = False
            def open(self):
                self.assert_passive = self.dtr is False and self.rts is False
            def set_buffer_size(self, **kwargs):
                pass
            @property
            def in_waiting(self):
                return 7
            def read(self, count):
                if self.chunks:
                    return self.chunks.pop(0)
                session.stop.set()
                return b""
            def close(self):
                self.closed = True
        with temp_dir() as temp, patch("sniffer.serial.Serial", FakeSerial):
            session = CaptureSession("fake", Decoder([("Test", KEY)]), temp)
            with contextlib.redirect_stdout(io.StringIO()):
                session.run()
            self.assertIsNone(session.error)
            self.assertEqual(session.snapshot()["packets"], 1)
            self.assertEqual((session.directory / "serial.raw").read_bytes(), fixture)


class GuiTests(unittest.TestCase):
    def test_replay_start_table_details_and_saved_capture(self):
        try:
            import tkinter as tk
            probe = tk.Tk()
            probe.withdraw()
            probe.destroy()
        except Exception:
            self.skipTest("Tk display unavailable")
        with temp_dir() as temp:
            fixture = Path(temp) / "input.raw"
            fixture.write_text(wire() + wire(seq=2, ms=2000))
            args = argparse.Namespace(port="replay", keys=None, replay=fixture, log_dir=Path(temp), duration=None, autostart=False)
            gui = SnifferWindow(args)
            gui.root.withdraw()
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    gui.start()
                    gui.thread.join(5)
                gui.tick()
                self.assertEqual(len(gui.table.get_children()), 2)
                gui.table.selection_set(gui.table.get_children()[1])
                gui.select()
                detail = json.loads(gui.detail.get("1.0", "end"))
                self.assertTrue(detail["duplicate"])
                self.assertEqual(detail["raw_hex"], GOLDEN.hex())
                self.assertTrue((gui.session.directory / "summary.json").exists())
            finally:
                gui.close()


if __name__ == "__main__":
    unittest.main()

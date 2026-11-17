"""USB retrieval for the Heltec handheld. Requires pyserial."""
import argparse
import csv
import os
import struct
import tempfile
import time
from pathlib import Path

import serial

MAGIC = b"\0SH1"
FRAME = b"\x94\xc3"
COLUMNS = ("site", "site_status", "round", "attempt", "repeater", "node_id",
           "elapsed_start_ms", "elapsed_end_ms", "outcome", "uplink_rssi_dbm",
           "uplink_snr_db", "downlink_rssi_dbm", "downlink_snr_db", "rtt_ms")


class Handheld:
    def __init__(self, port):
        self.io = serial.Serial(port=None, baudrate=115200, timeout=.08, write_timeout=2)
        self.io.dtr = self.io.rts = False
        self.io.port = port
        self.buf = bytearray()

    def __enter__(self):
        self.io.open()
        try:
            self.info()
        except BaseException:
            self.io.close()
            raise
        return self

    def __exit__(self, *_):
        self.io.close()

    def request(self, command, timeout=6):
        payload = MAGIC + command.encode("ascii")
        self.io.write(FRAME + struct.pack(">H", len(payload)) + payload)
        until = time.monotonic() + timeout
        while time.monotonic() < until:
            pos = self.buf.find(FRAME)
            if pos < 0:
                del self.buf[:len(self.buf) - int(self.buf.endswith(FRAME[:1]))]
            elif pos:
                del self.buf[:pos]
            elif len(self.buf) >= 4:
                length = int.from_bytes(self.buf[2:4], "big")
                if not 0 < length <= 512:
                    del self.buf[:1]
                    continue
                if len(self.buf) >= 4 + length:
                    packet = self.buf[4:4 + length]
                    del self.buf[:4 + length]
                    if packet.startswith(MAGIC):
                        answer = packet[4:].decode("ascii")
                        if answer.startswith("ERR"):
                            raise RuntimeError(answer)
                        return answer
                    continue
            self.buf.extend(self.io.read(max(1, min(2048, self.io.in_waiting))))
        raise TimeoutError("Handheld USB response timed out")

    def info(self):
        fields = self.request("INFO").split()
        if fields[:2] != ["INFO", "1"] or len(fields) != 10:
            raise ValueError("Unexpected handheld protocol")
        return dict(zip(("counter", "slots", "mask", "view", "attempts", "resolved", "utc", "storage"),
                        map(int, fields[2:]), strict=True))

    def export(self, writer):
        before = self.info()
        cursor = rows = sites = 0
        writer.writerow(COLUMNS)
        while cursor < before["slots"]:
            record = self.request(f"NEXT {cursor}").split()
            if record == ["END"]:
                break
            if len(record) != 6 or record[0] != "NEXT":
                raise ValueError("Invalid site descriptor")
            slot, number, status, mask = int(record[1]), int(record[2]), record[3], int(record[4])
            if not cursor <= slot < before["slots"] or number > before["counter"] or not 0 < mask < 1024:
                raise ValueError("Survey records changed during export")
            for i in range(mask.bit_count() * 10):
                raw = self.request(f"ROW {slot} {i}")
                if raw == "END":
                    if status == "complete":
                        raise ValueError("Completed site has missing attempts")
                    break
                if not raw.startswith("ROW "):
                    raise ValueError("Invalid attempt")
                data = next(csv.reader([raw[4:]]))
                expected = [str(number), status, str(i // mask.bit_count() + 1), str(i + 1)]
                if len(data) != len(COLUMNS) or data[:4] != expected:
                    raise ValueError("Attempt identity changed during export")
                writer.writerow(data)
                rows += 1
            cursor, sites = slot + 1, sites + 1
        if before["counter"] != self.info()["counter"]:
            raise RuntimeError("Site counter changed during export")
        return sites, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("status")
    sub.add_parser("clock", help="Set UTC from this computer")
    sub.add_parser("screen", help="Read the handheld's current OLED text")
    sub.add_parser("export").add_argument("--output", type=Path, required=True)
    sub.add_parser("clear").add_argument("--confirm-counter", type=int, required=True)
    args = parser.parse_args()
    with Handheld(args.port) as board:
        if args.action == "status":
            print(board.info())
        elif args.action == "clock":
            print(board.request(f"CLOCK {int(time.time())}"))
        elif args.action == "screen":
            print(board.request("UI"))
        elif args.action == "clear":
            print(board.request(f"ERASE SURVEYS {args.confirm_counter}", timeout=30))
        else:
            args.output.parent.mkdir(exist_ok=True, parents=True)
            tmp = None
            try:
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False,
                                                 dir=args.output.parent) as stream:
                    tmp = Path(stream.name)
                    sites, rows = board.export(csv.writer(stream))
                os.replace(tmp, args.output)
                print(f"Exported {rows} attempts across {sites} sites to {args.output}")
            finally:
                if tmp is not None:
                    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()

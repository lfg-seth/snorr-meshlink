"""Capture SNORR screenless gateway USB survey lines without opening a mesh API session."""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import re
import statistics
import time

import serial

LINE = re.compile(rb'SNWF (measured|unavailable|disconnected) (\d+) ms(?: (-?\d+) dBm ch (\d+) association (\d+))?\r?$')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--port', required=True)
    ap.add_argument('--label', default='', help='e.g. stock-vertical-20m')
    ap.add_argument('--samples', type=int, default=60)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if not 1 <= args.samples <= 1500:
        ap.error('use 1 to 1500 samples per run')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest = args.output or Path(__file__).resolve().parents[2]/'local-data'/'wifi-surveys'/f'{stamp}.csv'
    dest.parent.mkdir(parents=True, exist_ok=True)
    radio = serial.Serial(port=None, baudrate=115200, timeout=1)
    radio.dtr = radio.rts = False
    radio.port = args.port
    groups, losses = {}, 0
    with dest.open('x', newline='', encoding='utf-8') as f, radio:
        rows = csv.writer(f)
        rows.writerow(['utc','label','uptime_ms','state','rssi_dbm','channel','association'])
        radio.write(b'\nWIFI ON\n')
        seen, last = 0, time.monotonic()
        try:
            while seen < args.samples:
                if time.monotonic() - last > 20:
                    raise SystemExit('No survey data for 20 seconds; check firmware and close competing serial clients.')
                line = radio.read_until(b'\n', 1024).rstrip(b'\n')
                m = LINE.fullmatch(line)
                if not m or (m[1] == b'measured') != (m[3] is not None):
                    continue
                state, uptime, signal, channel, association = [s.decode() if s else '' for s in m.groups()]
                rows.writerow([datetime.now(timezone.utc).isoformat(timespec='milliseconds'),args.label,uptime,state,signal,channel,association])
                f.flush()
                print(m[0].decode().strip(), flush=True)
                if state == 'measured':
                    groups.setdefault((channel,association), []).append(int(signal))
                elif state == 'disconnected':
                    losses += 1
                seen += 1
                last = time.monotonic()
        finally:
            radio.write(b'\nWIFI OFF\n')
            radio.flush()
            print(f'{seen} samples, {losses} disconnected. CSV: {dest}')
            for (channel, association), values in groups.items():
                print(f'ch {channel} association {association}: n={len(values)}, min/median/max '
                      f'{min(values)}/{statistics.median(values):g}/{max(values)} dBm')


if __name__ == '__main__':
    main()

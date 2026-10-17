#!/usr/bin/env python3
"""Windows/Linux airtime sniffer. No serial commands or RF transmissions."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import queue
import sys
import threading
import time
import uuid

import serial
from serial.tools import list_ports

from capture import AirtimeStats, Decoder, WireParser, packet_line, utc_now

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KEYS = ROOT / "private/sniffer/channels.json"
DEFAULT_LOGS = ROOT / "local-data/sniffer"


class CaptureSession:
    def __init__(self, port, decoder, output=DEFAULT_LOGS, callback=None, replay=None, duration=None):
        self.port, self.decoder = port, decoder
        self.callback, self.replay, self.duration = callback, replay, duration
        self.directory = Path(output) / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8])
        self.directory.mkdir(parents=True, exist_ok=False)
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.stats, self.parser = AirtimeStats(), WireParser()
        self.started = time.monotonic()
        self.replay_clock = 0.0
        self.last_device_clock = None
        self.error = None
        self.completed = False
        self.events_file = None
        self.text_file = None
        self.receptions = 0
        (self.directory / "session.json").write_text(json.dumps({"started_at": utc_now(), "port": port,
            "tool_version": 1, "mode": "replay" if replay else "serial-rx-only", "baud": 115200,
            "keys_loaded": len(decoder.channels), "scope": "selected frequency/modem; receive interrupts only"}, indent=2), encoding="utf-8")

    def current_time(self):
        return self.replay_clock if self.replay else time.monotonic() - self.started

    def snapshot(self):
        with self.lock:
            return self.stats.snapshot(self.current_time())

    def emit(self, event):
        event["received_at"] = utc_now()
        if event["type"] == "reception":
            event.update(self.decoder.decode(event.pop("raw"), event["radio_state"]))
            if self.replay:
                current = (event["boot"], event["device_ms"])
                if self.last_device_clock and current[0] == self.last_device_clock[0]:
                    self.replay_clock += ((current[1] - self.last_device_clock[1]) & 0xffffffff) / 1000
                self.last_device_clock = current
            self.receptions += 1
        event["elapsed_seconds"] = round(self.current_time(), 3)
        with self.lock:
            self.stats.add(event, self.current_time())
        self.events_file.write(json.dumps(event, ensure_ascii=False) + "\n")
        if event["type"] != "radio_config":
            line = packet_line(event)
            # Keep each packet on one console line; full control characters remain escaped in JSONL.
            line = "".join(c if c.isprintable() else f"\\x{ord(c):02x}" for c in line)
            self.text_file.write(line + "\n")
            try:
                print(line, flush=True)
            except (BrokenPipeError, OSError):
                pass
        if self.callback:
            self.callback(event)

    def run(self):
        source = None
        try:
            with (self.directory / "events.jsonl").open("w", encoding="utf-8", buffering=1) as events, \
                 (self.directory / "messages.log").open("w", encoding="utf-8", buffering=1) as messages, \
                 (self.directory / "serial.raw").open("wb", buffering=0) as raw:
                self.events_file, self.text_file = events, messages
                if self.replay:
                    source = Path(self.replay).open("rb")
                else:
                    source = serial.Serial(port=None, baudrate=115200, timeout=0.2, exclusive=True)
                    source.dtr, source.rts = False, False
                    source.port = self.port
                    source.open()
                    try:
                        source.set_buffer_size(rx_size=65536)
                    except (AttributeError, NotImplementedError):
                        pass
                try:
                    self.emit({"type": "capture_started", "mode": "replay" if self.replay else "serial-rx-only"})
                    buffer = bytearray()
                    warned = False
                    while not self.stop.is_set():
                        if self.duration is not None and time.monotonic() - self.started >= self.duration:
                            break
                        chunk = source.read(4096 if self.replay else max(1, min(source.in_waiting, 4096)))
                        if self.replay and not chunk:
                            break
                        raw.write(chunk)
                        buffer.extend(chunk)
                        while b"\n" in buffer:
                            line, _, tail = buffer.partition(b"\n")
                            buffer = bytearray(tail)
                            for event in self.parser.feed(line.decode("utf-8", errors="replace")):
                                self.emit(event)
                        if len(buffer) > 8192:
                            buffer.clear()
                            self.emit({"type": "capture_gap", "reason": "Serial line exceeds 8192 bytes; resynchronizing"})
                        if not self.replay and not warned and self.current_time() > 20 and not self.parser.config:
                            warned = True
                            self.emit({"type": "notice", "reason": "Waiting for sniffer frames. Check target/port, antenna and matching RF profile; no packet may have arrived yet."})
                    if buffer:
                        for event in self.parser.feed(buffer.decode("utf-8", errors="replace")):
                            self.emit(event)
                    for event in self.parser.finish():
                        self.emit(event)
                finally:
                    source.close()
                self.emit({"type": "capture_stopped"})
        except Exception as exc:
            self.error = f"{type(exc).__name__}: {exc}"
            (self.directory / "error.log").write_text(self.error + "\n", encoding="utf-8")
            try:
                print(self.error, file=sys.stderr, flush=True)
            except OSError:
                pass
        finally:
            if source is not None:
                source.close()
            snapshot = self.snapshot()
            snapshot.update(ended_at=utc_now(), duration_seconds=round(self.current_time(), 3), error=self.error)
            (self.directory / "summary.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
            self.completed = True


class SnifferWindow:
    def __init__(self, args):
        import tkinter as tk
        from tkinter import ttk, filedialog
        self.tk, self.ttk, self.filedialog = tk, ttk, filedialog
        self.args, self.session, self.thread = args, None, None
        self.queue = queue.Queue(maxsize=10000)
        self.display_drops = 0
        self.root = tk.Tk()
        self.root.title("SNORR Airtime Sniffer — receive only")
        self.root.geometry("1320x800")
        self.root.minsize(920, 560)
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=26)
        self.port = tk.StringVar(value=args.port or "")
        self.keys = tk.StringVar(value=str(args.keys or ""))
        self.status = tk.StringVar(value="Choose the dedicated V3 port, then Start. Every reception is logged, including repeats.")
        self.metrics = tk.StringVar(value="Packets 0  ·  Duplicates 0  ·  Radio errors 0  ·  Serial gaps 0")
        self.path = tk.StringVar(value="Each Start creates a separate capture directory.")
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill="x")
        ttk.Label(top, text="Serial port").grid(row=0, column=0, sticky="w")
        self.ports = ttk.Combobox(top, textvariable=self.port, width=19)
        self.ports.grid(row=0, column=1, padx=7)
        ttk.Button(top, text="Refresh", command=self.refresh_ports).grid(row=0, column=2)
        ttk.Label(top, text="Channel keys").grid(row=0, column=3, padx=(18, 0))
        ttk.Entry(top, textvariable=self.keys, width=42).grid(row=0, column=4, padx=7, sticky="ew")
        ttk.Button(top, text="Browse", command=self.browse_keys).grid(row=0, column=5)
        self.start_button = ttk.Button(top, text="Start capture", command=self.start)
        self.start_button.grid(row=0, column=6, padx=(20, 6))
        self.stop_button = ttk.Button(top, text="Stop", command=self.stop, state="disabled")
        self.stop_button.grid(row=0, column=7)
        top.columnconfigure(4, weight=1)
        ttk.Label(self.root, textvariable=self.metrics, font=("Segoe UI", 12, "bold"), padding=(12, 5)).pack(anchor="w")
        ttk.Label(self.root, text="Observed RX airtime / last 60 seconds includes repeats and failed reads; excludes undetected RF energy.", padding=(12, 0)).pack(anchor="w")
        ttk.Label(self.root, textvariable=self.status, padding=(12, 8)).pack(anchor="w")
        panes = ttk.Panedwindow(self.root, orient="vertical")
        panes.pack(fill="both", expand=True, padx=12)
        table_frame = ttk.Frame(panes)
        columns = ("time", "sender", "id", "relay", "hop", "rssi", "snr", "toa", "result", "data")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for column, label, width in zip(columns, ("Time", "Origin", "Packet ID", "Relay byte", "Hops", "RSSI", "SNR", "Airtime ms", "Decode / repeat", "Data"), (90, 100, 85, 75, 55, 55, 50, 85, 155, 400)):
            self.table.heading(column, text=label)
            self.table.column(column, width=width, minwidth=45, stretch=column == "data")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        horizontal = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=scrollbar.set, xscrollcommand=horizontal.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        self.table.tag_configure("dupe", foreground="#97620b")
        self.table.tag_configure("error", foreground="#b02626")
        self.table.bind("<<TreeviewSelect>>", self.select)
        panes.add(table_frame, weight=4)
        lower = ttk.Panedwindow(panes, orient="horizontal")
        detail_frame = ttk.Labelframe(lower, text="Selected reception — complete raw bytes and decoded fields")
        self.detail = tk.Text(detail_frame, wrap="none", font=("Consolas", 10), height=12)
        self.detail.grid(row=0, column=0, sticky="nsew")
        detail_y = ttk.Scrollbar(detail_frame, orient="vertical", command=self.detail.yview)
        detail_x = ttk.Scrollbar(detail_frame, orient="horizontal", command=self.detail.xview)
        detail_y.grid(row=0, column=1, sticky="ns")
        detail_x.grid(row=1, column=0, sticky="ew")
        self.detail.configure(yscrollcommand=detail_y.set, xscrollcommand=detail_x.set)
        detail_frame.rowconfigure(0, weight=1)
        detail_frame.columnconfigure(0, weight=1)
        self.detail.configure(state="disabled")
        senders_frame = ttk.Labelframe(lower, text="Airtime by original sender — all received copies")
        self.senders = tk.Text(senders_frame, wrap="none", font=("Consolas", 10), width=48, height=12)
        self.senders.pack(fill="both", expand=True)
        self.senders.configure(state="disabled")
        lower.add(detail_frame, weight=3)
        lower.add(senders_frame, weight=2)
        panes.add(lower, weight=2)
        ttk.Label(self.root, textvariable=self.path, padding=12).pack(anchor="w")
        self.rows = OrderedRows()
        self.refresh_ports()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self.tick)
        if args.autostart:
            self.root.after(200, self.start)

    def refresh_ports(self):
        ports = [p.device for p in list_ports.comports()]
        self.ports["values"] = ports
        if not self.port.get():
            usb = [p.device for p in list_ports.comports() if p.vid is not None]
            if len(usb) == 1:
                self.port.set(usb[0])

    def browse_keys(self):
        path = self.filedialog.askopenfilename(title="Private channel-key JSON", filetypes=[("JSON", "*.json"), ("All", "*")])
        if path:
            self.keys.set(path)

    def on_event(self, event):
        try:
            self.queue.put_nowait(event)
        except queue.Full:
            self.display_drops += 1

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        try:
            if not self.port.get() and not self.args.replay:
                raise ValueError("Select a serial port")
            decoder = Decoder.from_file(self.keys.get() or None)
            self.session = CaptureSession(self.port.get(), decoder, self.args.log_dir, self.on_event, self.args.replay, self.args.duration)
        except Exception as exc:
            self.status.set(str(exc))
            return
        for row in self.table.get_children():
            self.table.delete(row)
        self.rows.clear()
        self.display_drops = 0
        while not self.queue.empty():
            self.queue.get_nowait()
        self.path.set(str(self.session.directory))
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status.set("Listening. Serial writes and LoRa transmit are disabled. Waiting for received packets…")
        self.thread = threading.Thread(target=self.session.run, daemon=False)
        self.thread.start()

    def stop(self):
        if self.session:
            self.session.stop.set()
            self.status.set("Stopping and flushing capture files…")

    def tick(self):
        for _ in range(300):
            try:
                event = self.queue.get_nowait()
            except queue.Empty:
                break
            if event["type"] == "reception":
                status = event["decode_status"] + (" / DUP" if event.get("duplicate") else "")
                origin = (event.get("sender_name", "") + " " + event.get("sender", "?")).strip()
                relay = f"0x{event['relay']:02x}" if event.get("hop_start") else "unknown"
                row = self.table.insert("", "end", values=(event["received_at"][11:23], origin, event.get("packet_id", "?"),
                    relay, f"{event.get('hop_limit', '?')}/{event.get('hop_start', '?')}",
                    event["rssi_dbm"], event["snr_db"], event["airtime_ms"], status, event["summary"][:500]),
                    tags=("error" if event["radio_state"] else "dupe" if event.get("duplicate") else "",))
                self.rows.add(row, event)
                if len(self.rows.ids) > 5000:
                    oldest = self.rows.ids.popleft()
                    del self.rows.data[oldest]
                    self.table.delete(oldest)
                self.table.see(row)
            elif event["type"] == "radio_config":
                self.status.set(f"Firmware {event.get('fw', '?')}  ·  {event.get('freq', '?')} MHz  ·  BW {event.get('bw', '?')} kHz  ·  SF {event.get('sf', '?')}  ·  TX disabled")
            elif event["type"] in ("capture_gap", "notice"):
                self.status.set(event["reason"])
        if self.session:
            s = self.session.snapshot()
            self.metrics.set(f"RX {s['rx_airtime_60s_percent']:.2f}%  ·  Peak {s['peak_rx_airtime_60s_percent']:.2f}%  ·  Packets {s.get('packets', 0)}  ·  Duplicates {s.get('duplicates', 0)}  ·  Radio errors {s.get('radio_errors', 0)}  ·  Serial gaps {s.get('gaps', 0)}")
            text = "Origin       Packets  Repeats   Total ms  Last60 %\n" + "\n".join(
                f"{r['sender']:11} {r['packets']:7} {r['duplicates']:8} {r['airtime_ms']:10} {r['rx_airtime_60s_percent']:8.2f}" for r in s["senders"])
            text += "\n\nRelay hints (8-bit, identities unverified)\n" + "\n".join(
                f"{r['relay_hint']:11} {r['packets']:7} {r['duplicates']:8} {r['airtime_ms']:10} ms" for r in s["relay_hints"])
            self.replace_text(self.senders, text)
            if self.display_drops:
                self.path.set(f"{self.session.directory} — GUI omitted {self.display_drops} updates; files retain all events")
            if self.session.completed:
                self.start_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.status.set(self.session.error or "Capture saved. Start creates a new log directory.")
        self.root.after(100, self.tick)

    @staticmethod
    def replace_text(widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.configure(state="disabled")

    def select(self, _event=None):
        selected = self.table.selection()
        if selected and selected[0] in self.rows.data:
            self.replace_text(self.detail, json.dumps(self.rows.data[selected[0]], ensure_ascii=False, indent=2))

    def close(self):
        self.stop()
        if self.thread and self.thread.is_alive():
            self.root.after(100, self.close)
        else:
            self.root.destroy()


class OrderedRows:
    def __init__(self):
        from collections import deque
        self.ids, self.data = deque(), {}

    def clear(self):
        self.ids.clear()
        self.data.clear()

    def add(self, row, event):
        self.ids.append(row)
        self.data[row] = event


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="COM6, /dev/ttyUSB0, or /dev/serial/by-id/…")
    parser.add_argument("--gui", action="store_true", help="Open the desktop window")
    parser.add_argument("--autostart", action="store_true", help="Start GUI capture immediately")
    parser.add_argument("--keys", type=Path, default=DEFAULT_KEYS if DEFAULT_KEYS.exists() else None, help="Private channel-key JSON; never printed/logged")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOGS)
    parser.add_argument("--duration", type=float, help="Stop after this many seconds; otherwise Ctrl+C / Stop")
    parser.add_argument("--list-ports", action="store_true")
    parser.add_argument("--replay", type=Path, help="Replay a serial.raw capture into a new log directory")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if args.list_ports:
        for port in list_ports.comports():
            print(f"{port.device}: {port.description}")
        return 0
    if args.duration is not None and args.duration <= 0:
        parser.error("--duration must be positive")
    if args.gui:
        try:
            SnifferWindow(args).root.mainloop()
        except ImportError:
            parser.error("GUI requires Tk (Debian/Ubuntu: python3-tk); CLI works without --gui")
        return 0
    if not args.port and not args.replay:
        usb = [p.device for p in list_ports.comports() if p.vid is not None]
        if len(usb) != 1:
            parser.error("Specify --port; use --list-ports to inspect connected devices")
        args.port = usb[0]
    try:
        session = CaptureSession(args.port, Decoder.from_file(args.keys), args.log_dir, replay=args.replay, duration=args.duration)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Capture: {session.directory}", flush=True)
    worker = threading.Thread(target=session.run, daemon=False)
    worker.start()
    try:
        while worker.is_alive():
            worker.join(0.5)
    except KeyboardInterrupt:
        session.stop.set()
        worker.join()
    print(json.dumps(session.snapshot(), indent=2), flush=True)
    return 1 if session.error else 0


if __name__ == "__main__":
    raise SystemExit(main())

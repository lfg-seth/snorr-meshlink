#!/usr/bin/env python3
"""Print each hot-plugged RAK's !node ID; never flash or change settings."""
import argparse
import contextlib
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ID = (0x239A, 0x8029)
BOOTLOADER_ID = (0x239A, 0x0029)


def clean(value):
    return "".join(c for c in str(value) if c.isascii() and c.isprintable())


def candidates(ports, excluded):
    """Skip Heltec/other devices and never guess between duplicate USB IDs."""
    excluded = {s.upper() for s in excluded}
    selected = [p for p in ports if (p.vid, p.pid) == RUNTIME_ID
                and p.serial_number and p.serial_number.upper() not in excluded]
    counts = {}
    for port in selected:
        key = port.serial_number.upper()
        counts[key] = counts.get(key, 0) + 1
    return [p for p in selected if counts[p.serial_number.upper()] == 1]


def identify(port, log, timeout=6, factory=None):
    if factory is None:
        from meshtastic.serial_interface import SerialInterface
        factory = SerialInterface
    interface = None
    # API/log output may contain private channel material: keep it in private/.
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        try:
            interface = factory(devPath=port.device, debugOut=log, connectNow=False,
                                noNodes=True, timeout=timeout)
            interface.connect()
            metadata = interface.metadata
            if metadata is None or metadata.hw_model != 9:
                raise ValueError("Connected USB device is not a RAK4631")
            user = interface.getMyNodeInfo().get("user", {})
            node_id = user.get("id", "").lower()
            if not re.fullmatch(r"![0-9a-f]{8}", node_id):
                raise ValueError("Missing complete node identity")
            if node_id != f"!{interface.myInfo.my_node_num:08x}":
                raise ValueError("Contradictory node identities")
            role = metadata.DESCRIPTOR.fields_by_name["role"].enum_type.values_by_number[metadata.role].name
            return {"nodeId": node_id, "name": clean(user.get("shortName", "")),
                    "firmware": clean(metadata.firmware_version), "role": role,
                    "usbSerial": port.serial_number.upper(), "port": port.device,
                    "hardwareId": interface.myInfo.device_id.hex()}
        finally:
            if interface is not None and getattr(interface, "stream", object()) is not None:
                interface.close()


def atomic_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


@contextlib.contextmanager
def station_lease(path):
    """OS releases the lock even if the console crashes or is closed."""
    with path.open("a+b") as lease:
        lease.seek(0, os.SEEK_END)
        if not lease.tell():
            lease.write(b"0")
            lease.flush()
        lease.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(lease.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            lease.seek(0)
            if os.name == "nt":
                msvcrt.locking(lease.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lease.fileno(), fcntl.LOCK_UN)


def show(row):
    return (f"{row['nodeId']}  |  {row['name'] or '(unnamed)'}  |  {row['role']}  |  "
            f"{clean(row['port'])}  |  USB {clean(row['usbSerial'])}  |  {row['firmware']}")


def poll(ports, seen, excluded, probe, emit, paused=lambda: False):
    available = candidates(ports, excluded)
    present = {(p.serial_number.upper(), p.device) for p in available}
    seen.intersection_update(present)
    rows = []
    for port in available:
        if paused():
            break
        signature = (port.serial_number.upper(), port.device)
        if signature in seen:
            continue
        try:
            row = probe(port)
        except Exception as error:
            # Do not print SDK exception bodies or saved configurations.
            emit(f"WAIT {clean(port.device)} USB {clean(port.serial_number)} ({type(error).__name__})")
            continue
        seen.add(signature)
        rows.append(row)
        emit(show(row))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="Identify connected RAKs once and exit")
    mode.add_argument("--pause", action="store_true", help="Ask the running watcher to release ports before bench writes")
    mode.add_argument("--resume", action="store_true", help="Resume and refresh IDs/names after bench writes")
    parser.add_argument("--exclude-usb", action="append", default=[], help="USB serial to leave alone; repeat as needed")
    parser.add_argument("--station-dir", type=Path, default=ROOT / "private/bench/rak-label-station")
    parser.add_argument("--poll", type=float, default=1, help="Hot-plug poll seconds (default: 1)")
    args = parser.parse_args(argv)
    station = args.station_dir.resolve()
    if not station.is_relative_to((ROOT / "private").resolve()) or args.poll < 0.2:
        parser.error("Use an ignored private/ station directory and poll >= 0.2 seconds")
    station.mkdir(parents=True, exist_ok=True)
    pause = station / "pause"
    if args.pause:
        pause.write_text("Pause requested before bench mutations.\n", encoding="utf-8")
        print("Pause requested. Wait for status.json paused=true before opening boards.", flush=True)
        return 0
    if args.resume:
        pause.unlink(missing_ok=True)
        print("Watcher resumed; connected boards will be reread and show new names/firmware.", flush=True)
        return 0
    from serial.tools.list_ports import comports
    status = station / "status.json"
    lock = station / "watch.lock"
    lease = station_lease(lock)
    try:
        lease.__enter__()
    except OSError:
        parser.error(f"A watcher already owns this station. Close its window first: {lock}")
    seen, known = set(), {}
    was_paused = False
    state = {"pid": os.getpid(), "running": True, "paused": False, "busyPort": None}
    emit = lambda message: print(message, flush=True)
    emit("SNORR RAK label station -- ID only, no configuration writes")
    emit("Plug boards in; label each with its !ID. Ctrl+C stops and closes ports.")
    try:
        while True:
            if pause.exists():
                state.update(paused=True, busyPort=None)
                atomic_json(status, state)
                if not was_paused:
                    emit("PAUSED -- all watcher serial ports are closed; bench preparation may run.")
                was_paused = True
                if args.once:
                    break
                time.sleep(args.poll)
                continue
            if was_paused:
                seen.clear()
                emit("RESUMED -- refreshing IDs, names and firmware.")
            was_paused = False
            state["paused"] = False
            def probe(port):
                state["busyPort"] = port.device
                atomic_json(status, state)
                safe_serial = re.sub(r"[^A-Za-z0-9_-]", "_", port.serial_number)
                try:
                    with (station / f"probe-{safe_serial}.log").open("a", encoding="utf-8") as log:
                        return identify(port, log)
                finally:
                    state["busyPort"] = None
                    atomic_json(status, state)
            for row in poll(list(comports()), seen, args.exclude_usb, probe, emit, pause.exists):
                known[row["usbSerial"]] = row
                atomic_json(station / "nodes.json", list(known.values()))
            atomic_json(status, state)
            if args.once:
                break
            time.sleep(args.poll)
    except KeyboardInterrupt:
        emit("Stopped; watcher serial ports closed.")
    finally:
        state.update(running=False, paused=False, busyPort=None)
        atomic_json(status, state)
        lease.__exit__(None, None, None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ID = (0x239A, 0x8029)
BOOTLOADER_ID = (0x239A, 0x0029)
MAX_HEARTBEAT_AGE = 30


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
            f"{clean(row['port'])}  |  USB {clean(row['usbSerial'])}  |  {row['firmware']}"
            + ("  |  REFERENCE" if row.get("reference") else ""))


def process_running(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    if os.name == "nt":
        # os.kill(pid, 0) must not be used on Windows: use a read-only query.
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL("kernel32", use_last_error=True)
        api.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        api.OpenProcess.restype = wintypes.HANDLE
        api.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        api.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = api.OpenProcess(0x1000, False, pid)
        if not handle:
            return ctypes.get_last_error() == 5  # Conservatively treat access-denied as alive.
        try:
            code = wintypes.DWORD()
            return bool(api.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
        finally:
            api.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def process_token(pid):
    """Read process creation identity, so a reused PID cannot validate old status."""
    if not isinstance(pid, int) or pid <= 0:
        return None
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL("kernel32", use_last_error=True)
        api.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        api.OpenProcess.restype = wintypes.HANDLE
        api.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        api.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = api.OpenProcess(0x1000, False, pid)
        if not handle:
            return None
        try:
            created, exited, kernel, user = (wintypes.FILETIME() for _ in range(4))
            if not api.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                                      ctypes.byref(kernel), ctypes.byref(user)):
                return None
            return f"windows:{created.dwHighDateTime:08x}{created.dwLowDateTime:08x}"
        finally:
            api.CloseHandle(handle)
    try:
        # Linux start ticks survive PID reuse. Other Unix systems fail closed.
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        return "proc:" + stat[stat.rindex(")") + 2:].split()[19]
    except (OSError, ValueError, IndexError):
        return None


def live_status(saved, now=None):
    result = dict(saved)
    alive = process_running(saved.get("pid"))
    same_process = bool(alive and saved.get("processStart")
                        and saved["processStart"] == process_token(saved.get("pid")))
    try:
        heartbeat = datetime.fromisoformat(saved.get("heartbeatUtc", ""))
        age = ((now or datetime.now(timezone.utc)) - heartbeat).total_seconds()
        recent = 0 <= age <= MAX_HEARTBEAT_AGE
    except (TypeError, ValueError):
        recent = False
    verified = same_process and recent
    result["running"] = bool(saved.get("running") and verified)
    result["stale"] = bool(saved.get("running") and not verified)
    if not result["running"]:
        result.update(paused=False, busyPort=None)
    return result


def stop_requested(path, state):
    """An orphan request for an earlier watcher must not stop a new instance."""
    try:
        request = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(isinstance(request, dict) and state.get("processStart")
                and request.get("pid") == state["pid"]
                and request.get("processStart") == state["processStart"])


def request_stop(path, saved):
    state = live_status(saved)
    if not state["running"]:
        return False
    atomic_json(path, {"pid": state["pid"], "processStart": state["processStart"]})
    return True


def update_presence(known, ports, excluded, emit):
    present = {p.serial_number.upper() for p in candidates(ports, excluded)}
    for usb, row in known.items():
        connected = usb in present
        if row.get("connected", True) and not connected:
            emit(f"{row['nodeId']}  |  DISCONNECTED  |  USB {clean(usb)}")
        row["connected"] = connected
    return present


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
    mode.add_argument("--stop", action="store_true", help="Stop the watcher after its current read closes")
    mode.add_argument("--status", action="store_true", help="Report status with a live process check")
    parser.add_argument("--exclude-usb", action="append", default=[], help="USB serial to leave alone; repeat as needed")
    parser.add_argument("--reference-usb", action="append", default=[], help="Show this USB unit as REFERENCE instead of hiding it")
    parser.add_argument("--station-dir", type=Path, default=ROOT / "private/bench/rak-label-station")
    parser.add_argument("--poll", type=float, default=1, help="Hot-plug poll seconds (default: 1)")
    args = parser.parse_args(argv)
    station = args.station_dir.resolve()
    if not station.is_relative_to((ROOT / "private").resolve()) or args.poll < 0.2:
        parser.error("Use an ignored private/ station directory and poll >= 0.2 seconds")
    station.mkdir(parents=True, exist_ok=True)
    pause = station / "pause"
    stop = station / "stop"
    status = station / "status.json"
    if args.status:
        saved = json.loads(status.read_text(encoding="utf-8")) if status.exists() else {"running": False}
        print(json.dumps(live_status(saved), indent=2), flush=True)
        return 0
    if args.stop:
        saved = json.loads(status.read_text(encoding="utf-8")) if status.exists() else {"running": False}
        message = ("Stop requested; watcher will close its current read and exit."
                   if request_stop(stop, saved) else "No verified running watcher; no stop request created.")
        print(message, flush=True)
        return 0
    if args.pause:
        pause.write_text("Pause requested before bench mutations.\n", encoding="utf-8")
        print("Pause requested. Use --status and require running=true, stale=false, paused=true, busyPort=null before opening boards.", flush=True)
        return 0
    if args.resume:
        pause.unlink(missing_ok=True)
        print("Watcher resumed; connected boards will be reread and show new names/firmware.", flush=True)
        return 0
    from serial.tools.list_ports import comports
    lock = station / "watch.lock"
    lease = station_lease(lock)
    try:
        lease.__enter__()
    except OSError:
        parser.error(f"A watcher already owns this station. Close its window first: {lock}")
    seen, known = set(), {}
    was_paused = False
    state = {"pid": os.getpid(), "running": True, "paused": False, "busyPort": None,
             "processStart": process_token(os.getpid()),
             "version": 2, "heartbeatUtc": datetime.now(timezone.utc).isoformat()}
    references = {s.upper() for s in args.reference_usb}
    emit = lambda message: print(message, flush=True)
    emit("SNORR RAK label station -- ID only, no configuration writes")
    emit("Plug boards in; label each with its !ID. Ctrl+C stops and closes ports.")
    emit("All RAKs are shown by default; reported names may be historical. REFERENCE is visible.")
    try:
        while True:
            state["heartbeatUtc"] = datetime.now(timezone.utc).isoformat()
            if stop_requested(stop, state):
                emit("Stop requested; watcher serial ports closed.")
                break
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
            ports = list(comports())
            present = update_presence(known, ports, args.exclude_usb, emit)
            def probe(port):
                state["busyPort"] = port.device
                state["heartbeatUtc"] = datetime.now(timezone.utc).isoformat()
                atomic_json(status, state)
                safe_serial = re.sub(r"[^A-Za-z0-9_-]", "_", port.serial_number)
                try:
                    with (station / f"probe-{safe_serial}.log").open("a", encoding="utf-8") as log:
                        row = identify(port, log)
                        row.update(reference=port.serial_number.upper() in references, connected=True)
                        return row
                finally:
                    state["busyPort"] = None
                    state["heartbeatUtc"] = datetime.now(timezone.utc).isoformat()
                    atomic_json(status, state)
            for row in poll(ports, seen, args.exclude_usb, probe, emit,
                            lambda: pause.exists() or stop_requested(stop, state)):
                known[row["usbSerial"]] = row
            state.update(connectedRaks=len(present),
                         identifiedConnected=sum(r.get("connected", False) for r in known.values()))
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
        stop.unlink(missing_ok=True)
        lease.__exit__(None, None, None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

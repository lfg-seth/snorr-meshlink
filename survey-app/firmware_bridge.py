"""Translate the firmware worker's SurveyAdapter public Python API for the recorder."""

from __future__ import annotations

import math
import queue
import threading
import time
from pathlib import Path


def display_settings(hello):
    capabilities = hello.get("capabilities", {})
    settings = {}
    limits = dict(hello.get("settings", {}))
    if "heartbeat_interval_ms" in capabilities:
        limits["heartbeat_interval_ms"] = capabilities["heartbeat_interval_ms"]
    for name, limit in limits.items():
        if isinstance(limit, dict) and "type" in limit:
            settings[name] = limit
        elif isinstance(limit, (list, tuple)) and len(limit) == 3:
            lo, hi, default = limit
            settings[name] = {
                "type": "integer",
                "min": lo,
                "max": hi,
                "default": default,
                "unit": "ms"
                if name.endswith("_ms")
                else "%"
                if name.endswith("_pct")
                else "",
            }
    profiles = capabilities.get("radio_profile_control")
    if profiles:
        settings["radio_profile"] = {"type": "enum", "choices": profiles, "default": ""}
    return settings


class FirmwareBridge:
    source = "live"

    @classmethod
    def open(cls, factory, port, expected_id, root):
        if not port or not expected_id or root is None:
            raise ValueError(
                "Firmware mode requires an explicit --device and --expected-id"
            )
        path = Path(root) / "live" / "adapter" / f"usb-{time.time_ns()}.jsonl"
        client = factory(port, expected_id, path)
        # This laptop recorder gates heartbeats on durable capture.
        client.auto_heartbeat = False
        client.__enter__()
        if client.hello.get("role") != "client":
            client.close()
            raise ValueError("The identified radio is not a survey client")
        return cls(client)

    def __init__(self, client):
        self.client = client
        self.hello = {}
        self.gps = {}
        self.last_tx = None
        self.measured_interval = None
        self.fault = None
        self.problem = None
        self.outbox = queue.Queue(12)
        self.done = threading.Event()
        self.stop_ack = threading.Event()
        self.stop_pending = False
        self.worker = threading.Thread(
            target=self.dispatch, name="survey-commands", daemon=True
        )
        self.worker.start()

    def send(self, envelope):
        if self.problem or self.client.problem:
            if envelope["name"] == "heartbeat":
                return
            raise ConnectionError(self.problem or self.client.problem)
        if envelope["name"] == "stop":
            self.stop_pending = True
            self.stop_ack.clear()
            # The recorder retains reserved IDs. Dropped queued commands have unknown outcomes.
            while True:
                try:
                    self.outbox.get_nowait()
                except queue.Empty:
                    break
        try:
            self.outbox.put_nowait((time.monotonic(), envelope))
        except queue.Full as exc:
            raise ConnectionError("Firmware command queue full") from exc

    def dispatch(self):
        while not self.done.is_set():
            try:
                queued, cmd = self.outbox.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                if time.monotonic() - queued > 3 and cmd["name"] != "stop":
                    raise TimeoutError("Queued command expired; inspect state")
                # The adapter publishes its normalized ACK to read_event as part of command().
                self.client.command(cmd)
                if cmd["name"] == "stop":
                    self.stop_ack.set()
            except (
                TimeoutError,
                ConnectionError,
                OSError,
                ValueError,
                queue.Full,
            ) as exc:
                self.problem = str(exc)
                return

    def poll(self, now):
        batch = []
        for _ in range(256):
            try:
                event = self.client.read_event(timeout=0)
            except queue.Empty:
                break
            batch.append(self.translate(event))
        if not batch and (self.client.problem or self.problem):
            raise ConnectionError(self.client.problem or self.problem)
        return batch

    def translate(self, event):
        name, raw = event["name"], event["data"]
        d = dict(raw)
        adapter_host = event["boot_id"] == self.client.host_boot
        if "session_id" in d:
            sid = d["session_id"]
            d["session_id"] = f"{event['boot_id']}/{sid}" if sid else None
        if name == "hello":
            self.hello = raw
            d["settings"] = display_settings(raw)
            d["hardware"] = (
                f"{raw.get('node_id', '')} · hardware {raw.get('hardware_model', '?')}"
            )
        elif name == "gps" and d.get("sample_at") in (None, "local_stream"):
            self.gps = dict(d)
        elif name == "fault":
            self.fault = d.get("reason")
        elif name == "state":
            settings = dict(d.get("settings", {}))
            caps = self.hello.get("capabilities", {})
            if "heartbeat_interval_ms" in caps:
                settings["heartbeat_interval_ms"] = self.client.heartbeat_ms
            profile = d.get("radio_profile", self.hello.get("radio_profile", {}))
            if "experimental" in profile:
                settings["radio_profile"] = (
                    "experimental_medium_fast"
                    if profile["experimental"]
                    else "production"
                )
            if d.get("run_state") == "running":
                self.fault = None
            gps = dict(self.gps)
            if d.get("gps_fresh") == 0:
                gps.update(valid=False, lat_deg=None, lon_deg=None)
            completed = d.get("success", 0) + d.get("timeout", 0)
            d.update(
                settings=settings,
                radio_profile=profile,
                gps=gps,
                transport="connected",
                heartbeat_ok=bool(d.get("heartbeat_healthy")),
                cadence_ms=d.get("interval_ms"),
                measured_interval_ms=self.measured_interval,
                quiet_remaining_s=math.ceil(d.get("quiet_remaining_ms", 0) / 1000),
                queue_dropped=d.get("firmware_dropped", 0)
                + event.get("display_dropped_total", 0),
                queue_depth=d["queue_capacity"] - d["queue_free"]
                if "queue_free" in d and "queue_capacity" in d
                else None,
                counts={"success": d.get("success", 0), "attempts": completed},
                round_trip_basis="completed",
                fault=self.fault,
            )
        elif name in ("result", "attempt"):
            d["enqueue_mono_ms"] = d.get("enqueue_ms")
            d["tx_mono_ms"] = d.get("tx_start_ms")
            d["receive_mono_ms"] = d.get("rx_ms")
            d["local_util_pct"] = d.get("channel_util_pct")
            if (
                name == "result"
                and d["tx_mono_ms"] is not None
                and d.get("status") != "late"
            ):
                attempt = d.get("sequence")
                if (
                    isinstance(attempt, int)
                    and self.last_tx
                    and self.last_tx[:2] == (d["session_id"], attempt - 1)
                ):
                    self.measured_interval = (
                        d["tx_mono_ms"] - self.last_tx[2]
                    ) & 0xFFFFFFFF
                else:
                    self.measured_interval = None
                self.last_tx = (d["session_id"], attempt, d["tx_mono_ms"])
        return event | {
            "data": d,
            "adapter_data": raw,
            "event_stream": "adapter-host" if adapter_host else "firmware",
        }

    def close(self):
        if self.stop_pending and self.worker.is_alive():
            self.stop_ack.wait(3.5)
        self.done.set()
        self.client.close()
        self.worker.join(4)

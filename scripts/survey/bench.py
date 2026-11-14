"""Record direct-hop vehicle surveys and cancellable, independently observed bench runs."""

import argparse
from collections import Counter
from contextlib import ExitStack, contextmanager
import json
import os
from pathlib import Path
import signal
import statistics
import sys
import time
import uuid

from adapter import SurveyAdapter, node_id, number


def device(text):
    try:
        port, identity = text.rsplit("=", 1)
        return port, node_id(number(identity))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected PORT=!xxxxxxxx") from exc


@contextmanager
def station_lease(directory):
    """Same first-byte OS lease as scripts/bench/watch-raks.py on the station host."""
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "watch.lock").open("a+b") as f:
        if not f.seek(0, os.SEEK_END):
            f.write(b"0")
            f.flush()
        f.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            f.seek(0)
            if os.name == "nt":
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f, fcntl.LOCK_UN)


def call(adapter, name, **params):
    ack = adapter.command(dict(v=1, kind="command", id=uuid.uuid4().hex, name=name, params=params))
    if not ack["data"]["ok"]:
        raise RuntimeError(f"{name}: {ack['data']['error']}")
    return ack["data"]["applied"]


def distribution(values):
    if not values:
        return None
    ordered = sorted(values)
    return {
        "min": ordered[0],
        "median": statistics.median(ordered),
        "p95": ordered[int((len(ordered) - 1) * 0.95)],
        "max": ordered[-1],
    }


def summarize(out, client_id, responder_ids, elapsed):
    """Join each successful result to independent RX and actual TX-start observations."""
    counts, faults, wires = Counter(), Counter(), Counter()
    successes, all_heard = Counter(), Counter()
    pings, rx, tx = {}, {}, {}
    results, air, responders = [], [], []
    rtts, measured_tx, local_util, remote_util = [], [], [], []
    gps_valid = gps_total = quiet_background = 0
    quiet_suppressed = {}
    for path in out.glob("*.jsonl"):
        observer = path.stem
        quiet_start = quiet_duration = None
        with path.open(encoding="utf8") as stream:
            for line in stream:
                event = json.loads(line)
                name, data = event["name"], event["data"]
                if name == "fault":
                    faults[data["reason"]] += 1
                elif name == "state" and "suppressed" in data:
                    quiet_suppressed[observer] = data["suppressed"]
                elif name == "gps" and observer == client_id and data.get("sample_at") == "local_stream":
                    gps_total += 1
                    gps_valid += int(data["valid"])
                elif name == "quiet":
                    pings[observer, data["request_packet_id"]] = data
                    quiet_start, quiet_duration = event["firmware_ms"], data["remaining_ms"]
                elif name == "statistics":
                    kind = data.get("type")
                    if kind == "pong" and data["enqueued"]:
                        responders.append((observer, data["request_packet_id"]))
                    elif kind == "rx":
                        rx[observer, data["from"], data["packet_id"]] = data
                    elif kind == "airtx":
                        air.append((observer, data))
                        tx[observer, data["packet_id"]] = data
                        if (
                            quiet_start is not None
                            and data["from"] == number(observer)
                            and data["local_class"] in (1, 3)
                            and (event["firmware_ms"] - quiet_start) % (2**32) < quiet_duration
                        ):
                            quiet_background += 1
                elif name == "result" and observer == client_id:
                    counts[data["status"]] += 1
                    if data.get("channel_util_pct") is not None:
                        local_util.append(data["channel_util_pct"])
                    if data["status"] == "success":
                        results.append(data)
                        successes[data["target_id"]] += 1
                        for key, samples in (
                            ("rtt_ms", rtts),
                            ("measured_tx_ms", measured_tx),
                            ("remote_util_pct", remote_util),
                        ):
                            if data.get(key) is not None:
                                samples.append(data[key])
                        if data.get("wire_bytes") is not None:
                            wires[data["wire_bytes"]] += 1

    uplink_matches = downlink_matches = uplink_mismatches = downlink_mismatches = 0
    matched_air = Counter()
    for data in results:
        target, request, reply = data["target_id"], data["request_packet_id"], data["reply_packet_id"]
        if responder_ids and all((observer, request) in pings for observer in responder_ids):
            all_heard[target] += 1
        sent = tx.get((client_id, request), {})
        replied = tx.get((target, reply), {})
        if (
            sent.get("from") == number(client_id)
            and replied.get("from") == number(target)
            and sent["local_class"] == replied["local_class"] == 2
        ):
            matched_air[target] += 1
        for observer, source, packet, direction in (
            (target, client_id, request, "uplink"),
            (client_id, target, reply, "downlink"),
        ):
            received = rx.get((observer, number(source), packet))
            if received and received["port"] == 310:
                matches = data[direction] == {
                    "rssi_dbm": received["rssi_dbm"],
                    "snr_db": received["snr_quarter_db"] / 4,
                }
                if direction == "uplink":
                    uplink_matches += int(matches)
                    uplink_mismatches += int(not matches)
                else:
                    downlink_matches += int(matches)
                    downlink_mismatches += int(not matches)

    survey_packets = {
        (source, packet) for (_, source, packet), observation in rx.items() if observation["port"] == 310
    }
    forwarded = header_violations = 0
    for observer, data in air:
        if data["local_class"] == 2 or (data["from"], data["packet_id"]) in survey_packets:
            forwarded += int(data["from"] != number(observer))
            header_violations += int(bool(data["hop_limit"] or data["hop_start"] or data["want_ack"]))
    unexpected = sum(
        pings.get((observer, request), {}).get("target_id") != observer for observer, request in responders
    )
    return dict(
        elapsed_s=round(elapsed, 3),
        statuses=dict(counts),
        successes_by_target=dict(successes),
        round_trips_per_min=round(len(results) * 60 / elapsed, 3) if elapsed else None,
        rtt_ms=distribution(rtts),
        request_wire_bytes=dict(wires),
        request_measured_tx_ms=distribution(measured_tx),
        client_channel_util_pct=distribution(local_util),
        target_channel_util_pct=distribution(remote_util),
        gps_samples=gps_total,
        valid_gps_samples=gps_valid,
        faults=dict(faults),
        all_observers_heard=sum(all_heard.values()),
        all_observers_heard_by_target=dict(all_heard),
        matched_tx_pairs_by_target=dict(matched_air),
        unexpected_responders=unexpected,
        uplink_metric_matches=uplink_matches,
        downlink_metric_matches=downlink_matches,
        uplink_metric_mismatches=uplink_mismatches,
        downlink_metric_mismatches=downlink_mismatches,
        observed_survey_forwards=forwarded,
        observed_hop_or_ack_violations=header_violations,
        observed_owned_background_tx_during_quiet=quiet_background,
        firmware_suppressed_since_boot=quiet_suppressed,
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--client", required=True, type=device)
    p.add_argument(
        "--responder",
        type=device,
        action="append",
        default=[],
        help="independent USB observer; repeat per RAK",
    )
    p.add_argument("--target", required=True, action="append", help="RF node ID; repeat for round-robin")
    p.add_argument("--mode", choices=("survey", "bench"), default="survey")
    p.add_argument(
        "--station-dir", type=Path, help="canonical watcher directory; required with RAK observers"
    )
    p.add_argument("--output", type=Path, required=True, help="new private run directory")
    p.add_argument("--seconds", type=float, default=7200)
    p.add_argument("--interval-ms", type=int, default=3000)
    p.add_argument("--timeout-ms", type=int, default=4500)
    p.add_argument("--fixed", action="store_true")
    args = p.parse_args()
    if not 0 < args.seconds <= 86400:
        p.error("duration must be positive and at most 24 h")
    if args.responder and not args.station_dir:
        p.error("select the actual station lease directory")
    all_devices = [args.client, *args.responder]
    if len({p for p, _ in all_devices}) != len(all_devices) or len({n for _, n in all_devices}) != len(
        all_devices
    ):
        p.error("duplicate physical device")
    for target in args.target:
        number(target)
    out = args.output.resolve()
    root = Path(__file__).resolve().parents[2]
    if out == root or (
        out.is_relative_to(root) and out.relative_to(root).parts[0] not in ("private", "local-data")
    ):
        p.error("repository runtime evidence belongs under private/ or local-data/")
    out.mkdir(parents=True, exist_ok=False)
    stop = [False]

    def cancel(*_):
        stop[0] = True

    signal.signal(signal.SIGINT, cancel)
    signal.signal(signal.SIGTERM, cancel)
    elapsed = 0
    reason = "startup"
    started = None
    failure = None
    observer_ids = [n for _, n in args.responder]

    def save(name, value):
        tmp = out / (name + ".tmp")
        tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf8")
        tmp.replace(out / name)

    try:
        with ExitStack() as stack:
            if args.station_dir:
                stack.enter_context(station_lease(args.station_dir))
            connected = []
            for port, n in all_devices:
                a = stack.enter_context(SurveyAdapter(port, n, out / (n + ".jsonl")))
                connected.append(a)
            client = connected[0]
            if client.hello["role"] != "client" or any(
                a.hello["role"] != "responder" for a in connected[1:]
            ):
                raise RuntimeError("wrong hardware role")
            for a in connected:
                if not a.hello["enrolled"]:
                    raise RuntimeError("device enrollment missing")
            call(
                client,
                "configure",
                min_attempt_interval_ms=args.interval_ms,
                response_timeout_ms=args.timeout_ms,
                max_attempt_interval_ms=max(args.interval_ms, 15000),
                adaptive=not args.fixed,
            )
            call(client, "set_target", target_ids=args.target)
            try:
                call(client, "heartbeat")
                call(client, "start", mode=args.mode)
                started = time.monotonic()
                last_summary = 0
                while True:
                    elapsed = time.monotonic() - started
                    if stop[0] or (out / "STOP").exists():
                        reason = "cancelled"
                        break
                    if any(a.problem for a in connected):
                        raise ConnectionError("USB transport lost")
                    if client.state.get("run_state") == "paused":
                        raise RuntimeError("firmware paused")
                    if elapsed >= args.seconds:
                        reason = "duration_reached"
                        break
                    if elapsed - last_summary >= 30 or not last_summary:
                        save(
                            "progress.json",
                            dict(
                                elapsed_s=round(elapsed, 1),
                                requested_s=args.seconds,
                                state=client.state,
                                observer_counts=[a.state.get("suppressed") for a in connected[1:]],
                            ),
                        )
                        last_summary = elapsed
                    time.sleep(min(0.2, max(0.01, args.seconds - elapsed)))
            finally:
                if started is not None:
                    elapsed = time.monotonic() - started
                if not client.problem:
                    call(client, "stop")
                time.sleep(0.3)
    except Exception as exc:
        reason = "failed"
        failure = f"{type(exc).__name__}: {exc}"
    result = summarize(out, args.client[1], observer_ids, elapsed)
    faults = result["faults"]
    counts = result["successes_by_target"]
    passed = (
        reason == "duration_reached"
        and elapsed >= args.seconds
        and not failure
        and all(counts.get(t, 0) > 0 for t in args.target)
        and not faults.get("event_gap")
        and not result["unexpected_responders"]
        and not result["observed_survey_forwards"]
        and not result["observed_hop_or_ack_violations"]
        and not result["observed_owned_background_tx_during_quiet"]
    )
    if observer_ids:
        observed_targets = set(args.target) & set(observer_ids)
        passed = (
            passed
            and all(result["all_observers_heard_by_target"].get(t, 0) for t in args.target)
            and all(result["matched_tx_pairs_by_target"].get(t, 0) for t in observed_targets)
            and result["uplink_metric_matches"] >= len(observed_targets)
            and result["downlink_metric_matches"] >= len(args.target)
            and not result["uplink_metric_mismatches"]
            and not result["downlink_metric_mismatches"]
        )
    result.update(reason=reason, error=failure, passed=passed, requested_s=args.seconds, mode=args.mode)
    save("summary.json", result)
    print(json.dumps(result, indent=2), flush=True)
    return 0 if passed else (130 if reason == "cancelled" else 1)


if __name__ == "__main__":
    sys.exit(main())

# Direct-hop survey USB v1

Firmware source `bcb22e037293df5531da391bb88d46b6969633b0` implements this protocol on the dedicated `rak4631-survey` and `heltec-v4-survey` targets. The [normalized interface](survey-interface-v1.md) defines command and event semantics. The [Python adapter](../../scripts/survey/adapter.py) and [bench recorder](../../scripts/survey/bench.py) implement the physical USB connection. The [bench record](survey-firmware-20261114.md) distinguishes source, installation and measured acceptance.

## Host connection

Use Python 3.10 or later with `pyserial`. On Windows use the project virtual environment and an explicit COM port. On Linux select the device's stable `/dev/serial/by-id/` path and run as a user with serial access. The adapter opens one device at 115200 baud, 8N1. It verifies the supplied node ID during the first hello, before sending state-changing requests. The RAK watcher retains its OS lease while paused. Use its stopped state and the canonical station lease for the four-board CLI.

The GUI imports `SurveyAdapter(port, expected_id, log_path)` from `scripts/survey/adapter.py`. The log path must be new for each connection. Keep logs and the command journal together in ignored private storage. Load `scripts/survey` on the Python path, or use the GUI bridge's explicit module-file argument.

```python
from pathlib import Path
from uuid import uuid4
from adapter import SurveyAdapter

with SurveyAdapter(port, expected_node_id, Path("private/survey/run-001.jsonl")) as radio:
    command = {"v": 1, "kind": "command", "id": uuid4().hex, "name": "get_state", "params": {}}
    ack = radio.command(command)
    state = ack["data"]["applied"]
    event = radio.read_event(timeout=2)
```

`read_event()` raises `queue.Empty` on timeout. The adapter normally supplies host heartbeats. A recorder can set `auto_heartbeat = False` **before opening** and send its own `heartbeat` commands while recording is healthy. A physical reconnection pauses a still-running controller. A browser reconnect does not open USB. After a firmware reboot or transport fault, reconnect, inspect the snapshot, and explicitly start or resume. Query state if a command times out. Reusing a completed mutation ID with identical content returns its recorded ACK. A conflicting request or an interrupted journal entry cannot reapply it. Keep one host owner and one command-journal directory per device.

`configure` accepts the following values. Commands changing active attempts are rejected. A failed command carries a reason. The host publishes applied settings in the ACK and snapshot.

| Setting | Default | Range |
| --- | ---: | --- |
| min_attempt_interval_ms | 3000 | 1000–60000 |
| response_timeout_ms | 4500 | 1000–30000 |
| max_attempt_interval_ms | 15000 | minimum interval to 120000 |
| gps_max_age_ms | 2000 | 500–10000 |
| gps_update_interval_ms | 1000 | 500–5000, USB stream cadence |
| heartbeat_interval_ms | 1000 | 250–5000, at most half of timeout |
| heartbeat_timeout_ms | 6000 | 2000–30000 |
| utilization_target_pct | 65 | 5–94, below backdown threshold |
| utilization_backdown_pct | 80 | 6–95, above target |
| adaptive | 1 | 0 or 1 |
| radio_profile | production | production or experimental_medium_fast, as a separate command |

`production` restores the boot profile. `experimental_medium_fast` applies the alternate preset in RAM. Apply profiles deliberately to each participating device while idle and record the snapshot. Transmission requires a known radio configuration. Select one target using `{"target_id":"!00000003"}` or up to eight in order using `{"target_ids":["!00000003","!00000004"]}`. IDs in these examples are synthetic. Start with `{"mode":"survey"}` or explicitly choose `bench`. Bench retains null location when GNSS is unavailable. Both modes require a healthy host heartbeat.

## USB framing

The existing stream envelope is `94 c3 | uint16 length (big endian) | body`. Ordinary protobuf messages and text diagnostics use independent paths. A survey body begins with four bytes `00 53 56 31`. Only the physical serial console consumes survey commands and the device must enable serial in its existing security settings. TCP, BLE and RF packets cannot invoke these controls.

A command body is exactly 118 bytes. Python format `<4sIIBB10I64s` defines the little-endian layout. Fields are magic, boot ID, command serial, opcode, argument count, ten unsigned 32-bit argument slots, and 64 key bytes. Zero unused fields. Opcode numbers in order from 0 are `hello, get_state, configure, start, pause, resume, stop, set_target, heartbeat, _enroll, _clock, _profile`.

- The adapter probes identity with a hello using boot zero and serial one. After verifying the expected device, it sends hello with boot and serial zero to pause any prior active run. The returned boot and last command serial establish the new connection. Mutating requests must match the observed boot and increase the serial. Repeating the immediately preceding byte-identical command returns its prior outcome.
- Configure takes nine unsigned integers in the order `min interval, timeout, max interval, GPS max age, heartbeat timeout, GPS interval, utilization target, utilization backdown, adaptive`. Heartbeat interval is host-owned. Start argument zero selects survey and one selects bench. Target takes one to eight numeric node IDs. Profile uses zero for production and one for experimental MEDIUM_FAST.
- Physical enrollment uses argument zero for the peer ID. Key bytes are its 32-byte X25519 public key followed by the separately generated 32-byte cohort secret. Use each individual node's own preserved keypair. Only the selected tester is enrolled on each RAK. The client can enroll eight RAKs. The separate `enroll()` method keeps credentials outside the normalized GUI API, event log and command journal. Secure commissioning inputs stay private. Clock accepts current Unix seconds on the stopped device. Headless RAK replay checks continue after loss of their local clock.

Device event bodies are the four-byte survey magic and ASCII CSV with no terminator. The common first fields are `boot,seq,firmware_millis,type`. The adapter handles framing splits and partial reads, skips non-survey frames, and reports gaps. Raw field order after the type is listed below. Counters and identifiers are unsigned decimal. Signal strength is signed. The adapter translates sentinel fields to JSON null according to validity and result status.

| Type | Fields |
| --- | --- |
| hello | node, build, is_client, hardware_model, region, preset, channel_num, tx_power, use_preset, tx_enabled, last_command_serial, enrolled |
| ack | command_serial, opcode, error_code |
| state | run_state (0 idle, 1 running, 2 paused), bench, session, segment, next_target, interval_ms, quiet_remaining_ms, dropped, queue_free, queue_capacity, successes, timeouts, deferrals, rejections, suppressed, fresh_gps, healthy_heartbeat, command_serial |
| profile / settings / targets | experimental, preset, hardware_verified / nine settings in wire order / count followed by eight target slots |
| gps / sendfix / txfix | session, attempt, valid, latitude_e7, longitude_e7, altitude_m, altitude_known, fix_utc_s, fractional_ms, age_ms, quality, satellites_known, satellites |
| attempt | session, segment, attempt, target, bench, enqueue_ms, applied_interval_ms, utilization_pct |
| result | session, segment, attempt, target, bench, status, request_mesh_id, reply_mesh_id, enqueue_ms, tx_start_ms, tx_done_ms, finish_ms, uplink_rssi, uplink_snr_quarters, downlink_rssi, downlink_snr_quarters, request_wire_bytes, estimated_airtime_ms, local_util_pct, remote_util_pct |
| quiet | source, request_mesh_id, target, remaining_ms, receive_rssi, receive_snr_quarters |
| late | session, attempt, target, reply_mesh_id, duplicate_flag, previous_completion_ms |
| pong | request_mesh_id, reply_mesh_id, enqueued, attempt |
| rx | source, destination, mesh_id, hop_start, hop_limit, want_ack, decoded_port_or_zero, receive_rssi, receive_snr_quarters |
| airtx | source, destination, mesh_id, hop_start, hop_limit, want_ack, local_class, wire_bytes, predicted_airtime_ms |
| tx / txdone / fault | mesh_id, wire_bytes, predicted_airtime_ms / mesh_id / reason |

ACK error codes 0–6 mean success, wrong boot, stale command, invalid state/parameters, enrollment, interlock, unsupported command. A result timeout is an unsuccessful round trip. An enqueued packet has a separate TX-start event and hardware TX-complete notification when observed. The measured client transmit interval is TX-start to TX-done callback, including callback latency. RTT starts at TX start. Host UTC receipt, firmware monotonic milliseconds, and original fix UTC have separate fields. A null TX snapshot means that sample was unavailable. Firmware keeps 16 events. The adapter writes received events as JSONL before forwarding them to its bounded display queue. Each new connection uses a new log, an authoritative snapshot and the persistent command journal.

## RF framing and quiet

Both packet directions use encrypted Meshtastic broadcast on the configured primary channel and private port 310. Each contains a 47-byte v1 payload. The physical mesh ID is independently allocated for each transmission. Application fields in little-endian order are version (u8), type (u8, 1 PING or 2 PONG), session (u32), attempt (u32), responder node ID (u32), Unix seconds (u32), uplink RSSI (i16), SNR in quarter dB (i16), channel utilization percent (u8), and two 12-byte tags. The PING metric fields are zero. A PONG echoes the session, attempt, responder and request timestamp, returns the measured uplink signal, and carries the responder’s utilization. The client independently measures downlink signal on that exact PONG.

The first tag authenticates the private survey frame with the locally enrolled cohort key. All participants can recognize that frame independent of tester authorization. The second tag uses the tester/responder X25519 shared secret derived from the pinned peer public key. Both tags are truncated HMAC-SHA256 over `SNORR-SV1`, a domain byte (1 or 2), little-endian source and mesh packet ID, and all payload bytes preceding the first tag. Each tag uses its own key. Tag overhead is 24 RF payload bytes. No keys or test vectors from enrolled radios are published.

All direct hearers renew quiet on each fresh, group-valid PING, including a PING for another node or without a valid tester tag. Only the selected responder with a verified tester tag replies. Both directions have zero starting/remaining hops, no generic responses, no routing ACK, and no reliability retries. The router consumes decoded survey packets before duplicate, upgraded-hop, relay and application handling. Only the physical LoRa receive path sets the local provenance flag. MQTT/UDP publishing is excluded for locally originated survey frames. Firmware can identify encrypted traffic only on channels it can decode.

Quiet lasts 900 seconds from the latest accepted PING. Locally generated autonomous packets are marked before encryption and checked again immediately before TX, including queued packets from the previous quiet generation. The dedicated client suppresses its own GPS RF, including the lost-and-found coordinate text. Local GNSS and USB continue. Report timers advance normally. Ordinary relay traffic and explicit admin traffic retain their existing paths. A RAK reboot with an unresolved quiet marker conservatively begins a fresh 900-second window. Clockless RAKs persist per-source replay reservations and can need up to 60 seconds before accepting a new authenticated epoch after reboot. The selected authorized tester has a reserved lane, as does the enrolled tester selecting a different target. Seven additional group senders fit the bounded table. A lane admits at most eight distinct packet IDs per second and rejects repeats for the entire epoch. The four-board bench uses one tester.

## Cancellable CLI

For a Windows bench use the canonical watcher directory. Supply each board's live identity. Use a new ignored run directory. On Linux replace the COM ports with the actual stable device paths.

```powershell
python scripts/survey/bench.py --mode bench --seconds 7200 --client 'COM5=!699c2ed8' --responder 'COM8=!a65601b3' --responder 'COM9=!b456f760' --responder 'COM32=!49ac6d7f' --target '!a65601b3' --target '!b456f760' --target '!49ac6d7f' --station-dir '<shared checkout>/private/bench/rak-label-station' --output 'private/survey/soak-001'
```

Ctrl+C or a `STOP` file in the run directory cancels. Progress is replaced atomically every 30 seconds. `summary.json` reports duration, counts, witnesses, asymmetric metrics, measured TX timing, violations and cancellation status. Exit 0 requires the requested duration and acceptance counters; 130 indicates cancellation. Raw board logs stay private. Independent receive observations, collocated radio measurements and a relay-only field geometry are separate evidence.

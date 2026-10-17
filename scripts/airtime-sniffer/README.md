# SNORR Airtime Sniffer

Use the dedicated **Heltec V3 sniffer firmware**, connected by USB. Capture every receive event it exports, including repeated copies, unknown channel keys, other destinations and failed radio reads. Show known-channel text, GPS, NodeInfo, battery/environment/power telemetry, standard neighbors, routing/traceroute, waypoints and SNNS v1 reports. Unknown application payloads remain available as bytes.

## Windows

Install Python 3.10+ with Tk and the Python launcher. Double-click **`run-windows.cmd`** in this directory. It creates an isolated environment under ignored `local-data/sniffer-venv`, installs the pinned dependencies, and opens the GUI. Select the V3's current COM port and click **Start capture**. **Stop** flushes and closes the session; the next Start creates new files. Close other serial monitors/Meshtastic clients before starting.

From a terminal, with dependencies installed in your chosen environment:

```powershell
python scripts/airtime-sniffer/sniffer.py --list-ports
python scripts/airtime-sniffer/sniffer.py --port COM6 --gui
python scripts/airtime-sniffer/sniffer.py --port COM6
```

CLI prints each reception, including full raw hex for opaque/error packets. Ctrl+C stops cleanly. `--duration 120` captures for two minutes. Both GUI and CLI use the same capture/decoder/logging code; GUI also prints to its launching console. Packet details include the entire raw frame and decoded content; the table retains the most recent 5,000 rows while files retain the full session. The GUI reports omitted display updates if it cannot keep up. Current/peak receive airtime and original-sender/relay-hint totals help locate repeated traffic.

## Linux

Use Python 3.10+ with `venv` and Tk; on Debian/Ubuntu those are provided by `python3-venv` and `python3-tk`. Run:

```bash
bash scripts/airtime-sniffer/run-linux.sh --port /dev/ttyUSB0
```

Prefer `/dev/serial/by-id/…` when several devices are attached. The user running the tool needs serial-port permission (usually membership in `dialout`, applied after login). The CLI works without Tk or a display:

```bash
python3 -m venv local-data/sniffer-venv
local-data/sniffer-venv/bin/python -m pip install -r scripts/airtime-sniffer/requirements.txt
local-data/sniffer-venv/bin/python scripts/airtime-sniffer/sniffer.py --port /dev/ttyUSB0
```

## Logs and optional keys

Each capture creates `local-data/sniffer/YYYYMMDD-HHMMSS-unique/` containing:

- `serial.raw`: exact serial bytes, including raw packet chunks and firmware diagnostics.
- `events.jsonl`: structured receptions, complete RF bytes, decode results, configuration observations, gap/error events and host receipt timestamps.
- `messages.log`: readable message stream, including repeat labels and opaque raw hex.
- `session.json` and `summary.json`: capture settings, counters, total airtime by origin and observed receive airtime for the trailing sixty seconds.
- `error.log` if the capture failed, including a disconnected/busy serial port. Start again after reconnecting to create a new session.

These files can contain real messages, names and locations. Keep them in ignored `local-data/` or `private/`. `--log-dir PATH` overrides the destination. Logs are flushed as records are written; a hard power loss/process kill can still leave an incomplete final record.

The decoder automatically loads `private/sniffer/channels.json` when present. It can contain several channel keys, including several with the same channel name:

```json
{"channels":[{"name":"MyMesh","psk":"AQ=="}]}
```

This example is the **public default key alias**, not a private key. For private channels, use their real base64 key in this ignored file; pass `--keys PATH` to use another file. The prepared desktop has the connected V3's original channel key and the verified pilot key privately. A Linux machine needs its own authorized private copy. No key is printed or written to capture metadata. Built-in public default keys are tried for standard channel names. No brute force or PKI key import is performed. Other nodes' PKI DMs remain opaque.

Channel AES-CTR has no authentication. Successful structural decoding is labeled **decoded_candidate**, not cryptographic proof of authenticity. Key-hash collisions and malformed payloads remain possible. Unknown/invalid application protobufs retain decoded Data fields and payload bytes. Relay is only an eight-bit last-hop hint; ambiguous suffixes must not be treated as a verified full node identity.

## Interpreting airtime

All copies count. **RX airtime / last 60 seconds** sums firmware-estimated receive airtime, including radio read errors, over a fixed sixty-second denominator. It is an observer-specific receive estimate, not the transmitting node's hour-based utilization or a spectrum-analyzer reading. The first minute has less than a full minute of observation. A repeated sender/packet/channel/payload within ten minutes gets a duplicate label; it remains printed/logged/counted. Totals are grouped by original sender, not the last relay. Source names learned from received NodeInfo are retained by the decoder; raw IDs remain the primary attribution.

The V3 listens continuously on **one frequency/modem and Meshtastic sync word**, preserving its selected US/channel-35 profile. It cannot listen to all frequency slots, all spreading factors or all protocols simultaneously. Do not channel-hop during an airtime investigation: that creates unobserved periods on every other channel. Arbitrary RF energy, collided packets and receptions never delivered by the radio are not recoverable. Even a dedicated receiver cannot promise every packet transmitted nearby.

Sequence, length and CRC32 validate serial reconstruction and report capture gaps. They cannot detect packets lost before the firmware handles a radio receive interrupt. For corrupted RF reads, bytes are explicitly untrusted and not decoded. CRC32 on chunks checks transport integrity; it does not authenticate the radio message. Very busy channels, a slow USB link or a stalled host can still lose data.

The dedicated target inhibits LoRa TX at compile time, skips routing/module handling of received frames and excludes Wi-Fi/Bluetooth/MQTT. The host sends **no serial commands**, requests or pings. It sets DTR/RTS inactive before opening, although some [USB drivers may briefly toggle those lines](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial.open) and reset the device. For provisioning/flashing, stop capture first. Firmware build details and the private recovery backup are recorded in the operation note.

## Replay and verification

```bash
python scripts/airtime-sniffer/sniffer.py --replay local-data/sniffer/SESSION/serial.raw
python -m unittest discover -s scripts/airtime-sniffer/tests -v
```

Replay creates a new capture directory and does not access serial. Its elapsed timeline follows packet device milliseconds (including timer rollover); wall timestamps are replay times. Time between different device boots and idle time after the final reception are unknown; replay's final summary ends at that reception. GUI interaction tests run when Tk/display are available and otherwise explicitly skip. Hardware reception, target identity/profile preservation and transmit inhibition are separate from synthetic replay checks.

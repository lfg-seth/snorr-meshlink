# Dedicated Heltec V3 airtime sniffer — 2026-10-16

Owner requests a dedicated debug receiver, Windows/Linux GUI/console tool, every observed packet including undecryptable packets/repeats, useful decoded data and a new log per run. Flashing is explicitly authorized. This is separate from the operational MQTT gateways.

## Hardware and image

- Connected **MC00 `!9ea0432c`**, API-identified HELTEC_V3 on Windows COM6; ESP32-S3, 8 MB flash. It is distinct from G001 `!9ea13cc0` and G002 `!849ad7a0`. Original firmware is `2.7.17.55580d10f`. This allocates one existing V3 to debugging; total owned count remains nine. Exact board subrevision/antenna model are unverified.
- Privately back up complete configuration/channels/security identity and all 8,388,608 flash bytes before updating. Recovery fingerprint: `19386e0c87a5adfcdbeed4a9681f0caa7b7758589ed48a9e0832c60d9029575e`. Backup/image/logs live under ignored `private/bench/v3-sniffer-20261016/`; do not publish the full-flash backup.
- Build **`heltec-v3-sniffer`**, source **`f95a443bba71ea2a1e135566547c4c593bd26436`**, version **`2.7.26.f95a443`**. Source consists of raw receive instrumentation `efca052b6` plus the necessary ESP32 OTA Wi-Fi-exclusion guard fix. These commits are published ancestors of the concurrent INA219 source `d929b8009`, already pinned by the project; retain that newer source pin. Do not roll back the concurrent sensor work to match this one image.
- Application image: `firmware-heltec-v3-sniffer-2.7.26.f95a443.bin`, **1,649,632 bytes**, SHA256 **`b2291f0fb3e350ef35a25365c06dc5b709f6823384e931239e8df8cc16e26e7b`**. Target reports 1,649,201 bytes flash / 118,876 bytes static RAM. The filesystem image produced by the build is **not flashed**.
- Final build uses a clean detached checkout under `private/bench/sniffer-source/firmware/`, excluding concurrent uncommitted sensor changes. Pinned Espressif32 6.13.0/Arduino ESP32 3.20017 dependencies; exact repository-configured clang-format 16.0.3 passes. Trunk is unavailable. Temporary short drive aliases resolve Windows' compiler subprocess command-length limit and are removed afterward.
- Generated partition table exactly matches the original first 3,072 partition bytes. Existing app0 is `0x10000` / `0x330000` bytes, active OTA sequence 1. Install only the verified application at **`0x10000`**; esptool reports hash verification. Bootloader, partition table, NVS, filesystem and recovery app are retained. No factory reset or full erase.

## Profile and receive behavior

Before flashing, persist/read back CLIENT_MUTE, LoRa TX off, Wi-Fi/Bluetooth/MQTT off, sensor/device telemetry off and normal serial console enabled. Keep debug-log API off for the plain-text capture stream. Independent post-update readback confirms the exact version, original identity/channel/key/security equality and original RF configuration except the intended TX disable. User record's role changes with the deliberately selected device role; its identity/name/key fields remain equal.

Actual receive profile is **US channel 35, 910.625 MHz, BW 250 kHz, SF11, CR 4/5**. The V3's original channel key differs from the current pilot key; both are available to the host decoder in ignored `private/sniffer/channels.json`. Channel settings/keys on the V3 itself are preserved. Cached node labels are private mutable display labels, not authenticated identities.

The dedicated build disables normal LoRa enqueueing and the final send entry point at compile time, excludes Wi-Fi/Bluetooth/MQTT, and returns before routing/module handlers for received frames. It exports raw receive bytes/status before decryption, ignore lists or duplicate suppression; rearm the radio before serial logging. Sequence/offset/length/CRC32 detect reconstructed-stream loss. Each handled receive is retained, including CRC/read errors (untrusted bytes), unknown keys, other destinations and duplicate copies. See [firmware contract](../../firmware/SNORR_SNIFFER.md).

## Host tool and verification

[Windows/Linux GUI, CLI, private keys, logging and replay instructions](../../scripts/airtime-sniffer/README.md). Windows launcher: `scripts/airtime-sniffer/run-windows.cmd`; Linux launcher: `bash scripts/airtime-sniffer/run-linux.sh`. The console mode uses the same capture engine. Each Start creates distinct `serial.raw`, `events.jsonl`, `messages.log`, session metadata and final summaries under ignored `local-data/sniffer/`. The host sends no serial commands/pings. Stop before any API/provisioning operation.

Twelve Windows tests pass, including real Tk start/table/selection/detail/file interaction. Eleven Linux checks pass with the GUI test explicitly skipped because Tk/display is unavailable; no native Linux USB capture/GUI claim. Linux launcher syntax passes. Portable C++ framing checks pass address/undefined-behavior sanitizers: standard CRC vector, all byte values, zero/max lengths, offsets and worst-width metadata. Host checks include known ciphertext, zero GPS/negative power, SNNS contract, unknown keys/PKI opacity, invalid application payloads, partial serial reads without writes, complete duplicate retention, sequence/chunk corruption and fresh per-run logs.

Live observation lasts **180.118 seconds**. All **10 receptions** reconstruct without a reported gap: seven POSITION_APP receptions from B002 and three PRIVATE_APP/SNNS receptions from R005. Three unique packet identities produce **seven duplicate receptions**, all retained and decoded. The final observed receive-airtime window is **10.27%**; the earlier reported 58% spike is not reproduced. Keyed and keyless replays preserve exactly the same ten raw byte strings and seven duplicate annotations. Without the pilot key, all ten remain opaque and their full hex is printed; with the key, all ten decode again. Real-capture GUI replay displays ten rows, duplicate annotations and complete raw/decoded SNNS details. Replay's reconstructed peak is 10.27%.

Automatic UART local status during the capture reports **TX 0 / RX 3 / bad RX 0**, with no Packet TX log entries in the full capture. A subsequent optional self-addressed telemetry-request probe times out; it is not used by the sniffer, changes no saved setting and is not treated as a fresh end-of-run counter measurement. No independent RF analyzer/silence measurement is claimed. Verification of failed-read/CRC handling uses synthetic records because no real RF read error occurs during this sample. Capture/probe interfaces are closed afterward; COM6 is available to the owner.

Private live evidence: `local-data/sniffer/20261016-212908-efb6988a/`. Keyed/keyless/GUI replay evidence, byte-for-byte comparisons and profile/build/flash records are retained under `private/bench/v3-sniffer-20261016/`.

## Limits and next use

One radio listens on one frequency/modem and Meshtastic sync word. It cannot recover arbitrary RF energy, collided/undetected packets, other frequencies/modems or data lost before a handled receive interrupt. Sequence/CRC checks reveal host reconstruction loss, not all RF loss. The receive-airtime estimate includes all observed copies/errors; it is not a spectrum measurement or another node's hour-based transmit utilization. The host uses a true trailing sixty-second window, which can differ from firmware's six ten-second buckets and another receiver's observations.

Known channel AES-CTR decoding is structurally validated and labeled `decoded_candidate`; channel encryption has no authenticity check. Other nodes' PKI DMs remain opaque. Relay suffixes are only eight-bit hints (invalid on legacy hop-start-zero frames), not verified identities. Long/high-rate observations and Linux hardware/GUI validation remain to perform.

Next useful step: run the GUI during a recurrence of the reported 58% spike, examine original-sender and relay-hint airtime/repeats, then compare a deliberately scoped one-router bench run. Keep actual gateway/repeater roles intact until that comparison is authorized.

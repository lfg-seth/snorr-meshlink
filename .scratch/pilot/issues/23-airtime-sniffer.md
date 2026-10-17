# Build a dedicated Heltec V3 airtime sniffer

Type: task
Label: wayfinder:task
Status: resolved
Assignee: airtime-sniffer-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Question

Owner requests a dedicated connected Heltec V3 debug sniffer, Windows/Linux script and GUI, every received packet including undecryptable packets/repeats, useful decoded content and a fresh log for every run. Flash as needed.

## Comments

2026-10-16 — Identify COM6 as HELTEC_V3 `!9ea0432c` / MC00, firmware `2.7.17.55580d10f`, US/channel 35. This is distinct from G001/G002. Preserve original identity, keys and complete settings privately. Dedicated target exports raw receive bytes before routing/decryption/duplicate filtering, with compile-time transmit inhibition. Host performs optional known-channel decryption; a single receiver stays on its selected frequency/modem rather than hopping and missing traffic.

## Answer

2026-10-16 — Dedicated `heltec-v3-sniffer` source `f95a443bb` is built in a clean isolated checkout and flashed as `2.7.26.f95a443` at app0/0x10000 only. Full private recovery backup, esptool hash verification and independent post-boot identity/security/channel/RF-profile checks pass. CLIENT_MUTE, TX/Wi-Fi/Bluetooth/MQTT disabled; receive export precedes filters/decryption and bypasses routing. The shared submodule retains later published sensor source `d929b8009`, which includes the sniffer commits.

- [Windows/Linux GUI and console tool](../../../scripts/airtime-sniffer/README.md) prints/logs every exported receive, preserves unknown ciphertext/repeats and decodes useful known-channel protobufs/SNNS. Each capture gets separate raw, JSONL, readable and summary files. GUI shows full details, current/peak receive airtime, original-sender and relay-hint totals. The host sends no serial commands.
- Twelve Windows checks pass, including Tk interaction; eleven Linux checks pass with its GUI check explicitly skipped for missing Tk/display. Portable firmware framing passes address/undefined-behavior sanitizers. [Build/hardware evidence](../../../docs/operations/airtime-sniffer.md).
- Three-minute hardware capture: ten receptions, seven duplicates, seven B002 GPS copies/three R005 SNNS copies, all decoded and zero reported capture gaps. Keyless replay prints all ten opaque payloads with byte equality; keyed/GUI replay preserves all rows/data. UART status observes TX zero; an extra optional local-statistics request times out and does not affect capture. No real RF error, external RF-silence measurement, 58% recurrence, high-load completeness or native Linux USB/GUI verification claimed.

Task complete. Next use is to capture the actual airtime spike, then deliberately compare a one-router bench condition; no repeater/gateway role change is activated.

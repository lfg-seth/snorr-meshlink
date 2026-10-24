# B002 firmware and three-minute reporting - 2026-10-24

Owner requests the latest firmware/configuration and three-minute telemetry and
SNNS on existing member tracker **B002 `!699ca878`**. USB identity
**`90:70:69:9C:A8:78`** independently matches COM4 and original
**HELTEC_V4 / heltec-v4 / 2.7.26.54e0d8d**. No other board is written.

## Selected image and preservation

The authorized firmware remote confirms **`snorr/develop`** at
**`a56466d8c127929c22a959b659296d8ddfb17921`** before installation. Reuse the
already built, verified **heltec-v4-gateway / 2.7.26.a56466d** application.
That target inherits the original OLED V4 and adds passive SNNS plus a
180-second fallback; its name does not assign a gateway role or enable MQTT.
This is a selected local build, not a published binary release.

The **2,118,976-byte application** has SHA256
`c5d0f0ff9c1f5ec6aad689d5b1744f4a82861c44b1bc71ee9f69035b81969901`.
Build-manifest MD5/target/model, original partition-table equality, active app0
selection and available application size pass. Application-only write and
independent esptool digest verification pass at **`0x10000`**. Bootloader,
partition table, other application, filesystem and settings are preserved.

Before writing, retain the complete original profile/keys and **16,777,216-byte
flash backup**, SHA256
`a2848812a14fb091efa4f497ece8cc8a0913993a6b1f61decfe601dbde12d373`.
The first 921600-baud read stalls at approximately 45% and is stopped before
any flash write. A 460800-baud retry completes in sixteen bounded 1 MB chunks;
all sizes and the assembled backup hash are recorded privately. No erase or
factory reset is used.

Private raw evidence, scripts, profiles, keys and any positions remain under
ignored `private/bench/B002-update-20261024/`.

## Saved member profile

The original device telemetry interval is **2,147,483,647 seconds**, with the
enable flag unset; neighbor reporting is unconfigured. The requested update
saves:

- **Device/battery telemetry enabled, 180 seconds.** Environmental and power
  telemetry remain disabled; no external sensor is inferred for B002.
- **Neighbor collection enabled, over-LoRa SNNS**, using the saved
  **180-second device interval**. Jitter, scheduler and airtime admission still
  apply, and reports require collected observations. Standard NeighborInfo
  remains separate at **21,600 seconds**.
- Existing **CLIENT member role**, names, individual security identity, private
  channels, US radio settings, **10 dBm configured TX power/FEM**, enabled TX,
  disabled Wi-Fi/MQTT and all other local/module settings are preserved.
- GPS remains enabled on **RX39/TX38/enable34**, **60-second acquisition** and
  **120-second ordinary position reporting**, with position flags **939**.
  GPS cadence is separate from the requested telemetry/SNNS cadence.

After flashing, complete original owner/identity/channel/local/module equality
passes. After configuration and again after an explicit reboot, complete
intended-profile equality passes, including keys. Final independent readback:
**2026-10-24T19:27:54.806409Z / 12:27:54 Pacific**. Firmware and target read back
as **2.7.26.a56466d / heltec-v4-gateway**.

## Fresh delivery acceptance

After the final reboot, an authenticated TLS subscriber receives **two new
device telemetry packets and two SNNS reports through each of G001, G002 and
G003**. Retained packets are rejected and per-gateway packet IDs deduplicate
the observation. No manual telemetry request or synthetic radio traffic is used.

| Measurement | New source reports | Observed interval |
| --- | --- | --- |
| Device/battery | Measurement times 19:28:59 and 19:32:00 UTC; 4.314 and 4.316 V | 180.19-180.20 s between MQTT receipts; source wall clock advances 181 s |
| Private SNNS | Same boot 1805623836, sequences 1/2, source uptimes 64/259 s | 195 s source uptime; 195.20-195.22 s between receipts, including jitter/scheduling |

Independent read-only production database and authenticated portal state verify
the same **two battery observations and two SNNS reports**, with each report's
G001/G002/G003 receipt preserved as accepted or duplicate. SNNS report row
counts grow from three to four. At the initial checkpoint, portal battery
voltage and measurement time match the latest observation: **4.316 V**, measured **19:32:00Z**, received
**19:32:01.682Z**, timestamp quality **valid**. Existing `lipo-1s` / 3000 mAh
metadata is retained; percentage remains unknown. Readings are device-reported,
not an independent voltage calibration.

Local MQTT evidence is `delivery-summary.json` and `mqtt-events.jsonl` in the
private directory above. Server verification and private API state are under
`/root/b002-update-20261024/`. Serial and MQTT handles are closed at handoff.
After the serial observer closes, the database records another boot,
**535549071**, sequence 1 at **19:33:38.373Z**, source uptime 74 seconds.
The cause is unverified; no additional reboot command is issued at that point.
The authenticated member snapshot also matches that boot's fresh **4.316 V**
observation measured **19:33:22Z**, received **19:33:24.334Z**. A separate
MQTT-only continuation leaves COM4 closed and receives **two more device and
SNNS packets per gateway** through G001/G002/G003. Both SNNS reports retain
boot **535549071**, sequences **2/3**, source uptimes **269/479 seconds**:
**210-second source gap**, approximately **213.30-second receipt gap**.
Device receipt gaps are approximately **180.31 seconds**. No further boot-ID
change is observed in this continuation; reset cause and longer stability
remain unverified. This also demonstrates why the saved 180-second SNNS
baseline is not an exact wall-clock receipt guarantee. Evidence:
`passive-delivery-summary.json` and `passive-mqtt-events.jsonl` in the same
private directory. The MQTT-only subscriber is closed at completion.

Final authenticated API/read-only database verification at **19:41:09Z**
matches **five unique battery observations and five unique SNNS reports**
since the reboot-verification cutoff, each with receipts through all three
gateways. The snapshot selects the latest **4.316 V** observation measured
**19:39:23Z**, received **19:39:24.730Z**, with valid timestamp quality.

No new GPS position is observed during this short capture; enabled GPS/profile
readback is not fresh-fix acceptance. Field GPS freshness, battery runtime,
forced-relay delivery, sustained cadence and outage behavior remain separate
gates under the [phone-free run preparation](../../.scratch/tasks/gh-2-run-plan.md).

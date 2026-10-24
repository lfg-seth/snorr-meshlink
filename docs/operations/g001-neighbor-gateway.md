# G001 passive gateway neighbor collection — 2026-10-19

## Saved-interval bench update - 2026-10-24

The owner-selected application-only update installs dedicated
`heltec-v3-gateway / 2.7.26.4c96b9b` on the independently identified G001.
Full private profile/flash backups, exact image/partition verification and
complete intended identity/key/channel/local/module equality pass through
explicit reboot. CLIENT, LoRa TX disabled, local-only collector, Wi-Fi/MQTT
and disabled device telemetry retain their original values. Its saved device
interval remains 2,147,483,647 seconds; local SNNS keeps its separate baseline.
[Shared image, controller, measurements and remaining gates](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24).
Historical images and portal acceptance below describe the October 19 run.

Owner connects G001 to complete [Enable richer passive neighbor measurements on Heltec V3 gateways](https://github.com/lfg-seth/snorr-meshlink/issues/31). Both gateways now run the dedicated collector with local MQTT reporting and LoRa transmission disabled. [G002's build, contract, source publication and initial portal mapping](g002-neighbor-gateway.md) remain the shared reference.

## Image, backup and preservation

- Identify **G001 `!9ea13cc0` / HELTEC_V3**, COM6, ESP32-S3 revision v0.2 / 8 MB flash, initially stock `2.7.26.54e0d8d`. Port reassignment follows physical board identity; G002 is not the connected serial target.
- Privately back up G001's complete configuration/channels/security identity and all **8,388,608 flash bytes**. Full-flash SHA256 **`63c4454b6db6ee4683b1ec6c5d79f5f8cdb3f110f0998f7dbe7fbaf79a9c1b1e`**. Recovery copy is board-specific.
- Reuse the exact cached **`heltec-v3-gateway` / 2.7.26.9d2fd8f** application, **2,111,152 bytes**, SHA256 **`fe28db2e11a090c535e40003764038a0dc349430c753062906771b56b2ef7777`**. Binary source `9d2fd8fd0025ccd658e383eaf6548c342a96e70d`; published project pin `473a9ed41137f16a51c4962ffb5c186f53d046ae` only adds the Markdown formatter correction. No rebuild or firmware-source change.
- Verify original partition bytes against the built table and OTA sequence 1 selecting app0, **0x10000 / 0x330000**. Flash only that application; esptool hash verification passes. Preserve bootloader, NVS, partition table, filesystem, recovery application and keys.
- Enable `neighbor_info.enabled`, disable `neighbor_info.transmit_over_lora`; the standard NeighborInfo default persists as **21600 seconds**, separately from the custom local minimum of 60 seconds plus jitter/scheduler delay. Full independent profile comparison passes after flashing and through explicit reboot: original user, channels, security identity, local configuration and all other module sections are identical. Preserve **CLIENT**, **LoRa TX disabled**, Wi-Fi and MQTT. G001 already has the owner's supplied Wi-Fi settings; no network rewrite is required.

The reused image's collector/module sanitizer tests, ESP32 build and PR checks are documented with G002. New G001 verification is checksum/partition matching, application hash, independent device readback and actual delivery; no new firmware regression-suite result is claimed.

## Measured delivery

The first validating-TLS subscriber window, **19:54:55–19:57:55 Pacific** (180.3 seconds), receives **six G001 deliveries with zero decode errors**. G001's own report arrives at the end of the window, so an earlier mid-window check correctly had no report yet. Early absence was not a firmware/network failure finding. Subsequent passive observation uses no serial access or active probes.

At **19:57:55.391 Pacific**, live archive/normalization accepts new non-retained encrypted SNNS packet **a1a5ea71**, boot ID **1325647066**, sequence **1**, reporter uptime **72 seconds**. Original sender, SNNS observer and MQTT gateway all identify **G001**; topic/envelope gateway IDs match. The report contains:

| Heard device | RSSI dBm | SNR dB | Hearing age at encoding, seconds | Observations |
| --- | --- | --- | --- | --- |
| R005 | -43 | 6.00 | 48 | 1 |
| R002 | -62 | 6.25 | 36 | 1 |
| R004 | -81 | 5.50 | 33 | 1 |

Independent authenticated live state exactly matches all three report rows, including values, direct-path classification, source/gateway provenance and null absolute hearing clocks. All **nine devices** and **13 pre-existing G002 reports** are preserved at that check. G001 also forwards fresh B002 GPS, R005 telemetry and R005/R002/R004 neighbor reports. Existing per-gateway duplicate handling remains active; R005 **19:56:14** and R004 **19:57:22** G001 copies are correctly recorded as duplicates. Member positions stay private.

Passive continuation records sequence **2** at **19:59:10** (six rows, uptime 147 seconds) and sequence **3** at **20:00:25** (seven rows, uptime 222 seconds), without another serial connection. Sequence 3 covers **R001–R005 and B001/B002**. R002/R004/B002 observation counts advance from 1 to **2**, with new signal readings and appropriately younger hearing ages. These short samples demonstrate collection/counter updates; they do not establish sustained delivery percentages or cadence.

A second authenticated snapshot independently matches every sequence-3 row/value, accepted G001 receipt, correct observer/gateway identity and unknown absolute hearing time. All nine devices and 14 G002 reports are retained at that later check.

The already configured gateway source mappings work without another portal configuration change, worker restart, replay or application deployment. This hardware run does not rerun the G002 session's isolated server recovery tests; its board-specific full-flash backup is retained for recovery. No factory reset, profile cloning, key replacement or other-board write occurs.

## Evidence and limits

Exact profile/full flash, image/manifest, console, MQTT envelopes/subscriber summaries and portal readbacks remain ignored under `private/bench/G001-neighbors-20261019/`. Remote sanitized-measurement snapshot evidence remains root-private at `/root/gateway-neighbors-20261019/g001-snapshot-evidence.json`. Serial/API sessions close after verification. The unrelated battery-box model remains untracked.

Both G001/G002 collector rollout acceptance checks now pass. These are short bench samples, not calibrated RF readings, packet-delivery ratios, sustained reporting/freshness, independent radio-silence proof, battery runtime or field coverage. Hearing age is at encoding and excludes backhaul delay. Power telemetry remains deliberately disabled on the current repeater bench profile; [the historical G002 sensor-power follow-up](https://github.com/lfg-seth/snorr-meshlink/issues/5) is separate.

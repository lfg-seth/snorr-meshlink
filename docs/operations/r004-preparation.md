# R004 preparation — 2026-10-16

Owner requests flashing the newly connected RAK with the handoff's latest pinned release, configuring/naming it R004, registering it in the live database/portal at R001's location, and recording the fitted temperature sensor and INA219. This allocates another inventoried board, without a purchase or site-installation claim.

## Firmware and saved configuration

- Independently identify RAK4631 `!77fdb9f1`, hardware ID `75762d0c4f9b0c82f1b9fd774661875b`, USB serial `820C9B4F0C2D7675`, normal Windows COM17. Former name MR03 and firmware `2.7.17.36133d29d`. Complete original local/module/channel configuration and keys are backed up in ignored `private/bench/COM17-before-rak.json`.
- Verify the complete cached [pinned prerelease](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1) using `scripts/bench/download-rak-release.py`; no rebuild. Request DFU only on this board, match COM18's USB serial and E: bootloader `WisBlock-RAK4631-Board`, bootloader 0.4.3 / S140 6.1.1. Copy the verified RAK UF2 and independently read **2.7.26.0b65f2e** on COM17. No factory reset, key replacement, bootloader update or other-board change.
- UF2 SHA-256: `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`; binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`, release/tooling pin `8fe47325e38b82c8b2358293484ff845320d1be6`.
- Name `SNORR Pilot Repeater R004` / `R004`; ROUTER, LOCAL_ONLY rebroadcast, node information 10,800 seconds, no power saving. Exact private pilot channel/key matches the verified G001 reference, other channels disabled, RAK channel uplink/downlink disabled. Existing US region retained; LONG_FAST, slot 35, hop limit 3, transmit enabled at 10 dBm and boosted receive match the saved pilot profile.
- Device, environment and power telemetry explicitly enabled at **900 seconds** each; unrelated air-quality/health disabled. NeighborInfo enabled with transmit-over-LoRa true and standard interval 21,600 seconds; companion cadence remains firmware-controlled. MQTT/Wi-Fi disabled, Bluetooth random PIN and serial administration retained, debug API off. Original device private/public keys and admin-key list are preserved exactly.
- Clear old fixed position; fixed-position mode off, GPS disabled. Planned coordinates remain portal configuration. Set the clock through serial administration. Independent complete profile/key readback passes before and after an explicit reboot. Ignored evidence: `R004-verified.json`, `R004-identity.json`, `R004-local-packets.json`, `R004-local-sensors.json`.

## Sensor evidence and limits

Owner reports the same temperature sensor as the other RAKs and an INA219. Exact printed sensor model, shunt polarity, charger junction and calibration are unverified. Existing owner-reported wiring is battery → INA219 → RAK.

| Local report | Firmware-reported values |
| --- | --- |
| Device telemetry | 4.087 V; level 101 is external-power/charging/no-battery status, not a percentage |
| Environment telemetry | 26.567078°C, 21.399498% RH, 0.008 V, 1.6 mA |
| Power telemetry | `ch3Voltage` 0.008 V, `ch3Current` 1.7 mA |

The INA219 bus voltage differs substantially from device battery voltage during USB use. Check wiring and compare against a meter before interpreting branch current. The pinned INA219 driver writes the legacy EnvironmentMetrics union even when called by PowerTelemetry; the observed channel 3 encoding does not establish a correct power-channel mapping. Do not label these values solar input, total battery charging current or verified charge direction.

New automatic post-registration reports through G001 (`!9ea13cc0`):

| Packet | MQTT receipt (UTC, 2026-10-17) | Result |
| --- | --- | --- |
| `56599808` | 02:35:35.802 | Device: 4.143 V, uptime 66; normalized into live R004 observation |
| `2408390913` | 02:35:46.081 | Port 256, 40 bytes, `SNNS` v1; archived, normalized decoding unsupported |
| `104352002` | 02:36:00.451 | Environment: 26.510239°C, 21.435547% RH, 0.008 V / 1.9 mA; temperature/humidity normalized |

Measurement clocks and MQTT receipt times remain separate. Earlier packets before R004 registration are excluded from ingestion success. G002's last recorded receipt was `2026-10-15T14:38:41.170Z`; this session does not verify its current radio/MQTT path. No gateway configuration is changed. Current and custom-neighbor normalized portal ingestion remain unsupported; receipt alone does not establish portal display.

## Live registration and recovery

Manual [add-r004.js](../../deploy/portal/add-r004.js) accepts only this verified hardware/node identity and pinned version. It reads root-private `/etc/meshlink/r004.json`, requires equality with R001's database latitude/longitude, refuses identity conflicts, and preserves existing records. It is outside ordinary schema migrations and never seeds the demo/live databases automatically.

Private staging/evidence: `/root/r004-provision/`. Isolated live-database-copy checks pass for invalid identity rejection, adding R004, repeat-run idempotence and preservation of every existing device row. After backup/recovery verification, stop live API/worker, apply the transactional migration, atomically merge worker mapping `!77fdb9f1 → r004` and verified hardware identity, and restart both services. Device security keys are never installed on the server.

Authenticated loopback proxy state verifies eight devices: B001/B002, G001/G002 and R001–R004. R004 shares R001's private **planned** coordinates and has fitted weather-sensor capabilities. Warnings remain disabled pending activation/threshold verification. R004's battery assembly, antenna and solar configuration stay explicitly unknown; sharing a location does not copy equipment. INA219 fitment, power cadence and unsupported current ingestion are recorded in metadata. Existing portal frontend consumes this new record without an application rebuild.

Append R004 to private `/etc/meshlink/repeaters.json`, preserving prior entries, for backup/device-count verification. Historical `add-repeaters.js` accepts exactly the original three boards and is not the update interface for this expanded manifest. Backups include both private provisioning files and the worker mapping.

Pre-change backup `meshlink-20261017T023250Z.tar.gz`, SHA-256 `600645a3c535e00f350a5ff103e488662021a069fcb40f0a617376e649281e06`, passes isolated recovery. Post-change backup `meshlink-20261017T023357Z.tar.gz`, SHA-256 `fc55edd72292cfeb11a411ce245779cf60f1db5fe93ee4fbcc61c16592788080`, restores eight devices and retained history/archive. Final backup after fresh reception and preserving migration source, `meshlink-20261017T023742Z.tar.gz`, SHA-256 `39d6e92630e9327a2e92af4900a3a23f18db823f404adf971c093d360ef02296`, also passes isolated recovery: eight devices, 703 observations, 2,689 receipts and 1,504 archived envelopes. Live-mode marker, proxy/authentication boundaries/throttling, public HTTPS/certificate checks and isolated database/API/history recovery pass. A first immediate post-restart sign-in hit API startup; subsequent authenticated checks pass. The verifier detects the missing fourth private-manifest entry; adding it restores full verification.

See [TEST-010](../../records/field-results.md#test-010--r004-released-firmware-and-live-registration). No authenticated browser visual review, forced relay, installed-site placement, field coverage, sustained cadence, battery endurance or calibration result is claimed.

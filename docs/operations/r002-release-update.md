# R002 released firmware update — 2026-10-16

Owner connects R002 and requests updating it, explicitly confirming **no external sensors**. This updates an existing inventoried repeater and portal record; stock counts, planned location/equipment and other radios are unchanged.

- Identify COM9, RAK4631 `!b456f760`, USB serial `BADB1E79E9739FC4`, name R002, stock `2.7.26.54e0d8d`. Save complete owner/local/module/channel profile and keys privately at `private/bench/R002-release-0b65f2e/before.json`.
- Verify all cached [pinned prerelease](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1) assets using `scripts/bench/download-rak-release.py`. Match DFU COM11's USB serial and F: `WisBlock-RAK4631-Board`, bootloader 0.4.3 / S140 6.1.1, then copy verified UF2. No rebuild, reset, bootloader update, region change or key replacement.
- Installed **2.7.26.0b65f2e**; binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`, release/tooling pin `8fe47325e38b82c8b2358293484ff845320d1be6`. UF2 SHA-256 `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`.
- Preserve entire original local configuration, channel records and owner record exactly, including device keypair/admin keys, ROUTER/local-only, US/LONG_FAST, slot 35, hop limit 3, 10 dBm transmit, MQTT/Wi-Fi disabled and debug API off. Firmware-introduced local default changes are restored from the original profile.
- Retain enabled **900-second device/battery telemetry**. Explicitly disable environment, power, air-quality and health measurements. Enable NeighborInfo and transmit-over-LoRa, standard interval **21,600 seconds**; custom companion retains firmware-controlled cadence. No AHT/INA219 capability assigned.
- Independent exact comparison of original local configuration, channels, owner and hardware ID passes; only intended telemetry/NeighborInfo module fields differ. Synchronize clock and explicitly reboot; complete independent readback passes again. Private final evidence: `private/bench/R002-release-0b65f2e/verified.json`.

## Portal record and verification

After a live backup, update only existing R002 configuration through the local-only PocketBase superuser API: verified firmware and owner-confirmed absent external sensors; weather/solar/intrusion equipment and temperature/humidity/solar-input capabilities remain false. Preserve identity, location, planned equipment, warnings and other fields; compare all other device configurations before/after. Mirror only these metadata fields in R002's private `/etc/meshlink/repeaters.json` entry and add a dated event. No worker identity/key change, schema migration, frontend rebuild or demo update.

Authenticated loopback portal verifies updated metadata and all eight devices. Private rollback/evidence: `/root/r002-update/`. An immediate API attempt encountered the backup restart window; subsequent code waits for health. Existing bootstrap login uses the email identity defined in `backend/manage.py`, rather than generated superuser username. No credentials printed or changed.

Fresh post-reboot automatic device packet `2575628823` reaches G001/MQTT at `2026-10-17T02:43:29.464Z` (October 16 Pacific): **4.202 V**, level 101, uptime 66, measurement time `02:43:26Z`. It normalizes into R002's live battery observation. Fresh port-256 packet `926194200` reaches G001/MQTT at `02:43:36.491Z`: **40-byte SNNS v1**, archived with normalized decoding unsupported. No fresh G002 delivery or two-gateway result is claimed.

Pre-update backup: `meshlink-20261017T024147Z.tar.gz`, SHA-256 `7b033e47be835dc192b4d7c0a1f2fa7609743438a131bf7ea8625bda7375ccb8`. Final backup `meshlink-20261017T024339Z.tar.gz`, SHA-256 `d2295228e4e7489f2ee53c2e0088525b8231c81d93cedb2a7ca8eef2381ddca7`, passes isolated database/API/history recovery: eight devices, 706 observations, 2,695 packet receipts, 1,513 archived envelopes and six events. Live-mode marker, proxy/authentication/throttling and public HTTPS/certificate checks pass.

See [TEST-011](../../records/field-results.md#test-011--r002-released-firmware-update-without-external-sensors). Custom-neighbor normalization remains unsupported. No calibrated voltage, sustained cadence/runtime, forced relay or field/site acceptance result claimed.

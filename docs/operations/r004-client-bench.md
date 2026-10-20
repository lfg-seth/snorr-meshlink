# R004 CLIENT bench reflash — 2026-10-19

Later same-evening verification: fresh R004 device telemetry and SNNS packets reach G001/MQTT; the live portal normalizes **27.470970°C** at 19:15:28 Pacific. [Receipt evidence and clock limits](repeater-gateway-check-20261019.md). Calibration, sustained cadence and G002 remain unverified.

Owner connects R004 during the authorized repeater rollout and requests the same CLIENT/temperature-only configuration as [R001](r001-client-bench.md), [R002](r002-client-bench.md) and [R003](r003-client-bench.md), with no INA219 configuration. This supersedes the earlier ROUTER/enabled-power profile. Historical [preparation](r004-preparation.md) and [INA219 audit](ina219-audit.md) remain separate evidence.

Identify RAK4631 **R004 `!77fdb9f1`**, COM17, USB serial `820C9B4F0C2D7675`, already on `2.7.26.0b65f2e`. Save fresh complete owner/local/module/channel/security backup under ignored `private/bench/R004-client-20261019/before.json`. Match the same USB serial on DFU COM18 and D: RAK4631, bootloader 0.4.3 / S140 6.1.1 / `WisBlock-RAK4631-Board`.

Reverify the complete pinned release cache with `scripts/bench/download-rak-release.py`, then reflash the verified UF2 directly. No rebuild, reset, bootloader update or key replacement. Installed **2.7.26.0b65f2e**, including AHT detection fix and passive neighbor-signal/SNNS reporting; binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`. UF2 SHA-256 `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`.

## Saved configuration and verification

- Meshtastic **CLIENT**, retaining `LOCAL_ONLY` rebroadcast mode and original radio profile (US, slot 35, 10 dBm, hop limit 3), names, channel/keys, security identity/admin keys, MQTT/network and debug settings.
- Device/battery and environment measurements enabled at **900 seconds** each. Temperature sensor may also report humidity; existing Fahrenheit display preference preserved. Previously enabled power measurements are now disabled; power display, air-quality and health measurements disabled. Battery INA address zero/unconfigured. Compiled INA219 support remains in this release; the power measurement module is disabled. Physical sensor presence/removal is not established by configuration readback.
- NeighborInfo enabled with transmission over LoRa, standard interval **21,600 seconds**; companion cadence remains firmware-controlled.

Independent exact profile/identity/channel comparisons pass before and after explicit clock synchronization/reboot. Account for the firmware API's role-dependent sleep default (CLIENT 300 seconds, formerly ROUTER 86,400), as documented for R001. Private `verified.json` retains final evidence.

A local environment request and 45-second observation yield no temperature response and no local environment metrics. Sensor operation on this update remains **unverified**. API device values carry uptime 3,065 seconds and are excluded as cached pre-reboot evidence. Private `sensor.json` retains the result. Next sensor check: confirm fitted sensor/wiring/detection and obtain a fresh environment report.

RF/MQTT and portal delivery, sustained cadence, utilization reduction, calibration, runtime, forced relay and field coverage remain unverified. Live portal metadata and other radios are unchanged in this run. Disabling power telemetry does not resolve the historical current discrepancy.

Tracking: [Reflash R004 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/29). Next board must be independently identified/backed up before applying the authorized rollout profile.

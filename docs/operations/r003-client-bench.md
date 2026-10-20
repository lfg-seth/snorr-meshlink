# R003 CLIENT bench reflash — 2026-10-19

Owner connects R003 during the authorized repeater rollout. Apply the same CLIENT/temperature-only configuration as [R001](r001-client-bench.md) and [R002](r002-client-bench.md), with no INA219 configuration. This supersedes the earlier ROUTER profile; historical [AHT build evidence](r003-aht-build.md) remains separate.

Identify RAK4631 **R003 `!05237743`**, COM14, USB serial `397EBE4F36E1F126`, initially `2.7.26.cc5907b`. Save fresh complete owner/local/module/channel/security backup under ignored `private/bench/R003-client-20261019/before.json`. Match the same USB serial on DFU COM16 and D: RAK4631, bootloader 0.4.3 / S140 6.1.1 / `WisBlock-RAK4631-Board`.

Reverify the complete pinned release cache with `scripts/bench/download-rak-release.py`, then flash the verified UF2 directly. No rebuild, reset, bootloader update or key replacement. Installed **2.7.26.0b65f2e**, retaining AHT detection fix and adding passive neighbor-signal/SNNS reporting; binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`. UF2 SHA-256 `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`.

## Saved configuration and verification

- Meshtastic **CLIENT**, retaining `LOCAL_ONLY` rebroadcast mode and original radio profile (US, slot 35, 10 dBm, hop limit 3), names, channel/keys, security identity/admin keys, MQTT/network and debug settings.
- Device/battery and environment measurements enabled at **900 seconds** each; temperature sensor may also report humidity. Power measurements/display, air-quality and health measurements disabled. Battery INA address remains zero/unconfigured. Compiled INA219 support remains in this release; no power sensing is enabled.
- NeighborInfo enabled with transmission over LoRa, standard interval **21,600 seconds**; companion cadence remains firmware-controlled.

Independent exact profile/identity/channel comparisons pass before and after explicit clock synchronization/reboot. Account for the firmware API's role-dependent sleep default (CLIENT 300 seconds, formerly ROUTER 86,400), as documented for R001. Private `verified.json` retains final evidence.

A local environment request followed by a 45-second observation yields no temperature response and no local environment metrics. Sensor operation on this update remains **unverified**; historical R003 temperature success is not fresh evidence. API device metrics carry uptime 167,566 seconds and are excluded as cached pre-reboot values. Private `sensor.json` preserves this result. Next sensor check: confirm fitted sensor/wiring/detection and obtain a fresh environment report.

RF/MQTT and portal delivery, sustained cadence, utilization reduction, calibration, runtime, forced relay and field coverage remain unverified. Live portal metadata and other radios are unchanged in this run.

Tracking: [Reflash R003 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/28). Next board must be independently identified/backed up before applying the authorized rollout profile.

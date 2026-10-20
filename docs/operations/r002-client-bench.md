# R002 CLIENT bench reflash — 2026-10-19

Owner connects R002 and explicitly requests the same CLIENT/temperature-only configuration as [R001](r001-client-bench.md), with no INA219 configuration. This supersedes R002's earlier ROUTER/no-external-sensor profile for this bench run; a requested temperature configuration does not establish actual sensor operation.

Identify RAK4631 **R002 `!b456f760`**, COM9, USB serial `BADB1E79E9739FC4`, already on `2.7.26.0b65f2e`. Save fresh complete owner/local/module/channel/security backup under ignored `private/bench/R002-client-20261019/before.json`. Match the same USB serial on DFU COM11 and F: RAK4631, bootloader 0.4.3 / S140 6.1.1 / `WisBlock-RAK4631-Board`.

Reverify the complete pinned release cache with `scripts/bench/download-rak-release.py`, then reflash the verified UF2 directly as requested. No rebuild, reset, bootloader update or key replacement. Installed **2.7.26.0b65f2e**, including passive neighbor-signal/SNNS reporting; binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`. UF2 SHA-256 `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`.

## Saved configuration and verification

- Meshtastic **CLIENT**, retaining `LOCAL_ONLY` rebroadcast mode and original radio profile (US, slot 35, 10 dBm, hop limit 3), names, channel/keys, security identity/admin keys, MQTT/network and debug settings.
- Device/battery and environment measurements enabled at **900 seconds** each; temperature sensor may also report humidity. Power measurements/display, air-quality and health measurements disabled. Battery INA address remains zero/unconfigured. Compiled INA219 support remains present in this release; no power sensing is enabled.
- NeighborInfo enabled with transmission over LoRa, standard interval **21,600 seconds**; companion cadence remains firmware-controlled.

Independent exact profile/identity/channel comparisons pass before and after explicit clock synchronization/reboot. Account for the firmware API's role-dependent sleep default (CLIENT 300 seconds, formerly ROUTER 86,400), as documented for R001. Private `verified.json` retains final evidence.

A local environment request followed by 45 seconds of observation yields no temperature response and no local environment metrics. Sensor operation remains **unverified**. API device metrics show 4.069 V, battery level 91 and uptime 65 seconds; these local values are not RF/MQTT/portal delivery evidence. Private `sensor.json` records the result. Next sensor check: confirm fitted temperature sensor/wiring/detection and obtain a fresh environment report.

Fresh RF/MQTT and portal evidence is separate from saved configuration. Live portal metadata is unchanged. Sustained cadence, utilization reduction, calibration, runtime, forced relay and field coverage are unverified. Other radios are unchanged in this run.

Tracking: [Reflash R002 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/27). Next board must be independently identified/backed up before applying the authorized rollout profile.

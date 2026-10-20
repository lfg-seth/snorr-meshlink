# R005 CLIENT bench reflash — 2026-10-19

Owner connects R005 during the authorized repeater rollout and requests the same CLIENT/temperature-only profile as R001–R004, with no INA219 configuration. Replace the historical [one-off dummy-load image](r005-preparation.md) with the ordinary pinned RAK release. Its GPIO31 HIGH startup override is removed; this does not measure physical load state/current or establish removal of the fitted circuit.

Identify RAK4631 **R005 `!f95b5501`**, COM19, USB serial `E93C5FF0F97DD76B`, initially `2.7.26.8dd4dac`. Save fresh complete owner/local/module/channel/security backup under ignored `private/bench/R005-client-20261019/before.json`. Match the same USB serial on DFU COM20 and E: RAK4631, bootloader 0.4.3 / S140 6.1.1 / `WisBlock-RAK4631-Board`.

Reverify the complete pinned release cache with `scripts/bench/download-rak-release.py`, then flash the verified UF2 directly. No rebuild, reset, bootloader update or key replacement. Installed **2.7.26.0b65f2e**, including AHT detection fix and passive neighbor-signal/SNNS reporting; binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`. UF2 SHA-256 `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`.

## Saved configuration and verification

- Meshtastic **CLIENT**, retaining `LOCAL_ONLY` rebroadcast mode and original radio profile (US, slot 35, 10 dBm, hop limit 3), names, channel/keys, security identity/admin keys, MQTT/network and debug settings.
- Device/battery and environment measurements enabled at **900 seconds** each; temperature sensor may also report humidity. Existing Fahrenheit preference preserved. Previously enabled power measurements now disabled, with power display, air-quality and health measurements disabled. Battery INA address zero/unconfigured. The ordinary release retains compiled INA219 support; the power measurement module is disabled.
- NeighborInfo enabled with transmission over LoRa, standard interval **21,600 seconds**; companion cadence remains firmware-controlled.

Independent exact profile/identity/channel comparisons pass before and after explicit clock synchronization/reboot. Account for the firmware API's role-dependent sleep default (CLIENT 300 seconds, formerly ROUTER 86,400), as documented for [R001](r001-client-bench.md). Private `verified.json` retains final evidence.

A local environment request plus 45 seconds of observation yields no temperature response and no local environment metrics. Sensor operation remains **unverified**. API device values carry uptime 1,453,310 seconds and are excluded as cached pre-reboot evidence. Private `sensor.json` retains the result. Next sensor check: confirm fitted temperature sensor/wiring/detection and obtain a fresh environment report.

RF/MQTT and portal delivery, sustained cadence, utilization reduction, calibration, runtime, forced relay and field coverage remain unverified. Other radios/live portal metadata unchanged. Historical load/current investigations remain unresolved; source replacement is separate from physical verification.

Tracking: [Reflash R005 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/30). R001–R005 now have the same release/role/measurement policy, preserving their individual identities and other settings.

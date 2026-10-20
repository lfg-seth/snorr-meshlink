# R001 CLIENT bench reflash — 2026-10-19

Owner requests reflashing repeaters with Meshtastic **CLIENT** role for bench testing and temperature sensors only, with no INA219 configuration. This run handles only connected R001; other radios retain their previous state until individually identified and updated. This supersedes the handoff's preserved ROUTER instruction for this requested bench rollout.

R001 identifies as RAK4631 `!a65601b3`, COM8, USB serial `AA474A4710B85C2C`, initially stock `2.7.26.54e0d8d`. Fresh complete local/module/channel/owner/security backup is ignored at `private/bench/R001-client-20261019/before.json`. Match the same USB serial on DFU COM10 and D: RAK4631, bootloader 0.4.3 / S140 6.1.1 / `WisBlock-RAK4631-Board`.

Verify all pinned cached release assets with `scripts/bench/download-rak-release.py`; copy the verified UF2 directly, without rebuilding, factory reset, bootloader update or key replacement. Installed **2.7.26.0b65f2e**, binary source `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`; UF2 SHA-256 `59fff11dad4b8c83bfe1fd1b8a13438bf0147dd734db6e2821585b9710791f47`.

## Final saved profile

- `device.role=CLIENT`; retain `rebroadcast_mode=LOCAL_ONLY`, existing names, channel records/keys, security identity/admin keys, US radio configuration, slot 35, 10 dBm, hop limit 3, and other original local/module fields.
- Device/battery and environment measurements enabled, both at **900 seconds**. Temperature sensor may also report humidity. Power measurements/display, air quality and health measurements disabled; no battery INA address configured.
- NeighborInfo enabled, transmit-over-LoRa enabled, standard interval 21,600 seconds. Companion cadence remains firmware-controlled.
- Debug API remains off; MQTT/network settings preserved.

Independent full readback passes after explicit clock synchronization/reboot: device identity, hardware ID, owner fields, channels and security match the fresh backup; only intended role/telemetry/neighbor changes and the role-dependent API sleep value differ. `PhoneAPI.cpp` reports `default_ls_secs` rather than the stored value: ROUTER returns 86,400 seconds, CLIENT returns 300 seconds. An attempted restoration therefore still reads 300; it is not evidence of lost power settings. Private `verified.json` records final readback.

A post-reboot local environment request followed by a 45-second observation produces no environment response and no local temperature metrics. Sensor operation remains **unverified**, despite the saved enable flag. The cached device metrics returned by the API carry uptime 170,266 seconds and are not counted as fresh post-reboot battery or utilization evidence. Private `sensor.json` preserves this result. Check fitted sensor/wiring/detection and obtain a fresh temperature report before accepting sensor operation.

Gateway RF/MQTT receipt, live portal metadata/ingestion, sensor calibration, sustained cadence, utilization improvement, battery runtime and field coverage remain unverified. Firmware includes INA219 support, but power telemetry is disabled; this is a configuration change, not removal of its compiled driver. Historical INA219 investigations remain separate.

Tracking: [Reflash R001 for CLIENT bench operation with temperature telemetry only](https://github.com/lfg-seth/snorr-meshlink/issues/26). Next: repeat private backup/identity checks for the next physically connected repeater before flashing; use this CLIENT/temperature-only profile and account for per-board exceptions such as R005's previous dummy-load image.

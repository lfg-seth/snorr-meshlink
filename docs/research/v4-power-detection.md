# Heltec V4 power detection for SOS

Checked 2026-10-12 against primary documentation and moving upstream source. Preliminary source inspection, not a pinned release audit or hardware test; owned V4 revision remains unknown.

## Findings

- The regular V4 [variant definition](https://github.com/meshtastic/firmware/blob/develop/variants/esp32s3/heltec_v4/variant.h) defines battery ADC input GPIO1 and measurement control GPIO37. Battery status can be estimated from voltage; accuracy requires calibration and load/charging tests.
- Neither that variant nor its local [OLED build settings](https://github.com/meshtastic/firmware/blob/develop/variants/esp32s3/heltec_v4/platformio.ini) explicitly defines a dedicated external-power/charging sense input. This is not an exhaustive audit of inherited settings or other V4 revisions.
- Upstream [Power.cpp](https://github.com/meshtastic/firmware/blob/develop/src/Power.cpp) supports external-power inputs and a voltage-based fallback. Its USB-host detection option observes host traffic, which does not detect a wall charger or ordinary power bank. Battery voltage alone does not establish external power with a depleted battery. Do not treat a charging icon as verified source detection.
- Heltec documents [revision differences](https://heltec.org/project/wifi-lora-32-v4/) and publishes a [V4.2 datasheet/schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf). Inspect the actual board and matching schematic before choosing a firmware signal or added sensing circuit. No hardware modification or purchase selected.

## Requirement and verification gate

Owner wants battery status on the SOS screen, maximum configured SOS effort on external power even with a low battery, and reduced reminder/position frequency at low battery only when battery-powered. Maximum effort must still respect the network airtime budget.

Test low/medium/full battery on battery alone, a powered computer USB port, a wall charger, and a power bank. Include plug/unplug transitions, full battery without active charging, an unpowered cable, and reboot. Solar input is a separate case if later included; connected input alone does not prove sufficient power.

Until a dependable signal is established, expose source as unknown rather than claiming plugged-in detection. Unknown-source policy, battery thresholds, cadence tiers, and transition hysteresis remain to agree. A manual source-mode override is a possible fallback, not a selected design. No measurements recorded.

## Pinned follow-up — battery trend heuristic

2026-10-12: Owner directed deferring this investigation for now and suggested inferring charging from the sustained direction of battery level over a configurable observation window, perhaps 1 minute. This is a candidate heuristic, not an agreed detection method or validated duration.

Evaluate sampled battery voltage/estimated level, a minimum meaningful change, smoothing, and hysteresis before choosing a trend rule. Label the result as inferred charging, separate from confirmed external power. A flat trend must remain ambiguous: this proposal does not establish that full-battery external power or external power under load can be identified. Verify behavior experimentally rather than treating a trend as proof.

When resumed, compare the trend with known power-source states across load changes and plug/unplug transitions; retain unknown state when evidence is insufficient. Do not delay the SOS workflow interview for this investigation. No code, thresholds, samples, or hardware changes made.

2026-10-12 — Related display option: owner requested a configurable option to keep the display always on while charging is detected/inferred. Store alongside the charging heuristic for later implementation; enabling/disabling this option, the detection confidence, and behavior when charging ends or becomes unknown remain to specify. No default selected or firmware behavior changed.

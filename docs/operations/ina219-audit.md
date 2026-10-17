# INA219 current audit — 2026-10-16

Owner reports R004 displaying roughly one amp despite a battery-only desk-multimeter measurement of **8–16 mA**, and confirms the sensors' resistors are marked **R100**. R004 has the ordinary release, without R005's dummy-load target. The one-amp discrepancy remains unresolved; the channel fix below does not explain its magnitude.

Owner follow-up confirms the current meter is **in series between the battery and INA219** and the reading is **8–16 mA**; `8016 mA` was a typo. No usable physical shunt-voltage reading is available: the owner reports unstable millivolt readings with open leads. This alone does not establish a meter fault or validate its low-voltage accuracy. The series-current result remains owner-reported evidence, without a simultaneous raw INA219 register capture under the same battery-only conditions.

## Calibration and configuration

- Both RAK targets inherit Adafruit INA219 **1.2.3**. Its `begin()` selects `setCalibration_32V_2A()`: **0.1 Ω**, calibration register **4096 / 0x1000**, current divider **10**, or **0.1 mA per current-register count**. Config register is **0x399f**, including ±320 mV shunt range. These are compatible with R100. The 2 A preset is a measurement range, not an imposed load or a minimum reading. [Pinned library implementation](https://github.com/adafruit/Adafruit_INA219/blob/1.2.3/Adafruit_INA219.cpp).
- `INA219_MULTIPLIER` defaults to **1.0**. Neither RAK target overrides it. The separate Raspberry Pi Pico UPS target defines 10 for its 0.01 Ω shunt; that setting does not apply to R004/R005. `ADC_MULTIPLIER` is the separate battery-voltage divider compensation, not INA219 current calibration.
- Identity-checked COM17 readback confirms R004 still runs **2.7.26.0b65f2e**, with device/environment/power telemetry enabled at **900 seconds**, debug API off, and `device_battery_ina_address` unset (protobuf default zero). The device battery-voltage path does not select INA219. There is no saved shunt-resistance/current-scale setting in this path.
- The MQTT adapter passes signed floats in milliamps through unchanged. Power and environment reports are separate observations; the frontend lists each without summing, taking absolute values, or multiplying by 1,000. Twelve adapter checks pass, including encrypted-wire current/channel preservation. No portal or historical-reading rewrite was applied.

## Observed readings

Read-only live database history confirms the owner's high-current symptom. Times below are **October 16, Pacific**; they are sample times unless marked as receipt-only.

| Device/time | Report | Bus voltage | Signed reported current |
| --- | --- | --- | --- |
| R004, 20:57:36 | Power channel 3 | 4.020 V | +1,030.0 mA |
| R004, 20:58:21 | Environment | 4.040 V | +939.4 mA |
| R004, 21:12:36 | Power channel 3 | 4.044 V | +1,071.1 mA |
| R004, 21:13:21 | Environment | 4.052 V | +1,002.2 mA |
| R004, USB audit, local uptime 69 | Environment | 4.192 V | −5.9 mA |
| R004, 21:17:22 | Environment | 4.140 V | −5.8 mA |
| R004, 21:17:37 | Power channel 3, portal | 4.188 V | −5.8 mA |
| R005, 20:45:55 receipt-only | Environment | 3.812 V | +3,200.0 mA |
| R005, 20:46:09 receipt-only | Power channel 3 | 3.840 V | +3,195.6 mA |

R004's paired environment/power values agree in magnitude before and after USB connection. This rules out an inflation confined to the power union or portal channel display. The USB-state change also prevents treating the fresh −5.8 mA as a simultaneous validation of the owner's battery-only 8–16 mA measurement. R005's near-full-scale reports are evidence to investigate, not verified multiamp consumption.

Private captures: `private/bench/R004-ina219-audit.json` (identity, relevant configs and local readings), `private/bench/INA219-history.json` (read-only sanitized power-history extraction). No firmware, saved configuration, debug setting or explicit reboot changed on R004 during this audit. Serial access is closed afterward.

## Confirmed source defects and fix

`INA219Sensor::getMetrics()` always wrote `environment_metrics`, including when its caller selected the `power_metrics` union. The generated C layout placed those fields over **power channel 3**, retaining their float values. A portable harness compiling the actual sensor source, pinned Adafruit source and generated telemetry layout reproduced the failure at `has_ch1_current`.

The source fix writes **power channel 1** for a PowerMetrics request, retains legacy environment fields for EnvironmentMetrics, and rejects other variants. It also applies the existing current multiplier consistently to `getCurrentMa()`; that inconsistency affected non-default multiplier targets, not these RAKs. A further failing transport test established that the old sensor reported success even after a failed I2C read; the fix checks each read's status before publishing fields. No live I2C failure was captured, so this is not established as the cause of the high-current samples. No arbitrary current correction factor is added.

The harness emulates only I2C registers and Meshtastic runtime services, checking the actual library conversion for zero, ±8, ±16, ±50 and ±1,000 mA with R100, both telemetry formats and integer accessors. A second build checks the existing 10× multiplier convention. Failed voltage/current reads in each telemetry format must leave measurement fields absent. It does not measure real sensor accuracy, noise, I2C integrity or wiring. Run under Linux/WSL:

```sh
python3 firmware/test/test_ina219_sensor/run.py
```

Firmware source commit [`d929b8009`](https://github.com/lfg-seth/firmware/commit/d929b8009) is published on `snorr/rak-survey`. The ordinary published prerelease and R004/R005's flashed images remain unchanged. Future flashing must distinguish the corrected source from those old binaries. Historical channel 3 readings retain their original labels.

An isolated ordinary `rak4631` target build passes: **759,336 bytes flash / 105,252 bytes static RAM**. It uses base `8dd4dacef` plus the exact final INA219 source, excluding concurrent sniffer work; source SHA256 is `50e53f12df663f687b216a06e1b860a965eb366af84e96bd39f0b503d96b7fa7`. Log and artifacts remain under ignored `private/bench/INA219-rak-build.log` and `private/bench/ina219-source/`. Its inherited `8dd4dac` filename is **not a new release identity** and must not be confused with the earlier R005 load binary. It is not published or flashed. Trunk is unavailable; pinned clang-format 16.0.3 with the repository's `.trunk/configs/.clang-format`, Black 26.5.1 and whitespace checks pass.

## Next discriminating measurement

While the battery-only discrepancy is present, measure **DC millivolts directly across R100** and compare the simultaneous sensor report. For 0.1 Ω, 8–16 mA produces **0.8–1.6 mV**; 1 A produces **100 mV**. This follows the shunt-voltage/current relationship in the [TI INA219 datasheet](https://www.ti.com/lit/ds/symlink/ina219.pdf).

If the meter sees roughly 1 mV while the sensor reports roughly 1 A, inspect the chip's actual shunt/current/config/calibration register values and input connections; the present firmware does not expose those registers through its normal administration API. If the physical drop is roughly 100 mV, reconcile the meter's series-current path and all connected supply/load paths. Do not assume charging, calibration or R005's load explains R004's discrepancy without that evidence. A diagnostic firmware flash needs explicit owner scope; no flash is performed here.

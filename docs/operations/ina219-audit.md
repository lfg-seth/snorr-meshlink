# INA219 current audit — 2026-10-16

## R004 reinvestigation — 2026-10-21

Owner reconnects R004, confirms an installed **R100** with INA219 inline
between battery and board, and explicitly authorizes diagnostic flashing.
This activates [Investigate INA219 current discrepancy with simultaneous
same-path measurements](https://github.com/lfg-seth/snorr-meshlink/issues/4).
VIN+/VIN− orientation, common-ground wiring, other supply/load branches and
simultaneous physical measurements still await confirmation.

Identify RAK4631 R004 `!77fdb9f1`, COM17, USB serial
`820C9B4F0C2D7675`, initially on **2.7.26.0b65f2e**. Full owner/security,
local/module configuration and eight channels are backed up privately under
`private/bench/R004-ina219-20261021/`. Native nRF USB requires DTR asserted
for this API connection; RTS stays inactive. With both inactive the initial
read timed out; the successful baseline retains uptime about 151,988 seconds.

### Reproduction and first probe

The private feedback command is
`.venv/Scripts/python.exe private/bench/r004-ina219-20261021.py baseline`.
It requests local environment telemetry and fails for a current magnitude
at or above 1,000 mA; absence of a fresh current is inconclusive. It reproduced
**−1,152.6 mA / 4.244 V** before any flash. The threshold catches the original
one-amp symptom, not all inaccurate subamp values. Repeat observations with
the same saved settings give **+263.8 mA / 4.244 V**, then **+929.9 mA /
4.048 V**. No deterministic fixed scaling error is established. Console
reports USB power and charging; these flags are not measured charge current.
RAK specifies **350 mA charging current** for the
[RAK19003](https://docs.rakwireless.com/product-categories/wisblock/rak19003/datasheet/#battery-connector).

Ranked hypotheses before probing: an erroneous/large physical shunt input;
wrong live calibration/configuration; corrupt or inconsistent I2C/device
register data; a later conversion/telemetry error. No arbitrary current
correction is applied.

First diagnostic source
[`4ad67eb35`](https://github.com/lfg-seth/firmware/commit/4ad67eb35414aa4f7d6064fe3888ce2bd9857503),
target `rak4631-ina219-debug`, builds with **760,136 bytes flash / 105,252
bytes static RAM**. Flashed UF2: **1,520,640 bytes**, SHA-256
`152579f6499945943a80a1e5fe0fde98bb565c67dbab79c6241bee7786a66ac2`.
The build started before the source commit: its initial artifact basename
contains `473a9ed`, but the compilation/ELF and independent device readback
confirm **2.7.26.4ad67eb**. The preserved copy is renamed to its actual
runtime version; `image.json` records both names. It is a diagnostic image,
not the ordinary published prerelease. Matched DFU COM18 / RAK4631 UF2
bootloader 0.4.3 / S140 6.1.1; no factory reset or bootloader update.
Independent full owner/local/module/channel equality passes after flash.

The first diagnostic report remains wrong: **−1,437.4 mA / 4.028 V**.
Captured address **0x40**, config **0x399F**, calibration **0x1000** and
overflow **0** support the expected R100 preset. Selected raw snapshots:

| Probe | Shunt register / converted drop | Current register / converted current | Bus |
| --- | --- | --- | --- |
| Before normal read | `E704` / −63.960 mV | `FF93` / −10.9 mA | 4.088 V |
| After normal read | `E7CF` / −61.930 mV | `D3CF` / −1,131.3 mA | 4.088 V |

These are sequential reads while conversion continues, not an atomic
snapshot. With calibration 4096 the current and shunt register counts should
agree for the same completed conversion; rapidly changing inputs could
explain differences between separate conversions. Raw shunt readings alone
already imply hundreds of milliamps with R100, so a portal-only inflation
cannot explain the entire symptom. Actual shunt voltage and current accuracy
remain unverified. [TI register/conversion specification](https://www.ti.com/lit/ds/symlink/ina219.pdf).

The existing actual-source R100 conversion/transport harness passes in WSL
for multipliers 1 and 10, including signed values, telemetry variants and
failed reads. Pinned clang-format 16.0.3 and whitespace checks pass; Trunk is
unavailable. These are source checks, not hardware accuracy tests.

### Held-conversion follow-up

Source [`09d8a9dbf`](https://github.com/lfg-seth/firmware/commit/09d8a9dbf)
adds one triggered shunt-plus-bus conversion, waits 3 ms at the verified
12-bit preset, reads the held registers three times and restores the original
sensor configuration before normal telemetry reads. The probe changes no
saved radio settings or calibration factor. [Scoped firmware review](https://github.com/lfg-seth/firmware/pull/2).
Build passes with **760,440 bytes flash / 105,252 bytes static RAM**. UF2
**1,521,152 bytes**, SHA-256
`640c6f86b6ce2020d4db900f07bc5b4880780266df90326a5e26a76bfb149813`.
Flash and two independent API profile comparisons pass on **2.7.26.09d8a9d**.
Full owner/identity, local/module settings and channels match the original
backup exactly. CLIENT, device/environment 900 seconds, disabled power
telemetry and unset battery INA address persist. No other board is changed.

All **six held conversions × three reads** retain identical shunt, current,
power, calibration and bus-voltage counts. Only the expected conversion-ready
bit clears after the power-register read. Every current word exactly equals
the signed shunt word at calibration 4096. Triggered config **0x399B** is
confirmed, and continuous **0x399F** is restored before ordinary readings.
No I2C/config-write error or math overflow is captured.

| Local uptime | Held shunt word / voltage | Current word / R100 current | Bus voltage |
| --- | --- | --- | --- |
| 17 s | `F057` / −40.09 mV | `F057` / −400.9 mA | 4.248 V |
| 66 s | `3058` / +123.76 mV | `3058` / +1,237.6 mA | 4.228 V |
| 78 s | `CACB` / −136.21 mV | `CACB` / −1,362.1 mA | 4.160 V |
| 90 s | `C54F` / −150.25 mV | `C54F` / −1,502.5 mA | 4.204 V |
| 91 s | `10F7` / +43.43 mV | `10F7` / +434.3 mA | 4.236 V |
| 102 s | `ED8A` / −47.26 mV | `ED8A` / −472.6 mA | 4.076 V |

These are the chip's reported voltages and implied currents, not independent
physical measurements. The clock is unknown after diagnostic reboot; small
telemetry time fields are not treated as Unix measurement times. The repeat
feedback command, now matching replies to newly sent request IDs to exclude
queued/cached packets, is
`.venv/Scripts/python.exe private/bench/r004-ina219-20261021.py single-repeat`.
Four fresh matched replies give **+514.2, −1,293.0, −437.9 and −1,436.2 mA**,
so the original symptom remains red. Held values above are distinct probe
conversions, not the later ordinary telemetry conversion. The 91-second probe
comes from the unchanged local phone-reporting path, not a fifth request or
new LoRa interval. Private `single.held.json` and
`single-repeat.held.json` preserve the mechanical repeat/math checks.

**Narrowed finding:** the large values originate in shunt-voltage conversions
inside the sensor/device path. Correct live calibration, repeatable held
register reads and exact current multiplication argue against a firmware
current-scale/unit error or observed unstable digital register reads as the
cause. Varying physical differential input, sense/ground/power wiring,
interference and a faulty sensor/module remain candidates; this evidence
does not distinguish them or establish actual amp-scale branch current.
The firmware change is an opt-in diagnostic, not an accuracy fix. It retains
tagged probes for continued collection; ordinary targets exclude them.

### Next discriminating check and handoff

Keep the present connection unchanged and measure DC millivolts directly
across the two metal ends of R100, noting stability and polarity. **350 mA
through 0.1 ohm is 35 mV**. The held sensor claims as much as about ±150 mV;
compare actual shunt voltage and a fresh probe under the same supply/load
conditions. A meter may average brief interference/transients; a stable small
DC result would call for sense wiring/module inspection and, if available,
waveform inspection rather than a scale correction. Confirm VIN+/VIN−,
common ground, VCC and all attached supply/load paths. A known-zero
differential-input test or comparison with another existing sensor can then
separate wiring from sensor faults under an explicitly described bench setup.

Owner proposes disconnecting the battery while USB remains connected as a
zero-current test. With an intact installed R100, the inputs remain connected
through the shunt and battery-branch current should be near zero if no other
branch remains attached there. A subsequent transition trace captures three
fresh matched replies **−11.2, −11.1, −11.3 mA**, with four held conversions
at **−1.12 to −1.13 mV / −11.2 to −11.3 mA** (uptime 298–331 s). Every held
triple remains stable and mathematically consistent. **Battery removal has
not yet been confirmed by the owner**, so this is not accepted as a measured
zero-current result or proof that unplugging the battery caused the change.
Capture and assessment remain under private `transition.*` files. The next
zero-state capture uses a conservative ±5 mA diagnostic threshold, not a
claimed hardware calibration specification.

Owner has been asked for battery-disconnection state, physical shunt reading
and wiring confirmation; these remain pending. Serial is closed, diagnostic image
**2.7.26.09d8a9d** is retained for the comparison, and the ordinary pinned
release remains the recovery image. No RF/MQTT/portal accuracy, charging
current, battery-only accuracy, endurance or field acceptance is claimed.
Issue #4 remains open for physical verification; no retained session claim.
GitHub Project reconciliation is pending an authenticated GitHub CLI: the
documented helper reports that it is unavailable on this desktop.

### Historical October 16 evidence

Owner reports removing an R100 shunt and measuring **0.45 Ω out of circuit**, then confirms **0.16 Ω with the probes shorted on the same range**. Subtraction gives an estimated **0.29 Ω**, not a calibrated resistance: differing contact resistance and meter resolution/accuracy remain unquantified. Exact sensor allocation and reinstallation are unconfirmed. Two-wire lead/contact resistance requires compensation; a four-wire measurement would better establish the actual component value. [Manufacturer guidance](https://www.keysight.com/sg/en/use-cases/make-resistance-measurements.html). If the true shunt were 0.29 Ω, the firmware's 0.1 Ω calibration would report **2.9×** current: 8–16 mA would appear as **23.2–46.4 mA**, still far below the recorded roughly one amp. Do not recalibrate from this approximate measurement alone. The affected sensor's shunt was removed; subsequent assembled readings require confirmation of its physical state.

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

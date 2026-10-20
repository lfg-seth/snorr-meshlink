# R005 dummy-load preparation — 2026-10-16

Superseded hardware profile on 2026-10-19: owner requests the same ordinary release/CLIENT/temperature-only configuration as the other bench repeaters. [R005 reflash evidence](r005-client-bench.md) replaces this one-off image and removes the GPIO31 HIGH startup override. Preserve the following as historical development/measurement evidence, not the current flashed state.

Owner requests a one-off build of the latest project RAK source, with the
dummy load on during normal board operation, then flashing the connected
RAK as R005 and registering it at R001's saved planned location. Owner
reports RAK19007, INA219, temperature sensor, and an AIN1-controlled 2N2222
with a **2 kΩ base resistor**. Load resistance, supply path, transistor
temperature and actual current are unmeasured.

## Source and selection

Published firmware source `8dd4dacef` on `snorr/rak-survey` adds the explicit
`rak4631-r005-load` target atop the latest project source `8fe47325e`.
This retains the existing AHT fix, INA219 driver and passive neighbor
reports. It is a separate development build, not the cached prerelease.
Ordinary `rak4631` builds do not enable the load.

`initVariant()` preloads HIGH then configures `PIN_A1` as OUTPUT. RAK19007
AIN1 maps to RAK4631 **P0.31 / Arduino GPIO31**, not Nordic analog channel
AIN1. Battery ADC remains P0.05. The target excludes Dropzone, which would
otherwise configure A1 as an input. The inherited target also excludes
RemoteHardware. No PWM, timer or runtime load-control interface is added.
Reset, bootloader, shutdown and power loss are outside the normal-operation
HIGH guarantee. [Firmware behavior](../../firmware/SNORR_R005_LOAD.md),
[RAK pin reference](https://docs.rakwireless.com/product-categories/wisblock/rak4631/datasheet/).

Independent initial API identification: RAK4631 `!f95b5501`, hardware ID
`6bd77df9f05f3ce901555bf96d5ed7fc`, USB serial `E93C5FF0F97DD76B`, normal
COM19, former short name MR02, firmware `2.7.17.36133d29d`, existing US
region. Complete initial configuration/channel/security snapshot retained
privately as `private/bench/COM19-before-rak.json`.

## Verification

Committed-source target build passes in 198.41 seconds: flash 759,288 /
815,104 bytes (93.2%), static RAM 105,252 / 248,832 bytes (42.3%). Linked
disassembly independently confirms `digitalWrite(31, HIGH)`,
`pinMode(31, OUTPUT)` and startup invocation of `initVariant()`.

| Artifact | SHA-256 |
| --- | --- |
| UF2, 1,518,592 bytes | `c66ca721eeefcc3251cfc0ca73534232e742eb43cac6e9d13132ca339fea9822` |
| OTA ZIP, 760,306 bytes | `01433c2e95560acff02947303e807dfcf37a1575d0d44031018c8718c70448bf` |

Match COM20 bootloader USB serial to COM19 and E: board ID
`WisBlock-RAK4631-Board` (bootloader 0.4.3, S140 6.1.1). Copy the verified
UF2, then independently read `2.7.26.8dd4dac` on COM19. No factory reset,
bootloader update, key replacement or other-board change.

Name `SNORR Pilot Repeater R005` / `R005`; ROUTER, LOCAL_ONLY, node-info
10,800 seconds, existing US region retained, saved pilot LONG_FAST / slot
35 / hop 3 / 10 dBm profile and exact private primary channel/key, no
channel uplink/downlink. Other channels disabled. No power saving, GPS
disabled and old fixed position removed, MQTT/Wi-Fi disabled. Device,
environment and power telemetry enabled at **900 seconds**; NeighborInfo
enabled with LoRa transmission and standard 21,600-second interval.
Independent readback of intended profile and original private/public/admin
keys passes before and after explicit reboot. Final temporary debug API
logging is off. An asynchronous serial-close race after the reboot request
raises `AttributeError`; subsequent independent readback passes.

## Sensor evidence

Startup detects two I2C devices and opens the AHT-family driver (named
`AHT10` in firmware) and INA219. Exact environmental-sensor model and
calibrated accuracy remain unverified. Local reports include:

- Before battery disconnection: environment 26.702309°C, 21.423817% RH,
  4.184 V / **−1125.6 mA**; power reports `ch3Voltage` 4.184 V and
  `ch3Current` −1121.4 mA. Another environment sample reports −1106.3 mA.
- Owner expects roughly 50 mA from the dummy load, confirms **R100** shunt
  marking, and disconnects batteries for a second reading because the
  initial path may include charging. Those initial negative readings do
  not establish dummy-load draw or calibrated charge direction.
- After the owner disconnects batteries, new local environment packet
  `1715372667`, measurement epoch `1792206505`, reports **4.180 V / −0.4 mA**,
  28.25737°C / 19.884396% RH. New power packet `2342162044`, epoch
  `1792206520`, reports **4.188 V / −0.3 mA** on the observed channel 3.
  Both measurement times follow the explicit second-read request; buffered
  pre-disconnection readings are excluded. The 1.1 A magnitude disappears,
  consistent with charging having contributed, but near-zero current does
  not demonstrate the expected 50 mA load. Load supply/path after battery
  removal remains to clarify; physical current verification stays false.
- Follow-up setup: owner installs one reportedly fully charged cell and a
  USB input meter, which reads **0.08 A**. This is an owner-observed total
  USB-input reading, not an independently measured dummy-load or battery-
  branch current. Cell capacity/chemistry and USB voltage are unspecified.
  Fresh post-request PowerMetrics at epoch `1792206853` reports **4.200 V /
  −323.1 mA** on the observed channel 3; device voltage is 4.177 V. Raw
  evidence: `private/bench/R005-full-cell-usb-meter.json`. This is distinct
  from the previous disconnected-battery reading. The USB meter and INA219
  readings do not establish a calibrated common path or isolate load draw;
  no 50 mA verification or charging-rate claim is made.

The inherited INA219 writer fills the legacy EnvironmentMetrics union even
when called by PowerTelemetry; channel 3 encoding is observed, not a verified
power-channel contract. Normalized portal current/SNNS decoding remains
unsupported. Reboot startup reports with uptime-like clocks remain separate
from reports with valid epoch clocks; final serial time is set again.

## Database and delivery

Manual [add-r005.js](../../deploy/portal/add-r005.js) accepts only verified
R005 hardware/node/version, requires exact equality with R001's private
planned coordinates, rejects conflicting identity assignments and preserves
existing records. It is outside ordinary migrations. Isolated live-copy
invalid-input rejection, registration, idempotence and preservation of every
existing device row pass. Private staging is `/root/r005-provision/`.

Live authenticated state confirms nine devices (B001/B002, G001/G002,
R001–R005), R001 site equality and fitted-sensor/load metadata. Worker mapping
and private recovery manifest include R005. Battery/antenna/solar equipment
remain unknown; warnings remain disabled pending activation. Location
sharing is not an installation or permission claim.

Fresh post-registration battery packet `1146376171` reaches G001 at
`2026-10-17T03:02:14.449Z`: measured `03:02:11Z`, 4.258 V, uptime 66,
level 101 (external-power status, not percentage). It normalizes into R005's
battery observation. Fresh packet `1541732332` at `03:02:17.489Z` carries
40-byte SNNS v1 and is archived. G002 delivery remains unverified.

Fresh environmental packet `1230127916` reaches G001 at `03:04:11.831Z`,
measurement `03:04:07Z`: 26.702309°C / 21.423817% RH and 4.184 V / −1125.6 mA.
Temperature/humidity normalize; current remains archived but unsupported
in the normalized portal. Power packet `1176379181` reaches G001 at
`03:04:25.804Z` with the −1121.4 mA channel-3 values and is archived as
unsupported. Post-reboot reports at `03:06:02Z` / `03:06:27Z` carry invalid
uptime-like measurement clocks (65 / 90), not valid epoch measurement times.

Pre-change backup `meshlink-20261017T030146Z.tar.gz`, SHA-256
`e17bf7907cec65a1f3d759182a4e8ba3f724977f99930654e41c5cf31ab5bd6a`,
passes isolated recovery. Post-registration backup
`meshlink-20261017T030508Z.tar.gz`, SHA-256
`5f17e8f1abdfa262ed1ff5798ecf46dff56b50a45b1afea95accffae3ff7097c`,
restores nine devices, 713 observations, 2,713 receipts and 1,539 archive
envelopes. Public HTTPS/certificate/protected routes, proxy/authentication
throttling and isolated database/API/history recovery pass.

Final backup after recording the R100/current-check metadata,
`meshlink-20261017T031003Z.tar.gz`, SHA-256
`a48de79bd74d06c40b748639f641c643cd1d528b18cca7950fb26a17e0a1ec2f`,
also passes public/authentication checks and isolated recovery: nine devices,
718 observations, 2,720 receipts and 1,549 archive envelopes. Authenticated
portal readback verifies R005's final metadata and preservation of the other
eight device configurations. Normalized weather records preserve unknown
measurement clocks separately from valid epoch clocks.

No sustained cadence/endurance, field coverage, installed-site acceptance,
native browser visual review or calibrated load-current result is claimed.
Private build artifacts, original profile, final identity/profile and raw
sensor evidence remain under ignored `private/bench/`.

Trunk is unavailable on this host. Exact repository clang-format 16.0.3
format/whitespace checks pass for the modified variant. No full native or
MCP hardware-suite result is claimed for this simple GPIO addition.

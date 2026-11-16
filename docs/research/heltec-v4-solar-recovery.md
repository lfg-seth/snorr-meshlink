# Heltec V4 gateway solar recovery - 2026-11-16

## Recommendation and evidence limit

First test the existing panel through the V4's **dedicated solar input**, with
a healthy battery connected and **USB disconnected**. Check the exact panel,
voltage and connector polarity first. This is a conditional bench remedy to
evaluate before adding an external charger; it is not a confirmed field fix.

The [November 15 AAR](../../records/aar/2026-11-15-mount-charleston.md)
reports G001 unstable in daylight on nominal 5 W USB-C solar and apparently
normal after dark. On November 16 the owner confirms the battery was connected,
identifies [panel ASIN B0C4L1L1BD](https://www.amazon.com/dp/B0C4L1L1BD), and
reports **2-4 V outside direct sunlight, especially dawn/dusk**. This is
owner-reported voltage; the measurement point, instrument and loaded condition
are unverified. Reset cause, battery condition and calibrated charging current
remain unverified. G001 is the screenless V4.3 `!1bbf0638`; do not generalize its
behavior to every V4 gateway or to the RAKs.

## What the official board documents establish

Heltec's [V4.3.1 datasheet, sections 3.2 and 3.4](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.3.1_Datasheet.pdf)
specifies **4.7-6 V** for USB and solar, nominally 5 V, and **3.3-4.2 V** for
the battery. Its example consumption table includes 750 mA at 27 dBm TX and
500 mA charging at 5 V; these are separate vendor conditions, not measured
G001 peaks or a combined current budget. A 5 W label does not establish
available current in weak sun. A nominal raw 6 V panel may exceed 6 V open
circuit and needs its actual maximum checked. USB and the 5 V header must not
be independently powered together. The owner's reported 2-4 V USB output is
below the board's specified input range; a connected battery does not establish
seamless operation under that out-of-range input.

The [V4.3 schematic, power block A1-A5](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/HTIT-WB32LAF_V4.3.pdf)
shows these distinct paths:

- USB feeds `VDD_5V`, the system regulators through D2, and charger input
  through D3. `VDD_5V` also drives battery-path Q1's gate.
- The dedicated `VIN_Solar` input feeds `VIN_Charge` through Q3; it does not
  directly feed the regulator input bus. With USB absent, the battery path
  remains available to run the system while solar charges it.
- U4 is **CN3165**, with R13 = 2.2 kΩ and a schematic charge setting of
  **540 mA**. This is a programmed ceiling before input/thermal limits and
  system consumption, not guaranteed net battery charging.
- CN3165 TEMP is grounded in this drawing; a thermistor function in the chip
  does not establish battery-temperature charge protection on the board.

**Engineering inference:** a weak USB source can interact with Q1's USB-driven
switching and D2 voltage drop. Q1's body diode still provides a possible battery
fallback; it is inaccurate to say weak USB completely disconnects the battery.
Moving the same compatible source to the solar input avoids this USB system
supply selection. Capture the rails and reset cause to test this explanation.

Consonance's [CN3165 manufacturer description](https://consonance-elec.com/103.html)
identifies a single-cell **linear solar charger** with automatic charge-current
adaptation to a limited source, nominal 4.2 V regulation and C/10 termination.
The V4 already has solar-aware charge control; replacing it with a basic USB
charger is not automatically an improvement. It has no separate SYS pin; the
connected system load must be considered when verifying full-charge behavior.

Heltec's [hardware update log](https://wiki.heltec.org/docs/devices/open-source-hardware/esp32-series/lora-32/wifi-lora-32-v4/hardware-update-log)
documents V4.3.1 power-routing/protection changes. Match the physical board
revision and fitted parts before applying its schematic; V4-R8 is a separate
variant. No official source checked establishes a diagnosed fleet-wide solar
brownout defect or a guaranteed firmware correction.

## When an external charger is justified

The onboard roughly 0.54 A linear charging path is a separate limitation from
daylight reset behavior. If measured harvest cannot cover gateway Wh/day and
recharge the pack, choose a suitably rated **switching charger with input
voltage/current regulation and a system power path**. Require battery
supplement during input collapse, clean restart in intermittent sun, proper
charge termination under load, and actual cell-temperature charge inhibition.

[TI BQ25895](https://www.ti.com/product/BQ25895) illustrates that class: buck
charging, input current/voltage control and battery supplement. It is an IC,
not a verified module or wiring recommendation. Its 3.25 A input ceiling also
matters for the earlier three-panel objective. Regulated USB outputs hide the
raw photovoltaic voltage, so downstream tracking cannot directly track the
cells through an unknown panel regulator. Preserve the coordinated multi-input
design requirements in [the existing solar-bank study](gateway-solar-banks.md).

A [TP4056](https://www.toppwr.com/uploadfile/file/20240130/65b892bb04a3c.pdf)
is a 1 A linear CC/CV charger with C/10 termination; its pinout has no separate
system output or solar input-regulation control. A continuous load at BAT can
interfere with termination. It does not solve source collapse or load sharing
by itself, and was already excluded for the owner's three-panel harvesting
objective. Do not parallel arbitrary charger/SYS outputs or add external
charging alongside the onboard charger without a complete reviewed circuit.

## Charging-current follow-up - 2026-11-16

Owner now reports **560 mA net into the battery** in the current setup. No
reference-meter capture, supply voltage, shunt path or simultaneous gateway
load was inspected. This is close to the schematic's nominal 540 mA setting;
component variation, measurement error or different fitted parts are possible
explanations, not diagnosed causes. It is not evidence of unused charger capacity.

The [CN3165 chip](https://consonance-elec.com/103.html) supports up to 1 A, but
the stock V4 schematic programs roughly 0.54 A. USB and solar use that same
charger. A resistor change alone is not a verified board upgrade; thermal,
connector, input and protection limits still apply.

USB can supply the gateway through the separate system path while the charger
feeds the battery. With solar only, the gateway draws from the charger/battery
bus, reducing the current left for battery charging. Thus the solar-port remedy
may improve stability while reducing net charging relative to good USB power.

| Arrangement | Nominal charger output | Illustrative net battery charge with a 160 mA load on the battery bus |
| --- | ---: | ---: |
| Stock V4, solar input only | 540 mA | 380 mA |
| TP4056 set for 1 A, gateway on its BAT bus | 1,000 mA | 840 mA |

These are current-balance examples, not forecasts. The earlier 160 mA report
has an uncertain measurement path; use a calibrated load measurement at the
same bus before relying on the subtraction. Actual charge current falls with
weak input, thermal regulation and the constant-voltage phase near full charge.

The [TP4056 datasheet](https://www.toppwr.com/uploadfile/file/20240130/65b892bb04a3c.pdf)
specifies programmable charging up to 1 A and thermal current reduction. It can
exceed 560 mA gross with adequate input and cooling; it is not rated as a
multiamp charger. At an illustrative 5 V input, 3.7 V battery and 1 A output,
linear-regulator dissipation is about **1.3 W**, before small additional losses.
It cannot maintain that current from a collapsing 2-4 V panel, and adding it
alone does not supply solar input regulation or an independent system power
path. Charger selection must address both current and weak-sun stability.

## Outstanding gates

Identify the linked panel's regulated/raw output, cold open-circuit maximum,
current-limit/restart behavior, cable loss and polarity; inspect the actual
board and battery/protection wiring. Compare battery-only, stable USB and solar
operation before changing parts. Verify transitions through shade, dawn and
dusk with uptime/reset cause, input/battery/3.3 V rails and SD/MQTT continuity.
Then measure daily energy and cold-charge protection. None of those bench or
field checks was performed by this research; no wiring, purchase, firmware or
deployment change is recorded here.

## Ready-made module options - 2026-11-16

The owner wants an assembled standalone PCB similar in convenience to a
TP4056 module, using the existing 5 V USB panels and improving on the V4's
roughly 540 mA charging ceiling. These are online candidates, not tested
assemblies or purchase selections. Amazon stock/listings could not be verified;
use the exact model numbers below when searching and compare with the primary
seller's specification.

| Module | Useful capability | Fit and limitation |
| --- | --- | --- |
| [DFRobot Solar Power Manager 5V, DFR0559](https://www.dfrobot.com/product-1712.html) | CN3165, up to **900 mA charge**, **5 V / 1 A regulated output**, 33 × 63 mm. | Closest documented match to an existing nominal 5 V source. Linear charging, so this is a modest current increase rather than a multi-panel high-power solution. |
| [Adafruit Universal USB/DC/Solar charger, product 4755](https://www.adafruit.com/product/4755) | BQ24074, **1 A default / 1.5 A selectable charge**, independent load sharing and input droop regulation. | Better system power-path behavior, but additional output interfacing is required for a Heltec. Adafruit recommends raw **6-10 V solar** and warns that raw 5 V panels droop too far. |

For **DFR0559**, the [manufacturer reference](https://wiki.dfrobot.com/dfr0559/docs/21586)
describes nominal 5 V solar input and an always-on boosted USB output. The
module's specified solar operating range is roughly 4.4/4.5-6 V; 6.5 V is a
damage boundary, not a normal design target. Its output can be evaluated as a
regulated supply to the gateway USB input, with the pack managed by the
external module. Do not leave the same pack also wired to the Heltec battery
connector in that arrangement: it creates overlapping charging paths. The
CN3165 still has a shared BAT/load node; verify termination under continuous
gateway load, restart after depletion and thermal behavior. The 1 A output
rating also needs testing against radio/SD/Wi-Fi peaks. Battery-temperature
charge cutoff is not established by the listed protection features.

For **Adafruit 4755**, a regulated 5 V USB output from the existing panel is
different from a raw 5 V photovoltaic panel, so the raw-panel warning alone
does not rule it out. Nevertheless, the panel's reported 2-4 V periods will
stop useful charging and require battery fallback. Its [LOAD/OUT range is
approximately battery voltage to 4.4 V](https://learn.adafruit.com/adafruit-bq24074-universal-usb-dc-solar-charger-breakout?view=all):
**do not connect LOAD directly to the Heltec's 4.2 V maximum BAT input**, or
expect it to meet the Heltec USB minimum of 4.7 V. A suitable 5 V boost stage
from LOAD is one integration option requiring full testing. Its optional NTC
must actually be fitted and coupled to the cells to provide temperature
monitoring; it is not supplied by default.

Two shopping filters prevent misleading upgrades:

- Small **CN3065/CN3165 mini solar modules** are the right inexpensive search
  family, but check the actual programmed current and output topology. A chip
  advertised as capable of 1 A does not mean its assembled board charges at
  1 A; [PMD Way's CN3065 solar/USB module](https://pmdway.com/products/cn3065-solar-and-usb-lithium-battery-charger)
  is specified at **500 mA charge**, so it does not improve this ceiling.
- **CN3791 switching solar modules** can offer more current, but the
  [manufacturer's MPPT divider is programmed for an input operating voltage](https://www.consonance-elec.com/en/static/upload/file/20220426/1650944536175148.pdf).
  A module sold with a 6/9/12 V tracking setpoint is not automatically suitable
  for an existing 5 V USB panel. Its charge-current marketing also does not
  establish load sharing, pack protection or cold-charge cutoff.

The practical first external-board candidate for the existing panels is
**DFR0559 for bench evaluation**. Adafruit 4755 is a useful alternative when
true load sharing justifies the extra output stage. Neither board makes a
collapsing panel charge at 2-4 V, and neither has been verified here as a
drop-in winter gateway supply.

The [planned comparison](../../records/field-results.md#2026-11-16---g001-solar-power-isolation-plan-not-run)
defines controls and proposed short bench criteria. The [inventory follow-up](../../records/inventory.md#2026-11-16---g001-usb-solar-panel-identified)
preserves the owner-supplied panel identity and voltage report separately from
seller ratings and measured results.

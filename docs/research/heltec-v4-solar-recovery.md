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
are unverified. Reset cause, battery condition and charging current remain
unmeasured. G001 is the screenless V4.3 `!1bbf0638`; do not generalize its
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

## Outstanding gates

Identify the linked panel's regulated/raw output, cold open-circuit maximum,
current-limit/restart behavior, cable loss and polarity; inspect the actual
board and battery/protection wiring. Compare battery-only, stable USB and solar
operation before changing parts. Verify transitions through shade, dawn and
dusk with uptime/reset cause, input/battery/3.3 V rails and SD/MQTT continuity.
Then measure daily energy and cold-charge protection. None of those bench or
field checks was performed by this research; no wiring, purchase, firmware or
deployment change is recorded here.

The [planned comparison](../../records/field-results.md#2026-11-16---g001-solar-power-isolation-plan-not-run)
defines controls and proposed short bench criteria. The [inventory follow-up](../../records/inventory.md#2026-11-16---g001-usb-solar-panel-identified)
preserves the owner-supplied panel identity and voltage report separately from
seller ratings and measured results.

# Gateway solar and parallel-bank options - 2026-11-01

Owner is considering larger 5 V USB solar panels and two or three groups of
four parallel 18650 cells per Heltec gateway (8-12 cells total), with one panel
per group. These are proposed allocations, not purchases or installed hardware.
Exact gateway revision, panel/module ratings, holders and cell identities remain
to confirm. No wiring or charger selection is approved by this discussion.

Directly paralleling the groups produces one 1S8P/1S12P battery: any connected
charger charges that shared battery, not its designated four cells. Multiple
chargers require compatible regulation, aggregate current limits, termination
and protection design; separate protected TP4056 modules are not a verified
plug-together solution. Shared grounds can bypass some low-side protection
arrangements; the complete circuit must preserve fault isolation.

Two conceptual alternatives:

- One protected parallel pack, panel inputs combined through appropriately
  rated reverse-blocking circuitry, and one suitably rated solar-aware charger
  with load sharing. Regulated USB panel outputs require compatibility checks;
  simple diode ORing does not guarantee equal or additive panel contributions.
- Independent protected 1S4P packs, each with its own panel and charger/load
  sharing, feeding a common load through reverse-blocking ideal-diode paths.
  Batteries are not directly paralleled. Output selection need not share load
  equally. The Heltec input/regulation and protection return paths must be
  checked against its exact board schematic before giving pin-level wiring.

TP4056 is a 4.2 V, up-to-1 A linear charger, with internal reverse-discharge
blocking and C/10 termination. It lacks a separate system power path and solar
input regulation; a continuous load on BAT can interfere with termination and
weak sunlight can collapse its input. Die thermal regulation is not battery
temperature protection. Do not add a diode between BAT and its battery as a
generic fix: that changes the voltage the charger senses.

Use compatible healthy cells matched in voltage before parallel assembly,
appropriately designed cell/branch fusing, pack over/undervoltage and short
circuit protection, and cell-temperature charge inhibition. Mount Charleston
cold conditions make low-temperature charge cutoff a design requirement.
More battery capacity does not establish solar energy sufficiency: measure
gateway Wh/day, daily harvest and recovery after a no-sun interval.

Primary references checked 2026-11-01:

- [Top Power TP4056 datasheet](https://www.toppwr.com/uploadfile/file/20240130/65b892bb04a3c.pdf):
  charger limits, reverse blocking, termination and temperature input.
- [TI BQ2407x datasheet](https://www.ti.com/lit/ds/symlink/bq24074.pdf):
  example of independent system power path and battery-current monitoring;
  not a selected module or approved Heltec connection.
- [TI dual-charger application note](https://www.ti.com/lit/an/slyt651/slyt651.pdf):
  coordinated parallel charger design is possible, rather than inherently forbidden.
- [EVE 26V manufacturer specification, distributor-hosted](https://www.nkon.nl/en/amfile/file/download/file/556/product/5745/):
  charge-temperature restrictions; match the actual cell revision before design.

Next: obtain exact panel links/labels, Heltec variant and proposed charger and
holder details; choose shared-pack versus independent-module architecture,
then specify protection, charge current and Heltec power interface.

## Follow-up: harvest three 5-6 W panels

Owner clarifies the objective: charge twelve parallel 18650 cells using three
5-6 W panels without a small charger becoming the power bottleneck. TP4056 is
excluded. Shared-pack charging remains an option; separate four-cell batteries
are not required by this clarified objective.

Recommended design direction for independent USB panel outputs: one switching
charger channel per panel feeding a shared protected 1S12P pack, with coordinated
charge termination and a designed system power path. Each channel should accept
at least the panel's 1-1.2 A at 5 V and provide about 2 A battery-side capability.
At an illustrative 90% conversion efficiency, 15-18 W yields 13.5-16.2 W, or
3.65-4.38 A at a 3.7 V battery before gateway consumption. These are calculations,
not measured harvest. Charge acceptance necessarily falls near full capacity.

The [TI BQ25895](https://www.ti.com/product/BQ25895) is a potential switching
charger building block with input regulation and power path, not a selected
ready-to-wire module. TI's [MPPT reference design](https://www.ti.com/lit/ug/tidudj2/tidudj2.pdf)
uses host software for panel tracking. Parallel charger termination/power-path
coordination still requires design; do not parallel arbitrary SYS outputs.
Regulated USB output is not the raw photovoltaic voltage, so downstream MPPT
cannot directly track the photovoltaic cells through an unknown regulator.

An alternative for compatible matched raw panels with similar illumination is
parallel panel combining into one sufficiently rated 1S switching solar charger.
For 5 V / 18 W, allow at least 3.6 A input (roughly 4-5 A design capability) and
5-6 A battery-side capability to avoid low-battery clipping. Chip charge-current
marketing alone is insufficient: BQ25895 input limit is 3.25 A, below 18 W at 5 V.
Waveshare Solar Power Manager D specifies a 6-24 V solar input and therefore is
not an approved match for regulated 5 V USB panels.

Next decisive input is the exact panel product link: determine raw versus
regulated output, delivered current, and restart/overload behavior before a
module purchase recommendation. No off-the-shelf three-input assembly has been
verified; do not represent the architecture as a tested parts list.

# Excel energy and runtime planner

[Open the calculator](../../outputs/01a16f5b-c31a-7b33-b76b-a12c97d65221/SNORR_Energy_Planner.xlsx).
Created 2026-10-24 for the owner, extending the
[solar/runtime analysis](../research/solar-runtime-20261024.md). The workbook
uses ordinary Excel formulas and one editable native chart, with no macros or
external data connections. Amber cells are inputs; formulas elsewhere recalculate.

## Included calculations

- **Fleet:** R002/R004/R006/G003/G004 plus a custom node. Separate series and
  parallel counts, cell ratings, capacity condition/cold factor, initial SOC,
  reserve and average battery load. Calculate usable Wh, battery runtime,
  minimum sun/net charging, daily energy margin, overnight capacity, required
  battery/panel sizing and post-outage recovery. Sunny input can be net battery
  mA, total supply mA at battery voltage, or panel nameplate watts with derating,
  conversion loss and a gross charger limit.
- **Backup pack:** four/eight-cell examples feeding the selected node, with
  node quantity, 5 V boost/cable/node-path losses, idle draw and converter output
  limit. Calculate external-only runtime, usable USB Ah/Wh, internal-node charge
  time, complete recharge batches while nodes run, peak output demand and required
  external cells for the shared no-sun target. Energy and power limits are distinct.
- **Pack recharge:** select the external pack and compare hypothetical 1/2/4 A
  chargers with available input voltage/current, charger/pack limits, charge-end
  voltage, efficiencies, SOC window, taper and concurrent load. Calculate limiting
  input, current, time, input Wh/cost, useful charging days and conversion loss.
  PD advertised watts do not establish battery charge current or compatibility.
- **Sizing:** live sunlight/current matrices, no-sun battery sizing and a chart
  for 20 mA RAK / 160 mA Heltec comparisons.
- **Measurements:** duty-cycle average current/power, a blank interval-energy
  log and the original dated bench snapshot. Sources and scenario provenance
  are collected here. Invalid/partial intervals block the log total.

Defaults preserve the last interactive scenario: Heltec load **155 mA**, R006
net charge **200 mA**, and G003 **500 mA**. These are scenario selections, not
new measurements; the owner originally recalled **160 mA at the battery**.
Other charge inputs are historical bench magnitudes with unverified sign/path/
source. R002's four-cell allocation remains provisional. The RAK 20 mA load,
conversion efficiencies, pack topology and example current limits remain assumptions.

## Ticket reference and limits

Owner explicitly identifies **LOCAL-10 through LOCAL-13**, read from
[wishlist revision 84e9c136](https://github.com/lfg-seth/snorr-meshlink/blob/84e9c1368296739f76ab472da910a4ca674b3706/records/wishlist.md).
The planner covers dual-panel sizing, combined-path energy accounting, emergency
four/eight-cell packs and faster car/PD recharge comparisons. It does not select
a dual-charger circuit, protection topology, connector, CAD design or purchase.
Other work in those tickets remains held until separately selected.

Use measured battery-side average draw and net sunny charge below taper to
replace the defaults. Do not insert USB current directly as battery current.
Temperature/cell condition factors are editable assumptions, not calibrated curves.
The present model estimates aggregate energy, not a temperature-aware charger
simulation, a voltage discharge curve or weather forecast. Verify physical
limits and integrate actual day/night behavior before unattended use.

## Verification

- Artifact Tool recalculation and independent spot calculations pass, including
  changed loads, gross/net/panel modes, zero/missing sun, blank versus zero charge,
  node/pack selectors, converter overload, zero charge window, concurrent load
  exceeding charging, and one-hour measurement integration.
- Formula error scan reports no errors. Saved XLSX inspection confirms cached
  error-free formulas, five sheets, editable validation controls and a native
  two-series chart with range bindings and intended line colors.
- All five sheets and their lower input/calculation/source sections were rendered
  and visually reviewed. Native Microsoft Excel execution has not been tested.
- No hardware, production service or deferred implementation changed.

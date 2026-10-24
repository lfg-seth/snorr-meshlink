# Infrastructure solar and battery budget - 2026-10-24

Owner requests R002/R004/R006/G003/G004 autonomy and four-hour solar viability.
This is a conditional engineering estimate, not a measured endurance result.
No radio, server, charging configuration or deployment changes.

## Battery and load assumptions

[Inventory](../../records/inventory.md) records EVE 26V cells: 2550 mAh,
3.6 V nominal. [EVE's specifications](https://www.evebatteryusa.com/18650-and-21700-specifications)
confirm those ratings. Four parallel cells provide nominal 10.2 Ah / 36.72 Wh;
eight provide 20.4 Ah / 73.44 Wh. These totals assume matched 1S parallel
assemblies, not independently verified usable capacity. R002's four-cell
allocation is historical/planned; R004/R006/G004 have four and G003 eight
owner-allocated cells. Exact assemblies still need confirmation.

Owner clarifies the recalled Heltec **160 mA is measured at the battery lead**.
Use that as a planning average, not a validated load for both gateways. G003
is V3; replacement G004 is V4 with GPS. Their loads can differ. RAK draw has
not been established with a battery-only average: use **20 mA**, with **10-30
mA** sensitivity. Do not treat USB charging current as operating consumption.
Usable capacity defaults to **80% of rating** for reserve/cutoff/condition;
this is a planning allowance, not a measured cold-temperature derating.

| Node | Parallel cells assumed | Average battery load assumed | Battery only, 80% usable | Battery only, full nominal |
| --- | ---: | ---: | ---: | ---: |
| R002 | 4, provisional | 20 mA | 408 h / 17.0 d | 510 h / 21.3 d |
| R004 | 4 | 20 mA | 408 h / 17.0 d | 510 h / 21.3 d |
| R006 | 4 | 20 mA | 408 h / 17.0 d | 510 h / 21.3 d |
| G003 | 8 | 160 mA | 102 h / 4.25 d | 127.5 h / 5.31 d |
| G004 | 4 | 160 mA | 51 h / 2.13 d | 63.75 h / 2.66 d |

At 10-30 mA, the four-cell RAK estimate spans **34.0-11.3 days** at 80% usable.
These runtimes start full; present charging voltage does not establish remaining
runtime. More cells extend weather reserve but do not fix a daily solar deficit.

## Current evidence and limits

Read-only production SQLite snapshot at **2026-10-24 19:24:40 UTC / 12:24:40
Pacific**, rolling 30-minute receipt window. Query only requested-device
observations, using `mode=ro` and a read transaction. No secrets or positions
returned. Private probe: `private/bench/solar-budget-probe.py` in the coordinating
checkout. INA219 channel 1 remains separate from device battery voltage and
legacy environment readings. Source/receipt times are retained in private output.

| Node | Latest battery, V | Latest signed channel-1 mA | 30-minute channel-1 range, mA | Samples |
| --- | ---: | ---: | --- | ---: |
| R002 | 4.154 | -0.6 | -104.3 to -0.1 | 10 |
| R004 | 3.621 | -107.1 | -109.5 to -79.4 | 10 |
| R006 | 3.977 | -106.9 | -112.8 to -54.3 | 10 |
| G003 | 3.919 | -4.2 | -141.7 to +129.3 | 6 |
| G004 | 3.896 | -545.8 | -545.8 to +169.4 | 9 |

Polarity, calibration, supply source and solar provenance remain unverified.
Do not call these confirmed net solar charging measurements. Sparse readings
and mixed signs do not establish an integrated day/night charge budget. R002's
near-zero value may reflect taper/termination or another operating state; it
does not bound panel capability. G004's latest high magnitude is not evidence
of sustained solar output or a reason to override controller specifications.

## Solar balance

Let `L` be average battery discharge mA without external power, `C` net battery
charging mA while external power also runs the node, `H` equivalent hours/day
at that current, and `e` usable charge retention (default **0.90**).

- Daily change: `e*C*H - L*(24-H)` mAh.
- Minimum hours: `24*L/(L+e*C)`.
- Minimum net charge for chosen hours: `L*(24-H)/(e*H)`.
- Battery-only hours: `cellCount*2550*usableFraction/L`.

If using total supply at battery voltage `S`, first subtract daytime load:
`C=S-L`. A deficit during sun is a discharge, without charge-retention loss.
Do not directly insert a 5 V USB/panel current into a battery-voltage current
equation. Use measured net battery current or a separate voltage/efficiency
energy model. If input measurements already represent usable stored charge,
set retention to 100% to avoid counting losses twice.

| Assumed battery load | Minimum net charge at 4 h, ideal | Minimum net charge at 4 h, 90% retention | Total battery-voltage supply at 4 h, 90% retention |
| --- | ---: | ---: | ---: |
| RAK 10 mA | 50 mA | 55.6 mA | 65.6 mA |
| RAK 20 mA | 100 mA | 111.1 mA | 131.1 mA |
| RAK 30 mA | 150 mA | 166.7 mA | 196.7 mA |
| Heltec 160 mA | 800 mA | 888.9 mA | 1048.9 mA |

If the latest negative readings really are **net solar charging sustained
throughout the useful window**, the 90%-retention break-even hours would be
R002 **23.37**, R004 **4.12**, R006 **4.13**, G004 **5.90**. R002's tapered
snapshot is unsuitable for solar sizing; G003's sunny charge rate is unknown.
R004/R006 are marginal around four hours at a 20 mA load, but would sustain at
10 mA. These are counterfactuals, not acceptance results.

For a Heltec at 160 mA, **500 mA net** charging requires **6.30 h/day**;
**500 mA total battery-voltage supply** leaves 340 mA net and requires **8.24
h/day**. At 90% retention, 160 mA net permits average battery load up to **28.8
mA** with four useful hours. Thus small panels may support RAKs after validation;
a 160 mA Heltec needs substantially more daily energy.

Useful hours mean current-integrated equivalent exposure, not any four clock
hours with sunlight. For example, four hours averaging half the tested current
provide two equivalent hours. Check night capacity too: at the default loads,
20 dark hours require 400 mAh per RAK and 3200 mAh per Heltec; all assumed packs
cover one such interval at 80% usable. Seasonal shade, clouds and snow can still
create multiple deficit days.

## Charging path limits and next evidence

[RAK19003 datasheet](https://docs.rakwireless.com/product-categories/wisblock/rak19003/datasheet/)
specifies 350 mA charging and a 5 V solar input. The earlier
[RAK19007 reference](battery-charge-estimate.md#rak19007-charging-and-low-voltage-behavior)
also records 350 mA. These are charger specifications, not guaranteed net
harvest or measured RAK operating loads.

[Heltec V4 datasheet](https://resource.heltec.cn/download/WiFi_LoRa_32_V4/datasheet/WiFi_LoRa_32_V4.2.0.pdf),
section 3.4, lists charging at USB 5 V as 500 mA. That entry alone does not
establish a calibrated net solar charging ceiling for this assembly. Even the
optimistic scenario of 500 mA continuously **net** for four hours cannot replenish
a 160 mA load for the other twenty hours. Larger panels cannot bypass an actual
charger bottleneck. Exact G003 V3 revision/charger and G004 solar path need
confirmation before selecting hardware changes.

Next: verify cell wiring/counts, current sign and full battery path; measure
battery-only average with normal Wi-Fi/GPS/traffic; then log real sunny net
charging below taper and integrate a complete day/night cycle. Confirm controller
limits and cell-temperature charge restrictions before outdoor acceptance.
No new purchases, physical changes or field acceptance are implied.

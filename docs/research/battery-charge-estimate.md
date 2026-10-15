# Approximate infrastructure battery state of charge

Recorded 2026-10-15 for the local portal UI. This is an uncalibrated display estimate, not a measured fuel gauge, operating threshold or runtime prediction.

## Confirmed inputs and scope

The owner identifies the relevant repeater cells as EVE 26V 18650, rated 2550 mAh and 7.5 A, with 3.6 V nominal, 4.2 V full charge and 2.5 V discharge cutoff. Telemetry measures battery terminals directly. The owner reports parallel packs of either two or four cells: 1S2P/1S4P. Their nominal capacities sum to 5100/10200 mAh; this is rated arithmetic, not measured usable capacity. Parallel count does not multiply voltage or change which single-cell voltage lookup applies.

The UI applies the profile to the project repeaters R001/R002/R003. Explicit `batteryProfile: 'eve-26v-1s'` also selects it; another explicit value overrides the project fallback. Demo repeaters explicitly carry this profile. Unconfigured backhauls, other batteries and member tracker percentages do not acquire this estimate. The frontend project fallback lets the existing live voltage contract work without rewriting hosted configuration. Move profile selection into device configuration when additional cell types are introduced.

## Source and approximation

- [EVE Energy North America cylindrical NCM specifications](https://www.evebatteryusa.com/18650-and-21700-specifications) lists the 26V model and nominal rating.
- [EVE manufacturer-authored reference sheet, distributor-hosted PDF](https://www.hestore.eu/en/prod_getfile.php?id=21996), PDF page 2, specification LLB-EVEICR18650/26V1-SS03-LF (2015): the Discharge Rate Characteristics graph supplies the reference shape. The manufacturer uses both INR/ICR naming on this sheet; it is a reference for the 26V family, not a batch-specific certificate for the owner's cells.
- [EVE full specification, distributor-hosted PDF](https://www.neexgent.com/Uploads/202308/eve_icr18650-26v_rd-eve_icr18650-26v-s118-lf-a.pdf), revision A (2020), confirms charge/discharge endpoints; these endpoints alone do not determine percentage.

Read approximate points from the green 0.2C discharge curve at 77°F. The horizontal axis is **capacity discharged**; invert it to estimate charge remaining. This is a loaded discharge curve, not a rested open-circuit-voltage calibration. The plot's effective starting voltage is below the fully charged endpoint; 4.2 V/100% is the specified full-charge anchor. These visually sampled points have no verified accuracy tolerance.

| Battery voltage | Reference charge remaining |
|---:|---:|
| 2.50 V | 0% |
| 3.23 V | 5% |
| 3.38 V | 10% |
| 3.47 V | 20% |
| 3.53 V | 30% |
| 3.56 V | 40% |
| 3.61 V | 50% |
| 3.69 V | 60% |
| 3.78 V | 70% |
| 3.87 V | 80% |
| 3.99 V | 90% |
| 4.20 V | 100% |

Interpolate between points and round to 5% steps, always showing an approximation mark and measured voltage alongside it. Unknown/nonfinite/nonpositive voltages remain unknown. Above 4.25 V, withhold the estimate as outside the 1S profile rather than treating a regulated supply or series pack as full. At/below 2.5 V, show approximately zero with an explicit cutoff note. No ingestion or warning thresholds change.

## Limits and later calibration

Charging can overstate charge, load can depress voltage, and temperature/aging shift the relationship. The repeater load per cell is not measured and may differ substantially from the reference discharge current. Existing enclosure weather temperature is not assumed to be cell temperature. A rising-voltage trend adds a charging-bias note; it does not prove charger state. Stale/unknown-time and offline readings retain an explicitly historical estimate.

The cell's 2.5 V cutoff does not establish a working node's shutdown voltage. A node can stop while the cell still has charge. Keep usable runtime and safety thresholds separate from this UI percentage. Later compare telemetry with a multimeter and collect normal-load discharge traces from full charge to the actual node/protection cutoff. No such field measurements or calibration were performed for this change.

## RAK19007 charging and low-voltage behavior

Owner asks about RAK power specifications on 2026-10-15. The inventory lists RAK19007 base boards with RAK4631 cores; individual base-board revisions remain physically unverified. Charging belongs to the base board rather than the RAK4631 radio/MCU module.

[RAK19007 datasheet](https://docs.rakwireless.com/product-categories/wisblock/rak19007/datasheet/) documents a 5 V solar connector, 5.5 V maximum solar input, 3.3–4.3 V battery operating range, 4.2 V rechargeable-cell charging target and 350 mA charging current. The 4.5–5.5 V charging-input specification is not a battery charge target. The specified minimum battery operating voltage is not a promised hard-disconnect threshold. RAK describes the red LED as a local charger-status indicator.

[RAK support's RAK19007 explanation](https://forum.rakwireless.com/t/battery-max-voltage-charging/16859) identifies TP4054, shared USB/solar charging, low-battery precharge near 2.9 V, and recharge hysteresis of approximately 100–200 mV below 4.2 V. The 2.9 V threshold concerns precharge of a low battery, not discharge protection or minimum solar input. RAK recommends approximately 5.0–5.5 V input allowing for the diode drop; the datasheet's 5.5 V maximum still applies. Panel voltage/rating under actual conditions remains unverified for the inventoried 160 mA panels. Charge current into the battery is limited by available input, system load and the charger; 350 mA is not a guarantee of solar harvest.

These sources do not establish a guaranteed battery-disconnect threshold for our assemblies. RAK support explicitly distinguishes charger operation from undervoltage/short-circuit protection; its [RAK19012 answer](https://forum.rakwireless.com/t/rak19012-low-voltage-cutoff/14316) describes no low-voltage disconnect on that related power board, but does not independently certify every RAK19007 revision. Inspect the actual pack protection and board revision rather than equating the charger with a complete protection circuit.

Separately, the locally pinned Meshtastic source (`54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`) has a default 3100 mV bottom lookup point in `firmware/src/power.h`. `Power.cpp` triggers low-battery deep sleep after more than ten consecutive readings below that threshold when a battery is detected and USB is not detected. `PowerFSM.cpp` enters low-battery sleep. The RAK4631 variant defines a comparator wake threshold corresponding nominally to about 3.76 V in its comments; actual analog tolerance and recovery behavior remain untested. This firmware behavior is not a physical battery disconnect, and source inspection does not prove successful recovery for our assemblies. No firmware or UI thresholds changed in this research follow-up.

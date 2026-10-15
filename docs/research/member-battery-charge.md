# Member battery voltage and approximate charge

Recorded 2026-10-15. Owner authorizes member-node battery voltage ingestion, configurable battery type/capacity and an estimate similar to the repeater display.

## Inventory and profile

The purchase list rows 10/11 describe 1000/3000 mAh member batteries. Existing inventory identifies the smaller on-hand packs as owner-reported 1100 mAh. This request identifies the relevant batteries as LiPo. Preserve both labels; no stock counts or per-device installed capacities are inferred. Configuration offers 1000, 1100 and 3000 mAh suggestions, accepts other positive whole capacities, and permits unknown type/capacity.

MakerFocus's [3000 mAh product](https://www.makerfocus.com/products/makerfocus-3-7v-3000mah-lithium-rechargeable-battery-1s-3c-lipo-battery-pack-of-4) identifies a 3.7 V 1S LiPo. The manufacturer's [battery listing](https://www.makerfocus.com/collections/best-selling/categories_battery) also identifies the 1100 mAh family as 3.7 V 1S LiPo. Product-family descriptions do not verify individual pack labels, calibration or protection behavior. No pack-specific discharge curve was established.

Use explicit `batteryProfile: 'lipo-1s'` for the generic 3.7 V nominal / 4.2 V full profile. Capacity (`batteryCapacityMah`) records rated pack size; it does not change the voltage curve or imply remaining runtime. Devices stay unconfigured until an admin records the installed pack.

## Estimate and evidence

Use the nonlinear generic lookup already in pinned Meshtastic source [power.h](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/power.h), inspected locally at that commit, with interpolation as in [Power.cpp](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/Power.cpp). These are generic reference points, not a measured MakerFocus calibration or a guarantee that a particular board uses this exact curve.

| Voltage | Approximate charge |
|---:|---:|
| 3.10 V | 0% |
| 3.30 V | 10% |
| 3.42 V | 20% |
| 3.53 V | 30% |
| 3.63 V | 40% |
| 3.72 V | 50% |
| 3.80 V | 60% |
| 3.89 V | 70% |
| 3.99 V | 80% |
| 4.05 V | 90% |
| 4.19 V | 100% |

Interpolate and round to 5%, always showing ≈ and raw volts. Nonpositive/nonfinite/missing voltage and voltage above 4.25 V yield unknown. Positive voltage below the reference range clamps to 0%; this is an estimate endpoint, not a new protection/shutdown setting. Charging, load, temperature, aging and ADC error affect the estimate. [Adafruit's LiPo voltage explanation](https://learn.adafruit.com/li-ion-and-lipoly-batteries/voltages) describes the nonlinear discharge shape and full-charge voltage; its example is not calibration for these packs.

The shared estimator preserves the earlier EVE reference lookup separately. Its source is the manufacturer-authored [EVE 26V sheet](https://www.hestore.eu/en/prod_getfile.php?id=21996), 0.2C / 77°F discharge graph, with discharged capacity inverted; EVE lookup points remain unchanged from the local repeater work. Neither curve is a fuel gauge.

## Data and UI boundary

Meshtastic [device telemetry](https://meshtastic.org/docs/configuration/module/telemetry/) carries voltage separately from positions. The adapter now normalizes member device-voltage telemetry to existing observations/receipts, with two-gateway deduplication. Member environmental/intrusion/solar observations remain unsupported by operational ingestion; the raw MQTT archive preserves all traffic.

The snapshot exposes batteryVoltage, batteryMeasuredAt, batteryReceivedAt, batteryTimestampQuality, batteryProfile and batteryCapacityMah. Existing `battery` percentages retain their prior meaning. Battery packets do not overwrite GPS measurement timestamps/coordinates/history. Older, future and unknown measurement times do not replace a newer known voltage. Unknown measurement clocks stay explicit.

Selected tracker details show approximate charge, raw voltage, independent measured/received times, profile and nominal capacity. Offline, unknown-time and 15-minute stale battery indicators remain visible. The 15-minute battery display threshold is a simple UI convention, not a fitted warning threshold or radio cadence change. Admin configuration uses the existing authenticated configuration route; ordinary members cannot alter it. No battery firmware, reporting cadence, warning thresholds or installed battery assignments are changed.

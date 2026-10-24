# Device-card battery summary — LOCAL-8

2026-10-24. Owner activates the [canonical request](../../records/wishlist.md#device-card-battery-summary-without-duplicate-sensor-readings)
for frontend implementation. Source is prepared on `codex/local-8-battery-summary`
from `origin/main` at `520fbfc`; production deployment is a separate step.
The original checkout and its unrelated hardware edits remain untouched.

## Card presentation

One shared [summary](../../portal/src/BatterySummary.tsx) appears near the top
of member details (Map and Users), repeater/router map cards, gateway map cards
and the selected Infrastructure detail. It shows estimated percentage, device
battery voltage, charging/discharging state and one current value. Member GPS
quality sits to the right of percentage; its header battery icon stays present.
The icon retains its existing reported-percentage semantics, distinct from the
profile-based voltage estimate. Missing values remain Unknown.

The entire Sensor voltage & current section is removed, including on equipped
devices. The history detail no longer repeats current, percentage or last voltage;
graphs, period controls and exact voltage-history tables remain. Temperature,
humidity, relationships, placement, solar, warnings and configuration controls
are preserved. GH-44's conditional sensor-section retention is superseded by
LOCAL-8's complete removal; GH-45's percentage/GPS placement is included.
Historical imported issues stay unchanged. LOCAL-7 and page redesigns are outside
this change.

## Measurement selection

- Battery voltage continues to come from `DeviceMetrics.voltage`, normalized as
  `battery`, and projected as infrastructure `battery` or member `batteryVoltage`.
  Sensor bus voltage never replaces it. Existing EVE/LiPo profile curves and
  percentage rounding are reused without modification.
- [Adapter](../../backend/mqtt_adapter.py) and
  [state projection](../../backend/pb_hooks/meshlink.js) keep environment current
  (`sensorCurrentMa`) separate from power channels (`powerNCurrentMa`). Ordinary
  INA219 firmware's documented output is channel 1; see the
  [R006 acceptance](ina219-audit.md#local-power-only-acceptance). The presentation
  selects channel 1 only when it is the sole reported power-current channel,
  preferring it over the legacy environment current to eliminate duplicates.
  With no power-current channels, a single environment current can be shown.
  Other/multiple channels, duplicate metric entries and nonfinite current remain
  Unknown. There is no selection by array order, sign, magnitude or bus voltage.
- Displayed current is explicitly **measured sensor-path current**, with source
  and unverified battery-flow/calibration accounting visible. It is not promoted
  to a confirmed whole-battery measurement. The old optional `batteryCurrentMa`
  frontend field had no producer in the inspected state API; it no longer drives
  card interpretation.
- Direction from measured current requires the API's explicit
  `currentConvention: "positive-charging"`. This is the
  [owner-confirmed, deployed convention](radio-report-ingestion.md#fleet-current-polarity-correction---2026-10-24),
  already normalized by [telemetry projection](../../backend/pb_hooks/telemetry.js).
  The frontend never inverts again. Positive/negative/zero display as
  Charging/Discharging/Steady **(sensor path)**. Unmarked signs do not establish
  charge direction. Current keeps its sign, one decimal and mA; voltage uses
  three decimals and V.
- Without confirmed measured direction, the existing battery-voltage trend may
  supply an explicitly labeled **voltage estimate** of direction. Its age comes
  from the latest valid history sample, not the newest device contact. It never
  supplies mA. Sparse history produces Unknown; member data has no current or
  voltage-history source in this contract, so those fields remain Unknown.
- Battery voltage and current use their own measurement clocks and receipt
  fallbacks, cadence and missing thresholds. Fresh GPS/contact/temperature never
  refreshes them. Old measurements retain stale labels even after a new receipt;
  feed outages mark retained readings historical. Unknown cadence stays unknown.

No adapter, ingestion, API projection, database/history, radio or live device
configuration is changed. Multi-channel battery-path mapping and physical
calibration remain separate prerequisites for stronger battery-flow claims.

## Verification and remaining gates

- `python scripts/check-project.py portal`: **60 tests pass**, TypeScript and
  production build pass on Node 22.23.1. Existing large-chunk build warning remains.
  Focused tests cover complete-section/duplicate removal across repeater/gateway
  details, member integration, retained environment/history/configuration, missing
  values, stale and offline data, receipt fallback, zero, both current directions,
  unmarked polarity, arbitrary/ambiguous channels and labeled voltage estimates.
- In-app browser visually verifies actual components with synthetic readings at
  desktop **985 × 782** and mobile **390 × 844**: two-column wrapping, member
  percentage/GPS alignment, header icon, repeater current and missing/offline
  gateway. Mobile scroll retains the header and exposes all summary fields.
  The preview uses ignored local fixtures; it does not access live telemetry.
- Authenticated deployed cards, owner phone/browser acceptance and calibrated
  whole-battery flow remain unverified. Review/merge and an explicitly selected
  manual production release precede deployed acceptance. This source change
  leaves the released application version unchanged.

# LOCAL-4: gateway power measurement plan

## Outcome and inputs

Prepare the gateway power-characterization procedure and exact-parts checklist
from [LOCAL-4 section A](../pilot/issues/26-gateway-production-readiness.md#a-measure-power-and-select-the-supply).
Read the [gateway hardware page](../../docs/hardware/heltec-v3-gateway.md) and
relevant inventory entries; distinguish last-confirmed equipment from planned
four/eight-cell and solar alternatives.

## Scope and ownership

Put the planned procedure in `records/field-results.md`; add confirmed parts to
inventory only when evidence supports them. This step prepares measurements,
without selecting pack topology, purchasing, wiring batteries, changing gateway
profiles or starting a soak. Power selection, enclosure CAD and physical tests
follow measured evidence in separate assignments.

## Prerequisites

Identify missing board/cell/holder/charger/panel/antenna/INA219 model information
and reference-meter availability. Require the actual battery/charging/load path
before recommending connections. Prepare the procedure while parts identification
is pending; use primary vendor specifications once exact models are known.

## Done and verification

Cover section A's operating states, battery and USB input paths, calibrated
current/polarity checks, Wh/day and peak/brownout recording. Include Wi-Fi/broker
outage recovery, charging while operating and the two solar options. Identify
the autonomy, no-sun and recovery criteria that need owner agreement before a
run. An advertised wattage or instantaneous current is not a measured power budget.

## Evidence and handoff

Link the planned record and unresolved parts/criteria from LOCAL-4's tracker
row. Report procedure checks, confirmed versus missing inputs, commit/branch
and the next parts-identification or measurement step. Preserve receive-only RF.

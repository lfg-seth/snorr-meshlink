# Heltec V3 gateway hardware and setup

Status: design brief, 2026-10-23. Existing gateways are Heltec V3; the planned
outdoor power/enclosure configuration below is not yet assembled or validated.
Work is tracked in [LOCAL-4](../../.scratch/pilot/issues/26-gateway-production-readiness.md).

## Intended assembly

| Part | Owner's direction | Outstanding |
| --- | --- | --- |
| Radio/controller | Heltec V3 | Confirm individual board revision before wiring/flash. |
| Battery | Four or eight 18650 cells | Actual cells/capacity, arrangement, protection, holders and charging path. |
| Solar option A | Two 60 x 100 mm panels | Electrical ratings, connection and delivered charging energy. |
| Solar option B | Larger external 5 V USB solar charger, advertised 6 W | Model, actual output and intermittent-input behavior. |
| Antenna | Muzi whip | Exact model, connector, mounting and RF specifications. |
| Power sensor | INA219 | Wiring branch, I2C pins/address, shunt, polarity and calibration. |
| Enclosure | Custom 3D-printed case | Measurements, CAD, material, prototype and weather/thermal tests. |

Last confirmed installed gateway batteries were one 1000 mAh LiPo each; this
new design does not establish that those packs have been replaced. Wi-Fi/MQTT
energy use, four/eight-cell runtime and solar sufficiency are unmeasured.

## Firmware and setup status

Use a Heltec-specific build from the shared Meshtastic fork. The dedicated
`heltec-v3-gateway` target enables SNNS in addition to ordinary V3 functionality.
The RAK4631 binary targets a different processor and cannot be reused.

Current verified gateway image is `2.7.26.9d2fd8f`, configured CLIENT,
receive-only LoRa, private Wi-Fi/MQTT and local-only neighbor reporting.
Production work includes INA219 acceptance, TLS/logging fixes, reconnect tests,
shared timing changes and release verification. Preserve each board's identity
and keys; credentials are supplied privately, never in this page.

Existing setup/evidence: [G001](../operations/g001-neighbor-gateway.md),
[G002](../operations/g002-neighbor-gateway.md). Final public step-by-step wiring,
power and provisioning instructions await tested hardware and public review.

## Photos and enclosure files

Pending: actual front/back board photographs, annotated power/sensor wiring,
four/eight-cell assembly, antenna/panel mounts, finished enclosure and service
access. No photos or CAD/print files have been supplied for this design yet.
Strip location metadata and obscure secrets before public use.

## Acceptance evidence

Pending: measured Wi-Fi operating/reconnect power, battery/solar energy balance,
reference-meter INA219 validation, cold boot/outage recovery, enclosure fit and
weather/thermal behavior, sustained end-to-end reporting and field acceptance.
Record actual results in the project field log before replacing these unknowns.

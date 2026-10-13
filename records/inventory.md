# Hardware inventory

Updated: 2026-10-12. Imported the owner's [original purchase list](<../Mesh Purchase List - Purchase List.csv>) without modifying it. Listed quantities come from the source `Total QTY` column. Six higher-value groups now have owner-confirmed on-hand counts from the 2026-10-12 inventory check-in; other counts remain unknown. These are owner reports, not independent inspections or bench tests. Blank/dash source quantities remain unknown, not zero.

Source row numbers count the header as row 1. Stable IDs below link to the original rows. Split entries into identifiable units when counted or assigned; preserve the original source references. Specs and roles below are source labels, not verified compatibility or performance.

| ID | Source row | Category | Item / source spec | Listed quantity | Confirmed on hand | Verification / notes |
| --- | --- | --- | --- | --- | --- | --- |
| HW-001 | 2 | Repeater | RAKwireless WisBlock RAK19007 | 10 | 8 | Owner found 1 additional RAK with a broken carrier board requiring replacement; exclude that unit from ready-to-use stock. Other 7 units untested. Plus 2 deployed remotely at Mount Charleston, recover when replacement nodes are ready. 10 now accounted for against 10 listed. Exact core modules/variants unknown |
| HW-002 | 3 | Repeater | 18650 cells; source EVE 2550mAh | Unknown (source dash) | 88 | Owner confirms 88 on hand. Additional cells in mountain repeaters estimated at perhaps 4 per repeater (about 8 across the 2 reported deployments); excluded from on-hand stock. On-hand cell identities, capacities, condition, and test results unverified; do not assume all match the source EVE label |
| HW-003 | 4 | Repeater | Solar panel; 6W | 4 | Unknown | Source describes an externally mounted alternative; output untested |
| HW-004 | 5 | Repeater | Solar panel; 1W | 40 | Unknown | Source note estimates closer to 0.25W each; not a measured project result |
| HW-005 | 6 | Repeater | Fiberglass antenna; labelled 5.8dBi LoRa 915MHz | 10 | 10 | Owner-confirmed count matches listed quantity; condition and actual connectors/variant unverified |
| HW-006 | 7 | Repeater | INA219 current/power sensor | 10 | Unknown | Verify boards and interfaces |
| HW-007 | 8 | Repeater | Four-slot 18650 holder | 18 | Unknown | Verify wiring/layout; source quantity is holders, not cells |
| HW-008 | 9 | Repeater | Coax; Type N to U.F.L1 | 10 | Unknown | Source associates these with fiberglass antennas |
| HW-009 | 10 | Client | Battery; source 1000mAh, owner reports 1100mAh | 4 | 6 | Owner confirms 6 × 1100mAh batteries for V3 units. Capacity label differs from source description; chemistry, connector, and condition unverified |
| HW-010 | 11 | Client | Battery; 3000mAh | 2 | 2 | Owner confirms 2 × 3000mAh batteries for V4 units; chemistry, connector, and condition unverified. Owner suspects larger batteries are needed; capacity choice awaits runtime testing |
| HW-011 | 12 | Client | Whip antenna; labelled 915MHz | 16 | 11 | Owner identifies these as Muzi whip antennas; exact model, condition, and connectors unverified. 5 fewer on hand than listed; disposition unknown |
| HW-012 | 13 | Client | Heltec V3 | 4 | 9 | Owner confirms no GPS on these units. Proposed use: silent internet/backhaul nodes, possibly repeaters depending on installation; capability/configuration unverified. Count is 5 above source quantity; provenance, exact radio variant, and condition unknown |
| HW-013 | 14 | Client | Heltec V4 | 6 | 2 | Owner confirms both have GPS modules. On 2026-10-12 owner plans to order 2 more and recover 2 member-held units, all with GPS and 3000mAh batteries. Planned additions are not available stock; purchase, recovery, exact variants, and condition remain unverified |
| HW-014 | 15 | Client | SMA roof mount / antenna base | 2 | Unknown | Verify connector and cable |
| HW-015 | 16 | Both | Case filament; first source entry | 2 | Unknown | Separate source product link; amount remaining unknown |
| HW-016 | 17 | Both | Case filament; second source entry | 2 | Unknown | Separate source product link; amount remaining unknown |
| HW-017 | 18 | Client | Power switch | 20 | Unknown | Verify switch type |
| HW-018 | 19 | Client | USB-C jack | 20 | Unknown | Verify breakout/wiring |
| HW-019 | 20 | Client | Push button; black | 30 | Unknown | Verify type |
| HW-020 | 21 | Client | Push button; red | 10 | Unknown | Verify type |
| HW-021 | 22 | Repeater | Temperature sensor | 10 | Unknown | Model not stated in source item fields |
| HW-022 | 23 | Repeater | Battery cable | 20 | Unknown | Confirm connector and polarity |
| HW-023 | 24 | Repeater | Solar cable | 10 | Unknown | Confirm connector and polarity |
| HW-024 | 25 | Misc | Solder | 1 | Unknown | Amount remaining unknown |
| HW-025 | 26 | Client | LILYGO T-Deck (source: “Tdfeck”) | 2 | 2 | Owner confirms 2 brand-new devices with GPS modules and their own included batteries; battery capacity unknown. Exact variant/frequency and bench operation unverified |
| HW-026 | 27 | Repeater | M3×20 screws | 120 | Unknown | Count remaining |
| HW-027 | 28 | Repeater | M3×30 screws | 120 | Unknown | Count remaining |
| HW-028 | 29 | Repeater | O-ring seal | 1 | Unknown | Verify dimensions/material and remaining amount |
| HW-029 | 30 | RF | Coax; SMA female to U.F.L1 | Unknown (blank) | Unknown | Source shows 2 packs, with no pack size or total quantity |
| HW-030 | 31 | Client | SD card adapter | Unknown (blank) | Unknown | Source shows 1 pack, with no pack size or total quantity |
| HW-031 | 32 | Client | SD card; data logging/testing | Unknown (blank) | Unknown | Source shows 1 pack, with no pack size or total quantity |
| HW-032 | 33 | Camera | Card labelled “SD Card” | Unknown (blank) | Unknown | Source explicitly excludes it from mesh project; track separately for content equipment |
| HW-033 | Owner report 2026-10-12 | Field computing | Rugged Dell laptop/tablet running Linux | Not in source CSV | 1 | Owner reports available for field use. Exact model, Linux distribution, battery condition/runtime, ports, and Meshtastic app/browser compatibility unverified. No purchase/value recorded |

## First confirmation pass

The updated pass accounts for 21 radio boards/devices on hand: 8 RAK (1 with a broken carrier board), 9 Heltec V3, 2 Heltec V4, and 2 LILYGO T-Deck. Excluding the damaged RAK leaves 20 candidates for inspection, not 20 bench-verified working devices. Another 2 RAK units are deployed and unavailable for the bench pilot pending replacement and recovery. Member-held Heltec V4 quantities remain unknown.

Four on-hand devices have owner-confirmed GPS modules: 2 Heltec V4 and 2 T-Deck. All 9 V3 units have no GPS; RAK GPS status remains unknown. No device has bench-verified passive tracking recorded. Identify exact radio/core builds and GPS models, then confirm operation and HW-002 cells before a pilot parts decision. The source-listed quantities are historical references and are preserved even where current counts differ.

Owner-directed planning baseline: use only confirmed on-hand stock. Exclude the 2 deployed RAK units, possible member-held V4s, and the damaged RAK until its carrier board is replaced and operation verified. The newly found RAK closes the numerical difference against the source-listed 10; the prior possible third repeater/destroyed-unit explanation is no longer needed to reconcile that count. Historical differences do not block this first-pass inventory closure.

2026-10-12 — Pilot planning update: owner explicitly expanded the planning baseline to include 2 Heltec V4 purchases and recovery of 2 member-held V4s, each intended to have GPS and a 3000mAh battery. This would provide 6 V4s including the 2 on hand, with the 2 existing T-Decks a separate potential addition to the pilot. Actual trial participant count remains to be agreed. Keep the 4 planned V4s and their batteries separate from confirmed on-hand counts until received/recovered. No order, recovery, price, or additional battery stock confirmed.

Available member-device batteries: 6 × 1100mAh for V3, 2 × 3000mAh for V4, plus included batteries in both T-Decks. V3 backhaul/repeater use is a proposed role, not a firmware decision. Larger V4 batteries are a concern to evaluate against mission duration and measured GPS/runtime behavior, not a confirmed purchase requirement.

2026-10-12 — Owner set battery runtime to a 4-hour minimum and 12-hour target, and is open to purchasing larger batteries. Evaluate runtime before selecting a larger capacity; no new battery size, quantity, order, or available stock established.

No charge-controller or battery-protection hardware is separately identified in this CSV. Check whether it is integrated, owned separately, or absent before treating it as a purchase gap.

Source rows for INA219 and RF coax have unusual per-repeater/unit-cost placement. Use source `Total QTY` only when present; do not use the purchase sheet's per-device columns as an approved bill of materials. Preserve source quantities and replace only the separate confirmed-count field when physically verified.

## Additional inventory to capture

2026-10-12 — Future SOS hardware idea: owner suggested adding a buzzer or similar audible alert to Heltec boards, alongside an OLED popup/flashing alert. No buzzer model, quantity on hand, GPIO/driver compatibility, wiring, cost, or purchase confirmed. Evaluate existing parts and the selected board before choosing hardware; SOS remains beyond the passive-tracking MVP.

2026-10-12 — Pilot infrastructure allocation: owner includes RAK repeaters from HW-001 (count/builds still open) and 2 Heltec V3s from the 9 on hand in HW-012. These 2 V3s are planned receive-only internet backhauls, not member GPS trackers or RF repeaters. Internet forwarding with radio silence is an intended requirement, not a tested capability. Allocations do not change stock counts. Use on-hand RAK candidates; the damaged unit requires repair/verification and the 2 deployed units are not assumed available.

2026-10-12 — Portal-planning amendment: owner authorizes one of the 2 allocated V3 backhauls to transmit portal-originated shared-channel replies. The other remains receive-only/uplink-only. Individual unit selection and firmware/radio behavior are unverified; this changes proposed roles, not the confirmed count of 9 V3s or any working-device count. Owner proposes stable numeric device labels with portal-managed member assignments/self-claims; no physical labelling or assignment performed yet.

2026-10-12 — Owner selected 2 undamaged, on-hand RAKs for initial relay evaluation, subject to identifying cores and verifying operation. Select from the 7 undamaged on-hand units; no individual units are assigned yet and stock counts are unchanged. Owner also reports 1 rugged Linux Dell laptop/tablet (HW-033) available for field viewing. Both companion-app and laptop/portal viewing remain intended; the first local-viewing MVP may use the Meshtastic app.

2026-10-12 — Final pilot scope: owner selected the 6 planned V4s only and excluded the 2 T-Decks to reduce device/firmware complexity. T-Decks remain in inventory for later use. Confirmed on-hand counts are unchanged; 2 V4 purchases and 2 recoveries remain pending.

- Complete nodes and radio boards: exact model, frequency variant, count, current firmware if known.
- GPS modules: model, count, which nodes already contain one.
- Antennas, feedlines, connectors, mounts, and enclosures.
- Solar panels, charge controllers, and battery protection hardware.
- 18650 cells/packs: count, cell identity if known, condition, and any test results.
- Keyboard/display nodes and other member-facing hardware.
- Backhaul equipment and spares.

Photos, labels, receipts, and bench tests can support entries later. Record unknowns explicitly. Link spending or contributions to the same hardware IDs in [finances](finances.md). Do not overwrite the purchase-list source when reconciling stock.

# Hardware inventory

Updated: 2026-10-12. Imported the owner's [original purchase list](<../Mesh Purchase List - Purchase List.csv>) without modifying it. The owner says most items are still held, but possibly not all. Listed quantities come from the source `Total QTY` column; **all current on-hand counts and conditions are unconfirmed**. Blank/dash source quantities remain unknown, not zero.

Source row numbers count the header as row 1. Stable IDs below link to the original rows. Split entries into identifiable units when counted or assigned; preserve the original source references. Specs and roles below are source labels, not verified compatibility or performance.

| ID | Source row | Category | Item / source spec | Listed quantity | Confirmed on hand | Verification / notes |
| --- | --- | --- | --- | --- | --- | --- |
| HW-001 | 2 | Repeater | RAKwireless WisBlock RAK19007 | 10 | Unknown | Confirm exact assembled board, radio/core module, variant, and condition |
| HW-002 | 3 | Repeater | EVE 18650 battery; 2550mAh | Unknown (source dash) | Unknown | Count and identify cells; record condition/test results |
| HW-003 | 4 | Repeater | Solar panel; 6W | 4 | Unknown | Source describes an externally mounted alternative; output untested |
| HW-004 | 5 | Repeater | Solar panel; 1W | 40 | Unknown | Source note estimates closer to 0.25W each; not a measured project result |
| HW-005 | 6 | Repeater | Fiberglass antenna; labelled 5.8dBi LoRa 915MHz | 10 | Unknown | Source calls for Type N to U.F.L1 cable; verify actual connectors/variant |
| HW-006 | 7 | Repeater | INA219 current/power sensor | 10 | Unknown | Verify boards and interfaces |
| HW-007 | 8 | Repeater | Four-slot 18650 holder | 18 | Unknown | Verify wiring/layout; source quantity is holders, not cells |
| HW-008 | 9 | Repeater | Coax; Type N to U.F.L1 | 10 | Unknown | Source associates these with fiberglass antennas |
| HW-009 | 10 | Client | Battery; 1000mAh | 4 | Unknown | Confirm label, chemistry, connector, and condition; URL label differs |
| HW-010 | 11 | Client | Battery; 3000mAh | 2 | Unknown | Confirm label, chemistry, connector, and condition |
| HW-011 | 12 | Client | Whip antenna; labelled 915MHz | 16 | Unknown | Source calls for SMA female to U.F.L1 adapter |
| HW-012 | 13 | Client | Heltec V3 | 4 | Unknown | Exact revision/radio variant and GPS fitted status unknown |
| HW-013 | 14 | Client | Heltec V4 | 6 | Unknown | Exact revision/radio variant and GPS fitted status unknown |
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
| HW-025 | 26 | Client | “Tdfeck” (source spelling) | 2 | Unknown | Possibly intended as T-Deck; confirm actual model, variant, and GPS fitted |
| HW-026 | 27 | Repeater | M3×20 screws | 120 | Unknown | Count remaining |
| HW-027 | 28 | Repeater | M3×30 screws | 120 | Unknown | Count remaining |
| HW-028 | 29 | Repeater | O-ring seal | 1 | Unknown | Verify dimensions/material and remaining amount |
| HW-029 | 30 | RF | Coax; SMA female to U.F.L1 | Unknown (blank) | Unknown | Source shows 2 packs, with no pack size or total quantity |
| HW-030 | 31 | Client | SD card adapter | Unknown (blank) | Unknown | Source shows 1 pack, with no pack size or total quantity |
| HW-031 | 32 | Client | SD card; data logging/testing | Unknown (blank) | Unknown | Source shows 1 pack, with no pack size or total quantity |
| HW-032 | 33 | Camera | Card labelled “SD Card” | Unknown (blank) | Unknown | Source explicitly excludes it from mesh project; track separately for content equipment |

## First confirmation pass

Start with HW-001, HW-012, HW-013, and HW-025: count usable radios and identify their exact builds. The source lists 12 client-board/device entries by quantity (4 + 6 + 2), but does not establish 12 complete GPS trackers. Dedicated GPS modules are not separately listed; that does not prove none are owned or fitted. Confirm GPS hardware and HW-002 cells before a pilot parts decision.

No charge-controller or battery-protection hardware is separately identified in this CSV. Check whether it is integrated, owned separately, or absent before treating it as a purchase gap.

Source rows for INA219 and RF coax have unusual per-repeater/unit-cost placement. Use source `Total QTY` only when present; do not use the purchase sheet's per-device columns as an approved bill of materials. Preserve source quantities and replace only the separate confirmed-count field when physically verified.

## Additional inventory to capture

- Complete nodes and radio boards: exact model, frequency variant, count, current firmware if known.
- GPS modules: model, count, which nodes already contain one.
- Antennas, feedlines, connectors, mounts, and enclosures.
- Solar panels, charge controllers, and battery protection hardware.
- 18650 cells/packs: count, cell identity if known, condition, and any test results.
- Keyboard/display nodes and other member-facing hardware.
- Backhaul equipment and spares.

Photos, labels, receipts, and bench tests can support entries later. Record unknowns explicitly. Link spending or contributions to the same hardware IDs in [finances](finances.md). Do not overwrite the purchase-list source when reconciling stock.

# Inventory owned hardware for the pilot

Type: task
Label: wayfinder:task
Status: resolved
Assignee: inventory-session-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

What equipment is already available, in what quantities and condition, so pilot hardware choices can use it before purchases?

## Completion evidence

Record the owner's first-pass model/variant names and counts in [Inventory](../../../records/inventory.md), including unknowns. Identify which items need inspection or bench verification. Do not require a complete electrical characterization to finish this first pass.

## Comments

2026-10-12 — Claimed to record the owner's confirmed higher-value stock, GPS and battery details, and the instruction to plan from on-hand stock only. Remaining inspections will be explicit follow-up work rather than blockers to this first-pass inventory.

2026-10-12: Requested rough hardware models and quantities from the owner; no inventory facts have been supplied yet.

2026-10-12 — Owner supplied `Mesh Purchase List - Purchase List.csv` and said most items are still held, but possibly not all. Imported all 32 source rows into [Inventory](../../../records/inventory.md), preserving source row references, listed quantities, and unknown current counts. The original CSV is retained unchanged. First confirmation priorities are RAK/Heltec/keyboard nodes, dedicated GPS hardware, and 18650 cells. This ticket stays open until a first-pass usable-hardware set is confirmed; a historical list alone does not establish available pilot hardware.

## Answer

The owner-confirmed first-pass inventory is recorded in [Inventory](../../../records/inventory.md): 7 RAK units, 9 Heltec V3 without GPS, 2 Heltec V4 with GPS, 2 brand-new LILYGO T-Decks with GPS and included batteries, 10 fiberglass antennas, and 11 Muzi whip antennas on hand. Separate batteries are 6 × 1100mAh for V3 and 2 × 3000mAh for V4.

Use these confirmed on-hand quantities as the planning baseline, as directed by the owner. Exclude 2 remote deployed RAK units until replacements and recovery, any additional member-held V4s, and the uncertain tenth source-listed RAK (possibly a third mountain repeater or destroyed). No stock recovery or purchase is required to close this first pass; historical differences and kit/consumable counts remain documented unknowns.

Four on-hand devices have GPS modules; this does not establish five ready passive member trackers. Proposed V3 use is silent internet/backhaul nodes and possibly repeaters depending on installation. Larger V4 batteries are an owner concern pending runtime evidence, not an approved purchase or technical requirement.

Follow-up for hardware/firmware and pilot selection: inspect exact RAK core modules and radio variants, GPS modules, battery connectors/condition, and bench operation; confirm 18650/power hardware if needed by the chosen build. Do not require complete electrical characterization to close this inventory pass. No firmware compatibility, runtime, or field performance has been verified.

2026-10-12 follow-up: owner found another RAK with a broken carrier board requiring replacement. Updated baseline is 8 RAK on hand (1 excluded pending repair), plus 2 deployed; all 10 source-listed units are now numerically accounted for. Owner confirms 88 × 18650 cells on hand; perhaps 4 per mountain repeater is a separate deployed estimate, not available stock. First-pass inventory remains resolved; replacement carrier model and cell condition need inspection before use.

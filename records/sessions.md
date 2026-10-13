# Session log

## 2026-10-12 — Project setup

- Captured the owner's mission, priorities, existing-hardware preference, intended member devices, solar/18650 repeaters, backhaul possibilities, dashboard, content, and grant-reporting goals.
- Initialized local Git on `main` and established the project brief, agent instructions, glossary, local Wayfinder tracker, and record templates.
- Proposed the first planning checkpoint: a measurable field pilot using owned hardware. This checkpoint is provisional pending owner input.
- Requested rough hardware models/counts and pilot member count/acceptable position age.
- Owner supplied an initial scale of roughly 20 trackers, starting with as few as 5, and a tentative GPS target of 5–15 minutes. Recorded these without treating them as verified performance or final acceptance criteria.
- Completed a [primary-source protocol comparison](../docs/research/protocol-baseline.md) on `research/protocol-baseline` for incorporation into `main`; resolved the research ticket. Existing Meshtastic timing settings warrant evaluation before a fork; MeshCore passive GPS behavior requires build-specific verification. Firmware selection remains open.
- Verified local Markdown links, Git whitespace checks, and ignore rules for local secrets/operational data. The local issue tracker is tracked. No firmware or hardware tests performed.

Next: confirm a usable subset of owned radio boards, GPS hardware, and 18650 cells, then agree pilot requirements. No current equipment quantities, verified expenses, field outcomes, or installation permissions have been invented.

## 2026-10-12 — Purchase-list import

- Owner added `Mesh Purchase List - Purchase List.csv` and reports retaining most, but potentially not all, listed items.
- Preserved the source CSV unchanged and imported all 32 rows with stable hardware IDs and source row numbers. Listed quantities are distinct from unknown current counts.
- Used the bundled Python CSV reader and exact decimal arithmetic to check source structure and costs. All rows have 22 fields; all 32 item rows were accounted for.
- Reconciled listed extended costs to $1,989.79; $129.00 is explicitly outside the mesh project, leaving a $1,860.79 listed mesh subtotal. These are not booked cash transactions or current stock valuations.
- Prioritized confirming radio/core variants, GPS hardware, and cells. Kept inventory and firmware-choice tickets open pending that evidence.

# Show plain-language GPS quality in tracker cards

Type: task
Label: wayfinder:task
Status: resolved
Assignee: gps-quality-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Question

How should dispatch see the quality of a recorded GPS position without technical abbreviations or an unsupported accuracy radius?

## Comments

2026-10-16 — Owner keeps the existing member position flags and requests an understandable visual quality indicator, possibly a pill. Carry existing PDOP/satellite values through ingestion and historical/latest storage. Add a shared Map/Users GPS quality pill with text and color, plus touch/keyboard-accessible explanation. Keep GPS age separate, do not infer metre accuracy or a probability, and preserve old/missing/duplicate packet behavior. No firmware changes or hosted deployment requested.

## Completion evidence

Verify wire scaling and missing values; validate optional metadata at ingestion; preserve matching position/quality across duplicate and out-of-order receipts and restart; cover pill labels, accessible explanation and independent freshness; run frontend and backend checks. Record thresholds as a provisional application policy, not field-validated confidence.

## Answer

2026-10-16 — Implemented locally. The existing tracker detail component shared by Map and Users now includes a **GPS quality** pill: green **Good** (three bars), amber **Limited** (two bars), red **Poor** (one bar), or neutral **Unknown** (unfilled bars). Text conveys the state independently of color; a native details/summary control opens a plain-language explanation with touch, click or keyboard activation. Its explanation describes the recorded fix's satellite layout, acknowledges remaining environmental errors and directs the reader to Last GPS for age. The card exposes no technical score, accuracy radius, confidence percentage or asserted current GPS lock. Satellite count appears only as supplemental reported context in the explanation.

The adapter scales positive wire PDOP by 100 and retains positive satellite count. The backend validates nullable optional fields and stores them with each historical/latest position in existing JSON fields; no schema migration/new collection. Missing/zero values stay unknown. A newer fix without quality clears the old quality rather than borrowing it. Delayed, unknown-time and future-time positions do not overwrite a newer known fix; duplicate gateway receipts do not create observations or refresh GPS age. There is no archive replay/backfill. Demo-only values illustrate the four visual states; no synthetic quality is assigned to live data.

Provisional presentation policy: dimensionless PDOP below 3 is Good; 3 through 6 inclusive is Limited; above 6 is Poor. Null/absent/nonfinite/nonpositive input is Unknown. These are broad application categories, not calibrated confidence boundaries or measured accuracy. [Trimble](https://help.fieldsystems.trimble.com/tbc/2468.htm) describes values below 3 as good and above 7 as poor; this implementation starts caution earlier, with 6 as its provisional upper Limited boundary. [NovAtel](https://novatel.com/an-introduction-to-gnss/basic-concepts/computation) explains that DOP concerns satellite geometry; other errors still matter. The [Meshtastic schema](https://github.com/meshtastic/protobufs/blob/master/meshtastic/mesh.proto) defines DOP in hundredths. Satellite count does not independently upgrade the category. Revisit the presentation bands with field evidence rather than treating them as a validated SAR reliability score.

Verification: all 48 backend checks pass with the real pinned PocketBase binary and disposable databases (initial sandbox run blocked localhost sockets; rerun outside that restriction passes). Frontend tests, TypeScript check and production build pass in both default and live build modes, including quality boundaries/absence, encrypted-wire scaling, gateway deduplication, out-of-order quality association, restart preservation, missing-quality replacement and shared Map/Users rendering. DOM tests verify the native disclosure toggles, plain text and no exposed score/radius. Browser inventory has no available surfaces; native layout, keyboard/touch behavior and visual sizing remain unverified. Existing MapLibre bundle-size warning remains.

No firmware/settings change, hardware test, field accuracy measurement, hosted deployment or commit performed. Release worker, backend hook and frontend together when deployment is authorized; review the pill visually on desktop/mobile. This resolves the local implementation task, not field validation or operational-readiness verification.

### Deployment follow-up — 2026-10-16

Owner authorizes publishing/deploying all accumulated changes. Application source `3ca3a94` is pushed to `origin/main` and deployed to the LXC, including these frontend/backend/worker changes and the separate hosted database demo. Local/server frontend and backend checks, exact public assets, protected live/demo API separation and isolated live/demo backup recovery pass. Live signal rows remain empty pending real ingestion; no synthetic rows enter live state. Native browser/WebGL/mobile and field verification remain outstanding. [Release evidence](../../../docs/operations/portal-lxc.md#gps-neighbor-maps-battery-history-and-database-demo-release--2026-10-16).

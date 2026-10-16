# Serve the demo and neighbor table from a separate PocketBase

Type: task
Status: resolved
Assignee: database-demo-neighbor-table-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Request

Keep the fork proposal parked. Build the infrastructure neighbor table with synthetic data stored in a separate inspectable PocketBase, and track the demo database in Git. Production stays on the VM with its private state outside Git.

## Comments

2026-10-16 — Owner explicitly requests implementation and expands scope to separate production/demo databases. Use a tracked synthetic seed database and a separate writable local demo runtime. Demo frontend data and mutations must use its API, including neighbor rows; no production snapshot, credentials, live traffic or firmware changes. Preserve prior working-tree changes.

## Answer

2026-10-16 — Implemented the Infrastructure Neighbor signals table and separate database-backed demo. [Run/inspect instructions](../../../backend/demo/README.md).

- `backend/demo/data.db` is a synthetic PocketBase checkpoint generated from fictional fixtures in a fresh disposable database; manifest checksum and demo marker verify it. It contains six member trackers, five fictional members, four infrastructure nodes and ten directional signal rows, plus the existing scenario observations/assignments/messages/incidents. Initialization copies it to ignored `local-data/demo/pb_data/data.db` and rebases scenario times once in storage; later launches retain dashboard/portal edits. It refuses to overwrite existing runtime files.
- View demo and local-development startup now read and mutate the separate demo API. Browser fixture fallback and application memory-only demo operations are removed. Live and demo requests use separate origins/proxies, demo tokens never become saved live sign-ins, and a non-simulation response is rejected. Unit-test fixture exports remain available for tests; page defaults are empty.
- The table supports receiver filtering and preserves direction, original source vs final-hop identity, valid zero SNR, unknown readings/relay identities, separate report receipt/hearing times and saved observations through feed loss. Samples include differing gateway reception, relayed packets and standard neighbor reports without RSSI or per-neighbor hearing timestamps. No delivery percentage or reverse-link inference.
- Additive migration creates a locked `link_observations` collection; authenticated humans receive bounded rows in state. Normal migrations never seed sample data. Production remains on the VM; raw operational data/credentials stay outside Git. The fork proposal is explicitly parked and no firmware changes were made.
- All 51 backend checks pass in the project virtual environment against actual disposable PocketBases. Frontend tests/typecheck/default live build and explicit demo build pass. Integration checks cover dashboard edits flowing into state, persistence through restart, seed integrity, existing-runtime protection, absence of samples in ordinary migrations, permissions, receiver filtering, unknown/zero values and demo/live API separation. Actual Vite `/demo-api` proxy returns ten signal values matching writable SQLite, with the synthetic worker online. Browser inventory has no available surfaces, so native visual/mobile review is unverified; existing MapLibre bundle warning remains.

The existing frontend already occupies 5173, so leave it intact and run the demo API on 8092 plus its worker alongside it. Local portal and dashboard are available; no VM deployment, commit or push performed. The demo checkpoint is added to Git tracking separately from runtime state. Before a public frontend release, provision its separate demo API route/service and apply the additive migration with the state hook. Real signal ingestion remains a separate next step.

### Deployment follow-up — 2026-10-16

Owner authorizes publishing/deploying all accumulated changes. Application source `3ca3a94` is pushed to `origin/main` and deployed to the LXC, including these frontend/backend/worker changes and the separate hosted database demo. Local/server frontend and backend checks, exact public assets, protected live/demo API separation and isolated live/demo backup recovery pass. Live signal rows remain empty pending real ingestion; no synthetic rows enter live state. Native browser/WebGL/mobile and field verification remain outstanding. [Release evidence](../../../docs/operations/portal-lxc.md#gps-neighbor-maps-battery-history-and-database-demo-release--2026-10-16).

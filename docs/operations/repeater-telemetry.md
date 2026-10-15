# Live repeater provisioning and telemetry

Deployed and verified 2026-10-14 Pacific. R001, R002 and R003 are registered in the authenticated PocketBase/portal alongside the existing two trackers and two gateways. Exact owner-provided planned coordinates stay in private provisioning and authenticated device configuration, outside Git. R002/R003 share a site; the map groups their marker while retaining separate device cards and true coordinates. Installation and coverage remain unverified.

Recorded equipment: R001/R002 Muzi whip, R003 fiberglass; each planned for four 18650 cells rated 2550 mAh per cell and a 160 mA solar cell. Chemistry, pack wiring/capacity, panel voltage/wattage and solar-input sensing are unknown. Do not infer a 10.2 Ah pack or measured solar output. Monitoring warnings remain disabled for the planned deployments pending activation and verified thresholds; telemetry ingestion/display is enabled.

## Ingestion

The receive-only worker now accepts TELEMETRY_APP only from explicitly registered infrastructure IDs. `/etc/meshlink/mqtt.json` adds `infrastructure` mappings for the three verified RAK identities; member GPS behavior is retained. Device voltage becomes battery volts, without interpreting battery level 101 as a percentage. Environmental temperature and relative humidity become Celsius and percent RH. Missing fields stay absent; finite ranges and presence are checked, including legitimate zero readings. Unsupported telemetry is ignored.

Telemetry time is preserved when it is a plausible Unix timestamp. Zero/uptime-like clocks remain unknown; arrival time is separate. Unknown-time readings can advance other unknown-time readings by receipt order but cannot replace a valid known measurement. The portal labels unknown measurement time. Actual verification reports below carried valid wall-clock timestamps; earlier post-flash R003 reports had uptime-like clocks.

Each source packet produces one observation and separate per-gateway receipts. The four live reports below each arrived through G001 and G002: eight receipts, four accepted and four duplicates, with four observations. No synthetic data was inserted into the live database.

## Provisioning and recovery

`deploy/portal/add-repeaters.py` takes staged source and root-private settings. It first tests rollback on an invalid third device and preservation of existing records in an isolated database copy. It backs up/verifies the live installation, stops services, applies the guarded transactional manual migration, merges radio identities, installs the tested source/frontend and restarts services. It does not reset the database. The manual migration is outside ordinary schema migrations; do not run demo initialization on live data.

The root-private `/etc/meshlink/repeaters.json` retains exact planned configurations. A repeat migration preserves matching identities and refuses mismatches; it is not an equipment/location update interface. Backups include this private plan, matching source and the worker spool. The restore verifier derives expected device/account counts from the actual deployment rather than assuming the earlier four-device/four-account baseline.

## Verification

- Staged backend: 39 tests pass; frontend: 8 tests, TypeScript and production build pass. Encrypted telemetry fixtures cover field presence, zero/invalid values, clocks and gateway deduplication. Transactional provisioning rollback/preservation passes.
- Authenticated live state matches all three private configurations exactly, preserving B001/B002 and G001/G002. Actual reports: R001 4.115 V; R002 4.159 V; R003 3.634 V and 19.8942°C / 36.7484% RH. Measurements at 21:34–21:38 Pacific; voltage/sensor calibration is unverified.
- Proxy authentication boundaries, throttling, public Cloudflare HTTPS/certificate/protected-route checks and isolated restore pass. Final backup `meshlink-20261015T043840Z.tar.gz`, SHA-256 `3e47036f2472dffc85c5c4674245413c289ab66201121fa57ae17144bdcef668`.

Authenticated browser visual review, sustained cadence, calibrated readings, solar input, pack endurance, installed-site coverage and off-host backup remain outstanding. See [TEST-009](../../records/field-results.md#test-009--live-repeater-provisioning-and-telemetry).

## Frontend mode correction

The owner found standalone demo data after this deployment. The staged build omitted `VITE_PORTAL_MODE=live`, selecting the previous demo default. Live records and the worker stayed correct, but API/restore checks did not exercise the signed-out browser entry. A fresh public browser reproduced six fictional trackers; the served bundle matched the staged artifact.

Production builds now default to live; local development defaults to demo, with explicit `VITE_PORTAL_MODE=demo` available for standalone builds. Invalid modes fail. Vite records the resolved mode in HTML; live provisioning rejects non-live artifacts, and the hosted verifier checks the served mode. Two regression tests cover default/explicit modes; all 10 frontend tests/typecheck/build pass. Public browser reload shows sign-in; authenticated configuration checks confirm records retained. Authenticated rendering still awaits account-holder review.

Corrected-build backup: `meshlink-20261015T045657Z.tar.gz`, SHA-256 `da3ee1a345982ed1ec0b4654857871419eb4237dbc10ed7d90886b89f55fbc7f`. Served live mode, public boundaries and isolated restore pass, preserving seven devices and eight genuine telemetry observations.

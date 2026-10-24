# Local MeshLink backend

PocketBase **0.40.5** owns authentication, SQLite storage and transactional API operations. The Python simulation/replay worker uses the standard library; the separate MQTT worker uses the pinned dependencies in `requirements-mqtt.txt`. The React portal signs in and reads saved records. Demo viewing now uses its own PocketBase with a synthetic SQLite checkpoint tracked in Git; production stays on the VM.

Native development uses fictional records. The receive-only Meshtastic GPS adapter, persistent private receipt queue and real-device cutover are implemented; see [live ingestion and deployment](../docs/operations/live-mqtt.md). All MQTT messages received under the project root are now privately archived as exact bytes plus receipt metadata, including unsupported/rejected packets; broker ACLs constrain delivery. Radio transmission, operational inbound text decoding and remote rename remain unimplemented. Member battery voltage is also normalized independently of GPS; admins can configure `batteryProfile` and `batteryCapacityMah` per device, with a frontend-only approximate charge estimate. See [member battery profile](../docs/research/member-battery-charge.md). Registered infrastructure voltage and temperature/humidity ingestion are deployed; see [verification](../docs/operations/repeater-telemetry.md).

The owner-authorized [Ubuntu LXC portal](../docs/operations/portal-lxc.md) runs this backend with service supervision, HTTPS Tunnel routing and tested isolated backup recovery. The instructions below remain local-development commands; use the deployment guides for hosted state and the explicit real-device cutover.

The hosted worker uses `MESHLINK_WORKER_CREDENTIALS` to read a separate worker-only JSON credential file, under its own OS account. Native development keeps the existing default private credentials file. No worker or admin credential is sent to the browser.

RAK `SNNS` v1/standard neighbor reports and signed sensor voltage/current are now supported. The additive `1792201000_radio_reports.js` migration creates private report deduplication storage and adds link metadata. [Contract, archive replay and verification](../docs/operations/radio-report-ingestion.md). Storage retains the literal current sign. Since MeshLink 0.1.1, the state API inverts every environment/power-channel current once to the owner-confirmed fleet convention: positive charging, negative discharging. Current entries include original `rawValue` and `currentConvention: "positive-charging"`; API consumers must not invert again. Existing caches need no rewrite. Calibration and exact sensor-path accounting remain unverified.

## Start and inspect the database demo

Follow [the tracked demo guide](demo/README.md). From the repository root:

```sh
python3 backend/manage.py install
python3 backend/demo_database.py init
npm --prefix portal ci
python3 backend/launch.py
```

The launcher runs the separate demo PocketBase on localhost:8092, its synthetic worker and Vite on localhost:5173. Local development opens demo viewing automatically; every page reads records from that database. The writable copy is `local-data/demo/pb_data/data.db`; the tracked synthetic checkpoint is `backend/demo/data.db`. Dashboard edits and portal mutations persist across refresh/restart. Initialization verifies/copies the checkpoint and rebases its scenario timestamps once; subsequent launches preserve data. It refuses to replace an existing runtime.

Inspect **http://127.0.0.1:8092/_/** with email `demo-admin@example.invalid` and password `fictional-demo-only-password`. These are deliberately public demo-only credentials; the demo guide lists portal accounts too. `link_observations` contains ten sample neighbor/gateway rows, including unknown values, valid zero SNR, differing gateway readings and unresolved relays. Production's ordinary migrations create empty collections and never seed sample rows. Live neighbor reporting is separate from these synthetic examples.

The launcher checks for occupied ports/duplicate launches and stops its children on Ctrl+C. Its logs stay in ignored `local-data/demo/logs/`. `npm run dev` alone requires the separate demo API already running; it no longer supplies browser fixtures when the database is unavailable. Vite proxies `/demo-api` to 8092, separately from the existing `/api` development proxy on 8090. A production frontend release needs its own separate demo API route/origin; no live VM deployment is part of this change.

The older `manage.py init-demo`/`serve` commands remain available for an independent private local test backend on 8090, with random credentials in `local-data/backend/`. They are not the tracked demo or a local production database. Use disposable databases for tests and keep operational production state on the VM.

## Storage and account administration

The verified binary and legacy test-backend state live under ignored `local-data/backend/`; the default demo runtime lives under ignored `local-data/demo/`. Only the deliberately synthetic `backend/demo/data.db` checkpoint is tracked. The credentials file has owner-only permissions on Linux. Keep that directory private and outside Git. Initialization stores credentials before provisioning, so a setup failure does not lose the generated secrets; it stops rather than automatically deleting or replacing partial data. Inspect the private setup log if initialization fails. Do not rerun initialization over existing pilot records.

The generated portal admin is an ordinary `accounts` record with the admin role. The worker is a separate non-superuser account with access only to heartbeat/ingestion routes. PocketBase collection writes are locked for ordinary API clients; custom routes enforce permissions. The locally provisioned PocketBase superuser is for trusted database/schema administration, not frontend or worker use. Its password is in the private credentials file; its username is `bootstrap@example.invalid`.

The legacy private local backend supports owner-run account commands using its local admin account and passwords without echo (use the demo dashboard for the separate tracked demo):

```sh
python3 backend/accounts.py create
python3 backend/accounts.py reset-password --id ACCOUNT_RECORD_ID
python3 backend/accounts.py disable --id ACCOUNT_RECORD_ID
```

A member account needs an existing member key. Registered humans share operational viewing access; members may claim only a free tracker for themselves and release only their own. Admins may transfer devices, create/disable accounts, reset passwords, configure warnings and resolve intrusion incidents. Disabling accounts preserves their earlier records. Password resets invalidate prior tokens. Worker provisioning remains local; the account endpoint cannot create worker/superuser accounts. Use the applicable PocketBase dashboard (demo: `http://127.0.0.1:8092/_/`; legacy local test backend: port 8090) for trusted provisioning of additional member/device records; no public registration is enabled.

Member map shortnames (2026-10-15): migration `1792110000_member_shortnames.js` adds optional `members.shortName` (maximum five characters), preserving existing records/roles/assignments. Account creation accepts an optional member-chosen `shortName` and saves it with the account transaction; `accounts.py create` prompts for it. Members choose/change their own value on Users through `POST /api/meshlink/profile` with `{"shortName":"CJ_5"}`. The route accepts 1–5 ASCII letters/numbers/underscores/dashes, derives the member association from authentication, rejects other fields and blocks workers/anonymous users. It changes only the member's map label; device radio short names and historical assignments are unchanged. The authenticated snapshot includes member shortnames and configured tracker `deviceType`. The migration fills missing Heltec V4 type metadata for verified B001/B002; live cutover records the known board type for newly provisioned bench devices.

The simplified user card now shows only reported battery percent; the existing admin battery type/capacity route and voltage normalization remain intact, while their card form is removed. Friendly-area resolution still needs the owner KML/KMZ dataset; the UI reports unknown rather than deriving an area from an invented boundary.

## Normalized worker boundary

See [the contract](../docs/research/portal-backend-contract.md) for collections, timestamp quality, receipt preservation, bounded snapshots, role checks and endpoint shapes. No selected-firmware packet adapter is implied.

A bounded JSONL replay can be submitted without connecting a broker:

```sh
python3 backend/worker.py --replay local-data/example-normalized.jsonl
python3 backend/manage.py worker --once
```

Every received normalized envelope creates a receipt, including duplicates and validation rejections. Only unique valid observations enter the display collections. Older/unknown/future GPS timestamps do not overwrite a newer known measurement or become fresh because they arrived recently. Contact time is independent. Historical position records capture the carrier at measurement time; dated assignments remain intact through transfers.

Infrastructure stores each observation and updates supported metrics independently. Low battery uses configured voltage trigger/recovery values only on fresh evidence. Missing reports use supported/enabled capabilities and expected cadence, with separate per-report overrides. An unsupported intrusion sensor is not an all-clear. Reported intrusion latches an incident; acknowledgment or a later normal reading cannot resolve it. Only an admin resolution note closes it. All warning, acknowledgment, recovery, configuration and incident events remain recorded.

Messages are persisted with authenticated author identity, a display-name prefix and a separate send-attempt record through exactly one designated demo gateway. The 280-character composer bound is a development guard, **not a selected firmware payload limit**. Simulated submission never asserts radio delivery or human receipt. Sending and demo name-job outcomes are disabled when `MESHLINK_SIMULATION` is unset or not `1`; the native development launcher explicitly enables it. No real radio publish path exists.

## Checks and next integration work

Telemetry clock fallback (2026-10-21, #53): unique telemetry readings are selected by valid measurement time, otherwise their original receipt time. The database keeps unknown measurement clocks null/empty with timestamp quality intact. The portal displays receipt time as the temporary measurement-time fallback, and supported telemetry health uses the same age. Infrastructure state retains actual `readingTimes` and adds per-metric `readingReceivedTimes`; `reportedAt` summarizes the effective telemetry clocks. Both snapshot samples and battery history merge measured-time and receipt-time observations before applying limits and return source/receipt clock provenance. Duplicate gateway receipts cannot advance a selected reading's fallback age. GPS and neighbor timing are unchanged; uptime is not used. [Evidence and limits](../docs/operations/battery-contact-freshness-20261021.md#receipt-fallback-correction).

```sh
python3 backend/manage.py check
cd portal
npm run check
```

Install `backend/requirements-mqtt.txt` in the test environment before the backend suite; it includes encrypted-wire adapter and durable-queue tests. CI installs these dependencies automatically. The hosted runtime uses a separate `/opt/meshlink-mqtt-venv`; the simulation worker remains a local development tool.

Backend integration tests use fresh temporary databases and the actual pinned binary, covering authorization/bypass rejection, account lifecycle, concurrent claims, original measurement age, duplicates, timestamp quality, retained invalid receipts, gateway send/outage behavior, latched intrusion, battery/missing-report rules, reconnect grace, stale name jobs and restart persistence. Tests disable rate throttling only in their disposable databases; the development schema enables PocketBase rate limits. The GitHub-hosted Backend CI workflow installs the verified pinned binary and runs the same tests without credentials or external services.

Development and production browser review covers authenticated tracking/history, assignment persistence after reload, messages and outage drafts, warnings/incidents, member controls, mobile layout and API loss while retaining observations. The portal polls an authenticated snapshot every two seconds; history is bounded to the latest 500 points per tracker within 12 hours, messages/events to 200, and other lists to 2,000. All received pilot data remains in storage. Cursor pagination, larger historical queries, realtime subscriptions and load testing follow before wider use.

Still required before operational use: sustained delivery/freshness and field evidence, real message payload/expiry policy and radio/admin gateway tests, retention review, off-host backups, and device/browser testing. The GPS adapter and LXC deployment/isolated backup recovery are implemented; consult the live deployment record for measured verification. Copying only frontend code does not back up database/files, queued receipts or private provisioning credentials. Survey and wishlist work remain deferred.

Implementation references checked 2026-10-13: [official release](https://github.com/pocketbase/pocketbase/releases/tag/v0.40.5), [migrations](https://pocketbase.io/docs/js-migrations/), [routing/auth middleware](https://pocketbase.io/docs/js-routing/), [record operations/transactions](https://pocketbase.io/docs/js-records/), [API rules](https://pocketbase.io/docs/api-rules-and-filters/) and [JavaScript handler scope](https://pocketbase.io/docs/js-overview/).

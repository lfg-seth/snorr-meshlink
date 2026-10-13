# Local MeshLink backend

PocketBase **0.40.5** owns authentication, SQLite storage and transactional API operations. The Python worker uses the standard library to submit normalized synthetic packets. The React portal can sign in and read saved records; standalone demo mode remains available.

This is a local development backend with fictional records. No MQTT connection, firmware decoder, radio transmission, remote rename, VM or external deployment is implemented.

## Start on the Dell

From the repository root, using Python **3.14.3** (the CI/runtime pin in `.python-version`) and the existing Node setup:

```sh
python3 backend/manage.py install
python3 backend/manage.py init-demo
```

The installer verifies the downloaded release archive against the tracked official SHA-256 manifest. Repeating `install` reuses a matching verified binary, even while PocketBase is running. Older installations without a verification receipt download once to compare the binary, then subsequent repeats work offline. Replacements use a staged file and atomic rename; a locked replacement leaves the existing binary intact and asks you to stop the backend first. Stop the worker/backend before an intentional version upgrade and restart them afterward. Initialization creates unique random passwords, admin/member accounts, a separate worker account, six fictional trackers and four illustrative infrastructure devices. It seeds observations through the same authenticated ingestion API used by the worker. It refuses to overwrite an existing database or credential file.

Use three terminals:

```sh
# Terminal 1: persistent API/database, bound to localhost
python3 backend/manage.py serve
```

```sh
# Terminal 2: synthetic position/telemetry updates and worker heartbeat
python3 backend/manage.py worker
```

```sh
# Terminal 3: portal with a localhost API proxy
cd portal
npm ci
npm run dev
```

Run `python3 backend/manage.py credentials` **privately** to view the generated admin and member portal logins. Open the Vite address and choose **Backend sign in**. The role preview disappears when authenticated. Reloading signs out because the browser keeps its token in memory; sign in again to see the saved assignments, messages and observations. Sign-out clears drafts and page-local selections. Worker and superuser credentials never go to the browser.

`npm run preview` also proxies `/api` to the local backend. `VITE_BACKEND_URL` may specify an explicit API origin when needed; it is a public URL, never a place for credentials. No tunnel or router changes are needed. This setup is verified on Linux amd64; the manifest includes other official release archives, whose runtimes have not been tested here.

Stop each terminal with Ctrl+C. A stopped worker becomes unavailable after a 20-second heartbeat timeout; existing observations continue aging. The demo feed override pauses the simulation producer and rejects sends, preserves warnings and unsent drafts, and does not resend on reconnect. A known outage suppresses new missing-report warnings. Reconnect grace uses each configured missing timeout, normally three reporting intervals.

## Storage and account administration

The verified binary, credentials, database, auxiliary logs and setup log live under ignored `local-data/backend/`. The credentials file has owner-only permissions on Linux. Keep that directory private and outside Git. Initialization stores credentials before provisioning, so a setup failure does not lose the generated secrets; it stops rather than automatically deleting or replacing partial data. Inspect the private setup log if initialization fails. Do not rerun initialization over existing pilot records.

The generated portal admin is an ordinary `accounts` record with the admin role. The worker is a separate non-superuser account with access only to heartbeat/ingestion routes. PocketBase collection writes are locked for ordinary API clients; custom routes enforce permissions. The locally provisioned PocketBase superuser is for trusted database/schema administration, not frontend or worker use. Its password is in the private credentials file; its username is `bootstrap@example.invalid`.

Owner-run account commands use the local admin account and prompt for passwords without echo:

```sh
python3 backend/accounts.py create
python3 backend/accounts.py reset-password --id ACCOUNT_RECORD_ID
python3 backend/accounts.py disable --id ACCOUNT_RECORD_ID
```

A member account needs an existing member key. Registered humans share operational viewing access; members may claim only a free tracker for themselves and release only their own. Admins may transfer devices, create/disable accounts, reset passwords, configure warnings and resolve intrusion incidents. Disabling accounts preserves their earlier records. Password resets invalidate prior tokens. Worker provisioning remains local; the account endpoint cannot create worker/superuser accounts. Use the PocketBase dashboard at `http://127.0.0.1:8090/_/` for trusted provisioning of additional member/device records; no public registration is enabled.

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

```sh
python3 backend/manage.py check
cd portal
npm run check
```

Backend integration tests use fresh temporary databases and the actual pinned binary, covering authorization/bypass rejection, account lifecycle, concurrent claims, original measurement age, duplicates, timestamp quality, retained invalid receipts, gateway send/outage behavior, latched intrusion, battery/missing-report rules, reconnect grace, stale name jobs and restart persistence. Tests disable rate throttling only in their disposable databases; the development schema enables PocketBase rate limits. The GitHub-hosted Backend CI workflow installs the verified pinned binary and runs the same tests without credentials or external services.

Development and production browser review covers authenticated tracking/history, assignment persistence after reload, messages and outage drafts, warnings/incidents, member controls, mobile layout and API loss while retaining observations. The portal polls an authenticated snapshot every two seconds; history is bounded to the latest 500 points per tracker within 12 hours, messages/events to 200, and other lists to 2,000. All received pilot data remains in storage. Cursor pagination, larger historical queries, realtime subscriptions and load testing follow before wider use.

Still required before operational use: selected-build decoding and verified physical identities/units, real delivery evidence and payload/expiry policy, radio/admin gateway tests, VM/HTTPS setup, service supervision, tested backup/restore, retention review, and device/browser/field testing. Copying only frontend code does not back up the database; a deployment backup plan must include PocketBase data/files and private provisioning credentials. Restart persistence has been tested; backup/restore and VM rollout have not. MQTT connectivity investigation and wishlist features remain deferred.

Implementation references checked 2026-10-13: [official release](https://github.com/pocketbase/pocketbase/releases/tag/v0.40.5), [migrations](https://pocketbase.io/docs/js-migrations/), [routing/auth middleware](https://pocketbase.io/docs/js-routing/), [record operations/transactions](https://pocketbase.io/docs/js-records/), [API rules](https://pocketbase.io/docs/api-rules-and-filters/) and [JavaScript handler scope](https://pocketbase.io/docs/js-overview/).

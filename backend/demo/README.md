# Synthetic demo PocketBase

`data.db` is a complete, deliberately synthetic PocketBase 0.40.5 checkpoint tracked in Git. It contains six member trackers, five fictional members, four infrastructure nodes, saved positions/telemetry/assignments/messages/incidents, and ten directional `link_observations`. It also includes more than 17,000 saved battery observations over 30 days: Demo ridge relay recovers with each sun cycle, Demo canyon relay loses about 0.51 V over a month despite daytime charging, and Demo dispatch gateway stays nearly steady. Open their map cards or Infrastructure battery detail and select **24hr / 7day / 30day**. The curves are illustrative, not real solar or battery measurements. The checkpoint is generated from code in `../demo_database.py`, `../demo_power.py` and `../fixtures.py`; it is never exported from production. `manifest.json` records its checksum and scenario reference time.

Fictional members have saved map shortnames AVERY, JORD, MORG, RILEY and CASEY. Assigned tracker icons use the member's shortname; unassigned trackers retain their S00X device label. These portal labels do not rename radios.

Production remains on the VM. Its database, credentials, raw MQTT and actual location tracks stay outside Git. This demo has no MQTT connection or radio command path. The fork neighbor-reporting proposal remains parked; signal rows here are synthetic examples of current gateway/NeighborInfo fields, not new firmware measurements.

## Start and inspect

From the repository root:

```sh
python3 backend/manage.py install
python3 backend/demo_database.py init
npm --prefix portal ci
python3 backend/launch.py
```

Open the portal at **http://127.0.0.1:5173**; local development opens the database demo automatically. The live build's **View demo** also selects this separate API when its demo proxy is configured. Open **Infrastructure → Neighbor signals** to view/filter saved signal observations.

Open **http://127.0.0.1:8092/_/** for the PocketBase dashboard:

- Superuser email: `demo-admin@example.invalid`
- Password: `fictional-demo-only-password`

These are public demo-only credentials, deliberately included in the fictional checkpoint. The portal accounts `meshlink-admin`, `meshlink-member` and `meshlink-member2` use that same public password. Never use these credentials for live operations or expose the development database dashboard publicly. The hosted demo serves only portal routes from its own synthetic database.

Inspect/edit `link_observations` in the dashboard. `observerDeviceId` identifies the receiver; `heardDeviceId` is nullable when a relay cannot be identified. `originalSourceDeviceId` stays separate. `signal` stores nullable `snrDb`/`rssiDbm`, preserving a real zero. `receivedAt` is report receipt; `observedAt` remains empty when the report supplies no hearing time. All frontend reads come through the authenticated state endpoint and poll every two seconds. Dashboard edits and portal changes persist in this demo.

The writable database actually served to the frontend is **`local-data/demo/pb_data/data.db`**. Open that file in a SQLite viewer too. Initialization verifies and copies the tracked checkpoint, rebasing scenario timestamps once in the database so the initial examples retain their intended relative ages. Subsequent launches preserve edits; the simulation worker keeps selected member GPS and r1/r2/b1 voltage telemetry fresh using the saved battery scenario clock and leaves signal examples aging naturally. The worker can overwrite the particular GPS/telemetry records it simulates; it does not change signal records.

The tracked checkpoint at **`backend/demo/data.db`** remains unchanged by viewing, simulation, logins or edits to the working copy. Runtime SQLite journals/logs and credentials remain ignored. Ctrl+C stops all three local processes.

## Refresh the checkpoint deliberately

```sh
python3 backend/demo_database.py build
```

This builds a fresh disposable PocketBase from fictional fixtures, then saves only its compact main database and manifest. It never copies the running demo or production. Review and commit the checkpoint with its generator/schema changes. It does not replace an existing runtime. `init` refuses to overwrite existing files; preserve an old runtime elsewhere before initializing a new default copy, or use `init --dir /tmp/meshlink-demo-review` for a separate inspectable copy.

## API separation and release

Vite proxies `/demo-api/api/*` exclusively to the demo on localhost:8092, stripping `/demo-api`. Existing `/api` and `VITE_BACKEND_URL` are the live/backend sign-in path; demo tokens remain in memory and cannot become saved live sign-ins. `VITE_DEMO_BACKEND_URL` may explicitly select a separately hosted demo API origin. Demo state must identify itself as simulation; an unavailable or misdirected demo produces an error, without browser-fixture fallback.

The LXC release uses `deploy/portal/enable-demo.py` to initialize a separate `/var/lib/meshlink-demo` working copy, a dedicated `meshlink-demo` OS account, and two systemd services. The API binds only to localhost:8092; Nginx forwards `/demo-api/api/` portal/authentication routes there and denies dashboard, raw collection and worker routes. Live routes continue to localhost:8090. The synthetic worker uses no MQTT configuration. Existing hosted demo edits survive reprovisioning; never initialize it from live state. Demo interactions share this fictional workspace with other demo viewers.

Deploy the additive `1792190000_link_observations.js` and `1792191000_battery_history_index.js` migrations with the state/history hooks. Ordinary migrations create an empty signal collection and never seed samples; real signal ingestion is a later integration. Standard backups include hosted demo state/binary/services and Nginx configuration. Run `python3 deploy/portal/verify-demo.py` on the LXC after a post-release backup to check API separation, history, token rejection by live routes, OS access boundaries and isolated demo recovery. Keep the dashboard bound to localhost and use owner SSH forwarding for inspection. [Release operations](../../docs/operations/portal-lxc.md).

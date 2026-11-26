# Live GPS and infrastructure telemetry ingestion

## Shared-channel broker overlap

MeshLink 0.5.0 adds `meshlink-channel.service` alongside the established
`meshlink-worker.service`. Keep the legacy worker running while Lee Fire
uses its existing broker. The new unit loads the same private radio mappings
from `/etc/meshlink/mqtt.json`, subscribes to CT 101 at `mqtt.spp.lol:8883`
with a distinct client ID, and drains its own SQLite receipt queue in
`/var/lib/meshlink-channel`. Its archived receipts carry the broker hostname.
The existing GPS heartbeat belongs to the legacy worker. Messages shows the
new subscriber connection separately. Both workers preserve GPS solution time.

The Messages send control requires a fresh channel heartbeat (20 seconds),
an authenticated dispatch connection, a validated G008 uplink during this
connection within seven minutes, and exactly one designated backhaul matching
the physical G008 ID. The server adds the member's map short name or account
display name, enforces 233 UTF-8 bytes, and records the authenticated account.
A manual click reserves an account-scoped UUID and radio packet ID before
opening a one-shot MQTT 5 connection. It publishes once with QoS 1, a short
expiry and retain disabled on `snorr/pilot/2/e/SNORRbench/dispatch`. A positive
PUBACK records broker acceptance. An interrupted attempt retains uncertain
evidence. Repeating its request ID reads the recorded result. No process loads
saved replies for publication. Verify delivery separately on the member radio.

For installation, provision a root-owned mode 0600 `/etc/meshlink/dispatch.json`
with the dispatch account's `password` and the full base64 `channelKey` matching
the receiver. The two live units use systemd LoadCredential. Install
[`dispatch.conf`](../../deploy/portal/dispatch.conf) as a live API drop-in and
[`meshlink-channel.service`](../../deploy/portal/meshlink-channel.service) as a
separate unit. Apply the additive send-attempt migration serially to live and
demo while their APIs are stopped. Preserve the demo unit and database.

Use the release [backup helper](../../deploy/portal/backup.py) for pre-release,
scheduled and post-release backups during overlap. It quiesces the APIs, takes
consistent SQLite snapshots of the receiving queues, and retains the established
broker sockets. Verify each archive's SHA-256 and restore live and demo in
isolation. Compare the legacy worker PID, established socket and new Lee Fire
receipts before and after. For rollback, stop and disable only the channel
unit, remove the live dispatch drop-in, restore the saved application files,
source marker and static build, reload systemd and restart the APIs. Preserve
the additive fields, queues, evidence and overlap-safe backup procedure.

### November 25 release preflight

[PR #104](https://github.com/lfg-seth/snorr-meshlink/pull/104) at `d57e85e`
passed project, portal and backend CI. The isolated release checkout on the
portal LXC passed 72 portal, 107 backend and 55 dashboard tests and built the
live frontend. The Windows portal build and targeted PocketBase dispatch
integration passed. The full Windows backend run had five errors, including
four loopback resets. The complete Linux suite passed.

The live registry and private worker configuration agree on unassigned B004
(`!a35a5fec`), B005 (`!a35b3888`) and G008 (`!9ea13cc0`), the only backhaul
with downlink enabled. A separate staged subscriber authenticated to CT 101 and
normalized traffic from both members through G008. The dispatch login passed.
At 02:46:43 UTC on November 26, the release decoder matched the exact unique
text and packet ID `fa71d48c` from a physical B004 broadcast through G008.
The COM44 library also reported a corrupt serial frame during the check.
The matched broker receipt and payload were independently verified.

The staged publisher ran under the live API service identity with its private
credential mount. Its first positive PUBACK had no matched USB evidence because
the observer excluded the MQTT-origin flag. G008 preserves that flag over RF.
A fresh marker, packet `6638c42b`, received a positive PUBACK and matched the
exact attributed UTF-8 bytes on B005 at 02:49:11.744 UTC and B004 at
02:49:11.947 UTC. Both USB observations reported `TRANSPORT_LORA` with the
MQTT-origin flag set. Both ports and the station lease closed. Production
browser acceptance requires a separate send from the signed-in Messages page.

The pre-release archive `meshlink-20261126T023122Z.tar.gz` passed SHA-256
(`82be7b1956baa278878a4c88ab54483fda29d9e6f74741838056f8f953c8baf7`)
and isolated live and demo recovery. Lee Fire's original worker process and
TCP session survived the backup, with a later receipt at 02:43:50 UTC.
The private promotion, verification and rollback scripts are staged under
`/root/meshlink-release-050` on the LXC.

The receive-only Python worker decodes channel-encrypted Meshtastic ServiceEnvelope packets from the stock `2.7.26.54e0d8d` bench. It saves normalized positions through the existing authenticated PocketBase worker API. It never publishes MQTT commands, sends radio messages or changes radio names. Registered member battery-voltage telemetry and infrastructure voltage/temperature/humidity telemetry are also decoded; unsupported packet kinds are archived without updating operational state. See [repeater provisioning and measured verification](repeater-telemetry.md).

GPS quality extension (2026-10-16; included in the owner-authorized accumulated release): the adapter now preserves positive `Position.PDOP` (wire value / 100) and `sats_in_view` as normalized `pdop` and `satellites`, attached to the same measurement. Absent/zero wire scalars stay unknown. PocketBase retains them in historical/latest position JSON, and the shared Map/Users card presents a plain-language GPS quality pill without exposing the score or claiming a metre radius. Existing member position flags stay unchanged. [Policy and local checks](../../.scratch/pilot/issues/15-gps-quality-pill.md). New worker/backend/frontend source must be released together to make the indicator available live; existing points without quality display Unknown until a new quality-bearing fix arrives. No archive replay/backfill is part of this change.

## RAK neighbor and power extension — 2026-10-16

Deployed application `bed40dd` adds strict `SNNS` v1 and bounded standard NeighborInfo decoding, transactional report/link storage and per-gateway receipt deduplication. Signed sensor current and voltage retain their literal environment source or PowerMetrics channel 1–8, separately from device battery/solar values. An explicit cutoff-bounded replay recovers only newly supported archive data with original clocks; archived payloads/outcomes stay unchanged. Live archive recovery, fresh R005 reports through G001, public/authentication boundaries and isolated backup recovery pass. [Contract, tests and release evidence](radio-report-ingestion.md). No radio configuration or hardware change; sensor interpretation/calibration and fresh G002 delivery remain unverified.

## Raw MQTT archive — 2026-10-15

Owner authorizes recording all MQTT traffic now and deciding how to use it later. The worker subscribes to `snorr/pilot/#` (the configured project root), rather than one channel/gateway pattern. Broker ACLs still determine which messages it can receive. The documented `pilot-worker` read ACL is `snorr/pilot/2/e/#`; broader topics require a broker-admin ACL update. Gateway publishing rights are unchanged.

Every delivery is stored in the private `mqtt_archive` PocketBase collection: exact binary payload encoded as base64, byte count, topic, original worker arrival time, MQTT QoS/retain/duplicate flags, stable receipt UUID, normalization outcome and bounded rejection reason. This includes other application kinds/channels, unknown sources/gateways, retained messages, malformed packets and separate gateway copies. Encrypted payloads stay encrypted in this archive; later interpretation needs the matching private channel key. Unsupported fields can be recovered from the original bytes. No automatic expiry/pruning is added.

Collection reads/writes remain locked to trusted PocketBase superuser administration. The worker has only an authenticated write route on loopback; archive data is absent from portal snapshots and public proxy routes. Raw packets, queue and database stay out of Git. The existing private backups include the archive and matching private key/configuration.

One durable queue entry holds the archive plus any existing normalized packet. Archive storage succeeds before normalized ingestion; API retries reuse the UUID, while separate MQTT deliveries retain separate records. Old normalized queue entries drain compatibly. QoS 1 acknowledgement follows SQLite commit. This does not recover past discarded packets or traffic lost before delivery; QoS 0, clean-session disconnect gaps and upstream buffering still limit completeness. Archiving does not change source validation, last-contact semantics or measurement freshness.

After deployment, run `python3 /opt/meshlink/deploy/portal/verify-mqtt-archive.py` to verify new receipts, binary lengths, database integrity and pending queue count without printing payloads. Use the standard private backup and isolated restore verification too.

Deployment verified 2026-10-15: additive migration applied, both services active, one actual new receipt captured and binary length checked with an empty pending queue. All 42 backend tests pass locally and on the LXC runtime in disposable databases. Private backup `meshlink-20261015T202742Z.tar.gz` restores the archive in isolation and passes proxy/authentication checks. Broader ACL inspection/update could not proceed: owner SSH works, but sudo requires authentication and root SSH is denied. No broker ACL was changed.

Schema/API references: [PocketBase migrations](https://pocketbase.io/docs/js-migrations/), [record operations](https://pocketbase.io/docs/js-records/), [JSON size limits](https://pocketbase.io/jsvm/interfaces/core.JSONField.html).

## Member battery support — 2026-10-15

The adapter normalizes battery-voltage telemetry from registered member nodes into observations, preserving original measurement/receipt clocks and gateway deduplication. GPS fixes/history are unchanged by battery packets. Admins select a tracker on Map and use Battery configuration to save battery type and nominal mAh capacity. The approximate 1S LiPo percentage requires an explicit profile; existing B001/B002 settings remain unknown until the installed pack is recorded. Capacity suggestions include the source-list 1000/3000 mAh and earlier owner-reported 1100 mAh size. [Lookup, sources and limitations](../research/member-battery-charge.md).

Verified on 2026-10-15: 44 backend tests pass on both runtimes, frontend tests/typecheck/live build pass in an isolated staged source tree, and deployed proxy/authentication/backup checks pass. Backup `meshlink-20261015T203735Z.tar.gz` restores in isolation. Ten archived actual packets were checked through the new decoder; none contained member voltage, so no backfill was performed and real member voltage reception is not yet measured. Live pack selection and calibration remain owner/hardware follow-ups. Existing local infrastructure UI work was excluded from this release.

## Private configuration

The owner-authorized **SNORR MeshLink — Pilot** 1Password Developer Environment stores the private channel key, existing broker worker/gateway passwords, replacement gateway Wi-Fi settings and existing portal admin/worker/superuser provisioning credentials. No passwords were rotated. Its MCP interface returns variable names, not values. Windows local environment-file mounting is unavailable through this integration; the headless LXC uses a separately provisioned private configuration. Updating 1Password does not automatically update the running service.

`/etc/meshlink/mqtt.json` is root-owned, mode 0640, readable by `meshlink-worker`. It contains `host`, `port`, `root`, `channel`, a full base64 `channelKey`, `username`, `password`, `members`, `infrastructure`, `gateways` and verified `identities`. Do not print or commit it. Existing PocketBase worker credentials remain separate in `/etc/meshlink/worker.json`. The repository's ignored `private/bench/` contains source readbacks and private provisioning inputs; these do not move between machines through Git.

Owner corrected broker SSH access during this integration: `ssh -p 64582 setheth@mqtt.snorr.org`. The previous hostname/default-port attempt timed out. The worker-only export helper reads the existing owner-private broker export and writes only the `pilot-worker` account plus endpoint metadata, without changing accounts or displaying passwords. Root-private canonical broker state remains on the broker.

Registered source-node mappings are B001/B002 → the two V4 member trackers and G001/G002 → the two V3 gateways. Hardware identity is captured from each radio separately from its mutable node ID/name. These mappings constrain ingestion; they do not provide cryptographic authentication of the member carrying a node. Channel AES-CTR has no payload authentication tag.

## Receipt and freshness behavior

- Verify TLS hostname/certificate, subscribe only to the configured encrypted channel, and accept only registered source/gateway mappings with matching envelope/topic identities. Reject retained, plaintext, PKI, MQTT-forwarded, malformed and out-of-range position packets. All received messages are archived privately before normalization; counters and service logs never include raw payloads.
- Preserve `Position.timestamp` (plus its bounded millisecond adjustment) as GPS measurement time; a zero solution timestamp stays unknown. `Position.time` is a separate device/transmit clock and is never used to refresh a fix. Future times remain future for the existing backend validation. Subscriber receipt time is distinct from gateway radio reception time. No new location is invented from contact time.
- Packet identity combines source device, radio packet ID and a digest of decrypted channel/data content. Identical copies across gateways or replays create separate receipts and one displayed observation. Reused radio IDs with different fixes remain distinct. A different payload under a reused ID is retained as another observation rather than silently losing the fix.
- Private SQLite queue `/var/lib/meshlink-worker/receipts.sqlite` survives restarts/API outages. Remove a receipt from the queue only after the backend stores its outcome. A crash after API commit can create another duplicate receipt on retry; it cannot create another displayed position. Disk failure stops the worker. Broker/radio loss before receipt is not recoverable by this queue; gateway QoS and buffering do not guarantee full history.
- Heartbeats indicate accepted broker subscription and API availability, not gateway health or fresh GPS. Broker disconnect clears connection state; a stopped worker times out after 20 seconds. Existing positions continue aging toward the agreed 15-minute stale threshold. API retries and token refresh happen without any outbound radio action.
- Infrastructure voltage and R003 temperature/humidity are integrated. Planned RAK coordinates are owner-provided configuration, not measured placement; solar input remains unmeasured. Gateway locations are absent until measured, and map markers skip missing coordinates. Both gateways remain uplink-only. No fictional battery, solar, weather, sensor or assignment data is carried into live mode.

## Deployment and cutover

1. Stage the reviewed backend/deployment/frontend source in `/opt/meshlink`, preserving private runtime state. Create `/opt/meshlink-mqtt-venv` and install `backend/requirements-mqtt.txt`. Run the backend suite there against disposable databases.
2. Read device identities/settings with `scripts/bench/read-live-settings.py`. Export only the existing worker credential using `scripts/bench/export-portal-worker.py`, then combine private inputs with `scripts/bench/build-portal-config.py`. Transfer only the resulting worker configuration to `/etc/meshlink/mqtt.json` and restrict its permissions.
3. Build/check the portal with the installed pinned Node runtime and `VITE_PORTAL_MODE=live`. That build shows sign-in before operational pages; local development can still use the explicitly labelled standalone demonstration.
   Production builds default to live if the variable is omitted. Before installing, require the `meshlink-portal-mode` HTML marker to be `live`; after installing, verify public signed-out entry shows sign-in. The owner-authorized **View demo** button explicitly signs into the separate synthetic demo API using public demo-only credentials; the header says Demo, Exit demo returns to sign-in, and refresh resets to sign-in. Nginx routes `/demo-api` to the independent localhost:8092 service, never the live API. Operational API records remain authenticated. API-only checks cannot detect an incorrectly selected standalone-demo build over a live backend. Explicit demo builds are for standalone development/review only.
4. Keep both V4s powered with GPS sky view and both V3s on working Wi-Fi. `backend/mqtt_probe.py --config /etc/meshlink/mqtt.json --seconds 300` verifies actual decoded GPS and prints only device/gateway counts and measurement ages. It requires both trackers and all four paths; missing reports block this initial cutover.
5. Run `python3 /opt/meshlink/deploy/portal/enable-mqtt.py` as root. It requires a successful live preflight, takes a private backup and runs the existing isolated restore verifier before stopping services. The explicitly staged one-time migration replaces only the expected fictional database records with four verified devices in a transaction. It refuses unexpected devices/member evidence. Demo member accounts become disabled; admin and worker account credentials remain intact. No real member roster is created.
6. The API override sets `MESHLINK_SIMULATION=0`; the worker service selects the isolated MQTT runtime and a private state directory. Deploy the reviewed production build to `/var/www/meshlink` after backing up the earlier static build. Run `python3 /opt/meshlink/deploy/portal/verify-live.py` to confirm stored positions and both trackers' two-gateway deduplication without printing tracks. Check worker restart persistence and ordinary browser rendering, then take and verify a new live backup.

The migration lives in `deploy/portal/live-cutover.js`, outside ordinary schema migrations. Stage it as `1792010000_live_cutover.js` in `/etc/meshlink/cutover-migrations` only for this authorized cutover. Never add it to normal development initialization or run it on an unknown dataset. Backup archives preserve the discarded fictional records. A repeat already-applied migration is skipped by PocketBase; the preflight/verification steps still run.

## Recovery

Updated backups stop the worker and API and include database/files, private provisioning credentials, matching source/static build, `/etc/meshlink`, the durable worker queue and current API/worker service definitions. Archives remain root-private on the LXC; an off-host destination is still outstanding. The existing verifier restores an isolated API and checks schema/data integrity and preserved records without replacing the live database.

For a failed deployment, stop both services and first archive the current state, including any real positions and queue. Restore the matching prior private backup and source/static build, restore its service definitions/configuration and ownership, reload systemd, and verify before restarting service. Removing the simulation override alone does not restore the fictional data. Do not attempt to undo a successful live cutover with a blank database or `init-demo`.

## Primary implementation references

Reviewed the [pinned stock crypto implementation](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mesh/CryptoEngine.cpp), [ServiceEnvelope schema](https://github.com/meshtastic/protobufs/blob/master/meshtastic/mqtt.proto), [Position/MeshPacket schema](https://github.com/meshtastic/protobufs/blob/master/meshtastic/mesh.proto), and [cryptography release notes](https://cryptography.io/en/latest/changelog/) for the `50.0.2` runtime pin. Runtime generated protobuf classes come from the pinned Meshtastic Python package. Live preflight remains necessary to establish compatibility with actual bench packets.

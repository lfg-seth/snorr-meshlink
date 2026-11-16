# Field portal and activity

The [November 15 site table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations)
owns the fixed locations. The portal and its activity sampler share
[the seven placements](../../portal/src/placements.json). Match physical radio IDs before
applying site names and map pins. The map shows saved field coordinates.
Shady Hollow records locally and has no scheduled backhaul, Wi-Fi or remote SD
watchdog. Ordinary radio observations can still arrive through another gateway.
The live registry continues to collect the full fleet. Users retains member
assignments. The public demo uses its separate synthetic database.

## Serving Activity

The portal serves the field dashboard from the Activity tab after live sign-in.
The existing [desktop dashboard](https://github.com/lfg-seth/snorr-meshlink/tree/8cfd518/scripts)
supplies the card layout, ordering, receipt highlights, health filters and
watchdog calculations. The portal polls every three seconds and keeps the last
cards visible on a disconnect.

Install the release's `scripts/portal-activity.py`, `scripts/watch-nodes.py`,
`scripts/server/node_readings.py`, `scripts/node-cadence.json` and
`portal/src/placements.json` under `/opt/meshlink` at the same relative paths.
Install [the service](../../deploy/portal/meshlink-activity.service) in
`/etc/systemd/system`, reload systemd, and enable and start
`meshlink-activity.service`. It reads the local live database in query-only
mode and atomically publishes the selected cards to
`/run/meshlink-activity/snapshot.json`. The existing live API checks the
account role before returning it. The demo API rejects this route.

After the [normal release checks](meshlink-releases.md), verify that the live
map and Infrastructure show six repeaters plus G002 and that Activity returns
the same seven physical IDs in roster order, including silent radios. Verify
fresh snapshot timestamps, demo isolation and an anonymous request denial.
For rollback, stop and disable the sampler and restore the previous application
and static build under the deployment lock. The release writes no roster or
telemetry migrations.

## Production deployment

On November 15, 2026, the owner confirmed all seven placements, retained the
existing uppercase radio short names, and selected live deployment. The site
names are the portal's display names. The last available NodeInfo advertised
the earlier radio names for six placements. R001 had no NodeInfo receipt in
the checked window. The release changed no radio configuration.

[PR #71](https://github.com/lfg-seth/snorr-meshlink/pull/71) merged as
`e375a328fba6ef184a9edf6cf2b2023ec189b896`, tagged `meshlink-v0.4.0`.
Main and tag CI passed. The LXC built that clean commit in live mode on the
pinned runtime and ran the portal, backend and dashboard suites. Application
promotion under the deployment lock preserved hashes for the quiesced live
and demo databases, credentials, worker queue and configuration. Rollback
files are under `/opt/meshlink-rollback-field-e375a32`.

The served versions of all ten build files matched the staged hashes over
public HTTPS. Authenticated Edge checks found the seven correct map markers,
Infrastructure cards and Activity cards, in the expected card order. Filtering,
expanded details, advancing snapshots, retaining cards through a disconnected
browser and recovery passed. At 390 CSS pixels the cards used a single column.
Anonymous requests and demo tokens could not read live Activity. The demo
endpoint rejected the signed-in demo account's Activity request.

All seven services were active. The archive gained a fresh receipt, the last
200 checked envelopes were normalized and the durable worker queue was empty.
At 18:46 Pacific the live sampler assessed R010 as needing attention. At 18:50
R010 was reporting and the other six remained silent. These are receipt-based reporting states. Field coverage,
power and runtime require their own observations.

The clean release passed 67 portal tests, type checking, the production build,
94 backend tests and 42 dashboard tests on the LXC. Windows full-suite runs
encountered intermittent loopback connection resets. The member short-name
test passed separately. The archive authorization test also reset on a local
retry and passed on the release host and in GitHub CI.

Both full backups passed SHA-256 verification, isolated live and demo database
integrity, identity and API recovery checks. The post-release archive contained
the exact sampler, cadence file, placements and service definition. The live
sampler resumed fresh snapshots after the backup. Private receipts establish
that all seven placements were heard at least once since the morning registry
cutover, before or after installation. They do not establish continuous
delivery at the field sites.

| Backup | SHA-256 |
| --- | --- |
| `meshlink-20261116T023535Z.tar.gz` | `4c411e41384922c355e4e5d0df659bd26abe4815a75ba7a5a1f0a4e6615b86bd` |
| `meshlink-20261116T024644Z.tar.gz` | `b5210a5e2741965b9b5c123986064a2c71514cb005e8259499e5e35629b21ef5` |

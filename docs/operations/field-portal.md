# Field portal and activity

The [November 15 site table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations)
owns the seven saved radio pins. G001 at Lee Fire Station uses the deployment pin
supplied by the owner on November 15. The live registry for physical radio `!1bbf0638` stores the
coordinates with `locationSource=owner-deployment-pin` and
`locationLabel=Lee Fire Station`. Keep these coordinates in private backup
and recovery data. The portal and its activity sampler share
[the field placements](../../portal/src/placements.json). Match physical radio IDs before
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
map and Infrastructure show six repeaters, the Lee Fire Station backhaul G001
and offline recorder G002. Activity returns the same eight physical IDs in roster order,
including silent radios. Verify
fresh snapshot timestamps, demo isolation and an anonymous request denial.
To roll back 0.4.1, hold the deployment lock, stop the live sampler and
writers, and restore the saved 0.4.0 application, static files and sampler.
Restore G001's four prior location fields from its private pre-deployment
configuration, preserving later telemetry. Restart the services and verify
the previous seven-card snapshot.

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

## Lee Fire Station deployment

MeshLink 0.4.1 deployed November 15 at `bac80fd04531735ef13182692028a05266e00157`
with tag `meshlink-v0.4.1`. The field report identifies G001 as the Lee Fire
Station Wi-Fi backhaul. Its owner-supplied pin is in the authenticated live
registry. The deployment matched the physical radio before writing the
coordinates, source and site label. The previous release files are under
`/opt/meshlink-rollback-field-bac80fd`. [Field report](../../records/aar/2026-11-15-mount-charleston.md)

The public HTTPS version and all ten asset hashes matched the staged release.
The signed-in state returned the exact supplied coordinates. Edge showed eight
map pins, eight Infrastructure cards and eight Activity cards. The Activity
filters, single-column mobile layout and recovery after disconnect passed.
G001 reported online, and its Activity card included gateway, Wi-Fi and SD
watchdogs. The other gateway, G002, retained its offline recorder role.
All seven services were active. The archive gained a fresh receipt during the
check, all 200 recent envelopes were normalized, and the worker queue was empty.

The release host passed 68 portal tests, type checking, the live build, 94
backend tests and 42 dashboard tests. Main and tag CI passed. Both backups
passed SHA-256 verification and separate live and demo recovery checks. The
restored live database contained the owner's exact G001 pin and provenance.

| Backup | SHA-256 |
| --- | --- |
| `meshlink-20261116T031939Z.tar.gz` | `022423b9de4a00f2b0330c9d52d1edc2c9874240eb98934a96ba67081dfb3ced` |
| `meshlink-20261116T033213Z.tar.gz` | `69192d2207a5f9297bc303143a5dbd82f64ddcdfe2429bdbd48c992fb080abe1` |

## Remembered sign-in and Activity row order

On November 16 the production LXC moved from 0.4.1 to `meshlink-v0.4.2`
at `dd1b036ab2fac3563413691bf795afbcd1a6c158`. The release includes the
Activity fix at `159a3a1`. All 69 portal tests, 95 backend tests, 42
dashboard tests, type checking and the production build passed on the host.
The deployed backend hook matched the release file and all ten publicly
served build files matched the staged hashes. [Release PR](https://github.com/lfg-seth/snorr-meshlink/pull/74)

The public HTTPS form had a checked remember option and approximately 44 CSS
pixels between field borders at both 1280px and 390px. Production password
authentication issued a 30-day token for a remembered login and a one-hour
token for a shared-device login. Both accessed protected state. A temporary
read-only SSH test connection kept the production password and bearer token
on the LXC while a disposable Edge profile exercised the deployed form with a
test handle. One sign-in survived a full browser restart. Sign-out persisted
across a second restart. All eight live Activity cards appeared, and 15
reading rows in an expanded card kept their order and vertical positions
across two snapshot updates.

All seven services passed. The MQTT archive gained two receipts during the
check. Of 200 recent envelopes, 199 were normalized and one was unsupported.
The worker queue was empty. Promotion under the deployment lock preserved the
quiesced live and demo database, credential, queue and configuration hashes.
Prior application files and their install manifest are in
`/opt/meshlink-rollback-field-dd1b036`. Rollback restores 0.4.1 assets and
backend source together. Already-issued credentials retain their expiry.

Both backups passed SHA-256 and isolated recovery checks for the live and
demo databases. The post-release archive contained the exact deployed login
hook and portal version marker.

| Backup | SHA-256 |
| --- | --- |
| `meshlink-20261116T204952Z.tar.gz` | `c1b7a3add7d5b87ec3bac5f8f3c99d88e81352cd8ba5a782118e24b479a73198` |
| `meshlink-20261116T205547Z.tar.gz` | `853894fdca3103327cb857406378e4c88753780f52fcf8051d77f9f6e0b8c571` |

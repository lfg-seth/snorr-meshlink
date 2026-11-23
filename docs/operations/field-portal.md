# Field portal and activity

## November 23 member tracker Activity deployment

MeshLink 0.4.16 is live at tagged main commit
`35a309af05da3db619f0cbacb2b726d9b3e09687`.
[PR #100](https://github.com/lfg-seth/snorr-meshlink/pull/100) adds member
GPS and telemetry to Activity. PR, main and tag CI passed. The exact release
on the host passed 101 backend tests, 72 portal tests, 55 script tests,
typecheck, the live build and installed migration parity.

All ten public files matched the build, anonymous Activity returned 401 and
all seven services were active. The signed-in renderer showed eleven node
cards, including two member radios, and eight recent packet tiles. The feed
included a client node-info transmission. A new original packet matched its
archived receipt after service startup, and retained routes stayed stable.
Application table counts and private configuration and queue hashes matched
across promotion. Previous files are retained under
`/opt/meshlink-rollback-field-35a309a`.

Two earlier promotion attempts restored 0.4.15 automatically. The first
exposed a misencoded route separator in the verifier. The second received
a fresh packet, then timed out waiting for another within four minutes.
The corrected check matches a post-startup feed entry to its original archive
receipt and compares retained entries across refreshes.

| Backup (UTC) | SHA-256 |
| --- | --- |
| 20261123T174940Z | `3c00bd9f529d630c1c0070c81f2301ae00a5d3e24b09259249d98863b9aa7a94` |
| 20261123T180547Z | `d3217a0ff9da7cbf4a4af29c1c6f1e396b73bb9f79d14c159c38728d3ba4a6b7` |

Both backup checksums and all four isolated live/demo restores passed.
The public asset, service, authenticated render and fresh receipt checks
passed again after the post-release backup restarted the services.
Both member cards had stored GPS and telemetry, and one had a current
assignment. A check ending 270 seconds after promotion observed no new client
GPS or telemetry packet. Confirm those feed entries when a member radio next
reports through a gateway.

## November 21 member map restoration

MeshLink 0.4.15 ships [PR #98](https://github.com/lfg-seth/snorr-meshlink/pull/98)
at tagged main commit `b94fc05bb91f2bafcadb495b62562d23ff7b8c56`.
The November 15 field-placement view had passed an empty tracker list to the
signed-in map. The live map now plots trackers with recorded positions and
includes those positions in both its opening bounds and Fit area.

A signed-in Edge check reproduced the missing markers on 0.4.14. The same check
on the served 0.4.15 map found both positioned member trackers alongside eleven
infrastructure pins and opened the reported member's pin. The regression test
covers the assigned map label, initial bounds, Fit area and a tracker awaiting
its first position. PR, main and tag CI passed, as did the exact release-host
portal, backend, dashboard and migration-parity checks. All ten public files
matched the build. Seven services were active, and fresh archive and Activity
receipts arrived. The previous application files are retained under
`/opt/meshlink-rollback-field-b94fc05`.

Both release backups passed SHA-256 and isolated live/demo restores. The signed-in
map check passed again after the post-release backup restarted the services.

| Backup (UTC) | SHA-256 |
| --- | --- |
| 20261121T211912Z | `dddad652cb8d4eec06a52068af120b033fa7b00002d9aed2b85e26bf45ab62d0` |
| 20261121T212511Z | `63a9dcdbd32210e347812f5b813258b26b9e037933a8b3fa8866006c80772f3b` |

## November 17 compact Activity routes

MeshLink 0.4.14 is deployed from tagged main commit
`095c2c9305b71074c2285715398e1b6aae7386ea`.
[Route and layout PR #95](https://github.com/lfg-seth/snorr-meshlink/pull/95)
and [final alignment PR #96](https://github.com/lfg-seth/snorr-meshlink/pull/96)
capture the owner's preview refinements. Packet cards show their first receipt's
hop count, last identifiable relay and MQTT gateway. Long names take precedence;
unnamed radios use full mesh IDs, and an ambiguous relay byte adds no invented
identity. Duplicate gateway copies retain the original route. Main cards combine
last heard and route details beside the short name.

The row fits four phone, six larger portrait and eight wide-screen cards.
Cards size to their content, with larger text, type/time at the top and routes
at the bottom. The refreshed local/Tailscale preview was inspected. WebKit and
Edge fit 4/4/4/6/8/8 complete cards without content or page overflow at
320/382/580/669/951/1440 CSS pixels.

The exact release commit passed all 100 backend, 72 portal and 54 script tests
on the host, plus typecheck, clean live build and installed migration parity.
PR, main and tag CI passed. No migration or radio protocol change was needed.
Promotion preserved existing application table counts, private configuration
and worker-queue hashes. Previous files and modes are retained in
`/opt/meshlink-rollback-field-095c2c9/files.json` for rollback to 0.4.13.

The first live check matched all ten public file hashes, verified anonymous
Activity returns 401 and found all seven services active. Authenticated rendering
showed eight packet cards from 48 unique transmissions, eleven node cards and
ten fixed pins. It verified the compact text for Direct, relayed and Gateway
receipts, observed a new original packet and confirmed retained packet routes
and first receipt times stayed unchanged.

| Private LXC backup | SHA-256 |
| --- | --- |
| Before `meshlink-20261117T182832Z.tar.gz` | `b66a793899d1b6e8f4ca4e683397c9f71e3097206edcf3cb0b7462e2ec5dfc2b` |
| After `meshlink-20261117T183734Z.tar.gz` | `4f4b600eca2cff5aeba6e936054e8e5de504500766be518146d4e74c43da65cd` |

Both archives passed checksum verification and isolated live/demo recovery.
After the final backup restart, the public hashes, seven services, compact
authenticated rendering and another newly received original packet passed again.
The signed-in physical handset fold remains a separate acceptance check.

## November 17 recent packet row

MeshLink 0.4.13 shipped from tagged main commit
`9ff127dfb77447c11149e441e098672a32cf01d7` after owner review of the
phone preview. The production sampler publishes the 48 most recent original
transmissions heard from the field roster within the past hour. The signed-in
Activity row renders as many as fit, newest first. Gateway copies share
one packet identity. Separate transmissions keep their own receipt times.
[Release PR #93](https://github.com/lfg-seth/snorr-meshlink/pull/93).

The release host passed 100 backend, 72 portal and 54 script tests, typecheck
and a clean live build. PR, main and tag CI passed. The rollout verified
installed migration parity, application table counts, protected configuration
and worker-queue hashes. The rollback manifest and prior files are at
`/opt/meshlink-rollback-field-9ff127d/files.json`.

All ten public files matched the release build, anonymous Activity returned
401 and all seven services were active. The authenticated check observed an
advancing packet feed, unique IDs in newest-first order and stable first
receipts for retained packets. The released view rendered twelve packet cards
from 48 transmissions, eleven node cards and ten fixed map pins.

| Private LXC backup | SHA-256 |
| --- | --- |
| Before `meshlink-20261117T175113Z.tar.gz` | `745e94448fdc6d283e24f5c0353792ea7426b47165699fc4d878f38d90e491ac` |
| After `meshlink-20261117T175606Z.tar.gz` | `8e5b1167c6740d5fc240bfb45beeef7e990a9943559823c28ebd1e3b3bc95528` |

Both archives passed SHA-256 verification and isolated live and demo recovery.
After the final backup restart, the public hashes, seven services,
authenticated renderer and another newly received packet passed again.
The signed-in physical handset fold remains a separate acceptance check.

## November 17 Sahara roster update

**MeshLink 0.4.11** at tagged main commit
`fbf161aa7bc53fd9187174ffa929daea26a421c3` adds **R009 / Sahara** to the
map, Infrastructure and Activity. Its live registry records the supplied pin,
Case 12, eight cells and Muzi while retaining physical identity and history.
The live sampler and released renderer now show eleven cards.
[Release, validation and remaining field gates](r009-sahara-deployment.md#portal-and-activity-update).

The [November 15 site table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations)
owns the seven saved radio pins. G001 at Lee Fire Station uses the deployment pin
supplied by the owner on November 15. The live registry for physical radio `!1bbf0638` stores the
coordinates with `locationSource=owner-deployment-pin` and
`locationLabel=Lee Fire Station`. Keep these coordinates in private backup
and recovery data. The release history below describes the previous bundled placements. Match physical radio IDs before
applying site names and map pins. The map shows saved field coordinates.
Shady Hollow records locally and has no scheduled backhaul, Wi-Fi or remote SD
watchdog. Ordinary radio observations can still arrive through another gateway.
The live registry continues to collect the full fleet. Users retains member
assignments. The public demo uses its separate synthetic database.

## Updating the live field roster

To update the field roster in MeshLink 0.4.12, open the live PocketBase
`field_roster` collection through the existing private superuser connection.
Create or edit one record per physical radio. Enter its lowercase `!xxxxxxxx`
radio ID, short name, display name, kind and numeric sort order. Use
`repeater`, `stationBackhaul`, `offlineRecorder` or `mobileGateway`.
For a fixed site, enter the approved coordinates together in the JSON `pin`
field as `latitude` and `longitude`. A station can keep its existing
registry pin when its source and site label match. Mobile gateways appear
in Activity only. Removing a roster record withdraws it from the field views
and preserves device history.

The signed-in portal reads these rows on its normal state refresh and joins
them to registered infrastructure by radio ID. The Activity publisher checks
the same collection each sampling cycle (three seconds) and reloads its
selected radios and recent readings in process after an edit. A silent radio
can have a card before it has a receipt. Provision a new physical device and
its MQTT mappings through the existing intake process to receive telemetry.

For the first rollout, take the normal private backup, apply the PocketBase
migration and deploy the API hook, frontend and sampler together. The migration
seeds ten fixed placements and the G003 mobile card. Verify an authenticated
state refresh and Activity snapshot against the saved roster. Subsequent
roster edits take effect while both services are running. Roster data is
included in the normal PocketBase database backup. For rollback, preserve
that backup and restore the previous application files and placement file.

## November 17 field roster and radio routes

MeshLink 0.4.12 went live at tagged main commit
`1be8509cf54eb08befc38f3afa1041e6d20a1762`. The authenticated portal and
Activity sampler use the same eleven roster entries. The released renderer
verified ten fixed pins, eleven cards and route text in Readings and Timers.
The first successful production sample contained four Direct, four Relayed
and three gateway-local reports. [Combined PR #91](https://github.com/lfg-seth/snorr-meshlink/pull/91).

The deployment host passed 99 backend tests, 71 portal tests, typecheck, the
live build and 54 script tests on that commit. PR, main and tag CI passed.
Edge and WebKit preserved scroll and route text across synthetic refreshes at
382 and 740 pixels. All ten public files matched the host build. Seven services
were active and a new MQTT receipt reached the archive.

The additive migration seeded eleven rows on each database under the deployment
lock. Existing application table counts and private configuration and queue
hashes matched across migration. The demo worker initially started before its
API was listening. The first promotion restored the previous application files
and retained the migrated rows. The successful retry verified both migration
records, reused the original rollback manifest and waited for each API's health
endpoint before starting workers. Rollback files and original modes are at
`/opt/meshlink-rollback-field-1be8509/files.json`. Retain roster rows and any
later operator edits when restoring the earlier application.

| Private backup on the LXC | SHA-256 |
| --- | --- |
| Before `meshlink-20261117T164027Z.tar.gz` | `a0174a8298c2303d24754b9becb7d854f94a022a73ecf41f771cfa07202249d1` |
| After `meshlink-20261117T165140Z.tar.gz` | `b3a2779abecc8834a3057a106622586a333656aad687033affa4d1d972876171` |

Restore the archived PocketBase data directory together with its matching
SQLite write-ahead log. An isolated read of the post-deployment live database
and WAL verified the migration record and all eleven roster rows, field for
field, against the running database. Both full archives passed checksum and
isolated live and demo recovery. After the final backup restart, the signed-in
cards, map pins, seven services, public hashes and new receipt all passed again.

## November 16 portal appearance release

Production serves MeshLink 0.4.10 from tagged main commit
`dd5b65c74b4e8ebb26aa7f728a5d8da18aa7e598`. The portal, backend and sampler
source matched the tested desktop preview. The change installed frontend source,
release metadata and static files. It required no database migration. The previous
frontend and a file-by-file rollback manifest are in
`/opt/meshlink-rollback-field-dd5b65c`. Older hashed assets remain available to open tabs.
[Release PR](https://github.com/lfg-seth/snorr-meshlink/pull/86).

Portal and backend CI passed on main and the tag. The release host passed its
portal, backend and sampler suites. The first promotion automatically restored
0.4.9 when the public edge returned 403 to the Python HTTP client. The release
host reproduced this on 0.4.9 and obtained 200 for the same files with the
existing curl verifier. The retry confirmed that all ten files served over
public HTTPS matched the tagged build byte for byte.

The deployed renderer showed readings and timers for all ten nodes from the
current production sampler. Anonymous HTTPS Activity returned 401. Seven
services were active and a new MQTT receipt entered the archive. WebKit on
Windows verified that the public portal follows the device appearance and
remembers a Light override across reload. At 382 × 580, WebKit and Edge
preserved the user's scroll position through four three-second production
bundle refreshes with browser-local synthetic readings. A physical Duo fold
and a signed-in handset scroll remain unverified.

Both archive checksums and isolated live and demo restores passed. The twelve
installed backend hooks and eight migration files matched the tagged source.

| Backup | SHA-256 |
| --- | --- |
| Pre-release `meshlink-20261117T065201Z.tar.gz` | `3ebbb703fd1ae11ff6c107fa501cd064d535b3a80819491c2de60319839c7dc0` |
| Post-release `meshlink-20261117T065732Z.tar.gz` | `20f7ade69b073c226ba9777d5a44c915f2a0e3ad77151d0ab7164f1a74bb5757` |

## Activity packet routes

The route line in Readings and Timers describes the receipt selected for
**Last heard** and **through**. On a timestamp tie the first attributed gateway
keeps its place. When recovering a saved database contact, the sampler looks
up its gateway and receive time in the raw MQTT archive and verifies the
original source and normalized packet key. Multiple matching envelopes leave
the route unknown. Each newer contact replaces all route fields together.
Reports originating at the uplinking gateway appear as **Gateway-local report**.

The pinned firmware sets the original hop budget and writes the transmitter's
relay byte. The receiver extracts both three-bit hop fields and the relay byte
from the radio header. The gateway's encrypted MQTT envelope carries the
received packet with the gateway's own ID. The gateway can also publish its
own outgoing packet before radio transmission. [Transmit path](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/Router.cpp#L343-L390), [radio receive path](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/RadioLibInterface.cpp#L645-L654), [gateway receive path](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/Router.cpp#L732-L836), [MQTT envelope](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mqtt/MQTT.cpp#L822-L844).

**Reported hops** is the starting limit minus the remaining limit, with both
values in 0–7 and the remaining limit at most the start. A zero start requires
the optional bitfield in the decoded payload to establish sender support. In
that case the receiver has discarded the relay byte, so the count can be zero
with reception still Unknown. The first forward decrements the limit. Later
forwards can preserve it when the forwarding node and the previous relay
have ROUTER, ROUTER_LATE or CLIENT_BASE roles and the previous relay matches
a favorite. Physical relays can therefore exceed reported hops.
[Firmware hop calculation](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/NodeDB.cpp#L1675-L1691), [role checks](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/Router.cpp#L85-L133), [forwarding](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/NextHopRouter.cpp#L135-L159).

**Direct** requires RF evidence, a zero difference and a usable byte matching
only the sender in the known roster. **Relayed** requires RF evidence and a
positive difference. Its last relay is labeled **roster candidate** only when
the byte matches one named radio distinct from both source and gateway. The
lookup includes known radios outside the displayed fleet and treats IDs ending
in `00` and `ff` as a possible collision. Unknown radios can share the same byte.
[Packet fields](https://github.com/meshtastic/protobufs/blob/6b1ded439633cd03d4af85b44231b91d1d106278/meshtastic/mesh.proto), [byte encoding](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/NodeDB.h#L215), [neighbor telemetry limits](../research/node-neighbor-telemetry.md).

## Serving Activity

The portal serves the field dashboard from the Activity tab after live sign-in.
The existing [desktop dashboard](https://github.com/lfg-seth/snorr-meshlink/tree/8cfd518/scripts)
supplies the card layout, ordering, receipt highlights, health filters and
watchdog calculations. The portal polls every three seconds and keeps the last
cards visible on a disconnect.

Activity marks a node Attention when one scheduled stream misses three consecutive
cycles or contact misses three cycles of the shortest scheduled interval. Four
missed contact cycles mark it Silent. Both thresholds include three seconds of
grace. Individual timers still show earlier misses. Repeater cards omit GPS,
NeighborInfo and NodeInfo. SNNS neighbor reports retain their own timer and
readings. A reported Wi-Fi or MQTT Down value displays in red.

For the original file-based release, install `scripts/portal-activity.py`, `scripts/watch-nodes.py`,
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

## November 16 Activity health update

[Release 0.4.5](https://github.com/lfg-seth/snorr-meshlink/pull/78) changed
the Attention and Silent thresholds, removed GPS from repeater cards and
corrected the Wi-Fi and MQTT Down colors. [Release 0.4.6](https://github.com/lfg-seth/snorr-meshlink/pull/80)
also excludes standard NeighborInfo and NodeInfo from repeater cards. An
offline ten-node sampler fixture confirmed that the six repeater cards kept
SNNS and ignored overdue excluded streams. The four gateways retained their
stream selection. The tagged release passed portal and backend CI and the
isolated release-host build and dashboard checks.

Production serves `meshlink-v0.4.6` from `06e56cd`. The host passed 70
portal, 95 backend and 43 dashboard tests. Public HTTPS returned the staged
bytes for all ten build files. The authenticated endpoint returned all ten
cards with the expected contact and stream health, and all six repeaters
retained their SNNS timers. All seven services were active and a fresh MQTT
receipt arrived. Promotion preserved the quiesced private state hashes.
The rollback for this change is `/opt/meshlink-rollback-field-06e56cd`.

The following 0.4.6 deployment backups passed SHA-256 verification and
isolated live and demo recovery.

| Backup | SHA-256 |
| --- | --- |
| `meshlink-20261117T032428Z.tar.gz` | `8d2e58f8bf88f131dcda613e93156fb748e7e2b13e2e278803a7bd737d81a7d9` |
| `meshlink-20261117T032904Z.tar.gz` | `055c34b29dfe8f1c7deab59b636997518e78046a0077fb6b4ba9e9c1b6ac683f` |

## Terry Home gateway deployment

MeshLink **0.4.3** deployed from `31a905b` on November 16 Pacific.
[PR #75](https://github.com/lfg-seth/snorr-meshlink/pull/75) adds physical
radio **!b03d6790** to the field roster. The live registry retains the original
row and source/gateway mappings. Signed-in Edge verified the approved pin,
equipment card and Activity entry. [G006 configuration and receipts](g006-terry-home.md).

Main and tag CI, type checking, the production build and the release host's
70 portal, 95 backend and 42 dashboard tests passed. All ten public file
hashes and seven services passed. The pre- and post-deployment archives both
passed separate live and demo recovery checks. The restored live registry
contained the approved G006 pin. The post-deployment archive SHA256 was
`4e0ea7c30c461a06c1eb3c9e87c9283aeecda0d8e428da2d74951be37e5ddc38`.
Rollback files are under `/opt/meshlink-rollback-field-31a905b`.

## Activity reading pills

On November 16 Pacific, MeshLink 0.4.7 deployed from tagged main commit
`e7ed8b72564716a13b4ddbd237c0eed609815e4e`. The authenticated production
snapshot rendered both views for ten cards. Eight supplied battery current
as a headline. The other two supplied no INA current sample. The verifier
checked for duplicate labels, exact uptime seconds and the stream exclusions.
All ten public build files matched, seven services were active and a fresh
MQTT archive receipt arrived. The promotion retained the quiesced data and
configuration hashes. Rollback files are in `/opt/meshlink-rollback-field-e7ed8b7`.

Portal, backend and dashboard checks passed in the isolated release checkout,
and portal and backend tag CI passed. The Windows portal tests passed. Local
Windows backend integration encountered loopback connection resets.

Both archives passed checksum verification and isolated live and demo recovery.

| Backup | SHA-256 |
| --- | --- |
| `meshlink-20261117T034702Z.tar.gz` | `1d9ccfd9ffe4111efacbb21d23a7e1a9ff4bf20ea6be13f778b03113d800e7fc` |
| `meshlink-20261117T035344Z.tar.gz` | `7259d01e98ded9df8894cc6b9ad542e0e89a1297a3a3448d0b0995ca7cc1170a` |

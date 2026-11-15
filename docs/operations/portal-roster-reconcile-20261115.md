# Portal physical-roster reconciliation — 2026-11-15

Owner explicitly requests the portal mappings match the fresh roster, each
radio's history be preserved, and all nodes be checked for correct ingestion.
Applied from the reviewed one-time script at **2026-11-15 06:40:24 Pacific**.
Application source remains **62dcc0bfe70984332a9ffe5646238d8224320e7c**
(MeshLink 0.3.1); no application release, firmware, radio profile, key, physical
placement or power change was performed. API and worker were briefly stopped
under `/run/lock/meshlink-deploy.lock` for the transactional data/configuration
change. Existing queued receipts were drained using the original mappings first.

## Result and scope

All **16 current transmitting-device identities** now agree between the portal
device registry and private ingestion worker: R001–R011, G001–G003 and B002/B003.
The portal has **20 device records**: those 16 plus four explicitly identified
legacy V3 entries. MC00 `!9ea0432c` is the dedicated receive-only sniffer; no
ordinary portal telemetry or MQTT uplink is expected from it, so it was not
registered as a transmitting member or repeater.

Authenticated public HTTPS state returns all 14 current infrastructure entries
under the correct physical radio IDs and the unchanged B002/B003 member-device
identities. At **2026-11-15 07:06:16 Pacific**, new accepted receipts
verify **5 of 16** current sources. Fresh reception is
not established for **R002, R003, R004, R005, R006, R007, R008, R009, R010, R011, G003**; historical replay is explicitly excluded
from that count by original receipt time. A correct mapping alone is not proof
that a silent or held radio is transmitting.

| Current label | Physical radio | Fresh accepted / duplicate copies since cutover | Live evidence |
| --- | --- | ---: | --- |
| B002 | !699ca878 | 25 / 31 | Fresh accepted RF/uplink receipt |
| B003 | !699c2ed8 | 7 / 9 | Fresh accepted RF/uplink receipt |
| G001 | !1bbf0638 | 25 / 31 | Fresh accepted RF/uplink receipt |
| G002 | !1bbf0ab8 | 6 / 12 | Fresh accepted RF/uplink receipt |
| G003 | !849ad7a0 | 0 / 0 | Mapped; fresh reception not observed |
| R001 | !f95b5501 | 2 / 4 | Fresh accepted RF/uplink receipt |
| R002 | !05237743 | 0 / 0 | Mapped; fresh reception not observed |
| R003 | !b4d6bc9f | 0 / 0 | Mapped; fresh reception not observed |
| R004 | !49ac6d7f | 0 / 0 | Mapped; fresh reception not observed |
| R005 | !a65601b3 | 0 / 0 | Mapped; fresh reception not observed |
| R006 | !638b9515 | 0 / 0 | Mapped; fresh reception not observed |
| R007 | !b456f760 | 0 / 0 | Mapped; fresh reception not observed |
| R008 | !120b04fd | 0 / 0 | Mapped; fresh reception not observed |
| R009 | !da581e5f | 0 / 0 | Mapped; fresh reception not observed |
| R010 | !77fdb9f1 | 0 / 0 | Mapped; fresh reception not observed |
| R011 | !8737c2c9 | 0 / 0 | Mapped; fresh reception not observed |

No fresh-source `unknown source` archive rejection or backend rejection is
observed in the checked post-cutover window. All six production/demo/proxy
services are active. Worker queue at final inspection: **0**.
R009's unknown source clock remains a firmware/GNSS follow-up independent of
identity; B003 is the survey tester with deliberately suppressed position RF.
Held R003 and the receive-only MC00 are not promoted to field acceptance.
Any current survey quiet period or offline power condition must be cleared by
the hardware owner before missing sources can pass a fresh RF check.

## Identity migration and history preservation

The failing pre-change verifier reproduced 12 mismatches: all eleven R labels
and mobile G003. The old worker radio-to-key mapping, registry configuration,
fresh physical roster and real archived packets were compared. For all six
previously enrolled repeaters, an actual archived source packet decoded to
the old key and matched a stored normalized receipt. This also establishes
R005's old physical source despite its missing registry `radioNodeId` field.

Existing records are moved by physical radio, using these simultaneous key
substitutions. SQL unique keys use a collision-free intermediate namespace.

| Previous portal key | Reconciled key |
| --- | --- |
| r001 | r005 |
| r002 | r007 |
| r003 | r002 |
| r004 | r010 |
| r005 | r001 |
| r006 | r009 |
| r007 | r004 |
| r008 | r006 |
| r009 | r008 |
| g003 | legacy-v3-9e9f167c |
| g005 | legacy-v3-9ea039cc |
| g006 | legacy-v3-b03d6790 |
| legacy-v3-849ad7a0 | g003 |

The r007/r008/r009 rows were unassigned planned-site placeholders, not radios.
Each was checked for empty readings/contact/position and zero scalar, JSON or
composite history references before reuse as newly enrolled R004/R006/R008.
Their complete original planned configurations were archived root-private.
R003 and R011 were added as two new records; **no existing row was deleted**.
The ten renamed, already mapped radios retain their original PocketBase record
IDs, readings, last-contact and monitoring timestamps. Other existing physical
device IDs are untouched. Historical b001/g004 role records remain unchanged.

All affected structured references move with the physical records: observations,
packet/gateway receipts, positions, assignments, warnings/events, neighbor
archives, link endpoints, neighbor frontiers and current-evidence watermarks.
Packet deduplication keys and observer/pair keys receive the same substitution.
Original radio IDs, packet content, source/receipt timestamps and row IDs are
preserved. Original raw MQTT archive rows remain byte-for-byte unchanged.
Accounts, members and assignments preserve their original content and counts.

At the live transaction boundary, counts are:

| Record set | Before | After relabeling |
| --- | ---: | ---: |
| Devices | 18 | 20 |
| Positions | 6,784 | 6,784 |
| Observations | 39,785 | 39,785 |
| Packet receipts | 115,988 | 115,988 |
| Raw archive rows | 134,485 | 134,485 |
| Link observations | 129,706 | 129,706 |

Full per-table transformed-content SHA-256 comparisons pass, beyond simple row
counts. Raw archive and protected-table digests use the unchanged original
content. New live packets and historical recovery add rows only after that
preserved boundary.

Old planned coordinates and unverified assembly/site assumptions are removed
from current fresh RAK/mobile configuration, with originals retained privately.
Hardware identity, current bench firmware metadata and report baselines follow
the November 14 commissioning records. Existing monitoring policy remains
with each known radio; only newly assigned unmonitored bench records get bench
defaults. G001 SD metadata now matches its observed saved five-minute interval.
R011's verified USB readback retains hourly device/environment/power settings;
its portal metadata was corrected separately to 60 minutes rather than assuming
the other RAKs' three-minute baseline. No radio setting was changed.
No warning threshold, radio admission limit or authentication rule was relaxed.

`/etc/meshlink/repeaters.json` remains a **historical provisioning input**. It
must not be rerun as the current physical-roster authority. Current active
identity is the reconciled registry plus `/etc/meshlink/mqtt.json`; future
commissioning must use physical IDs and the owner's fresh roster rather than
old numbered profiles.

## Recovery of previously rejected telemetry

From November 12 00:00 Pacific through cutover, the new adapter mapping can
normalize **16,741 previously unnormalized gateway copies**,
representing **8,803 packet identities**. An initial
partial pass recovered 297 copies;
the final idempotent resume recovered the remaining 16,444.
The private backfill plan/result and zero-remaining post-check retain exact counts.
Only original `unknown source` archive rows are considered. Unsupported native
app packets remain archived and are not fabricated as telemetry.

Recovery uses the existing local worker-ingest API and deployed adapter, with
original measurement and receipt times. Raw envelopes and their original
decode-outcome audit fields are not rewritten. Already accepted/duplicate
packet + gateway + original-time matches are skipped; rejected receipts remain
retryable. Replaying historical SNNS does not renew current neighbor freshness,
and old readings cannot masquerade as fresh contact or GPS fixes. Recovery is
paced below the existing 300 requests/10 seconds API limit with retry on 429;
the first unpaced attempt was throttled and safely resumed. No rate limit was
disabled. The final plan reports zero remaining recoverable copies.

## Validation, review and rollback

- The live mapping verifier fails before the change and passes for all 16
  sources afterward. Authenticated public identity checks and actual new
  accepted/duplicate receipt checks pass for the sources listed above.
- An isolated copy of the real database passes the full migration, content
  digests, current per-radio state and source-history provenance assertions.
- Independent read-only review finds no remaining blocker after preserving
  monitoring policies and correcting service-start failure handling.
  Reviewed/applied migration SHA-256:
  `3afc5d7aec34f0601e768f619d6e59dcf94ef0334658982bc5524b4cc6d2297f`.
- Three isolated failure injections pass: failed config replacement after DB
  commit restores old DB/config; pre-commit API-readiness failure restores old
  state; post-commit worker-start failure retains the correct new DB/config
  so newly received history cannot be lost by rollback. Completion is marked
  only after services are active.
- Full pre/post backups pass whole-archive SHA-256 and isolated SQLite
  integrity. Task-local copies of the installed live verifier pass isolated
  API recovery, exact identities, credentials, accounts, assignments, history,
  protected routes and authentication throttling. The pre-change check accounts
  for the three unmapped placeholders; that exception is empty afterward.
  Only necessary live restore files are extracted; installed verifier files
  and application source are unchanged.
- The first post-backup check incorrectly extracted only `data.db`. The
  archive also contains an 832,223,552-byte `data.db-wal` and shared-memory
  file. Restoring the complete SQLite snapshot passes integrity and exposes
  all 20 current records and recovered history. The final isolated API check
  includes the complete `pb_data` files; the database-only failed check is not
  treated as an invalid archive or a passing recovery result.
  The obsolete first read-only backfill planner was found still running after
  its SSH client was canceled. Its exact command/start time/database handle
  were checked before terminating that owned helper; the pre-existing dashboard
  reader and production services were preserved.
- The separate installed **demo** recovery verifier timed out before the live
  migration. This is recorded as unverified, not a pass. Demo data is not part
  of the mapping transaction, its service is active, and both full backups
  include it. Off-host recovery and native owner-phone presentation remain
  separate checks.

| Full private backup | SHA-256 |
| --- | --- |
| `meshlink-20261115T143046Z.tar.gz` | `1c2567a7655eb47b09170838f65d453fe1dc9656fce421bd722d6312365ebf81` |
| `meshlink-20261115T145921Z.tar.gz` | `dc032e7d20fb17210180fb5f2fc1a91239cb505fa3996508ed4459d909704293` |

Private full backups remain under `/var/backups/meshlink`. Exact pre-apply
database and MQTT configuration, archived device configurations, reviewed
script, content-digest proofs and replay receipt-row IDs remain root-private
under `/root/roster-reconcile-20261115/`. Before reception restarts, the guarded
script can restore its matching database/configuration. After new reception,
take a new backup and preserve/replay newer receipts before any rollback; do
not blindly replace the live DB with the pre-apply snapshot.

Sanitized local proofs and read-only checks are in
`private/roster-reconcile-20261115/`. Credentials, member names and raw tracks
remain outside Git. The remaining immediate action is fresh RF evidence from
the silent sources, requiring their hardware owner to confirm power/quiet
state. Mapping correction and preserved historical ingestion do not accept
battery runtime, forced relay, enclosure, coverage or deployment readiness.

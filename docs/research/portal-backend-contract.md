# Portal backend contract — first local slice

2026-10-13. Owner approved backend development after reviewing the four-page portal. Implemented with pinned PocketBase 0.40.5, JavaScript hooks/migrations and a standard-library Python simulation worker. This is a normalized application boundary, not a Meshtastic/MeshCore wire-format claim. [Run/check instructions](../../backend/README.md).

2026-10-14: the separate [live Meshtastic GPS adapter](../operations/live-mqtt.md) now feeds this boundary on the LXC. It provisions B001/B002 and G001/G002 against verified physical identities, uses `Position.timestamp` for GPS measurement time, and identifies packets by source/radio ID plus channel/decrypted-content digest so identical gateway copies deduplicate while different fixes under reused IDs remain distinct. Native `d1`/`m5` fixture identifiers below still describe development simulation only. The hosted fictional operational records were privately archived and replaced; no real member roster is inferred.

2026-10-16, local implementation: [the separate database demo](../../backend/demo/README.md) replaces browser-memory demo records with a synthetic Git-tracked PocketBase checkpoint and ignored writable runtime. The authenticated snapshot now includes `links`, bounded to 2,000 observations sorted by report receipt. Each row has receiver, nullable heard node/original source, gateway/neighbor source, direct/relayed/unknown path, nullable `snrDb`/`rssiDbm`, `receivedAt` and nullable `observedAt`. Signal zero remains distinct from absent data. Raw collection access/writes remain superuser-only. The sample generator provisions ten rows explicitly; ordinary migrations create an empty collection. No real signal adapter, archive replay or firmware enhancement is implemented, and production was not changed. Release the additive migration before its state hook and provide a separate demo API route before releasing the new View demo frontend.

## Records and identities

| Collection | Purpose |
| --- | --- |
| `accounts` | Username/password authentication; admin/member/worker/disabled roles; optional stable member association |
| `members` | Stable member key/display identity plus optional five-character member-chosen map `shortName`, independent of login/physical device and radio name |
| `devices` | Stable portal key, role, device number/short name, declared configuration, latest observation pointers and separate contact time |
| `assignments` | Dated device/member associations and actor; partial unique indexes enforce one active tracker per member and one member per tracker |
| `positions` | Unique GPS observations with original measurement time, timestamp quality, first receipt time and measurement-time carrier |
| `packet_receipts` | Every authorized normalized receipt, including duplicates/rejections; gateway, receipt/ingestion times and original envelope |
| `observations` | Unique infrastructure reports; independent capability readings drive the current state |
| `link_observations` | Directional receiver/heard-node observations, separate original source, nullable signal values, report receipt and optional hearing time; seeded only in the separate demo |
| `messages`, `send_attempts` | Shared text, authenticated outbound author, reported inbound author, gateway attempt and explicit send evidence |
| `name_jobs` | Separate long-name request/outcome; the newest job alone can simulate confirmation/failure; static short names remain unchanged |
| `rules`, `warnings` | Shared battery default (`deviceId: "*"`) or device override; trigger/recovery, enabled state, acknowledgments and recovery history |
| `incidents` | Latched intrusion, acknowledgment actor/time and admin resolution actor/time/note |
| `events` | Audited assignment/configuration/warning/incident actions and actor/time |
| `feed` | Worker heartbeat/connection, demo outage override and restoration time for reconnect grace |

Collection record IDs are PocketBase-generated persistent IDs. Domain keys (`d1`, `m5`, etc.) are fictional stable identifiers for the seeded scenario, not verified hardware IDs or member names. Device provisioning must capture verified physical identity separately from mutable radio node IDs/names before live integration. Regular accounts cannot change raw collections, auth roles or device identity through generic PocketBase record writes. Superusers remain trusted database administrators.

## Ingestion envelope

`POST /api/meshlink/worker/ingest` requires the worker role and a body bounded to 64 KiB:

```json
{
  "packetId": "source-packet-identity-including-epoch-if-needed",
  "deviceId": "d1",
  "gatewayId": "b1",
  "kind": "position",
  "measuredAt": "2026-10-13T12:00:00.000Z",
  "receivedAt": "2026-10-13T12:00:02.000Z",
  "data": { "latitude": 36.265, "longitude": -115.633, "battery": 75 }
}
```

- `deviceId` is a provisioned stable portal device key. `gatewayId` is a provisioned backhaul key. The worker adapter, not an unauthenticated gateway/browser, resolves those identities.
- `packetId` must identify the same original packet across gateways/replays. Display uniqueness is `(kind, deviceId, packetId)`, deliberately excluding gateway and receipt time. Include source epoch/reboot context if the selected protocol can reuse IDs. Conflicting payloads under one identity retain both receipts but the first normalized observation wins; firmware identity/collision handling needs live samples.
- `measuredAt` is a timezone-qualified source measurement/sample time or explicit null. Missing, unparsable and future times become null with `unknown`, `invalid` or `future` quality; the original envelope remains retained. A valid time is canonical UTC. Source clocks/quality still need selected-build validation. Do not substitute receipt time for GPS/sample time.
- `receivedAt` is the adapter's timezone-qualified original receipt time, not a made-up fresh fix. Invalid/future receipt times are rejected. `ingestedAt` is server time. Delayed normalized records keep their source/receipt times. Contact uses the latest receipt independently of the current GPS measurement.
- `position` requires finite in-range coordinates; optional battery is 0–100 percent or null. It is allowed only for member trackers. Known newer measurements advance the current position; old/unknown/future observations remain stored without replacing a newer known measurement. No known position means no invented pin.
- GPS quality extension (2026-10-16, local only): optional `data.pdop` is the dimensionless value after dividing the Meshtastic wire integer by 100; optional `data.satellites` is an integer reported count. Validate against the respective uint32 wire ranges (PDOP maximum 42949672.95 after scaling); null, absent or zero become unknown. Persist both with each `positions.payload` and that same fix's `latestPosition`; the snapshot already forwards these objects unchanged. Older saved points without these fields remain supported. A newer point missing quality replaces old quality with unknown; never carry metadata forward from a different fix. The frontend uses provisional bands below 3 / 3–6 inclusive / above 6 for Good / Limited / Poor, plus Unknown for unusable values. These describe satellite geometry, not calibrated confidence or metre accuracy. Satellite count is supplemental context, not an independent confidence score. [Policy, primary-source rationale and verification](../../.scratch/pilot/issues/15-gps-quality-pill.md). No schema migration or new collection is needed.
- `telemetry` supports battery volts, temperature °C, solar W and boolean intrusion, with separate timestamps for each reported metric. Absent/unsupported metrics never become normal or missing merely by being absent from another report. As authorized 2026-10-21 in #53, selection, displayed age and supported telemetry health use valid `measuredAt`, otherwise the observation's original `receivedAt`. Persist missing/invalid/future measurement clocks as null/empty with their original quality; never synthesize stored measurement time. A delayed known measurement is ordered by measurement time, not delivery; unknown-time reports are necessarily ordered by receipt. Uptime is not used. No battery capacity/current/runtime is inferred from voltage/configuration. Capability fitment and units are fictional here and must be verified.
- `message` has bounded `text` and a reported `author`. Received authors are not treated as authenticated portal identities. Outbound author identity is taken from authentication, independently of the radio-text prefix.

A transaction first retains the receipt with `accepted`, `duplicate` or `rejected` outcome. Rejections return 400 after saving receipt evidence; auth failures save nothing. Duplicates may update contact time, but never create another observation/message/incident or change GPS measurement age. Position history keeps measurement-time attribution through delayed arrivals and transfers. A bounded frontend history slice does not delete stored data.

## Access and operations

All custom routes load PocketBase authentication and enforce current roles on the server. Account registration and direct collection mutation are locked. The worker cannot read the human snapshot; humans cannot ingest. State responses use `Cache-Control: no-store`. Browser bearer tokens are saved in tab-scoped `sessionStorage` so sign-in survives refresh (2026-10-16). Restoration validates the token against the protected state endpoint and uses its current account details; no account profile or operational snapshot is persisted in browser storage. Sign-out and rejected authentication clear the token; temporary connection failures allow retry without discarding it. Storage failure falls back to memory-only sign-in. Demo mode remains memory-only. This follows PocketBase's [stateless bearer authentication](https://pocketbase.io/docs/authentication/); no worker/superuser secret is shipped in the frontend.

| Endpoint | Allowed operation |
| --- | --- |
| PocketBase `accounts/auth-with-password` | Username/password login, no public registration |
| `GET /api/meshlink/battery-history/{id}?hours=24` | Admin/member infrastructure voltage history; accepts 24/168/720 hours, excludes unknown/future measurement times, returns chronological `{samples:[{at,volts}],truncated}` with latest 50,000 observations maximum; worker/anonymous access denied |
| `GET /api/meshlink/state` | Admin/member snapshot with current trackers, dated assignments, bounded history/messages/events, infrastructure, warnings/incidents and feed status |
| `POST /api/meshlink/assign` | `{deviceId, memberId}`; member self-claim only a free tracker with no active assignment; admin closes conflicts and transfers atomically |
| `POST /api/meshlink/release` | `{deviceId}`; member's own tracker or admin; preserve ended association and create separate release-name job |
| `POST /api/meshlink/messages` | Human manual send only while healthy; synthetic send only; `{text}`, max 280 development characters; exactly one configured downlink gateway |
| `POST /api/meshlink/rules` | Admin `{deviceId, trigger, recovery, enabled?}` in volts; `"*"` is shared default; per-device records override it; disabled rules retain history |
| `POST /api/meshlink/configuration` | Admin `{deviceId, configuration}`; positive device/per-report cadence and timeout overrides, or `disabledMonitoring`; no hardware/sensor assertions added |
| `POST /api/meshlink/incidents/{id}` | Human `{action:"acknowledge"}`; admin `{action:"resolve",note}`; normal samples/acknowledgment never resolve |
| `POST /api/meshlink/warnings/{id}/ack` | Human acknowledgment; does not recover a warning |
| `POST /api/meshlink/accounts` | Admin creates admin/member account, validates member association, accepts an optional member-chosen `shortName` transactionally, prevents worker creation |
| `POST /api/meshlink/profile` | Human with a member association saves only their own `{shortName}`; 1–5 ASCII letters/digits/underscores/dashes, association taken from authentication; no radio/assignment mutation |
| `POST /api/meshlink/accounts/{id}` | Admin resets password or disables account; preserves history; cannot disable self/last enabled admin; worker credentials remain locally provisioned |
| `POST /api/meshlink/worker/heartbeat` | Worker `{connected:boolean}`; server timestamp; expires after 20 seconds; evaluates configured health rules |
| `POST /api/meshlink/demo/feed` | Admin simulation-only outage override; requires `MESHLINK_SIMULATION=1` |
| `POST /api/meshlink/demo/name-job` | Admin simulation-only latest-job outcome; no radio command/read-back is performed |

Reporting configuration accepts `cadenceMinutes`, metric maps `reportCadenceMinutes` / `missingTimeoutMinutes`, and a `disabledMonitoring` list. Default missing timeout is three expected intervals. Solar/weather/intrusion rules apply only to supported capabilities. Monitoring starts at the recorded enable/provisioning time. While the worker is unavailable, preserve existing warnings and suppress new missing warnings; after restoration, wait the configured timeout before new missing warnings. Fresh evidence clears missing warnings and reaches a separate recovery threshold for low battery. Intrusion groups unique reports into an open incident until admin resolution; the next unique reported intrusion opens another incident. No infrastructure toast/sound is generated.

## Verification and remaining interfaces

Tests use the real pinned PocketBase binary and temporary databases. Authorization, direct-write bypass, atomic conflict handling, historical attribution, original timestamps, duplicate receipts, unknown/future fixes, invalid receipts, message/outage evidence, capability rules, account lifecycle, latched intrusion and restart persistence are exercised. The documented fresh initialization command and connected browser flow are also checked locally. Runtime and dependency identities are tracked; actual binary/database/credentials stay ignored.

The first portal uses a two-second snapshot poll, not PocketBase realtime. The API bounds current history to 500 points/device within 12 hours, messages/events to 200 and other lists to 2,000. Wider-scale pagination/history queries, operational retention/export/deletion, backup/restore, supervision/VM/HTTPS, source packet adapters, broker connection, real radio send/name execution and field/device performance remain work before deployment. No real radio action is queued or sent by this backend. The owner-deferred MQTT transport investigation remains parked.

Primary implementation references: [PocketBase routing/auth middleware](https://pocketbase.io/docs/js-routing/), [transactions/record operations](https://pocketbase.io/docs/js-records/), [migrations](https://pocketbase.io/docs/js-migrations/), [API rules](https://pocketbase.io/docs/api-rules-and-filters/), [handler isolation](https://pocketbase.io/docs/js-overview/) and [pinned release](https://github.com/pocketbase/pocketbase/releases/tag/v0.40.5), checked 2026-10-13.

2026-10-15 tracker presentation update: member snapshots expose `shortName` (blank until chosen), and tracker snapshots expose configured `deviceType` or null. The field is portal display metadata, independent of radio short names and physical identity. The new additive migration supplies the member field and fills missing type metadata for the two already verified Heltec V4 member nodes. User cards show reported percentage only; normalized battery-voltage/configuration data remain stored independently. No owner-defined area boundaries/resolver are configured, so the card's optional `position.areaName` remains unknown in live snapshots; no synthetic area lookup is claimed.


## Compact infrastructure battery history — 2026-10-16

Local implementation adds an on-demand, no-store infrastructure battery-history route. It filters saved observations by device, positive battery value and measurement-time window (24 hours, seven days or 30 days), sorts by measurement time and reports truncation rather than claiming complete coverage. The new `1792191000_battery_history_index.js` migration indexes device/time. Deploy both the route and migration before the frontend; the ordinary state snapshot remains small. The frontend refreshes selected history once a minute, merges recent timed readings and leaves missing-report intervals disconnected while drawing a monotone curve. No operational readings are synthesized.

The separate demo checkpoint adds 30 days of synthetic solar recovery/deficit and steady gateway examples, and its simulation worker continues those voltage functions. Existing demo runtimes require an explicit additive history refresh or a fresh initialization; the builder never overwrites them. Production, sensor calibration, solar sufficiency and field endurance remain untested by these examples.

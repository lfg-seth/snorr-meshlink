# Portal backend contract — first local slice

2026-10-13. Owner approved backend development after reviewing the four-page portal. Implemented with pinned PocketBase 0.40.5, JavaScript hooks/migrations and a standard-library Python simulation worker. This is a normalized application boundary, not a Meshtastic/MeshCore wire-format claim. [Run/check instructions](../../backend/README.md).

2026-10-14: the separate [live Meshtastic GPS adapter](../operations/live-mqtt.md) now feeds this boundary on the LXC. It provisions B001/B002 and G001/G002 against verified physical identities, uses `Position.timestamp` for GPS measurement time, and identifies packets by source/radio ID plus channel/decrypted-content digest so identical gateway copies deduplicate while different fixes under reused IDs remain distinct. Native `d1`/`m5` fixture identifiers below still describe development simulation only. The hosted fictional operational records were privately archived and replaced; no real member roster is inferred.

## Records and identities

| Collection | Purpose |
| --- | --- |
| `accounts` | Username/password authentication; admin/member/worker/disabled roles; optional stable member association |
| `members` | Stable member key and display identity, independent of login/physical device |
| `devices` | Stable portal key, role, device number/short name, declared configuration, latest observation pointers and separate contact time |
| `assignments` | Dated device/member associations and actor; partial unique indexes enforce one active tracker per member and one member per tracker |
| `positions` | Unique GPS observations with original measurement time, timestamp quality, first receipt time and measurement-time carrier |
| `packet_receipts` | Every authorized normalized receipt, including duplicates/rejections; gateway, receipt/ingestion times and original envelope |
| `observations` | Unique infrastructure reports; independent capability readings drive the current state |
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
- `telemetry` supports battery volts, temperature °C, solar W and boolean intrusion, with separate timestamps for each reported metric. Absent/unsupported metrics never become normal or missing merely by being absent from another report. Unknown measurement quality cannot supply fresh recovery evidence. No battery capacity/current/runtime is inferred from voltage/configuration. Capability fitment and units are fictional here and must be verified.
- `message` has bounded `text` and a reported `author`. Received authors are not treated as authenticated portal identities. Outbound author identity is taken from authentication, independently of the radio-text prefix.

A transaction first retains the receipt with `accepted`, `duplicate` or `rejected` outcome. Rejections return 400 after saving receipt evidence; auth failures save nothing. Duplicates may update contact time, but never create another observation/message/incident or change GPS measurement age. Position history keeps measurement-time attribution through delayed arrivals and transfers. A bounded frontend history slice does not delete stored data.

## Access and operations

All custom routes load PocketBase authentication and enforce current roles on the server. Account registration and direct collection mutation are locked. The worker cannot read the human snapshot; humans cannot ingest. State responses use `Cache-Control: no-store`. Browser bearer tokens stay in memory and are cleared on sign-out; no privileged secret is shipped in the frontend.

| Endpoint | Allowed operation |
| --- | --- |
| PocketBase `accounts/auth-with-password` | Username/password login, no public registration |
| `GET /api/meshlink/state` | Admin/member snapshot with current trackers, dated assignments, bounded history/messages/events, infrastructure, warnings/incidents and feed status |
| `POST /api/meshlink/assign` | `{deviceId, memberId}`; member self-claim only a free tracker with no active assignment; admin closes conflicts and transfers atomically |
| `POST /api/meshlink/release` | `{deviceId}`; member's own tracker or admin; preserve ended association and create separate release-name job |
| `POST /api/meshlink/messages` | Human manual send only while healthy; synthetic send only; `{text}`, max 280 development characters; exactly one configured downlink gateway |
| `POST /api/meshlink/rules` | Admin `{deviceId, trigger, recovery, enabled?}` in volts; `"*"` is shared default; per-device records override it; disabled rules retain history |
| `POST /api/meshlink/configuration` | Admin `{deviceId, configuration}`; positive device/per-report cadence and timeout overrides, or `disabledMonitoring`; no hardware/sensor assertions added |
| `POST /api/meshlink/incidents/{id}` | Human `{action:"acknowledge"}`; admin `{action:"resolve",note}`; normal samples/acknowledgment never resolve |
| `POST /api/meshlink/warnings/{id}/ack` | Human acknowledgment; does not recover a warning |
| `POST /api/meshlink/accounts` | Admin creates admin/member account, validates member association, prevents worker creation |
| `POST /api/meshlink/accounts/{id}` | Admin resets password or disables account; preserves history; cannot disable self/last enabled admin; worker credentials remain locally provisioned |
| `POST /api/meshlink/worker/heartbeat` | Worker `{connected:boolean}`; server timestamp; expires after 20 seconds; evaluates configured health rules |
| `POST /api/meshlink/demo/feed` | Admin simulation-only outage override; requires `MESHLINK_SIMULATION=1` |
| `POST /api/meshlink/demo/name-job` | Admin simulation-only latest-job outcome; no radio command/read-back is performed |

Reporting configuration accepts `cadenceMinutes`, metric maps `reportCadenceMinutes` / `missingTimeoutMinutes`, and a `disabledMonitoring` list. Default missing timeout is three expected intervals. Solar/weather/intrusion rules apply only to supported capabilities. Monitoring starts at the recorded enable/provisioning time. While the worker is unavailable, preserve existing warnings and suppress new missing warnings; after restoration, wait the configured timeout before new missing warnings. Fresh evidence clears missing warnings and reaches a separate recovery threshold for low battery. Intrusion groups unique reports into an open incident until admin resolution; the next unique reported intrusion opens another incident. No infrastructure toast/sound is generated.

## Verification and remaining interfaces

Tests use the real pinned PocketBase binary and temporary databases. Authorization, direct-write bypass, atomic conflict handling, historical attribution, original timestamps, duplicate receipts, unknown/future fixes, invalid receipts, message/outage evidence, capability rules, account lifecycle, latched intrusion and restart persistence are exercised. The documented fresh initialization command and connected browser flow are also checked locally. Runtime and dependency identities are tracked; actual binary/database/credentials stay ignored.

The first portal uses a two-second snapshot poll, not PocketBase realtime. The API bounds current history to 500 points/device within 12 hours, messages/events to 200 and other lists to 2,000. Wider-scale pagination/history queries, operational retention/export/deletion, backup/restore, supervision/VM/HTTPS, source packet adapters, broker connection, real radio send/name execution and field/device performance remain work before deployment. No real radio action is queued or sent by this backend. The owner-deferred MQTT transport investigation remains parked.

Primary implementation references: [PocketBase routing/auth middleware](https://pocketbase.io/docs/js-routing/), [transactions/record operations](https://pocketbase.io/docs/js-records/), [migrations](https://pocketbase.io/docs/js-migrations/), [API rules](https://pocketbase.io/docs/api-rules-and-filters/), [handler isolation](https://pocketbase.io/docs/js-overview/) and [pinned release](https://github.com/pocketbase/pocketbase/releases/tag/v0.40.5), checked 2026-10-13.

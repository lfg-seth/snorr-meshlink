# G003 MQTT account, portal registration and map placement - 2026-10-24

Owner requests a dedicated G003 MQTT account, live portal registration, a random
Las Vegas position, and the same default for routers/gateways missing positions
going forward. This follows the [verified board preparation](g003-gateway-preparation.md).

## Dedicated account

**pilot-v3-uplink-3** is created on the existing broker. Its 30-character secret
fits the installed V3 firmware. Existing accounts, password hashes, worker
credential and ACL entries remain intact. New rights allow writing only the
existing private encrypted channel's **G003 gateway topic**; no subscribe/read,
other-gateway, JSON or unrelated-topic rights are granted.

The first installer stops before writes because it incorrectly expects one
listener. Runtime socket inspection confirms loopback and private-network
listeners. The corrected parser prefers loopback and has regression coverage.
The owner executes the corrected sudo step and reports successful creation and
local authentication. Private broker rollback material is at
`/root/meshlink-maintenance/g003-account-20261024T163843.352007Z`.
Independent desktop login through certificate/hostname-validated public TLS
also passes. Real isolated Mosquitto tests cover listener parsing, authentication,
own-topic-only writes, denied reads/other topics, existing-account preservation,
rollback, idempotence and conflicting-rotation refusal.

Concealed **MESHLINK_G003_MQTT_USERNAME** and **MESHLINK_G003_MQTT_PASSWORD**
are saved in **SNORR MeshLink — Pilot**; names-only readback confirms both.
Private local input is `private/bench/G003-portal-20261024/g003-account.json`.

**Radio cutover is pending:** owner has G004 attached and will reconnect G003
later. G003 still has the earlier G002 uplink credential. Its recorded Wi-Fi API
address does not answer from this desktop, so no radio write is attempted.
On reconnection, independently identify `!9e9f167c` / hardware
`4393827189e95c03021dd7b37007a6a0`, back up its current complete profile, change
only MQTT username/password, and verify full preservation through reboot plus
fresh delivery. Retain receive-only operation and enabled 180-second device/power
telemetry. G004's serial ownership is respected.

## Portal and map acceptance

The live portal now has **11 devices**, including **G003** as a backhaul, with
its independently verified radio/hardware identity, installed firmware,
INA219-only capabilities, disabled downlink and three-minute battery/power
metadata. Unknown pack, chemistry, capacity, antenna, solar and physical sensor
path remain unknown. Monitoring enablement is not expanded.

Add G003 to worker gateway, infrastructure-source and identity mappings while
preserving all existing fields and credentials. Only the MQTT worker restarts;
no application/frontend/schema release is performed. Authenticated readback
confirms G003 and all intended configuration. Independent follow-up finds the
feed online, seven normalized G003 receipts and latest contact
**2026-10-24T16:46:45.832Z**. These receipts precede the pending radio credential
cutover and do not prove that G003 has adopted its new account.

**G003 and R006** receive persisted random central Las Vegas map points. R006
was the only pre-existing infrastructure device with no location. Existing
seven infrastructure locations and both member configurations are preserved;
no measured GPS record or radio fixed position is created. A visible
**Random Las Vegas map placement** suffix in each affected portal name and
explicit `locationSource` / `locationLabel` metadata identify the placeholders.
Original names and bench/deployment status are retained in configuration/history.
Locations are generated once and stay stable on repeated provisioning.

The [location policy helper](../../scripts/server/infrastructure-locations.py)
and its tests preserve existing valid coordinate pairs and all member devices,
replace incomplete/invalid infrastructure pairs together, label provenance,
and preserve unrelated configuration. Follow the
[standing provisioning rule](board-flashing-handoff.md#default-infrastructure-map-placement)
for future infrastructure nodes. These points are map placeholders, not measured
sites, installation plans, permission or coverage evidence. The latest owner
instruction supersedes the earlier unapplied R006 point request while its
prior private evidence remains historical.

## Backups and recovery

Both archives remain root-private under `/var/backups/meshlink/`:

| Stage | Archive | SHA256 |
| --- | --- | --- |
| Before registration | `meshlink-20261024T163547Z.tar.gz` | `ca1b97b1d1aa3df1745c17b1d93bf08c589ee144db05a8dcca0aaba8909d037c` |
| After registration | `meshlink-20261024T164157Z.tar.gz` | `50e044a31e92c4533f98db1fb1a7554058e02f000d98819073e910d5b867b95b` |

Pre-change installed verifier passes isolated restore, credentials, assignments,
history, proxy/authentication and throttling checks. Post-change it rejects G003
because its expected gateway set is hard-coded to G001/G002. A tested correction
derives infrastructure from the trusted worker mappings and retained repeater
plan. Two focused regression tests and the staged full post-change restore pass
with **11 devices**. Production verifier replacement awaits explicit approval
after automatic approval review rejected it as outside registration/location
scope; its original installed file is unchanged.

Live SQLite integrity and authenticated marker/identity readback pass. Private
before/intended/after records and exact points are under
`/root/g003-registration-20261024/apply-20261024T164049Z`; staged recovery verifier
is in its parent directory. Desktop private evidence is under
`private/bench/G003-portal-20261024/`. Application source marker stays `443ba03`.
Native browser map presentation, radio credential cutover and subsequent
fresh account-specific delivery remain separate gates.

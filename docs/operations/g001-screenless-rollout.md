# G001 screenless gateway and MeshLink 0.2.0 production rollout

**Current update, 2026-11-13:** G001 runs `2.7.26.5bd4923`; SD health now
shares the saved 300-second device telemetry cadence. MeshLink 0.3.1 is live.
[Cadence, recovery and acceptance](g001-sd-cadence.md). The daily interval and
0.2.0 version below describe the original rollout.

On 2026-11-12 the owner began a new rollout numbering sequence. **G001** is
the screenless Heltec V4.3 with USB MAC **F8:5B:1B:BF:06:38** and radio
**`!1bbf0638`**. Its earlier bench label was G007. The board's long name is
`SNORR Pilot Gateway G001`. Full radio identity, keys, channels and the
five-minute private uplink profile matched the intended configuration after
an explicit reboot. Firmware remains `2.7.26.898c113` and daily SD health
remains at 86,400 seconds. [Original installation and recovery hashes](g007-screenless-gateway.md).

The earlier V3 G001 (`!9ea13cc0`) has the production key
`legacy-v3-9ea13cc0` and the card name **Legacy Heltec V3 (former G001)**.
It retains its original database row and can still carry pilot traffic. Only
the screenless board's on-radio name changed during this assignment. Other
radios receive rollout labels as their hardware is selected.

## Production release

Deployed tagged MeshLink **0.2.0**, source `205b1909d2d04bc7617e3f83d916999388216f30`,
over 0.1.5. The clean tagged checkout passed 92 backend and 64 portal tests
in the production host's runtimes. The first backend test invocation used
system Python, which lacked the MQTT libraries. The installed worker runtime
passed the full suite. Installed migration files matched the release. The
source promotion preserved hashes of operational databases, private
configuration and the worker queue while services were stopped. The
rollback copy of the previous application and static assets is at
`/opt/meshlink-rollback-g001-205b190` on the LXC.

The recovery verifier previously required an empty operational roster even
after the application gained member registration. It now checks the actual
authenticated roster against the private live database and compares it with
the restored backup. A regression case exercises a populated roster and
detects a missing member. The remaining authentication, access and recovery
checks ran as before.

Registration was rehearsed against an isolated database copy. The live change
stopped the worker and API under the deployment lock, verified an empty
receipt queue, retained the old MQTT configuration and made an immediate
database backup. The transaction moved V3 identity references, including
source and transport receipt IDs, packet keys and stored neighbor and backhaul
references. Historical raw MQTT envelopes retained their original radio IDs,
timestamps and bytes. The screenless board received a new record, with its
own firmware, INA219 and SD configuration. No location, battery capacity or
solar hardware was copied from the older V3.

## Authenticated card evidence

The production broker archive already contained the genuine daily measurement,
with source time **2026-11-13 02:00:33 UTC** (November 12, 18:00:33 Pacific).
The 0.2.0 adapter decoded its original three envelopes. The normal worker
ingestion path preserved their original receipt times and stored one SD
observation. A further transmission of the same generation from the renamed
radio reached the active worker through G001 and the legacy V3. The schedule
and source timestamp stayed intact.

In desktop Edge, a live authenticated session at the public HTTPS site opened
**Infrastructure → G001 · Screenless Heltec V4.3**. The device card showed
**Logging · 0.0% used (393216 / 31902400512 bytes) · 0 dropped this boot**.
The one-decimal percentage rounds down while the byte count shows recorded
data. The final backup contains the same SD reading, both radio mappings and
the gateway receipts. The owner can revisit the [live Infrastructure page](https://meshlink.spp.lol/#infrastructure).

The transaction preserved 7,431 source receipts and 35,601
transport receipts attributed to the legacy V3. The final SD archive has
3 direct and 2 peer receipts for that one generation. All six services passed.
All 10 static files matched the release on loopback and public HTTPS.
The live and demo isolated recovery checks passed on the final backup.

| Private archive | SHA-256 |
| --- | --- |
| Before deployment, `meshlink-20261113T023845Z.tar.gz` | `c44bd6e9e672e0f17d21e1d59b7fb85af9ff0f2e4d1d932ebdf60f75296a979c` |
| After registration and live SD verification, `meshlink-20261113T030348Z.tar.gz` | `58cf05145c46006e18690b29380e7718e46686f1f390010c654b191d357f3b5b` |

Private verification logs and registration snapshots are under
`/root/g001-rollout-20261112` on the LXC. Physical retrieval of the SD files,
24-hour operation and solar endurance remain separate measurements.

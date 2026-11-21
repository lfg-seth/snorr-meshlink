# B003 client reassignment from the G004 V4 - 2026-10-25

Owner requests overwriting the connected V4 and flashing it as a new client.
Independent API/USB identification finds the existing OLED V4 **G004
`!699c2ed8`**, formerly B001, on **COM5**, USB **`90:70:69:9C:2E:D8`**,
hardware ID **`d4d91213c6f862de7a81383bc8843e59`**. Assign the next client
number **B003**, distinct from the current B002 and historical B001 identity.
This reuses existing hardware; no purchase or additional V4 is inferred.

## Recovery and image

Fresh complete owner/channel/security/local/module backup precedes writes.
Retain the existing board-specific 16 MB full recovery base from the prior G004
bench, plus fresh boot/partition, NVS, OTA, filesystem and coredump reads and an
independent digest check of the original current application. V4 filesystem is
**0xc90000 / 0x360000**, coredump **0xff0000 / 0x10000**. Initial helper reads
at V3 offsets are superseded before any write; corrected V4 recovery provenance
is retained in private `recovery.json`. This is a fresh mutable-state recovery
set plus an existing full base, not a newly read complete 16 MB image.

Reinstall the exact checked **heltec-v4-gateway / 2.7.26.6fea6aa** application,
**2,119,520 bytes**, SHA256
**`0fde49af9a4b270ce40c95474b8cf61c4981211955bf9a0d6913a0fc4c239a9a`**,
from published/project-pinned source
**`6fea6aa68842c43be261f2aa3ca0565e2e48db10`**. Match the original V4 partition
table and active app0, write only **0x10000**, then independently verify digest.
No rebuild, erase, factory reset, bootloader update or PKI rotation. The target
name enables SNNS capability; it does not select a gateway role or MQTT.

## Intended client profile

| Setting | Intended value |
| --- | --- |
| Identity/name | Own existing PKI/node identity; SNORR Client B003 / B003 |
| Role/radio | CLIENT; private US pilot, 10 dBm/FEM, hop 3/slot 35 retained; TX enabled |
| Wi-Fi/MQTT | Disabled, old SSID/password/broker credentials cleared |
| GPS | Enabled, original RX39/TX38/enable34, 60-second acquisition, 120-second reporting |
| Position | Existing quality flags retained; smart/fixed position disabled |
| Device telemetry | Enabled, 180 seconds |
| Environment/power telemetry | Disabled; existing INA219 does not become a client power claim |
| SNNS | Enabled over LoRa, saved 180-second baseline plus jitter/admission |
| Standard NeighborInfo | 21,600 seconds |

Temporarily disable only this board's radio/uplink while switching its logical
mapping from gateway to client. Preserve private channel/security settings and
remaining unrelated saved fields. Restore radio TX with the final profile.
No person is assigned to the new client.

## Portal identity transition

The portal confirms no existing B003 and no open G004 member assignment. A
checksum-verified complete live/demo backup precedes reassigning the existing
active device record from **g004 / Backhaul** to **b003 / member**, retaining its
internal record ID. Archive the old complete record privately; clear old cached
readings/position/contact on the newly named logical client. All historical
positions/observations/receipts/neighbor rows remain under **g004** rather than
being relabeled B003. Other device records/configurations and history are
unchanged. Switch only this physical node's worker mapping from gateway and
infrastructure to member, with the same hardware ID and new B003 short name.

The active G004 gateway role is retired. Historical V3 failure and former B001
and G004 evidence remain historical. The new client has no inferred battery
capacity/allocation or carried-over gateway site/solar plan. No member account
or assignment is created; no application release or demo data changes.

## Completed verification and delivery limits

Application-only write and separate digest verification pass. Complete intended
owner, channel, identity/key, local and module equality passes through an explicit
reboot at **18:23:15 UTC / 11:23:15 Pacific**. A later independent connection
again verifies the full saved profile. The final API transaction supplies time
once after verification; later SNNS/serial evidence still has an unknown source
wall clock. Persistence/cause is unverified, so autonomous GPS/mesh-clock startup
is not accepted by this task.

Fresh non-retained B003 **SNNS** sequence **1**, boot **189484357**, reaches
G002/G001 at **18:25:16.586 / 18:25:16.593 UTC** in the validating-TLS local
capture. Source measurement time is unknown. Authenticated public HTTPS and
read-only SQL independently confirm accepted G002 and duplicate G001 ingestion,
portal last contact **18:25:17.361 UTC**, B003/B003 as an unassigned **Heltec V4
tracker**, and no active G004 backhaul entry. No member assignment is created.

No new RF battery or GPS observation is accepted during this run. At source
uptime **182 seconds**, the console explicitly logs **Ch. util >25%. Skip send**
for device telemetry (reported utilization **25.915%**), reads **3.799 V** and
sends metrics **to the local phone/API only**. Position send attempts also log
channel-utilization skips. This is local device telemetry evidence, not a gateway
battery receipt or independent calibration. Preserve the airtime gates; sustained
three-minute radio cadence and fresh GPS fix remain unverified. The portal
correctly has no client position and no battery voltage at the final checkpoint.
Serial and validating-TLS MQTT handles close at handoff.

The complete server pre-update backup **`meshlink-20261025T182059Z.tar.gz`** has verified SHA256
**`e44deb65a051c6bc0df7e3e7d9f7ba6aa81a76a6b162b2004a8d72db6ca716b4`**. Private server audit:
`/root/b003-client-20261025/apply-20261025T182059Z/`. Existing internal device ID
is retained while its logical key/role changes; raw G004 historical rows remain
**1085 observations, 3691 receipts, 357 neighbor reports, eight events**, with
zero positions/assignments/name jobs at verification. All other device identity/
configuration fields and historical counts remain unchanged. All four live/demo
API/worker services are active, feed online and database integrity pass. No
software release or data migration is performed.

Existing full recovery base SHA256: **`cb99bbafcea47c8e112b278e25f2a952693ebe3d0fe3c3003d64bd72d479edaf`**. Fresh mutable recovery reads
and hashes are enumerated privately, including the corrected **3,538,944-byte**
V4 filesystem. The existing base and exact cached application remain retained;
no superseded V3-offset read is used as V4 recovery evidence.

The documented `scripts/check-project.py docs` scope passes inline links and
whitespace checks. Unrelated existing edits remain unstaged.


Fresh GPS fix, phone-free behavior/time bootstrap, native phone acceptance,
battery/runtime, sustained cadence and field coverage remain separate gates.
Raw keys, old credentials, backups, serial/MQTT logs and any GPS locations remain
under ignored `private/bench/b003-client-20261025/` and the private server audit.

## November 21 member commissioning

The connected original OLED Heltec V4 matched B003 by USB serial, physical
hardware ID and mesh ID. The installed survey target `2.7.26.7b766e6`
reported a fresh local GPS fix, and G003 delivered current telemetry, while
the live portal's latest position still dated to November 14. The installed
firmware classified the survey client's own position packets for suppression,
including during idle survey operation. The owner retired this unit from
survey duty and authorized transferring the portal assignment from B002.

The B003-specific laptop survey service was disabled and stopped. A fresh
16 MiB recovery image passed the board's flash digest and has SHA-256
`11266c04ff78060537faf4a8a06f0ae1432bda729f49d24b57d1e4c3ba53ea52`.
The remote builder compiled the OLED `heltec-v4-gateway` application from
`5bd492399f5f3d4a65c01256f907f7b907b80921`; all four packaged artifacts
passed SHA-256 on the builder and laptop. The app is 2,120,256 bytes with
SHA-256 `789871d31d3ae8b5ee2a12b6253a106b48cd7f04624d7e1bc5165c6073e2bbae`.
The backup and factory image agreed on the partition layout. Only app0 at
`0x10000` was written. Independent onboard digest verification and
post-reboot readback of `2.7.26.5bd4923` passed with the same identity,
private channel, keys, local settings and module settings.

The member profile retains CLIENT, automatic dynamic GPS, a 120-second
position broadcast interval, the private primary channel and permission for
gateways to relay to MQTT. The GPS receiver interval was restored from
one second to the established 60 seconds. Wi-Fi and direct MQTT are disabled
on B003. The firmware target name identifies the build and does not select
the device's role. Signed-in public HTTPS verified the normal portal transfer,
which closed B002's assignment and preserved history. The existing B003
registry and MQTT mapping were sufficient.

Independent USB readback after the settings restart verified the intended
profile with only the receiver interval changed. The B003 position packet
observed over USB had a GPS measurement time of **21:06:24 UTC** and matched
G003's accepted production receipt at **21:06:25.866 UTC** by packet ID.
Production stored the fix under the new member assignment, and the signed-in
public tracker response showed that same valid measurement. Both the radio
and portal checks passed with no change to the worker mapping or application.
Serial was closed. Battery-only operation, sustained cadence and field
coverage remain outside this bench check.

The [survey transfer record](https://github.com/lfg-seth/snorr-meshlink/blob/0530cc5/docs/operations/g005-site-survey.md#v4-survey-identity-and-ten-responder-transfer)
documents a separate physical V4 provisioned with the same on-air identity.
Production saw no B003 receipts during the plugged-in unit's flash backup.
Keep any survey unit with that copied identity off the mesh pending a unique
assignment. This check did not inspect or change other radios.

The private recovery and serial evidence are in
`private/bench/b003-member-20261121/`. No raw positions, member roster or keys
are included here.

## November 21 faster position reporting

USB serial, hardware ID, mesh ID and firmware matched the commissioned OLED
Heltec V4 before the position settings were updated.

| Setting | Before | After reboot |
| --- | --- | --- |
| Smart position | Off | On |
| Minimum displacement from last transmitted position | 100 m | 20 m |
| Minimum time since last position send for a smart report | 300 s | 15 s |
| Periodic position broadcast | 120 s | 60 s |
| GPS acquisition attempt interval | 60 s | 15 s |

The pinned firmware applies the longer position minimums to default channels.
B003 reports on its private primary channel. The 20 m / 15 s thresholds also
match the pinned firmware's fast-tracker defaults. At 15 seconds, GPS
acquisition can support the faster reporting and the receiver can still
enter its normal sleep path when time permits.

The entire intended radio profile matched after the write and again after an
explicit reboot on `2.7.26.5bd4923`. USB was closed. The private before and
rebooted readbacks are under `private/bench/b003-smart-20261121/`.
This check verified saved settings. Stationary and moving delivery, airtime
and battery runtime remain to be measured with the new profile.

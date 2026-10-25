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

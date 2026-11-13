# 13-node clock audit - 2026-11-12

Read-only production archive observation at **23:49:57 Pacific** on November 12
(2026-11-13 07:49:57 UTC), covering the preceding hour. The owner reports 13
running nodes, three GPS receivers and two Wi-Fi devices. No radio, serial,
configuration, service or deployment writes were made.

## Measured results

- All 13 active radio IDs supplied plausible current UTC telemetry.
- Deduplicated by radio ID, packet ID and encrypted payload: **635 unique
  packets** across application types. The legacy V3 uplink carried 635
  transport copies and screenless G001 carried 634. This is observed archive
  delivery, not a count of every attempted RF transmission.
- Of **410 unique telemetry packets**, 393 carried plausible UTC and 17
  carried unknown/uptime-like time. None carried a future timestamp relative
  to its first archived receipt; no source-time regression was observed within
  a node/telemetry-type stream. Unknown clocks are excluded from that ordering
  verdict. Decoder exceptions: zero.
- For clocked telemetry, first-receipt minus source time ranged approximately
  **0.45–56.95 seconds**. This includes queueing, RF/transport and clock offset;
  it is not a measurement of clock accuracy.
- Initial unknown-time reports occurred on R004/R005/R007/R008/R010.
  R004/R007/R008 device reports were clocked by 306 seconds uptime, and R005
  by 366 seconds. These bound observed acquisition, not the exact sync instant.
- R006 had clocked reports, then rebooted: source time was 306 seconds at
  23:13:21 Pacific receipt and 1266 seconds at 23:29:21. Its next observed
  clocked device report arrived at 23:37:26, uptime 1746 seconds. Thus it
  **still lacked UTC at 21 minutes uptime and had UTC by 29 minutes**.
  Reboot cause and exact acquisition trigger were not measured.

| Active label | Radio ID | Timestamp observation |
| --- | --- | --- |
| B002 | !699ca878 | Valid telemetry and GPS measurement timestamps |
| B003 | !699c2ed8 | Valid telemetry and GPS measurement timestamps |
| G001, screenless V4 | !1bbf0638 | Valid telemetry; NTP configured |
| Legacy V3, former G001 | !9ea13cc0 | Valid telemetry; active Wi-Fi/MQTT uplink |
| R001 | !f95b5501 | Valid telemetry |
| R002 | !05237743 | Valid telemetry |
| R004 | !49ac6d7f | Valid telemetry after initial unknown clock |
| R005 | !a65601b3 | Valid telemetry after initial unknown clock |
| R006 | !638b9515 | Valid telemetry after a prolonged unknown-clock boot |
| R007 | !b456f760 | Valid telemetry after initial unknown clock |
| R008 | !120b04fd | Valid telemetry after initial unknown clock |
| R009 | !da581e5f | Valid telemetry and position clock-sharing time |
| R010 | !77fdb9f1 | Valid telemetry after initial unknown power report |

R009's one position packet in this hour arrived at 23:06:47 Pacific, with
16 satellites, internal-GPS location source, and valid `Position.time`
1794553605. Its separate `Position.timestamp` is zero. It can therefore carry
mesh clock time while its GPS measurement age remains unknown in the dashboard.
The pinned sender includes the measurement timestamp only with the corresponding
position flag; the live flags were not read or changed in this audit.

## What this establishes

Current source timestamps are healthy across the observed mesh. The GPS senders
provide the primary-channel time-bearing position packets supported by the
[pinned position implementation](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/PositionModule.cpp).
Eligible receivers adopt remote internal-GPS time at network clock quality;
receivers with their own GPS/RTC or recent phone/NTP source may ignore it.
A node's locally originated position does not re-advertise network-quality
time as GPS/NTP quality; forwarding the original GPS packet is distinct.

This archive alone does **not prove GPS was the time source for every node**:
telemetry lacks clock-source provenance, Wi-Fi gateways can use NTP, and earlier
USB/phone provisioning may have supplied time. The remaining acceptance gate
from the [GPS/time record](../docs/operations/g004-gps-time.md) is a selected
cold-start receiver without competing USB/phone/NTP time, observed acquiring
network time and stamping subsequent telemetry, followed by forced-relay and
source-loss/recovery measurements. Do not interrupt the current run for that
test without selecting the hardware/run.

## Logging limits and evidence

The live worker heartbeat was current. G001's latest daily SD generation still
reports 393216 / 31902400512 bytes and zero drops **for that earlier boot**,
source 18:00:33 Pacific, NTP. A daily report does not prove the present boot's
drop count or card-file integrity. Physical copied SML inspection and sustained
logging remain open as recorded in the
[G001 rollout](../docs/operations/g001-screenless-rollout.md).

Ignored local evidence: `private/clock-audit-20261112/summary.json` and its
read-only SSH audit helper. Only IDs, times, counts and clock-related metadata
were exported; coordinates, member names, keys and raw packet bytes stayed on
the server. Existing dashboard sampler was also run once. No behavior changes
or hardware acceptance are claimed.

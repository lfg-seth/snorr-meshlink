# Shady Hollow relay gap - 2026-11-17

Owner sees R005/R009 and G002 through R005 in MeshLink Activity, but no fresh
R001/R008/R011 reports. Read-only production archive and Activity checks at
**09:51-09:53 PST / 17:51-17:53 UTC** reproduce that symptom twice. It is
upstream of the Activity display: none of those three sources occurs in the
last hour of raw MQTT receipts. Other sources continue reaching the archive.

## Measured reception

G002's **09:45:21 PST** SNNS report has a complete four-neighbor table:

| Source heard directly by G002 | RSSI | SNR | Hearing age when report generated |
| --- | --- | --- | --- |
| R001 / Cathedral Rock | -90 dBm | 1.5 dB | 110 s |
| R008 / Kyle Junction | -97 dBm | -4.75 dB | 26 s |
| R011 / Angel Peak Mountain Side | -104 dBm | -10.5 dB | 58 s |
| R005 / Angel Peak Vegas Side | -105 dBm | -11.25 dB | 71 s |

These observations establish recent RF activity from all three missing
repeaters at G002. They do not deliver those repeaters' original telemetry to
the server or establish continuous links.

R005's complete **09:50:43** SNNS table lists only G002 and R009. R009's
**09:48:18** table lists R005, R002 and G003. R005 hears R009 at
**-112 dBm / -9.5 dB**, age zero; R009 hears R005 at **-112 dBm / -7.5 dB**,
age 55 seconds. These are actual directional observations, not an end-to-end
delivery rate.

G002's latest archived power report at **09:46:33** reaches G003 with
`hop_start=3`, `hop_limit=1`, `relay_node=0x5f` (R009's relay-byte candidate).
R005 telemetry also reaches G003 with `hop_start=3`, `hop_limit=2` and the
same candidate. Combined with the neighbor reports, the evidence supports
G002 -> R005 -> R009 -> G003 as the useful outgoing path. A last-relay byte
alone does not prove every intermediate hop.

Last stored portal contact for R001 is **November 16, 22:17:17 PST**, and R008
**22:16:36 PST**. R011's stored contact is **November 15, 17:31:34 PST**;
its current activity is established by G002's fresh hearing report instead.
R008's latest received SNNS table is historical: its R005 observation was
already 1,795 seconds old at **November 16, 21:56:08 PST**, at
**-128 dBm / -20.75 dB**, with only one observation. It is not evidence of a
current reliable direct R008-R005 link.

## Confirmed forwarding blocker

The [G002 deployment profile](g002-shady-hollow-deployment.md) preserves
**CLIENT / rebroadcast NONE** for offline recording. More decisively, its
recorded installed **heltec-v4-sd-gateway-survey / 2.7.26.f6cdbeb** inherits
`SNORR_SD_GATEWAY=1`. In that exact published revision,
[`FloodingRouter::isRebroadcaster()`](https://github.com/lfg-seth/firmware/blob/f6cdbeb3f390f6dcf31c8e909cb4fcd1b24a9cdc/src/mesh/FloodingRouter.cpp#L161-L168)
returns false whenever that build flag is present. The
[target definition](https://github.com/lfg-seth/firmware/blob/f6cdbeb3f390f6dcf31c8e909cb4fcd1b24a9cdc/variants/esp32s3/heltec_v4/platformio.ini)
and [SD firmware contract](https://github.com/lfg-seth/firmware/blob/f6cdbeb3f390f6dcf31c8e909cb4fcd1b24a9cdc/SNORR_SD_GATEWAY.md) confirm the
inherited restriction. Exact source was checked from the local Git object;
no new board firmware attestation was performed.

Consequently G002 can hear and record other radios and originate its own
reports, while declining to relay their packets toward R005. That matches the
observed gap. **Changing only CLIENT to ROUTER or NONE to LOCAL_ONLY cannot
remove the compiled forwarding restriction.** The earlier corrected R011
MQTT-permission setting is separate from this bridge restriction.

## Verification and next action

Private reproducible audit:
`private/relay-diagnosis-20261117/audit.py`; saved sanitized output:
`private/relay-diagnosis-20261117/audit-sanitized.txt`. It runs through the
existing SSH route using the server's MQTT Python runtime, opens SQLite with
`mode=ro` and `query_only=ON`, decodes packets on the server, and prints only
infrastructure identities, readings, timestamps, routing fields and neighbor
observations. Both runs report **FAIL missing recent portal contact: R001,
R008, R011**, with **zero parse errors**. The 15-minute contact assertion is
a diagnostic predicate, not a newly accepted telemetry-delivery threshold.
Channel keys, packet payloads and exact locations are excluded from output.

Next owner-selected remedy: provide a relay-capable node at Shady Hollow
(reuse an accepted inventoried RAK), or separately develop and validate an
SD-recording build that permits the selected RF forwarding profile. Role-only
remote configuration is insufficient. No node/site choice, firmware build,
flash, RF/admin request, service restart or production mutation was performed.

After a selected remedy, verify new original R001/R008/R011 packets through
the actual forced relay path, retaining hop fields and per-gateway receipts.
The proposed path needs three retransmissions before G003; any additional
relay needs a fresh hop-budget check. Direct-link coverage, delivery rate,
airtime, power and sustained operation remain field acceptance gates.

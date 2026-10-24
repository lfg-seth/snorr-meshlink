# Gateway backhaul health and three-minute reporting

Owner authorizes implementation and flashing **G001/G002/G003/G004** on
2026-10-24. G004 is the replacement OLED V4 `!699c2ed8`; the failed V3 is
retired. One session owns all four USB ports during this rollout. Other boards
and the member tracker retain their individual firmware/profiles.

## Behavior and wire contract

Enable private LoRa transmission and over-LoRa SNNS, device telemetry at
**180 seconds**, and the same interval for already-enabled fitted sensors.
Preserve identities, keys, channel/radio power, Wi-Fi/MQTT credentials, GPS
settings and disabled downlinks. SNNS remains observation-driven with jitter,
schedule and airtime admission; 180 seconds is its baseline, not an exact
delivery deadline. A separate health heartbeat reports even with no neighbors.

Published firmware source **`6fea6aa68`** on `snorr/develop` adds **SNGH v1**
on the private application port. The 32-byte little-endian payload contains
magic/version, Wi-Fi and direct MQTT connection flags, reserved zero bytes,
observer node ID, boot ID, generation sequence, uptime seconds, source Unix
time (zero when unknown), and the configured interval. Wi-Fi association and
MQTT connection state are separate. The heartbeat follows the saved device
interval with a 180-second minimum, jitter and normal radio admission gates.
It never contains an SSID, address, credentials or position.

MeshLink **0.1.3** accepts health only from provisioned gateway identities.
Existing observations preserve history, including reports too old or unordered
to update current status. Fresh known source time plus increasing per-boot
sequence orders health. Previously accepted retired boots cannot replace the
current boot. Duplicate/multi-gateway receipts can establish a radio path for
that same generation, but cannot renew its source time or recover an outage.
Uptime is diagnostic; its approximately 49-day millisecond rollover does not
block a higher sequence with newer source time.

Fresh Wi-Fi/MQTT-disconnected reports open a persistent **Backhaul unavailable**
warning. A fresh connected report recovers it; acknowledgment only means seen.
Receipt via another gateway establishes that the reporting radio is alive.
All health becomes stale after three configured intervals (nine minutes at
180 seconds), including retained browser snapshots. Unknown/future source
clocks cannot prove current health or clear warnings. Feed loss preserves
existing warnings and marks health uncertain. This does not promise immediate
failure detection or prove end-to-end delivery from a local MQTT connection.

## Verification and rollout

Read-only independent review covered firmware serialization/rate limits and
backend/portal freshness; type placement, browser expiry and uptime ordering
findings were corrected. Five sanitizer-backed module/collector configurations,
gateway wire fixtures, isolated PocketBase replay/recovery/restart/rollover
tests and portal checks pass. Trunk is unavailable on this Windows/WSL host;
the attempted formatter cannot run. Target builds, exact image digests, full
backups, intended-profile comparison through reboot, fresh automatic receipts
and controlled outage/recovery remain distinct acceptance stages.

### Completed bench and deployment - 2026-10-24

All four boards run **`2.7.26.6fea6aa`**, built from published source
**`6fea6aa68`**. Both targets build successfully: V3 **365.86 s**, V4
**388.51 s**. Full flash backups (three 8 MB V3s and one 16 MB V4), original
partition/active-app checks, application-only installation at `0x10000`,
independent esptool digest verification and full intended-profile comparison
through explicit reboot pass. G004 retains its GPS/default pins and INA219;
G003 retains INA219. G001/G002 gain enabled device telemetry; fitted-sensor
enables, individual Wi-Fi/MQTT, keys, RF power and GPS settings are preserved.
All four use CLIENT, enabled radio TX and over-LoRa SNNS, device interval 180
seconds and active power telemetry at 180 seconds. Portal device/battery
cadence metadata now matches three minutes; other configuration is preserved.

| Target / boards | Application SHA256 |
| --- | --- |
| heltec-v3-gateway / G001, G002, G003 | `c26a61e96b4553958c4632bb4074e89bbea0a214dbed15289cc2bbf54f5263f7` |
| heltec-v4-gateway / G004 | `0fde49af9a4b270ce40c95474b8cf61c4981211955bf9a0d6913a0fc4c239a9a` |

Fresh automatic device, SNNS and health reports from each gateway reach peers;
G003/G004 also deliver INA219 power. Device/power measurement gaps include
**180–181 seconds**. Same-boot SNNS/health source gaps include **195–255
seconds**, rather than exact 180-second delivery: jitter/scheduler and the
existing 25% polite channel-utilization gate can defer reports. The controlled
G001 console records channel-utilization skips without brownout or duty-cycle
skip evidence. Preserve those gates; this is not sustained cadence/coverage
acceptance or a resolution of GH-8.

**G001 Wi-Fi outage:** temporarily use an unavailable SSID, retaining the
original network privately. That deliberate settings reboot loses the test
clock, so supply time **once over serial** before observing; this does not
prove autonomous time acquisition without Wi-Fi/GPS. Two disconnected health
generations, two subsequent device telemetry packets and two SNNS generations
reach peer gateways with Wi-Fi/MQTT unavailable. The portal opens a persistent
backhaul warning at **20:33:11.245Z / 13:33:11 Pacific**, with fresh radio-alive
evidence via G003/G004 (G002 also receives the later generation). Device
measurements during the outage include a **180-second** gap; health/SNNS
same-boot source gap is **255 seconds**, including airtime deferral.

Restore G001's exact original network and complete intended profile through
explicit reboot. A fresh connected report at **20:40:46Z** recovers the warning
at **20:40:49.075Z / 13:40:49 Pacific**. Authenticated public HTTPS checks
verify both the actual outage and recovery, then show all four gateways
connected with fresh peer-radio evidence. Serial is closed after restoration.

Owner explicitly approves [PR #62](https://github.com/lfg-seth/snorr-meshlink/pull/62)
merge and manual deployment. MeshLink **0.1.3**, clean main commit
**`d50925018ac27b2fd472f460b8f8f8bdd042d2ca`**, immutable tag
**`meshlink-v0.1.3`**, is deployed. All three PR checks, **87 Linux backend
tests**, Windows checks (87, seven platform skips), **61 portal tests/build**
and the five sanitizer configurations pass. Public release metadata matches
that exact commit. The independent reviewer confirms no remaining ordering
finding after the rollover correction. The deployment preserves database,
spool and credential/configuration hashes while stopped. Pre/post private
backups and isolated live/demo recovery pass; rollback source/static assets
are retained. No schema migration, member/other-board flash or field
installation is performed.

Remaining acceptance: native authenticated owner-phone presentation, sustained
outage/reconnect/airtime behavior, unknown-clock bootstrap, forced relay,
power/sensor calibration, runtime and field coverage. G003/G004 still use the
existing uplink account; separate account provisioning is unchanged.

Private profiles, full-flash backups, serial logs, image provenance and MQTT
receipts are under ignored `private/bench/gateway-health-20261024/`. No raw
locations or credentials belong in Git. Initial long G001 backup read failed
before writing hardware; bounded reads with speed fallback are used instead.

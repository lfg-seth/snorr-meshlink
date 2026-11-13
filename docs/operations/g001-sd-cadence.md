# G001 SD-health telemetry cadence

On 2026-11-13 the owner replaces the daily SD-health cadence with the existing
saved device telemetry setting. Screenless Heltec V4.3 **G001 `!1bbf0638`**,
USB **F8:5B:1B:BF:06:38**, runs **heltec-v4-sd-gateway / 2.7.26.5bd4923**.
Change `telemetry.device_update_interval` to change the SD baseline too; G001
retains **300 seconds**. SNGH uses the same setting. Airtime admission and the
15-second scheduler can defer sends; the streams need not share a send phase.

## Firmware and preservation

Published source is [5bd492399](https://github.com/lfg-seth/firmware/commit/5bd492399f5f3d4a65c01256f907f7b907b80921).
The app is **1,903,328 bytes**, SHA-256
`7cada4e0c2ff6dc636947bd331b2b34ea31d598c571717ac37c189df54c16e6b`.
Its manifest, target, partition fit and on-chip digest pass. The app-only write
at 0x10000 preserved checked bootloader, partition table, NVS and OTA-data
digests. Full owner/configuration, own keys, channel profiles and hardware
identity matched the private pre-update snapshot after reboot. No settings or
SD files were deliberately rewritten by the installer; normal logging continues.

SD timing and the SNSD v1 advertised interval now use
`moduleConfig.telemetry.device_update_interval`, with SNGH's 180-second minimum,
zero-value fallback and 2,147,468-second ceiling. The previous outstanding
cooldown survives a same-boot interval reduction. The existing persistent
`snorr-sd/daily` reservation is retained, so upgrades preserve generation
sequence and reboot suppression. Unknown-clock boots wait one configured
interval when no comparable saved UTC exists. The 52-byte format, 64-bit byte
counts, card/error flags and boot-local loss counter are unchanged.

Native C++17 scheduling/wire fixtures pass with address/undefined sanitizers
at 180/300/900/86,400 seconds, including reboot, unknown/backward/forward time,
interval changes and the legacy golden vector. Existing actual SNNS/SNGH
module/Throttle fixtures pass. The target build passes in 350.48 seconds.
Trunk is unavailable on this Windows host; the affected header/fixture use its
pinned clang-format 16.0.3 configuration. Existing source warnings remain.

Private recovery/evidence is under `private/bench/g001-sd-cadence/`, including
`before.json`, `after.json`, `rollback-app.bin`, `installed.json`, build and
flash logs, and encrypted-uplink observation summaries. The rollback app is
the verified previously installed `246ec7285` image, SHA-256
`29911d7350fafb560fdbd52d891b8a88aac58598a3dc21f3bfe1f2871f015f0c`.
The original diagnostic/full-layout recovery remains in the
[initial installation record](g007-screenless-gateway.md).

## MeshLink compatibility and release

[PR #68](https://github.com/lfg-seth/snorr-meshlink/pull/68) adds matching
Python adapter and PocketBase-hook interval validation. Older daily packets
remain valid. Cards use the advertised interval for freshness and await a
report without assuming daily timing. No database migration or private mapping
change is needed. MeshLink **0.3.1**, tagged at **62dcc0bfe70984332a9ffe5646238d8224320e7c**,
passes **94 backend and 66 portal tests**, typecheck and build on the isolated
release host. The old encrypted-wire test's invalid-interval mutation was
updated because it now represented a valid non-daily interval; the 20 MQTT
tests and full release-host suite pass after that correction.

The owner explicitly approves merge, tag and production deployment in this
session. The exact release is deployed: all ten static files match on loopback
and public HTTPS, all six services are active, protected state hashes match
through source promotion, and isolated live/demo recovery passes before and
after deployment. Main and tag backend/portal CI pass. Rollback source/assets
are retained at `/opt/meshlink-rollback-sd-62dcc0b`. Release-host evidence and
promotion/recovery logs are under `/root/g001-sd-cadence-20261113`.

| Private recovery archive | SHA-256 |
| --- | --- |
| Before, `meshlink-20261113T082358Z.tar.gz` | `6ab7362d57267b96e637f7bb46766a40b9525ef0bc01e0c80c67624f47fdba67` |
| After, `meshlink-20261113T082715Z.tar.gz` | `ec6546a54b9e841ee518020c5ff3b2ef94dbbae929de227fdeb4e00c2336d2da` |

## Live measurements and limits

The first automatic new SNSD generation is persistent sequence **2**, recorder
boot **1577970196**, uptime **75 seconds**, NTP clock, interval **300 seconds**.
Its own encrypted MQTT receipt is **2026-11-13 08:19:37 UTC**; independent RF
reception through legacy V3 `!9ea13cc0` arrives about 9.7 seconds later.
It reports healthy detected/mounted/writable storage, **2,981,888 /
31,902,400,512 bytes** and **zero dropped records this boot**. These are
filesystem counts, not raw card capacity or whole-card integrity measurements.

The second automatic generation is sequence **3**, uptime **436 seconds**:
the source gap is **361 seconds**, identical to SNGH in this window. Own MQTT
SD/backhaul receipt gaps are both **360.2 seconds**; peer SD receipt gap is
**352.6 seconds**. Device/Wi-Fi receipts also span about 360 seconds. These
measurements establish the shared configured baseline and actual deferred
behavior; they do not establish exact 300-second delivery. The extra delay's
specific cause was not isolated.

The third automatic generation is sequence **4**, uptime **781 seconds**:
both SD and SNGH source gaps are **345 seconds** and own receipt gaps are
**345.2 seconds**. Their peer receipt gaps are **348.1 seconds**. All three
SD generations advertise 300 seconds, remain in one boot and arrive through
both encrypted uplinks. Source delays are preserved rather than rounded to
the configured baseline.

After deployment, authenticated public HTTPS state returns sequence 4 at source
time **2026-11-13 08:31:21 UTC** (00:31:21 Pacific), interval **300 seconds**,
healthy storage, **3,080,192 / 31,902,400,512 bytes** and zero dropped records.
The SQL observation is unique for the generation; normalized raw MQTT archives
and accepted/duplicate receipts independently retain **g001** and
**legacy-v3-9ea13cc0**. Source age at verification is **7.1 seconds**.
`live-sd-evidence.json` preserves the sanitized result. The existing Cloudflare
rule blocks Python's default user-agent; public acceptance uses the documented
curl path with the token confined to private process input.

Serial and MQTT observers are closed, and the temporary PlatformIO package
mapping is removed. Physical copied-card inspection, a sustained run, calibration, field
coverage and battery/solar endurance remain separate acceptance work.

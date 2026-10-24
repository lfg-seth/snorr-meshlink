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

Private profiles, full-flash backups, serial logs, image provenance and MQTT
receipts are under ignored `private/bench/gateway-health-20261024/`. No raw
locations or credentials belong in Git. Initial long G001 backup read failed
before writing hardware; bounded reads with speed fallback are used instead.

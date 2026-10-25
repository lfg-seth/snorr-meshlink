# G005/G006 Heltec V3 gateway provisioning - 2026-10-25

Owner requests flashing the two connected Heltec V3s as G005/G006 and supplies
an alternate Wi-Fi network. The owner explicitly accepts that this network is
unavailable for association testing. Credentials remain only in ignored private
bench material; the saved default bench network is unchanged.

## Identity, image and recovery

| Assignment | Node | Port | Previous label | Original firmware |
| --- | --- | --- | --- | --- |
| G005 | `!9ea039cc` | COM6 | SNORR Unconfigured / MC00 | `heltec-v3 / 2.7.17.55580d10f` |
| G006 | `!b03d6790` | COM21 | SNORR BASE01 / SB01 | `heltec-v3 / 2.7.17.76d5156e7` |

Both independently identify HELTEC_V3 / ESP32-S3 with **8 MB flash**. G005 is
not the dedicated sniffer MC00 `!9ea0432c`; names/COM ports alone do not identify
a board. Fresh complete owner/security/channel/local/module backups preserve
the individual old profiles. Board-specific full-flash recovery copies stay
private. No factory reset, key rotation or bootloader update is requested.

Select the existing verified **heltec-v3-gateway / 2.7.26.6fea6aa** application
from published and project-pinned source
**`6fea6aa68842c43be261f2aa3ca0565e2e48db10`**; no rebuild or new release.
Application size **2,111,440 bytes**, SHA256
**`c26a61e96b4553958c4632bb4074e89bbea0a214dbed15289cc2bbf54f5263f7`**.
Match the original partition table to this build, verify active app0, flash only
**0x10000**, then independently verify the written application digest.

## Intended gateway configuration

- Names **SNORR Gateway G005 / G005** and **SNORR Gateway G006 / G006**.
- CLIENT, retained US region, private pilot channel and working gateway MQTT
  profile copied from the existing G001 intended profile. The earlier unrelated
  channels/MQTT settings are intentionally replaced; individual PKI identities
  and admin keys remain each board's own. Preserve remaining saved settings.
- Pilot RF power **10 dBm**, hop limit **3**, slot **35**, enabled LoRa TX;
  ignore MQTT-origin traffic. Uplink enabled and channel downlinks disabled.
- Owner-supplied Wi-Fi enabled; saved SSID/password verified privately.
  Encrypted MQTT/TLS enabled, JSON/map/proxy reporting disabled. Existing pilot
  gateway account reused; separate per-gateway account provisioning remains a
  follow-up rather than a new credential claim.
- Device telemetry enabled at **180 seconds**; over-LoRa SNNS and gateway health
  use that baseline with jitter/scheduling/airtime gates. Standard NeighborInfo
  remains **21,600 seconds**. Preserve disabled external environment/power
  telemetry and original GPS settings; no fitted sensor/GPS claim is inferred.

Both application-only writes and separate esptool digest verifications pass.
Independent full intended-profile comparisons pass before and after an explicit
reboot on each board, including names, each original PKI/admin identity, private
pilot channel/downlinks, MQTT profile, and exact owner-supplied SSID/password.
The checks verify stored credentials without claiming association.

| Board | Full 8 MB recovery backup SHA256 | Final reboot readback UTC |
| --- | --- | --- |
| G005 | `5f7e1adaea371a7b2d30d59b3bce37eca15633e65443d2ca29cd3386c1a7c720` | 2026-10-25T17:55:48.464639+00:00 |
| G006 | `935564d029e8bcd635e2b06f372982a68f7554e1b90019b6afe7c6a0472ad1d4` | 2026-10-25T17:58:33.993921+00:00 |

Upgrade-only readbacks preserve identities/keys/channels and all local settings:
G005 gains a firmware-default NeighborInfo interval; G006 has no observed
saved-profile difference. Provisioning deliberately replaces their earlier
channel/MQTT settings. Writing Device config normalizes the old 900-second
NodeInfo interval to **3600 seconds**, enforced by `AdminModule.cpp` and
`min_node_info_broadcast_secs`. Account for that rule in the intended profile;
it does not change the verified **180-second telemetry** setting. G005's initial
full-profile mismatch is resolved by identifying precisely that one clamp and
then repeating complete verification through an explicit reboot. No reset,
key rotation or second flash is used to resolve it.

A validating-TLS subscription with temporary local mappings independently
validates fresh non-retained encrypted reports through existing **G001/G002**.
Ignore pre-verification traffic and deduplicate gateway/packet IDs. G005's cutoff
is 17:55:48.464639 UTC and G006's is 17:58:33.993921 UTC. No manually requested
radio report is counted. Serial supplies the clock once after final reboot;
autonomous clock bootstrap is not accepted by this test.

| Board | Fresh report | G001 distinct packets | G002 distinct packets |
| --- | --- | --- | --- |
| G005 | Device/battery | 2 | 2 |
| G005 | SNNS | 1 | 1 |
| G005 | Backhaul health | 1 | 1 |
| G006 | Device/battery | 0 | 0 |
| G006 | SNNS | 1 | 1 |
| G006 | Backhaul health | 1 | 1 |

Health reports from both new gateways truthfully indicate **Wi-Fi disconnected /
direct MQTT disconnected**, with fresh peer-gateway receipts. This is radio
fallback delivery while the configured Wi-Fi is unavailable; it does not verify
that either new board can join that network or connect directly to MQTT. No
sustained three-minute delivery/cadence claim is made. Serial and MQTT handles
close after verification/observation.


The documented `scripts/check-project.py docs` scope passes local inline links
and whitespace checks. No firmware or repository tool source changes.


## Live portal registration - 2026-10-25

Owner separately requests adding G005/G006 to the live portal. Create exactly
two **backhaul** device records with names **SNORR Gateway G005/G006**, verified
node/hardware identities, HELTEC V3 model, installed firmware/target, bench
status, and **3-minute device/battery metadata**. Leave position/site,
battery chemistry/capacity, antenna and unconfirmed equipment unconfigured.
Bench battery/sensor monitoring remains disabled; no field-ready claim.

Add both radio IDs to the live worker's **infrastructure source**, **gateway**
and **identity** mappings. Existing gateway/member mappings, credentials and
unrelated worker settings are unchanged. Pause/restart the worker around the
update; all four live/demo API/worker services are active afterward. No software
release, schema migration, firmware change or demo data change.

Before mutation, the installed complete live/demo backup is checksum-verified:
**`meshlink-20261025T180545Z.tar.gz`**, SHA256 **`78f44edc968de8a9c21a4a8f1a73f80db4ce74bb8186bdf7a40bfabde4dceedb`**. Private audit at
`/root/g005-g006-registration-20261025/apply-20261025T180545Z/` preserves original
MQTT configuration, consistent pre-write database, intended/new records and
exact historical table-count comparison while ingestion is paused. All **14**
pre-existing device records retain identity/configuration; total becomes **16**.
Historical rows are unchanged by registration. The worker config write preserves
ownership/mode and checks that no concurrent edit occurred.

Authenticated **public HTTPS** state verification at **18:08:14 UTC / 11:08:14
Pacific** passes both names, Backhaul roles, model/node IDs, firmware and cadence.
Fresh health/SNNS receipts for each new gateway arrive through **G001 and G002**,
with accepted/duplicate outcomes preserved. Both new gateways show
**Wi-Fi disconnected**, direct MQTT disconnected and **radioAlive=true**;
this truthfully reflects the unavailable configured network. No battery
observation is present at this verification checkpoint. Positions are absent,
so no invented map marker is supplied. Database integrity and online feed pass.
Native owner-phone rendering, first battery data, direct Wi-Fi/MQTT and sustained
cadence remain separate checks. Markdown link/whitespace checks pass.

## Remaining acceptance

Wi-Fi association and direct MQTT connection remain unverified. Production
registration and fresh authenticated health/SNNS ingestion pass above. The requested unavailable network is not
a failed connection test. Local observation mappings do not register production
gateways. The separately authorized registration above adds the production
records/mappings without a device assignment, site installation, stock purchase
or firmware source change. Once the network is available, verify each gateway's
association and direct MQTT uplink/receipts. Runtime, power, sustained outage and field coverage remain
separate gates.

Private profiles, credentials, full flash backups, serial logs and observation
capture remain under ignored `private/bench/g005-g006-20261025/`.

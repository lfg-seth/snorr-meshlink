# R005 replaces R011 at Angel Peak Vegas Side - 2026-11-15

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

**Later same-day update:** owner reuses R011 / Case 6 at
[Angel Peak Mountain Side](r011-angel-mountain-deployment.md), with a new
fixed pin and reboot-verified MQTT permission enabled. R005 remains Vegas Side.
The swap-time R011 state below is historical.

After [R011's missing-telemetry diagnosis](r011-telemetry-diagnosis.md), owner
explicitly swaps that deployment assignment to connected **R005** at the same
supplied Angel Peak Vegas-side coordinates. Keep the enclosure **unnumbered**
until the owner identifies it: **ASA, eight cells, one SMA Muzi antenna, two
160 mA panels**. Do not infer Case 6 or select a matching inventory case.
No purchase, value, capacity or wiring inference.

## Configuration

USB **AA474A4710B85C2C**, radio **!a65601b3**, hardware
**2c5cb810474a47aab30156a671567827**, RAK4631; live backup independently confirms
**2.7.26.bcb22e0 / rak4631-survey**. **No flash/reset/rebuild/key replacement.**
R005 already has **`lora.config_ok_to_mqtt=true`**, matching R001/R008, unlike
R011's retained former-reference setting. Check this explicitly before writes
and in the intended/readback profile; do not waive it by preserving an old
profile blindly. Existing INA219 fit is owner-confirmed; AHT21 previously
undetected/unverified.

Set **ROUTER** and exact fixed position using integer coordinates, retaining
existing altitude or unspecified. Preserve full individual keys/admin list,
channel bytes, names, LOCAL_ONLY, US/LongFast slot 35, enabled TX at 10 dBm,
hop 3, MQTT upload permission, ignore-MQTT, Bluetooth/network and disabled
power saving. Reassert affected sections after role defaults: enabled
**180-second device/environment/power**, saved-baseline SNNS, **21,600-second
NeighborInfo and position cadence**. Preserve this unit's original GPS/position
flags. Accept ROUTER's unmessagable owner flag and role-derived API sleep value
86,400 seconds, with power saving still off.

Station lease and USB/radio/hardware guards precede writes. Complete intended
local/module/channel bytes, identity/owner/metadata and exact fixed coordinates
pass independent readback **before and after explicit reboot**. First verification
open has USB I/O errors; a read-only retry passes before the one explicit reboot.
The first final-read process ends unexpectedly; its read-only retry passes.
No configuration or reboot is repeated; serial is closed.
Private before/intended/readback snapshots, commands and logs:
`private/bench/R005-deploy-20261115/`. Exact coordinates remain private.

## Assignment and verification limits

R011 is **withdrawn from this site assignment**, not repaired or reset. Its last
verified saved state remains ROUTER with the old fixed site and MQTT upload
permission off; no command is sent to R011 during the swap. Keep it outside
the accepted deployment set until its future role/location/profile is selected.
The earlier Case 6 allocation remains historical; its current availability is
not inferred from this differently described replacement enclosure.

B003 is unplugged during R005 configuration, so no replacement ping is implied.
Physical mount/completed installation, actual sensor readings, RF/portal/CLI
freshness, forced relay, coverage and runtime remain separate from saved
settings. Survey PINGs renew 900-second autonomous-report quiet; a marker can
renew that quiet on reboot. New CLI reports must be later than configuration,
not old R005 history or PKI replies to explicit requests.

## New CLI delivery verified

The pre-replacement R011 check fails with no ordinary receipts. The same live
CLI path, through its existing tailnet SSH route, receives post-configuration
R005 **device** and **environment** at **2026-11-15T20:01:42Z**, **SNNS** at
**20:01:39Z** and fixed position at **20:01:36Z**. Exclude old R005 history and
PKI replies. Device voltage is **3.907 V**; fresh environment carries INA219
**3.912 V / -268.2 mA** as represented by the CLI, not calibrated whole-input
power or proven runtime. No temperature/humidity is observed. The separate
**PowerMetrics** stream then arrives at **20:01:53.689Z**, INA channel 1
**3.912 V / -270.8 mA** as represented by the CLI. All four device/environment/
power/SNNS streams are new after configuration; sustained cadence is not
established by these first receipts.

Local read-only survey-state handshake confirms **zero quiet time and zero
suppressed packets** at about 120 seconds uptime; no RF ping is sent to R005.
The first raw handshake used DTR disabled and timed out; using normal nRF52
USB DTR gives the state without changing firmware or configuration. Its survey
event-ring drop counter is 33; this is not a count of dropped LoRa telemetry.
New device/environment/power/SNNS receipts close the replacement's missing-CLI-report
symptom; sustained cadence, all-gateway receipts and field acceptance remain open.

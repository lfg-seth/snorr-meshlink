# R004 ordinary firmware and three-minute reporting - 2026-10-24

Owner reconnects existing R004 with INA219 and requests the latest firmware
and three-minute telemetry/SNNS. This authorizes replacing its diagnostic
image. The earlier [INA219 captures](ina219-audit.md#r004-reinvestigation--2026-10-21)
remain retained; physical bridge confirmation, calibrated accuracy and
battery-only behavior remain unresolved. This update does not close GH-4.

## ROUTER and three-minute profile restoration - 2026-10-25

Owner runs the prompted setup with long name **Southwest Ridge**, preserving
short name **R004**, selecting **ROUTER**, a private fixed point and B002 admin.
The write saves those selections but fails its full comparison: role defaults
replace LOCAL_ONLY with CORE_PORTNUMS_ONLY, device telemetry with 43,200 seconds
and environment/power/standard-neighbor intervals with unset defaults. The
initial failed result is retained; a saved readback file alone is not a pass.

Owner explicitly requests restoring three-minute telemetry. Independently
identify **`!77fdb9f1` / RAK4631 / USB `820C9B4F0C2D7675`**, now
`/dev/ttyACM1`, and take another full private backup. Keep ROUTER active while
restoring only the observed role-default changes: original rebroadcast mode,
saved sleep setting, telemetry intervals and standard-neighbor interval.
Firmware stays **2.7.26.4c96b9b**; no reflash, identity reset or other board write.

Full intended-profile comparison passes after the settings reboot and again
after an explicit reboot, final capture **2026-10-25T20:54:41.406611+00:00**:

- **Device, environment and INA219 power telemetry: enabled, 180 seconds each.**
- **Southwest Ridge / R004, ROUTER**, exact owner-entered fixed coordinates
  and fixed-position enablement persist.
- Original **LOCAL_ONLY**, **21,600-second** standard NeighborInfo, enabled
  over-LoRa neighbor collection and saved **180-second SNNS baseline** persist.
- Complete intended local/module/channel bytes, keys, owner flags, existing
  admins plus B002 match. Firmware metadata differs from the original intended
  snapshot only by its expected ROUTER announcement.

Read actual saved power config through an independent admin response, avoiding
the role-derived sleep value substituted in the USB PhoneAPI dump. Serial
connections are closed. Private original and recovery evidence is under
`private/bench/R004-role-20261025T204546095434Z/`; original `reconciliation.txt`
stays failed, and **`repair-reconciliation.txt`** records the successful recovery
for later portal reconciliation. Final readbacks:
`repair-verify-20261025T205355491542Z.json` and
`repair-verify-20261025T205440067617Z.json`.

This supersedes the CLIENT role in the October 24 measurements below. Fresh
RF/MQTT/portal delivery and cadence are not remeasured in this repair; portal
name/location/cadence metadata remain unreconciled here. Physical calibration,
runtime and field/forced-relay acceptance remain open. The general setup
script's role-default/readback fixes remain a separate follow-up before more
nodes are commissioned.

## Image and preservation

- Independently identify **RAK4631 `!77fdb9f1`**, USB serial
  **`820C9B4F0C2D7675`**, COM17. The original installation is
  **rak4631-ina219-debug / 2.7.26.09d8a9d**.
- Verify the published `snorr/develop` head and pinned source are both
  **`4c96b9ba0360f01752892a41d09ccacda82747bb`**. Reuse the exact reviewed
  ordinary **rak4631 / 2.7.26.4c96b9b** application from the
  [R006 bench](repeater-update.md#r006-and-gateway-admin-bench---2026-10-24),
  without rebuilding. This is an explicitly selected local build; no public
  release asset or production download pointer is changed.
- UF2: **1,519,104 bytes**, SHA256
  **`f83039d32c8637beff30f1a8d06e8addd106ad817f611dbc440b9bac04c65206`**.
  Hash, nRF52840 application bounds and matching RAK USB volume pass before
  application-only flashing. Bootloader and saved configuration are retained.
- Privately back up the entire original owner, hardware identity, keys,
  channels and local/module profile. Independent post-flash readback verifies
  the ordinary target/version and complete original-profile equality.
  The first helper's reconnect check times out after the successful write;
  a fresh independent API connection verifies it without another flash.

## Saved profile

At **2026-10-24T17:33:47Z / 10:33:47 Pacific**, complete intended-profile
comparison passes through an explicit reboot:

| Setting | Verified value |
| --- | --- |
| Role | CLIENT |
| Device/battery telemetry | Enabled, 180 seconds |
| Existing temperature/humidity telemetry | Enabled, 180 seconds |
| INA219 power telemetry | Enabled, 180 seconds |
| Passive SNNS | Enabled over LoRa; saved device interval supplies 180-second baseline |
| Standard NeighborInfo | Separate 21,600-second interval |

Only the intended telemetry/neighbor settings differ from the original.
Private channel, keys, radio settings, names, other local/module settings,
Fahrenheit preference and unset battery-INA address remain preserved. Set
device time over the local API after the reboot comparison. INA219 sensor
initialization/open succeeds. The tracked R004 sensor profile now retains
both environment and INA219 power, preventing a future updater run from
silently disabling power telemetry.

SNNS retains jitter, outstanding cooldown and airtime deferral; 180 seconds
is its baseline rather than a promise of exact three-minute reception.
Standard NeighborInfo does not control private SNNS cadence.

## Delivery and remaining gates

Validating-TLS MQTT subscription receives fresh, non-retained, encrypted
R004 reports through **G001 and G002** after the final reboot/profile check.
The live adapter independently decrypts/validates source, transport gateway,
measurement time, packet ID and metric units; duplicates are excluded per
gateway. Reports before **17:33:47.552 UTC** are excluded from this acceptance.

The first fresh device packet reports **3.654 V** at measurement time
**17:34:33 UTC**. Environment follows at **17:34:59 UTC**, reporting
**27.317 degrees C / 27.094% RH**, with INA219 **3.660 V / -298.0 mA**.
PowerTelemetry follows at **17:35:14 UTC**, reporting **channel 1,
3.660 V / -298.2 mA**. Preserve the measured sign without interpreting charging
or validating the battery current path. Both gateways also receive the new
SNNS boot's first report at **17:35:27.71 UTC**, sequence **1**, source uptime
**113 seconds**.

Two new automatic reports of each telemetry type reach each gateway:

| Report | Measurement gap | G001 receipt gap | G002 receipt gap |
| --- | --- | --- | --- |
| Device/battery | 180 s | 179.973 s | 179.975 s |
| Temperature/environment | 180 s | 180.143 s | 180.145 s |
| INA219 channel-1 power | 180 s | 180.159 s | 180.155 s |

The second SNNS report has the same boot ID, sequence **2**, source uptime
**308 seconds**: **195 seconds** after sequence 1, consistent with the
180-second baseline plus jitter/scheduling. Both gateways receive both
reports; G001/G002 receipt gaps are **193.540 / 193.549 seconds**. All eight
gateway/type combinations have two distinct automatic packets; no local
manual telemetry requests are used for this observation. Earlier boot/history
packets are excluded. Serial and MQTT handles close after the run.

All **34 offline updater checks** pass, including the updated fitted-sensor
expectation. Documentation link/whitespace checks pass. An initial sandbox
temporary-directory permission failure is resolved by rerunning the suite
with ordinary host access; no product failure is inferred from that attempt.

Authenticated portal ingestion and cadence metadata, physical sensor accuracy, runtime, sustained
operation and field coverage remain separate gates. SNNS requires changed
passive direct-reception observations and does not send empty/unchanged tables.
No other radio, server mapping or portal metadata is changed.

Private profiles, serial logs, image provenance and MQTT capture remain under
ignored `private/bench/r004-update-20261024/`. Historical diagnostic evidence
remains under `private/bench/R004-ina219-20261021/`. Raw keys, broker credentials,
neighbor identities and location data are excluded from Git.

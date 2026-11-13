# Fresh R001 board preparation - 2026-11-12

The owner supplies one bare RAK19007 with INA219/AHT21, requests identification,
firmware/settings preparation for Sunday, and explicitly starts new repeater/
gateway numbering. Case, battery, solar and location selection wait until
deployment. [The current roster](../../records/deployment-nodes.md) supersedes
historical number-to-hardware assignments without erasing their evidence.

## Identity, backup and retained firmware

- Fresh label **R001 / SNORR Repeater 001**, radio **!f95b5501**.
- USB **E93C5FF0F97DD76B**, runtime **COM19**; hardware ID
  **6bd77df9f05f3ce901555bf96d5ed7fc**. Carrier/modules are owner-confirmed;
  the API independently identifies the RAK4631 core.
- Reports ordinary **2.7.26.4c96b9b / rak4631**. The already selected firmware
  is retained; no flash, factory reset or key replacement on R001.
- Full private API profile, all channels, owner/identity/security and node
  information captured before writes. `before.json` SHA256:
  **91de2ec3ce9b9ccd96ed2e773331e2e34c94b4fdc20728e49b0141bb81bb7d7f**.
  Exact ordinary [UF2/OTA recovery assets](repeater-deployment-image.json)
  remain available separately. The installed runtime metadata is not a fresh
  flash-byte/hash readback or raw-flash backup.

## Saved configuration and verification

The incoming settings already have ROUTER, enabled AHT/environment/device
reports at 180 seconds, SNNS and the intended private pilot radio. INA219 power
reporting is disabled and a historical fixed location is present. Change only
the radio names, enable power reporting and remove that historical fixed
position through the supported command. No site coordinates are invented.
The owner then requires **CLIENT for all bench preparation**. Switch R001 to
CLIENT, retain the other intended settings and accept the firmware's CLIENT
`power.ls_secs` normalization to **300 seconds**, with power saving disabled.
Complete saved-profile comparison and explicit-reboot readback pass afterward.

| Setting | Final state |
| --- | --- |
| Role / rebroadcast | **CLIENT / LOCAL_ONLY** on the bench; ROUTER reserved for deployment |
| Device / environment / INA219 power | All enabled, **180 seconds** |
| SNNS | Enabled, over LoRa; saved device interval supplies 180-second baseline; jitter/admission remain |
| Standard NeighborInfo interval | **21,600 seconds**, retained |
| Radio | Private primary only; **US / LONG_FAST / slot 35 / 10 dBm / hop limit 3**, boosted RX, retained |
| MQTT / primary uplink/downlink | Disabled, retained |
| Location | Fixed-position mode disabled and old saved coordinates cleared; actual site pending |
| Security | Own keys/private channel unchanged; two existing admins preserved, including the enrolled B002 public key |

Complete owner/config/module/channel comparisons pass after save and after an
**explicit reboot**, including absent old coordinates. Both profiles still
match after sensor and paired RF testing. Actual remote administration through
a relay is not established by local allowlist/readback verification.

## Sensor observations

An initial short startup capture contains device telemetry only; retain that
partial result rather than treating enabled settings as sensor acceptance.
A subsequent current-connection USB capture returns both source-attributed
measurement types with the full saved profile unchanged:

| Source sample | Observed data |
| --- | --- |
| AHT21/environment, source time 91 s | **27.700424 C**, **25.928116% RH**; INA environment voltage/current also present |
| INA219 channel-1 power, source time 106 s | **3.492 V**, **-326.7 mA** in firmware-native sign convention |
| Earlier device sample, source uptime 66 s | External-power indicator 101, ADC 3.487 V; no battery state/capacity inference |

These demonstrate sensor-data availability on this assembly. Source clock is
uptime-like/unknown UTC at this check. No battery/solar, charging, calibration,
enclosure or location test is performed, as requested. GH-4 remains resolved
by the owner's earlier replacement-board outcome.

## Radio fixture and measured results

A single direct device-telemetry request to already-heard peer **!9ea13cc0**
gets no matching reply despite a known peer public key: **INCONCLUSIVE**, not
a hardware failure diagnosis. The owner then connects a reference RAK and
explicitly authorizes wiping it without an old-configuration backup.

Only reference USB **70DF102F58D2A034 / COM27** is factory-reset. Its own keys
are generated and remain distinct from R001; compatible installed firmware
**2.7.15.567b8ea** is retained. **REF1** gets a full reboot-verified private
CLIENT/no-rebroadcast, zero-hop radio profile matching R001's region/preset/
slot/key. No V4 serial access or R001 diagnostic profile change occurs.

Use existing version-2 ASCII broadcasts, zero hops, no ACK/response, and match
source/destination/packet ID/nonce at the opposite USB interface. This avoids
depending on peer PKI discovery for the measurement. Three attempts per
direction, four-second receive deadline:

| Run | R001 TX at REF1 | R001 RX from REF1 | Interpretation |
| --- | --- | --- | --- |
| Original 0.3-second inter-attempt pause, 24.8 s | **2/3**, successful -32 dBm / 6.5-7 dB | **2/3**, successful -38 dBm / 6-6.25 dB | Second packet missed in each direction; strict burst criterion fails. |
| Same packets/matcher/deadline, **5-second pause**, 43.7 s | **3/3**, -31 to -32 dBm / 6.5-7 dB | **3/3**, -37 dBm / 6.5-6.75 dB | **PASS for the paced bench function check**. |
| Final **CLIENT**, same 5-second pause, 44.4 s | **3/3**, -37 dBm / 5.75-6.25 dB | **3/3**, -43 to -44 dBm / 5.5-7 dB | **PASS after the requested bench-role change**, both profiles preserved. |

Both complete profiles remain unchanged. The comparison demonstrates a paced
two-way link; it does not isolate the initial burst-loss mechanism or prove a
board fault, range, sustained delivery percentage, forced relay or field
coverage. No firmware/radio policy is changed to obtain the paced result.
Keep both runs; do not convert the first result into a pass or generalize this
one comparison to historical triage units. Both serial handles are closed.

Private logs, per-packet receipts, sensor samples and original/intended/final
full profiles are under ignored
`private/bench/sunday-rak001-20261113T015750Z/`. Public records contain no keys,
raw coordinates or member tracks.

## Handoff

Board-level firmware/settings, sensor-data availability and paced radio
function checks are complete. Attach the physical **R001** label to USB suffix
**D76B**. Keep **REF1** connected for the next independently identified RAK.
Leave R001 in **CLIENT**. On Sunday, apply the actual site and ROUTER role
after assigning the case/power assembly; recheck the 180-second report settings
because role changes can install defaults. Portal enrollment under the fresh
roster and end-to-end/forced-relay acceptance
remain separate. No historical label supplies those selections.

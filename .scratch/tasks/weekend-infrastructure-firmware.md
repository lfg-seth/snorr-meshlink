# Weekend infrastructure firmware preparation

## Owner amendment - 2026-11-12

All bench-prepared nodes must remain **CLIENT**. Final ROUTER changes happen
Sunday, followed by complete cadence/profile verification. Use the
[batch ID label station](../../docs/operations/rak-batch-station.md) for 4-8
connected RAKs; sensor fit is mixed and owner-supplied per !ID.

Start all repeater/gateway labels fresh using the
[current physical roster](../../records/deployment-nodes.md). Case, battery,
solar and location will be selected Sunday; clear stale locations rather than
inventing replacements. Old numbered updater/role-helper selections below are
historical and cannot identify a freshly numbered board. The first R001 is
USB E93C5FF0F97DD76B, with retained 4c96b9b and
[completed board checks](../../docs/operations/r001-commissioning-20261112.md).

## Selected outcome and ownership

Owner selects RAK repeaters and screenless Heltec V4 gateways, two bench
windows (today/tomorrow) and Sunday deployment. Prepare the RAK ordinary-image
install/recovery inputs and one concise firmware acceptance checklist. The
tracker owns status; this brief does not authorize an unidentified board write
or declare the overall mountain deployment accepted.

This session owns RAK artifact preparation and these records. Another active
chat owns the screenless V4/SD firmware and its board/serial operations under
[LOCAL-10](local-10-screenless-v4-gateway.md). Do not edit, build from, stage or
publish that chat's unfinished shared firmware changes. Preserve independent
source pins for a proven RAK image and a newer V4 candidate if needed.

GH-4 is resolved on the owner's report that replacing INA219 boards fixed the
discrepancy, with no discrepancies seen since. Retain the existing sensor
firmware corrections; no new INA219 diagnosis is part of this assignment.

## RAK candidate preparation

- Prefer the existing bench-proven ordinary `rak4631 / 2.7.26.4c96b9b` image
  from published source `4c96b9ba0`, unless a demonstrated RAK defect requires
  a change. Verify exact local assets and manifests before choosing reuse or a
  clean isolated build. Do not substitute the older `0634b77` bundle or the
  historical `0b65f2e` public prerelease merely because they are downloadable.
- Retain saved device/SNNS cadence behavior, AHT compatibility and INA219
  channel/read/error fixes. Exclude diagnostic, dummy-load and sniffer targets.
  Preserve normal airtime admission and the minimum SNNS interval.
- Produce/check matching UF2 and OTA assets, exact source/target/flags,
  filenames/sizes/SHA256, install instructions and rollback inputs. An old
  release tag must never receive different bytes. Keep source verification,
  artifact publication and actual board installation separate.
- Reuse the existing updater and role/location/admin helper. Each selected
  board needs identity and full private backup, intended role/fixed position/
  B002 admin enrollment, fitted-sensor settings and full saved-profile readback
  through reboot. Use independent readback after an ambiguous write response;
  do not blindly retry. The ordinary image's CLIENT default does not prove the
  intended deployment role was applied.

## Screenless V4 handoff to its implementation owner

The selected screenless target, SD bus/partitions, recording and daily SD-health
support remain owned by the existing LOCAL-10 brief. The firmware handoff must
also identify exact source/image/checksums and verify:

- MQTT credentials are absent from logs; broker TLS identity is verified with
  documented trust/time provisioning, including cold startup. Do not treat
  `setInsecure()` as completed TLS acceptance.
- Wi-Fi and broker loss recover without a manual restart. Record queue drain,
  reset counts and fresh post-recovery traffic. Unknown clocks remain truthful
  until NTP succeeds; losing Wi-Fi at boot must not invent fresh health times.
- Own reports retain the selected 300-second baseline; gateway mesh relaying
  and MQTT downlinks are suppressed as selected. Preserve member GPS packets,
  source timestamps, existing SNNS/SNGH compatibility and private identities.
- SD absence/removal/write failure does not block radio/backhaul. Verify the
  selected rotation and loss reporting contract, full intended profile after
  reboot and recovery inputs before an inaccessible placement.

## Bench windows and freeze

First available window: identify selected units; verify candidate hashes;
back up/apply/reboot-check their intended configurations and obtain fresh
device/fitted-sensor/SNNS reports. Exercise authorized and unauthorized remote
admin on a selected RAK and confirm the existing acknowledgment caveat is
handled by independent readback. One owner controls each board/serial port.

Second window: force a real relay path excluding direct reception, verify
member GPS reaches the V4/MQTT/portal, and test interrupted admin commands,
Wi-Fi/broker recovery and power-cycle persistence. Preserve failed attempts,
timestamps and actual reporting gaps. Several successful cycles establish only
that bounded run, not long-term runtime or coverage.

Freeze the exact passing source/artifacts/configurations before departure.
Record per-device pass/fail/unverified, retain a spare/recovery package and
accept only the exact bytes tested. Report unfinished firmware gates explicitly
for the owner's deployment decision. Portal polish, broad release-version
redesign, new protocols and additional recorder assignments stay outside this
bounded preparation; the other chat's selected SD feature is not cancelled.

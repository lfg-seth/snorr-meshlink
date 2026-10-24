# LOCAL-3 — Production firmware readiness before mountain redeployment

Parent: [LOCAL-6 - SNORR firmware releases](28-snorr-firmware-releases.md). Shared product
versioning, cross-target manifests/changelog and fleet rollout accounting live
there; this child supplies its implementation and target-specific acceptance.

Created 2026-10-23 at the owner's request. Status: **Next — scoped, not implemented**.
This is the consolidated firmware release and board-acceptance ticket for
R001–R006, with explicitly identified G001/G002 dependencies. The current request
authorizes assessment and ticket consolidation; it does not flash boards or
authorize placement. Passive member GPS delivery remains the first priority.

## Baseline and scope

R006 runs ordinary `2.7.26.0634b77`: AHT compatibility, corrected INA219
telemetry and SNNS, with device/power configured to 180 seconds and environment
disabled. Three automatic cycles reach both gateways; device/power gaps are
180 seconds and SNNS gaps 195 seconds. Portal acceptance for this update is
pending access. R001–R003/R005 still have ordinary `2.7.26.0b65f2e`; R004 has
the separate `2.7.26.09d8a9d` INA219 diagnostic image. Published source is pinned
at `5c2c1adad`; the new production download pointer remains unset.

Evidence: [rollout and release state](../../../docs/operations/repeater-update.md),
[flashing handoff](../../../docs/operations/board-flashing-handoff.md),
[INA219 audit](../../../docs/operations/ina219-audit.md).

## Required firmware and configuration work

### Assignment sequence

Select one outcome at a time through the tracker. These boundaries partition
the criteria below; they do not create a second queue or authorize a board run.

| Outcome | Lane / inputs | Completion boundary |
| --- | --- | --- |
| [Saved SNNS interval](../../tasks/local-3-snns-interval.md) | Software; pinned source and toolchain | Section 1 code, actual-source tests and affected builds; hardware checks remain explicit. |
| Selected-controller remote administration | Bench; interval implementation, identified board/controller and authorized keys | Section 2 authorized/unauthorized behavior, relay path, profile restoration and reboot evidence. |
| Outage-safe neighbor freshness contract | Software; existing delay evidence and gateway coordination | Section 3 decision and replay/ingestion tests; delayed reports cannot revive stale links. Implement the selected contract before live acceptance. |
| RAK release artifacts and updater integration | Software; reviewed changes and LOCAL-6 metadata foundation | Section 5 source/build/manifest/CI/public-download verification and rollback pointer; no board rollout. |
| Selected-board rollout and receipt checks | Bench; verified artifacts, portal access and named board | Section 5 per-board identity/profile/reboot and both-gateway/authenticated receipts. |
| Battery-only soak and deployment gate review | Bench; rollout, GH-4/GH-8/LOCAL-4 and agreed criteria | Section 5 sustained measurements plus dependency disposition; field gates remain separate. |

Remote-admin setup and freshness design can be prepared independently; their
implementation must coordinate shared firmware writes. A ready software step
can proceed while a selected-board test waits for access/hardware.

### 1. Remotely configurable SNNS interval

- [ ] Make RAK over-LoRa SNNS use the saved
  `telemetry.device_update_interval`, as discussed with the owner. Device and
  SNNS reporting then share a baseline; environment and power retain their
  separate settings. Document this coupling in the updater/profile guidance.
- [ ] Define zero/unset as the existing RAK 180-second fallback and clamp values
  below 180 seconds for SNNS. Support longer configured intervals safely, with
  explicit overflow handling; do not silently retain the old one-hour compile
  limit. Standard `neighbor_info.update_interval` is not the selected setting:
  its existing admin validation enforces the separate standard-report minimum.
- [ ] Preserve random 0–15-second post-report jitter, the 15-second scheduler,
  startup delay, empty-report suppression, bounded rotation/expiry, background
  priority and airtime/channel gates. Preserve gateway local-only reporting
  cadence and disabled RF TX. A configured interval is not a delivery guarantee.
- [ ] Test actual module behavior for unset, below-minimum, 180/300/900 seconds,
  extreme input, shortening/lengthening, reboot, timer rollover and local/radio
  mode changes. Verify how admin writes/reboots affect the next send, without
  burst catch-up or accidental loss of the cooldown.

### 2. Prove remote administration before nodes become inaccessible

- [ ] Inventory each target's existing admin authorization privately. Provision
  the selected controller public key through an explicitly scoped board update;
  preserve node identities and channel keys. Shared channel membership alone
  must not grant admin access. Test unauthorized-key rejection and authorized
  read/change/readback, session handling and reboot persistence.
- [ ] From a transmitting controller, change device/SNNS cadence remotely and
  measure fresh reports; restore the intended production value and verify the
  complete profile. Include a relay-path test and interrupted-command recovery.
- [ ] Record the actual supported controller/app/CLI and physical recovery
  procedure. Existing G001/G002 and portal are receive-only; this ticket does
  not silently enable gateway downlink or build portal remote administration.
  A new gateway transmit path needs a separately selected scope if required.

### 3. Close neighbor freshness through relay/backhaul outages

- [ ] Resolve the shared GH-51/GH-52 delivery-age contract for RAK reports and
  gateway reports/forwarding. Test delayed RF delivery, MQTT queue/reconnect,
  duplicates/replay, reboot and unknown clocks. A newly received old report must
  not revive a stale link as fresh.
- [ ] Prefer the simplest demonstrated solution: bounded queue residence/source
  expiry or a versioned source-time extension if needed. Absolute timestamps
  are **not already selected**. Preserve relative ages, boot/sequence identity,
  valid zero SNR, passive reception filters and raw history. Any clock-based
  solution must explicitly handle unavailable/future/stepped time.
- [ ] Test the chosen firmware contract with portal ingestion and expiry through
  both gateways. Keep legacy/unknown-time data truthful, including telemetry
  receipt fallback. Prove the two-hour hearing limit or record that the release
  does not meet it; do not equate receipt time with hearing time.

Current portal relative-age behavior is already deployed; this work addresses
unseen upstream delay, not a mandate to deploy historical draft PR #50.
[Current decision](24-neighbor-current-state.md).

### 4. Gateway prerequisites (moved to LOCAL-4)

Gateway MQTT credential-log removal, verified TLS, unattended reconnect,
INA219/power acceptance and gateway-specific release/soak now belong to
[LOCAL-4](26-gateway-production-readiness.md), created 2026-10-23. GH-40's
remaining reconnect acceptance moves there too. This ticket retains the shared
SNNS freshness contract in section 3 and RAK readiness. Neither move claims a
fix or completed verification; LOCAL-4 is an end-to-end deployment dependency.

### 5. Release and per-board production acceptance

- [ ] Retain AHT detection and INA219 union/channel-1/error/multiplier fixes.
  Ordinary production images exclude INA219 debug and GPIO31 dummy-load flags.
  Complete R004's evidence handoff before replacing its diagnostic image.
- [ ] Resolve release Actions publication, publish verified UF2/OTA artifacts,
  source/manifest/checksums and rollback version, then set the production pin.
  A successful local build or unpublished bundle is not a published release.
- [ ] Test relevant actual-source sensor/neighbor/release paths; build each
  affected target. Pin published firmware source through this repository and
  update the updater's verified manifests/profile expectations.
- [ ] For every selected board, identify hardware, privately back up its complete
  profile/keys, apply the verified image and independently compare intended
  configuration through reboot. Preserve per-board fitted sensors: R006 is
  INA219-only; R001–R005 retain their selected environment profiles unless
  changed deliberately after physical identification. Verify R001/R002 sensor
  presence/detection and fresh temperature, rather than assuming enablement
  proves a working sensor.
- [ ] Measure fresh device, fitted-sensor and SNNS reports through each gateway
  and authenticated portal, with source/receipt clocks, duplicates and cadence
  separated. Restore server access and update portal cadence metadata. Record
  missing reports and actual jitter/congestion; keep exact locations private.
- [ ] Agree and complete a battery-only soak including power interruption,
  automatic boot, relay traffic, gateway outages and recovery. Record duration,
  reset/missing-report counts, airtime and GPS freshness against agreed criteria.
  Three successful bench cycles alone do not pass sustained acceptance.

## Consolidation and dependencies

Consumed means ownership moves here; it does **not** mean the criteria passed.
Immutable imports and GitHub issues/Project remain unchanged during the trial.

| Existing work | Disposition |
| --- | --- |
| [GH-51 gateway timing](../../../records/tracking-import/github-51.md) / [GH-52 repeater timing](../../../records/tracking-import/github-52.md) | Consumed into section 3 as one shared contract; original timestamp-only proposal remains superseded by the open design choice. |
| [GH-26 R001](../../../records/tracking-import/github-26.md) / [GH-27 R002](../../../records/tracking-import/github-27.md) | Remaining sensor, sustained and both-gateway acceptance consumed into section 5; preserve completed flash/profile evidence. |
| Three-minute repeater rollout | Firmware release/updater/remaining-board acceptance consumed here. R006 private map placement and pending portal acceptance remain a separate current handoff. |
| [GH-4 INA219](../../../records/tracking-import/github-4.md) | Separate hardware diagnosis dependency: confirm shunt/polarity and simultaneous same-path meter readings, including battery-only operation. No arbitrary scaling fix. Unvalidated current cannot support runtime/charging claims. |
| [GH-8 utilization](../../../records/tracking-import/github-8.md) | Separate diagnosis dependency; measure all selected nodes at the proposed cadence before accepting airtime/GPS impact. No blind role or radio-power change. |
| [GH-40 reconnect](../../../records/tracking-import/github-40.md) | Remaining acceptance consumed by LOCAL-4; original evidence retained. |
| [GH-2 GPS/runtime](../../../records/tracking-import/github-2.md), [GH-3 relay/outages](../../../records/tracking-import/github-3.md), [GH-18 field plan](../../../records/tracking-import/github-18.md) | Separate deployment gates: phone-free GPS, 15-minute stale threshold, member runtime four-hour minimum/12-hour target, forced relay, offline viewing and agreed field criteria. Those member-runtime targets are not an unattended repeater power budget. |
| GH-47 / GH-53 | Existing portal freshness/display verification stays separate; coordinate delayed neighbor and unknown-clock telemetry acceptance. |

Before mountain placement, also confirm actual repeater battery/solar autonomy,
enclosure/weather/power behavior, site access and the intended radio/antenna
configuration against current primary-source requirements. Record criteria and
measurements in the existing inventory, sites and field records. These are
deployment gates, not established firmware defects or proof of readiness.

Deferred portal messaging/admin GH-14, known-network switching GH-15, browser
flashing GH-16 and member no-fix battery broadcasts LOCAL-2 remain parked. This
ticket does not expand member firmware or implement those features.

## Next action and completion

Next: implement and test the saved-interval change, then verify the chosen
controller's admin setup on an explicitly selected bench board. Resolve the
shared freshness contract and gateway prerequisites before final release
acceptance. Hardware actions require their identified board scope.

Completion requires linked source/release evidence, individual board acceptance,
and explicit disposition of all dependencies. Distinguish firmware ready from
mountain deployment accepted; failures/unknowns stay open rather than becoming
implicit waivers. No build, flash, remote write or field result is claimed by
creating this ticket.

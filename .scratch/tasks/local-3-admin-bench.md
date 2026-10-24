# LOCAL-3: R006 and gateway interval/admin bench pass

## Outcome and inputs

Run the owner-authorized 2026-10-24 bench pass against
[LOCAL-3 section 2](../pilot/issues/25-production-firmware-readiness.md#2-prove-remote-administration-before-nodes-become-inaccessible)
and the [saved-interval contract](../../firmware/SNORR_NEIGHBORS.md).
Use reviewed/published source `4c96b9ba0`, ordinary `rak4631` and dedicated
`heltec-v3-gateway` images. This is an explicitly selected local-build bench
update; published production artifacts and rollout pointers remain separate.

## Scope and ownership

One worker owns R006, G001, G002 and B002 serial/admin access. Identify hardware
on each connection, not by old COM names. Flash only R006 and the two gateways;
use B002's existing identity/firmware for PKI admin. Preserve all private keys,
channels, Wi-Fi/MQTT and fitted-sensor profiles. V3 LoRa TX remains disabled and
neighbor reporting local-only throughout. Temporarily authorize B002's existing
public key on R006, then restore the original admin allowlist and intended
reporting settings. No identity reset, region change, gateway downlink or server
deployment. User authorizes storing relevant secrets in 1Password Pilot.

## Prerequisites

Fresh complete profile backups for every selected board; gateway full-flash
recovery images; verified source/image checksums and application-only bounds.
Store concealed rollback profiles in `SNORR MeshLink — Pilot` before mutation.
Confirm G002 by radio identity after its USB reconnect. Preserve a physical
serial recovery path while testing remote authorization.

## Done and verification

- Application-only flash and independent version/complete-profile comparison
  through reboot on each selected target.
- Before allowlisting B002, observe an explicit unauthorized remote-admin
  result; after allowlisting, prove PKI read/change/readback and session handling.
- Capture actual R006 SNNS/device behavior at 180/300/900-second settings,
  including changes, first opportunity, persistence/reboot and no burst catch-up.
  Saved interval is a baseline; report measured gaps and airtime deferrals.
- Capture gateway-originated local SNNS and each gateway's fresh R006 receipts;
  compare observer/sequence/boot identities. Preserve RF-disabled readbacks.
- Restore and independently compare complete intended profiles, including the
  original R006 admin allowlist, through reboot; close serial sessions.
- Test interrupted edit/recovery when possible. A forced relay path requires a
  distinct transmitting intermediate and proof excluding direct reception; the
  receive-only V3s are not repurposed to manufacture that result. Record any
  remaining relay, portal, sustained or field gate explicitly.

## Evidence and handoff

Private evidence: `private/bench/local-3-admin-20261024/`. Store pre/post profiles
and relevant secrets concealed in 1Password Pilot without publishing values.
Record sanitized results in existing repeater/gateway operations, inventory and
field records; update tracker/session once at handoff. Commit/push explicit root
paths on `bench/local-3-admin-cadence`. Distinguish bench outcomes from release,
sensor calibration, battery runtime, outage-safe freshness and deployment gates.

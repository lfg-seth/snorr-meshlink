# LOCAL-6 - SNORR firmware beta-to-production releases and fleet versioning

Created 2026-10-23. Status: Next; parent ticket requested by owner.
Owner identifies current work as beta. Establish one SNORR release identity
across supported node types, with traceable changes and verified installations.
This ticket captures release policy and implementation work; it creates no tag,
build, firmware rollout or production claim.

## Children and ownership

| Child | Owned work |
| --- | --- |
| [LOCAL-3 - RAK/shared firmware readiness](25-production-firmware-readiness.md) | RAK implementation and acceptance, configurable SNNS interval, common SNNS timing contract and RAK-specific tests. |
| [LOCAL-4 - Gateway readiness](26-gateway-production-readiness.md) | Heltec V3 firmware/security/reconnect/INA219 and gateway acceptance; its power/enclosure work remains a related hardware deployment gate. |

This parent owns cross-target versioning, build/release manifests, changelog,
compatibility, release promotion and fleet installation accounting. Child
release checks feed this single release process, not independent SNORR version
sequences. Keep existing target tooling while migrating it; do not rewrite old
tags/assets. LOCAL-5 public Markdown docs can later present approved release notes.

Member trackers B001/B002 still run stock firmware. Select and test their exact
Heltec V4 target before including them in a SNORR release; otherwise declare the
release scope infrastructure-only. Do not call the entire fleet SNORR-versioned
while member nodes remain stock. Diagnostic R004 and MC00 sniffer must also be
explicitly accounted for or excluded from the operational production fleet.

## Accepted release naming - 2026-10-23

Owner selects **0.1.0 as what we have now**, without a beta suffix.
[Recorded 0.1.0 baseline](../../../records/firmware-releases/0.1.0.md) pins current
source and maps the existing mixed fleet to its last verified images. It does
not falsely claim that old binaries now contain the latest source or report a
new embedded version. This explicitly supersedes the earlier beta.N proposal.

Use `0.1.1` for fixes, `0.2.0` for the next development feature milestone and
**1.0.0** for first accepted production. Breaking changes during 0.x require
explicit migration/compatibility notes. Dates/names remain supplemental.

Use release dates as metadata and optional names as display subtitles. Neither
replaces the version used by tooling. Keep upstream Meshtastic version and full
source SHA separately visible; SNORR 1.0.0 is not Meshtastic 1.0.0.

Follow [Semantic Versioning 2.0.0](https://semver.org/) after defining our public
compatibility contract: SNNS payload/consumer compatibility, supported admin
and configuration behavior, and persisted configuration migrations.

- `1.0.1`: backward-compatible fixes.
- `1.1.0`: backward-compatible features.
- `2.0.0`: incompatible changes to that declared contract, with migration notes.
- An upstream version update is assessed for actual compatibility; its number
  is not mechanically copied into the SNORR version.
- A change to source, build flags/toolchain or shipped defaults after publication
  requires a new release identity and checksums. Never replace published bytes.

## Implementation and acceptance

### Assignment boundaries

These steps partition release work; current state remains in the tracker.
LOCAL-3/LOCAL-4 supply target changes and acceptance, rather than creating
independent product-version sequences.

| Outcome | Prerequisite | Completion boundary |
| --- | --- | --- |
| [Version and manifest foundation](../../tasks/local-6-release-foundation.md) | Pinned source, existing tooling and readback compatibility | One product version, cross-target manifest validation and supported identity readback; no new release publication. |
| Explicit release scope and changelog | Owner-selected next version/targets and compatibility assessment | Named target matrix, profile migrations, changes/limits and selected release gates. |
| Immutable target build and publication | Reviewed source, working CI and selected scope | Exact artifacts, manifests/checksums, rollback and independently verified downloads. |
| Fleet ledger migration | Existing inventory/manifests and per-board evidence | Desired versus last-verified installed identity/profile and rollout state; unknowns retained. |
| Selected-device rollout | Published matching artifact, named board and operation scope | Per-board profile/key preservation, readback, receipts and rollback evidence. |
| Release acceptance | Child source/bench/sustained/field evidence required for the selected stage | Gate-by-gate disposition and named supported fleet; development release versus production readiness explicit. |

Shared version/build files require sequential ownership when another worker
changes the same firmware checkout. Product baseline, built bytes and installed
fleet remain separate claims.

- [ ] Store one authoritative SNORR product version in the firmware source and
  build all included targets from the same reviewed source commit and pinned
  dependencies. Resolve current release CI execution before relying on it.
- [ ] Build an explicit target matrix (ordinary RAK4631, Heltec V3 gateway,
  selected V4 member target when in scope). Keep debug/load/sniffer targets out
  of production assets unless separately named and intentionally included.
- [ ] Produce one release manifest listing SNORR version, upstream version,
  exact binary source commit, toolchain/dependency provenance, target/hardware
  compatibility, flags, files/sizes/SHA256, SNNS wire version and compatible
  portal/decoder requirements. Preserve source-versus-packaging-commit distinction.
- [ ] Package target-specific assets under that single release. Example names:
  `snorr-1.0.0-rak4631.uf2` and `snorr-1.0.0-heltec-v3-gateway.bin`.
  Publish source/artifacts/manifest immutably and verify public downloads.
- [ ] Expose SNORR version plus target/source identity in a supported device
  readback path and display tooling. Verify upstream version parsers, protocol
  field limits and app compatibility before altering any existing firmware
  version string. Until then, trusted flash manifests and device readback remain
  the provenance basis; a version label alone does not prove binary bytes.
- [ ] Version the nonsecret baseline profiles separately and link required
  profiles/migrations to each release. Record per-device overrides and effective
  settings separately. A remote cadence change changes configuration, not the
  installed firmware version; defaults/migration changes shipped in a release
  are included in release notes and compatibility assessment.
- [ ] Maintain a changelog entry per release: date, changes since prior release,
  affected targets, fixes/features, defaults/profile changes, upstream changes,
  decoder compatibility, upgrade/rollback steps, test evidence and known limits.
  Keep development/production status explicit and link the relevant work tickets.
- [ ] Keep a fleet ledger with device number, hardware/target, desired release,
  last verified installed release/source/image checksum provenance, profile
  revision/overrides, verification date/evidence and rollout state. Distinguish
  pending, verified, failed, rolled back, unreachable and excluded devices;
  stale last verification is not a fresh live audit.
- [ ] Exercise partial rollout and old/new compatibility, preserve keys/profiles,
  verify reboot/readback and end-to-end receipts per device. Test rollback with
  compatible saved configuration and portal data handling. No bulk reset.
- [ ] Define release gates with child evidence: build/tests, bench, sustained
  operation and required hardware/field acceptance. A tag or successful build
  alone does not approve mountain deployment. Name the supported fleet and
  unresolved exclusions in the release record.
- [x] Record owner-selected 0.1.0 current source/fleet baseline and initial
  changelog, preserving the exact historical image evidence.
- [ ] Publish the next numbered development release only after identifying its
  exact source and target set. Production 1.0.0 requires validation of its exact
  shipped bytes and all selected release gates. Do not rebuild or replace 0.1.0
  bytes under an unchanged identity; preserve older releases for recovery.

## What "all nodes are on version X" means

All devices in the explicitly named operational fleet have a verified install
of their matching target artifact from release X. Different targets share the
product version, not binary hashes. Also report rollout completion and profile
compliance separately: "SNORR 1.0.0: 8/8 infrastructure nodes verified; member
trackers remain stock" is an illustrative format, not a current measurement.

Current source is one fork/branch, but installed images span several commits.
Existing manifests, inventory and board logs remain authoritative until the
ledger migration is verified. The owner-assigned product baseline is now 0.1.0; installed runtime versions
and rollout states are unchanged.

Next: implement the version/manifest/changelog and target-matrix foundation,
coordinate LOCAL-3/LOCAL-4 builds, and choose the next numbered release's explicit fleet
scope before publication. Hardware rollout retains per-board authorization.

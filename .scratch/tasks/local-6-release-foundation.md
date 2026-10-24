# LOCAL-6: coordinated firmware release foundation

## Outcome and inputs

Implement one authoritative SNORR product version and a validated cross-target
manifest foundation. [LOCAL-6](../pilot/issues/28-snorr-firmware-releases.md#implementation-and-acceptance)
owns release criteria; the [0.1.0 record](../../records/firmware-releases/0.1.0.md)
preserves the immutable baseline and mixed installed fleet.

## Scope and ownership

Reuse existing firmware packaging/verification tooling. Own version metadata,
manifest schema/validation and the supported readback integration in the
firmware fork, with linked guidance here. Coordinate shared build/version files
with the SNNS worker; run sequentially when their write sets overlap.

Choose the next version and explicit target scope with the owner before producing
release artifacts. Preserve the older tags/binaries and upstream identity.
This foundation does not publish a new release, migrate the fleet ledger, flash
boards or relabel stock member images. Source publication uses `snorr/develop`.

## Prerequisites

Inspect the pinned packaging tests and current CI failure evidence. Resolve
version-field/readback compatibility against the actual source before altering
device strings. Member-target inclusion remains an explicit selection.

## Done and verification

Validate version/source/target/toolchain/flags/checksums and wire/decoder
compatibility; reject mismatched or incomplete provenance. Test ordinary versus
diagnostic target inclusion and preserve source-versus-packaging-commit identity.
Verify the product readback path against upstream parser/field limits; report
hardware readback separately if no board is selected.

Run `python scripts/check-project.py firmware-release` plus tests added for the
new metadata/readback behavior. Record what portable tests establish and which
target builds, public downloads and per-board checks remain for release acceptance.

## Evidence and handoff

Update LOCAL-6's existing release guidance and tracker row; add a session entry
with source/commit, checks and limits. Next: separately select release scope,
build/publish exact artifacts, then perform authorized per-board acceptance.

# Publish the cached RAK build as a fork prerelease

Type: task
Label: wayfinder:task
Status: resolved
Assignee: rak-prerelease-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Question

Scope inherited release automation to the appropriate repository, publish the existing checksum-verified RAK build on the owner's firmware fork, and make future flashing chats download those assets instead of rebuilding.

## Comments

2026-10-16 — Owner explicitly authorizes workflow fixes and prerelease publication on `lfg-seth/firmware`. Cached source is `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`; both retained binaries pass their recorded size/SHA256 checks. Preserve those exact bytes and identify their build source separately from any subsequent release-workflow commit. No hardware flash/configuration is requested.

## Answer

2026-10-16 — Publish [SNORR RAK4631 2.7.26.0b65f2e prerelease 1](https://github.com/lfg-seth/firmware/releases/tag/snorr-rak4631-2.7.26.0b65f2e-pre.1) with the unchanged cached UF2/OTA ZIP, public build manifest and SHA256SUMS. Tag `snorr-rak4631-2.7.26.0b65f2e-pre.1` points at release-only source `8fe47325e38b82c8b2358293484ff845320d1be6`; actual binary build source is explicitly `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2`. No rebuild or history rewrite.

- Gate all six inherited packaging/publishing/version-bump jobs to `meshtastic/firmware`. Fork SNORR tags run only read-only manifest/size/hash verification; no upstream secrets/builds/publication. [Actual GitHub run](https://github.com/lfg-seth/firmware/actions/runs/38994730691): fork verification succeeds and all six upstream jobs skip.
- Six integrity regressions, YAML guard/permission checks, staged/public asset verification, exact manifest/checksums and repeat download-helper cache reuse pass. Trunk unavailable; new Python formatted with pinned Black. No firmware/hardware retest needed for release-only changes.
- [Flashing handoff](../../../docs/operations/board-flashing-handoff.md) now defaults to `python scripts/bench/download-rak-release.py`, caching only verified released assets. It distinguishes binary source from later tooling and avoids build-first upload wrappers. Original local build evidence remains available.

Release publication and download handoff are complete. Flashing, actual RF/MQTT device reporting and portal neighbor/current decoding remain follow-ups; the prerelease stays explicitly hardware-unverified.

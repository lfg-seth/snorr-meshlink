# Improve passive neighbor signal reporting in the RAK fork

Type: task
Label: wayfinder:task
Status: resolved
Assignee: rak-neighbor-signals-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Question

Update the existing RAK firmware branch to report more useful directional neighbor signal information for placement and tracking diagnostics.

## Comments

2026-10-16 — Owner explicitly brings the previously parked fork proposal forward: check whether it is already implemented and implement it if missing. Fetch confirms `snorr/rak-survey` remains at `cc5907b1f`, containing only the targeted AHT compatibility fix beyond the pinned release. Implement a passive, bounded direct-reception collector and versioned companion reports while preserving standard NeighborInfo and GPS. Build/test/publish source; hardware flashing, gateway provisioning and portal integration are separate follow-ups.

## Answer

2026-10-16 — Implemented and published as firmware `0b65f2e8444ea2dd3566f61ba2614d6eb33d3fd2` on `snorr/rak-survey`. [Source, build artifacts and rollout boundary](../../../docs/operations/rak-neighbor-signals.md).

- Separate primary-channel collector records direct-neighbor RSSI/SNR, monotonic hearing age and accepted observation counts, including valid zero SNR. Unknown/relayed/MQTT observations are excluded. Default 32-entry bounded storage, least-recently-heard eviction and independent 30-minute expiry.
- Versioned companion payload on private port 256 carries at most eight rows/152 bytes, rotating larger tables with explicit subset/eviction flags. Standard NeighborInfo/GPS remain unchanged. Existing module settings control activation; conditional background reports use airtime gates, jitter and five-minute minimum radio cadence.
- Exact source builds as `2.7.26.0b65f2e`; collector checks at capacities 32/10 and actual-module harness checks pass with sanitizers. Formatting/whitespace pass using pinned clang-format; Trunk unavailable. Full upstream native/MCP suites, real RF delivery and endurance remain unverified.
- Initial fork push was rejected automatically because only project publication was explicit. Owner subsequently identifies and authorizes `https://github.com/lfg-seth/firmware`; push succeeds. Keep the published source pinned here, with no separate patch packaging or remote history rewrite.

Source implementation is complete. No flash or device configuration performed. Portal `SNNS` decoding, verified two-gateway export and GPS/airtime/runtime comparisons remain separate follow-ups; no live neighbor or field-readiness claim.

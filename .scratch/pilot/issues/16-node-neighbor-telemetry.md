# Check node telemetry and directional neighbor signal reporting

Type: research
Label: wayfinder:research
Status: resolved
Assignee: node-neighbor-telemetry-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Question

What additional node data can the pilot capture, especially signal measurements reported by repeaters and gateways, and how can a table represent those observations accurately?

## Comments

2026-10-16 — Owner asks what else nodes can report and whether neighbor signal strength can be captured in a table. Verify pinned Meshtastic behavior and primary documentation, distinguish gateway packet reception from node-reported neighbor observations, and propose a table. Implementation scope is awaiting optional owner clarification; proceed with documentation in the meantime. Preserve existing GPS-quality and other working-tree changes. No radio settings, firmware, services or deployment changes are part of the research.

## Answer

2026-10-16 — [Node and neighbor telemetry](../../../docs/research/node-neighbor-telemetry.md) records pinned-source findings, other useful metrics and a proposed table/storage model.

- Gateway packet receipts can expose final-hop SNR/RSSI. Retain separate gateway observations even when the original GPS or telemetry report deduplicates. Original source identity is not necessarily the final transmitter; ambiguous relay identities stay unknown.
- NeighborInfo gives the reporting node's directional neighbor SNR, without RSSI or transmitted per-neighbor hearing timestamps. Preserve report receipt time without presenting it as a fresh last-heard measurement. Pinned recurring reports default to six hours, minimum four hours, with at most ten neighbors.
- NeighborInfo requires verified module/build/configuration support along the export path; isolated RAK reports need LoRa transmission enabled, and disabled gateway modules or core-only rebroadcast filtering can prevent delivery. Existing visible ROUTER profiles should not be changed to the deprecated REPEATER role for this feature.
- Proposed columns: observer, heard node, original source, SNR, RSSI, direct/relayed/unknown, report received, measurement age when known, and source. Store directional history and derive a latest view; no reverse-link, route-completeness or packet-delivery guarantee.
- Other candidates include uptime, channel utilization/transmit airtime, diagnostic counters, additional transmitted GPS fields and fitted sensors. Schema support alone does not establish automatic MQTT delivery or installed hardware.

Research is complete; implementation remains a separate next step. Recommend first extracting existing gateway receipt metadata without changing nodes, then verifying NeighborInfo availability/delivery for repeater-side rows. No live archive inspection, device readback, implementation, deployment or hardware testing performed.

### Fork customization follow-up

2026-10-16 scope update — Owner explicitly keeps the fork proposal for later while bringing the database-backed sample table forward in [Serve the demo and neighbor table from a separate PocketBase](17-database-demo-neighbor-table.md). Firmware work remains parked.

2026-10-16 — Owner asks whether our fork could improve NeighborInfo for project needs. [Tailoring our fork](../../../docs/research/node-neighbor-telemetry.md#follow-up-tailoring-our-fork) records a feasible infrastructure-only passive collector/exporter: latest RSSI/SNR with explicit presence, monotonic hearing age and optional bounded window summaries. Separate expiry from publication cadence and local neighbor capacity from per-packet size. A 32-entry local table, gateway MQTT summaries at 30–60 seconds and repeater LoRa summaries at 5–15 minutes are proposed bench starting points, not approved settings or measured capacity.

Preserve standard NeighborInfo interoperability using a versioned private companion message for additional data; standard decode/re-encode paths cannot be assumed to preserve new fields. Keep GPS priority, radio airtime gates, jitter, packet caps, partial-snapshot handling and gateway silence. Existing module-level reception is after duplicate filtering: counts represent accepted observations, not packet delivery percentage or every RF reception. Reconcile the newer fork branch before implementation. No firmware code/configuration, build, flash or deployment performed; this answers feasibility rather than accepting a final design.

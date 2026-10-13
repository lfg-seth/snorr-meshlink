# Distinguish LoRaWAN and the candidate mesh firmware

Type: research
Label: wayfinder:research
Status: resolved
Assignee: protocol_research (2026-10-12 setup session)
Parent: ../map.md
Blocked by: none

## Question

What do official sources establish about LoRaWAN versus Meshtastic and MeshCore for passive GPS reporting, phone-free operation, relaying, internet backhaul, and configurable update frequency? Which facts should guide a later choice using owned hardware?

## Completion evidence

A short primary-source report in `docs/research/protocol-baseline.md`, with explicit uncertainty where needed. Separate terminology, verified capabilities, and questions that require hardware or bench tests. Do not pick a firmware, promise coverage, or prescribe an operating radio configuration.

## Comments

2026-10-12: Created for background research during project setup.

2026-10-12: Claimed for primary-source research on local branch `research/protocol-baseline`. Findings will be captured in `docs/research/protocol-baseline.md` and returned to `main` after review.

## Answer

Resolved on 2026-10-12 with [Protocol baseline for the SNORR tracking pilot](../../../docs/research/protocol-baseline.md), researched on `research/protocol-baseline` and reviewed before incorporation into `main`.

The sources distinguish LoRaWAN's gateway/server architecture from Meshtastic and MeshCore mesh behavior. Meshtastic exposes GPS acquisition and broadcast timing configuration; MQTT map reports are a separate, slower publication feature. MeshCore's GPS settings do not by themselves establish autonomous member reporting for every build. Inventory and bench verification must establish actual compatibility and reporting behavior before choosing firmware or requiring a fork.

This resolves the source comparison only. It does not select an architecture, set acceptance criteria, or establish coverage, battery life, radio compliance, or achieved position freshness.

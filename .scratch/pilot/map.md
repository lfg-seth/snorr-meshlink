# Define an owned-hardware field pilot

Label: wayfinder:map

## Destination

A concise, evidence-backed pilot plan for passive SNORR member GPS tracking on Mount Charleston: participating owned hardware, a justified network/firmware choice, a dispatch data path, and agreed test criteria. This first checkpoint is provisional pending owner feedback.

## Notes

- Full mission and standing priorities: [Project brief](../../PROJECT.md).
- Keep it simple. Chart decisions now; implementation and installation follow when their prerequisites are settled.
- Use Wayfinder with the local tracker in [Tracker conventions](../TRACKER.md). For live design questions use grilling/domain-modeling lightly; avoid exhaustive interviews at this stage.
- For research, use primary sources and capture a linked report. Firmware changes are a possibility to investigate, not a settled requirement.
- Owned hardware comes first; no speculative purchase list.
- Child tickets live in `issues/`; find the frontier using the tracker conventions rather than duplicating open questions here.

## Decisions so far

- [Distinguish LoRaWAN and the candidate mesh firmware](issues/03-protocol-baseline.md) — Separate architectures; existing timing settings warrant a configuration-first evaluation, while hardware compatibility and passive behavior still need bench evidence.

## Not yet specified

- Which hardware combinations can form the pilot after inventory and firmware evidence are available.
- How much firmware customization is actually needed for the agreed reporting behavior.
- A minimal dispatch portal and ingestion path, including multiple backhauls, delayed positions, and operation during outages.
- Test routes, acceptance thresholds, and a repeatable build/configuration for the pilot.
- Solar/18650 power and enclosure design matched to measured consumption and environmental requirements.
- Site surveys, permission, installation, maintenance, and member rollout after pilot evidence.
- Evidence needed for a supported expansion budget and stakeholder presentation.

## Out of scope

- Full mountain deployment and production portal implementation during this planning checkpoint.
- Law enforcement rollout; it remains a later project goal.
- Purchases, public publishing, external outreach, and grant submissions in this setup session.

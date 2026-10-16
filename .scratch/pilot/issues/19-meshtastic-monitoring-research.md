# Check Meshtastic monitoring and recording stacks for the pilot

Type: research
Label: wayfinder:research
Status: resolved
Assignee: monitoring-research-session-2026-10-16
Parent: ../map.md
Blocked by: none

## Question

Which current Meshtastic-specific monitoring/recording projects, Grafana dashboards, exporters and deployment templates fit our private encrypted MQTT feed and existing PocketBase/Python dispatch portal? What would deployment require, what data would each actually retain, and what staged setup and verification should we consider?

## Comments

2026-10-16 — Owner explicitly brings monitoring/logging exploration forward through Wayfinder. Research primary sources and distinguish metrics, service logs and exact packet archives. Evaluate compatibility with two V3 MQTT gateways, RAK repeaters, V4 GPS trackers, existing private raw archive and the Ubuntu Proxmox LXC. Scope recommendation: private sidecar alongside the dispatch portal, subject to owner feedback. Research/planning only; no service, broker ACL, device or firmware changes. Preserve unrelated staged/unstaged work.

## Answer

2026-10-16 — Research complete. [Meshtastic monitoring and recording projects](https://github.com/lfg-seth/snorr-meshlink/blob/f69b6a4/docs/research/meshtastic-monitoring-projects.md) compares current primary-source snapshots, ingestion/security paths, licenses, maintenance evidence, templates and data-retention/dedup limitations. Findings are committed as `f69b6a4` on `research/meshtastic-monitoring-20261016`, pushed successfully to origin. The isolated branch is an evidence asset; no PR or merge was made.

- MeshMonitor is the leading packaged evaluation candidate: standalone `subscribe_only` MQTT over TLS with private channel-key decryption, persisted telemetry, Prometheus metrics/Grafana assets and a Proxmox LXC template. Confirm feature availability in the actual pinned release and test two-gateway/GPS behavior. Its optional limited packet log stores summaries, not our exact original envelopes.
- tcivie's MQTT/TimescaleDB/Grafana bundle decrypts private-key traffic and provides dashboards, but packet-ID-only dedup drops second-gateway copies and its database prunes metrics after 30 days. Keep it separate from authoritative pilot evidence.
- MeshView and Malla offer useful packet exploration but lack TLS setup in the inspected intake paths. MeshView also logs secondary channel keys at startup. Hacktegic's Prometheus exporter supports MQTT TLS but skips encrypted packets. Local-radio polling tools add airtime and are a different design.
- [Proposed private monitoring setup](../../../docs/research/meshtastic-monitoring-setup.md) outlines prerequisites, metrics/log/archive separation, suggested dashboards, private access, recovery and planned acceptance checks. Preserve the existing exact PocketBase archive, content-aware position dedup, separate gateway receipts and 15-minute GPS-measurement stale rule.

This resolves research, not deployment or stack selection. [Choose a private monitoring scope and pilot stack](20-monitoring-scope-stack.md) remains open for the owner. Current resource headroom, paired-gateway compatibility, exact release selection, retention and access remain unverified/unaccepted. No live access, install, service/broker/device changes or runtime tests were performed. Main-worktree planning/tracker/session edits remain uncommitted; unrelated work is preserved.

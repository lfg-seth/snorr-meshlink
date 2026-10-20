# Choose a private monitoring scope and pilot stack

Type: grilling
Label: wayfinder:grilling
Status: open
Assignee: unassigned
Parent: ../map.md
Blocked by: 19
GitHub: https://github.com/lfg-seth/snorr-meshlink/issues/10

Migration 2026-10-17: GitHub owns current work status. Metadata above is a historical snapshot; preserve the discussion and decision evidence below.

## Question

Should the pilot add private metrics dashboards alongside the existing portal, and which collector/hosting approach should be evaluated first? Should searchable service logs be included immediately or follow the metrics evaluation?

## Comments

2026-10-16 — Follow-up to the owner-requested monitoring exploration. The research report and proposed setup are inputs, not an accepted implementation decision. Preserve exact MQTT archiving, measurement-time GPS freshness, separate gateway receipts, and existing silent infrastructure badges. Do not activate parked custom firmware, Slack, or Wi-Fi automation work.

## Answer

2026-10-17 — Owner explicitly selects and authorizes a private MeshMonitor evaluation/deployment on the separate existing Ubuntu LXC. Use standalone MQTT `subscribe_only` over certificate-verified TLS against the existing encrypted project feed. Reuse the owner's existing Grafana and Prometheus hosts; internal network access only. Metrics first; searchable logs remain deferred. Start with 30 days of Prometheus metrics and no automatic MeshMonitor packet/history pruning. Prometheus retention is server-wide; inspect existing retention and storage before applying the agreed duration. No public route, notification integration, radio change or historical import is authorized by this decision.

The existing PocketBase exact MQTT archive, separate gateway receipts, GPS-measurement-time freshness and silent infrastructure badges remain authoritative. Upstream charts are exploratory until timestamp/dedup semantics are verified; receiving an old position cannot establish a fresh GPS fix. Credentials/channel keys remain private. Record versions, access, persistence, backups, rollback and measured acceptance in the deployment record and GitHub deployment issue. This resolves stack/scope selection, not runtime acceptance.

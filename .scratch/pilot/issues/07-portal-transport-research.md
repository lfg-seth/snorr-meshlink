# Check portal MQTT hosting and backend options

Type: research
Label: wayfinder:research
Status: resolved
Assignee: codex-portal-transport-research-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

What do current primary sources establish about Meshtastic MQTT ingestion and one-gateway dispatch downlink, Cloudflare Tunnel broker exposure, and PocketBase as a simple locally administered portal backend?

## Comments

### 2026-10-12

Research supports the open dispatch-portal interview; technical feasibility is not a deployment or firmware-selection decision.

## Answer

2026-10-12 — Primary-source findings are in [Dispatch portal transport and backend](../../../docs/research/dispatch-portal-transport.md).

- Proxmox hosting with an HTTPS portal through Cloudflare Tunnel is feasible as a proposal. A normal stock Heltec MQTT TCP client cannot simply use a Cloudflare public TCP hostname: that route requires a client-side cloudflared adapter. Broker reachability needs LAN/site VPN, an actual MQTT TCP endpoint, or a separately verified software bridge.
- Meshtastic supports native protobuf MQTT ingestion and JSON `sendtext` through a designated gateway. Documented JSON commands need a technical downlink channel named `mqtt`, while `channel: 0` targets the single operational primary channel. Confirm exact topic/configuration on the selected firmware release.
- Preserve raw broker observations, derive deduplicated logical events, and separate GPS measurement age from gateway/server arrival time. Finite gateway queues and RF loss prevent a promise that every transmitted position is archived.
- PocketBase fits the small pilot's username/password, dashboard account administration, SQLite records, and SSE needs. It still needs MQTT ingestion/command logic, and its explicit pre-1.0 production-critical caveat is material for operational dispatch.
- One dispatch-capable transmitting gateway changes the previous receive-only intent. This research does not settle that workflow or radio-silence verification, select a backend, or authorize deployment/publication.

Documentation and source reviewed only; no installed-firmware checks, hardware tests, load tests, security tests, service deployment, or commit performed. Parent session will add the result link to the map.

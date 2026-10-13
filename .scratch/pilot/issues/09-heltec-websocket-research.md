# Check Heltec MQTT over WebSockets for Tunnel hosting

Type: research
Label: wayfinder:research
Status: open
Assignee: unassigned
Parent: ../map.md
Blocked by: none

## Question

Can current Meshtastic Heltec V3/V4 MQTT clients support MQTT over secure WebSockets through an HTTP Cloudflare Tunnel to a home-hosted broker, and what source-level dependencies and evaluation checks distinguish this candidate from a gateway-site bridge or an outbound connection to a separately hosted broker?

## Comments

2026-10-12 — Owner confirms local Proxmox VM and no inbound port forwarding. Source research only; no firmware implementation, extra equipment/service purchase, remote publication, or deployment. Focus on whether stock configuration works and what a custom transport would need, without estimating untested reliability or effort.

2026-10-12 — Owner explicitly deferred this investigation until later and asked portal planning to assume the local broker is reachable through Cloudflare using stock MQTT clients. Research agent interrupted and claim released; no completion implied. Do not resume this ticket until the owner asks to revisit connectivity. Existing transport findings remain evidence of unresolved compatibility, not a demand to settle networking during portal design.

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

2026-10-13 — Owner asked to revisit the MQTT broker issue, reopening connectivity research. Recheck stock-client transport and compare home hosting through site networking/bridging with a separate reachable private broker. Hosting preference awaits owner input; no deployment or firmware change authorized by a recommendation alone.

2026-10-13 — Rechecked primary sources and recorded a [broker revisit](../../../docs/research/dispatch-portal-transport.md#2026-10-13--broker-issue-revisited). Stock direct transport remains TCP/TLS; published Cloudflare TCP requires a client adapter. Recommend Mosquitto for evaluation; home site networking/bridge versus separate private-broker hosting awaits owner preference. Claim retained while discussing the route; research is not a hosting decision or deployment.

2026-10-13 — Owner supplied the old pilot broker and authorized read-only SSH investigation. [Server findings](../../../docs/research/dispatch-portal-transport.md#2026-10-13--existing-pilot-broker-inspected): Mosquitto active, external 8883 reachable but certificate expired, 1883 refused, password authentication configured and no topic ACL directive found. Existing endpoint reuse is recommended pending certificate/auth/access verification; no WSS modification is currently justified. No hosting adoption inferred; claim retained for route discussion.

2026-10-13 — Owner confirms hosting by Mike Rollins, ownership of the current domain and a planned port-80 change by Mike. Possible replacement hostnames captured in the [hosting record](../../../records/sites.md#broker-hosting-record--mike-rollins); migration is not selected. Certificate for the chosen new hostname and DNS/challenge routing are required before client cutover. No server change or decision resolution.

2026-10-13 — Owner explicitly put the broker issue on hold until Mike completes DNS/Nginx work. Mike is updating `mqtt.snorr.org` to point to the VM's public/proxy endpoint and placing the VM behind Nginx; completion, routing, certificate coverage and reachability are not verified. Mike owns certificate management. Intended path remains public TLS 8883 → Nginx → private MQTT 1883. Claim released; ticket stays open/deferred, not resolved. Do not resume broker research, reset, hardening or integration until the owner brings it back. On resumption, confirm the new endpoint/proxy path, adapt the fresh-reset installer away from direct broker TLS, then verify auth/ACLs, firmware settings and designated-gateway downlink. [Handoff](../../../docs/operations/mqtt-nginx-handoff.md).

2026-10-13 — Owner explicitly brought broker-only configuration updates forward during the infrastructure hold. Adapted/reset installer uploaded for private 1883 with no broker certificates; local sudo execution pending. Proxy source IP requested; default loopback-only. Mike's DNS/Nginx deployment remains deferred/unfinished. No research claim resumed or ticket resolved; configuration progress recorded in [maintenance notes](../../../docs/research/mqtt-server-maintenance.md#2026-10-13--private-backend-reset-adapted).

2026-10-13 — Fresh broker reset executed successfully by owner. Local auth/ACL checks passed; SSH follow-up verifies active Mosquitto on loopback 1883 only. Old state privately archived; see [maintenance record](../../../docs/research/mqtt-server-maintenance.md#2026-10-13--fresh-private-broker-installed-and-verified). Broker-local configuration complete; proxy source/restricted LAN access, external endpoint and actual firmware integration remain pending. Connectivity issue stays open/deferred with claim released.

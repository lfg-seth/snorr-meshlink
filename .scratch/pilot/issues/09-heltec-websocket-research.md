# Check Heltec MQTT over WebSockets for Tunnel hosting

Type: research
Label: wayfinder:research
Status: open
Assignee: unassigned
Parent: ../map.md
Blocked by: none
GitHub: https://github.com/lfg-seth/snorr-meshlink/issues/12

Migration 2026-10-17: GitHub owns current work status. Metadata above is a historical snapshot; preserve the discussion and decision evidence below.

## Question

Can current Meshtastic Heltec V3/V4 MQTT clients support MQTT over secure WebSockets through an HTTP Cloudflare Tunnel to a home-hosted broker, and what source-level dependencies and evaluation checks distinguish this candidate from a gateway-site bridge or an outbound connection to a separately hosted broker?

## Comments

2026-10-14 — Owner-run authenticated synthetic public TLS test passes: both V3 accounts publish and worker receives; anonymous/invalid logins, worker writes, gateway reads and JSON/unrelated-topic writes denied. Used temporary loopback SSH relay through external test origin because broker-origin public routing timed out. Relay closed; SSH verifies no 18884 listener and active Mosquitto. Initial uplink broker readiness established; actual firmware/worker integration and reconnect remain untested. Ticket remains open/unassigned; no broader research resolution inferred.

2026-10-14 — Owner resumes public endpoint testing after reporting DNS/Nginx live. DNS/TCP/TLS 8883 pass with a matching certificate expiring 2027-01-11; anonymous MQTT CONNECT receives no CONNACK and connection closes after about 10 seconds in two repeat probes. Root SSH on supplied port 64582 rejects available authentication, so current upstream/listener/firewall and authenticated ACLs remain unverified. [Sanitized evidence](../../../records/sites.md#broker-hosting-record--mike-rollins). Ticket stays open/unassigned; no protocol research claim or resolution inferred. Next inspect the proxy/backend path with working authorized SSH access. Other held work remains deferred.

2026-10-14 — Corrected `setheth` SSH login succeeds. Active broker remains loopback-only on 1883 and responds locally with anonymous access denied; separate-host Nginx cannot reach that listener. Privileged firewall/configuration inspection requires owner-interactive sudo. Await Nginx private source/upstream details and UFW status to prepare restricted LAN access, then verify external authenticated MQTT and ACLs. No remote change or ticket resolution.

2026-10-14 — Owner provides Nginx source `192.168.12.254` and current UFW rules. Prepared/uploaded guarded [private backend installer](../../../scripts/server/enable-mqtt-nginx-backend.py) for broker LAN `192.168.12.51`, retaining loopback/accounts and restricting 1883 to proxy. Syntax/checksum verified; privileged execution awaits owner sudo. Edge upstream must be plain TCP `192.168.12.51:1883`. External auth/ACL/reconnect and source restriction verification remain pending; no resolution.

2026-10-14 — Owner executes installer successfully and supplies active proxy-only UFW rules/local checks. SSH verifies active Mosquitto and both loopback/LAN listeners. Public certificate-valid TLS MQTT CONNECT now receives not-authorized CONNACK for anonymous/invalid logins in approximately 0.1 seconds: Nginx-to-broker reachability verified. Public 1883 times out. Valid-account publish/subscribe, external ACLs, unrelated-LAN denial and actual firmware/reconnect remain untested. Ticket stays open for remaining integration scope; no firmware/protocol choice or broader held work resumed.

2026-10-12 — Owner confirms local Proxmox VM and no inbound port forwarding. Source research only; no firmware implementation, extra equipment/service purchase, remote publication, or deployment. Focus on whether stock configuration works and what a custom transport would need, without estimating untested reliability or effort.

2026-10-12 — Owner explicitly deferred this investigation until later and asked portal planning to assume the local broker is reachable through Cloudflare using stock MQTT clients. Research agent interrupted and claim released; no completion implied. Do not resume this ticket until the owner asks to revisit connectivity. Existing transport findings remain evidence of unresolved compatibility, not a demand to settle networking during portal design.

2026-10-13 — Owner asked to revisit the MQTT broker issue, reopening connectivity research. Recheck stock-client transport and compare home hosting through site networking/bridging with a separate reachable private broker. Hosting preference awaits owner input; no deployment or firmware change authorized by a recommendation alone.

2026-10-13 — Rechecked primary sources and recorded a [broker revisit](../../../docs/research/dispatch-portal-transport.md#2026-10-13--broker-issue-revisited). Stock direct transport remains TCP/TLS; published Cloudflare TCP requires a client adapter. Recommend Mosquitto for evaluation; home site networking/bridge versus separate private-broker hosting awaits owner preference. Claim retained while discussing the route; research is not a hosting decision or deployment.

2026-10-13 — Owner supplied the old pilot broker and authorized read-only SSH investigation. [Server findings](../../../docs/research/dispatch-portal-transport.md#2026-10-13--existing-pilot-broker-inspected): Mosquitto active, external 8883 reachable but certificate expired, 1883 refused, password authentication configured and no topic ACL directive found. Existing endpoint reuse is recommended pending certificate/auth/access verification; no WSS modification is currently justified. No hosting adoption inferred; claim retained for route discussion.

2026-10-13 — Owner confirms hosting by Mike Rollins, ownership of the current domain and a planned port-80 change by Mike. Possible replacement hostnames captured in the [hosting record](../../../records/sites.md#broker-hosting-record--mike-rollins); migration is not selected. Certificate for the chosen new hostname and DNS/challenge routing are required before client cutover. No server change or decision resolution.

2026-10-13 — Owner explicitly put the broker issue on hold until Mike completes DNS/Nginx work. Mike is updating `mqtt.snorr.org` to point to the VM's public/proxy endpoint and placing the VM behind Nginx; completion, routing, certificate coverage and reachability are not verified. Mike owns certificate management. Intended path remains public TLS 8883 → Nginx → private MQTT 1883. Claim released; ticket stays open/deferred, not resolved. Do not resume broker research, reset, hardening or integration until the owner brings it back. On resumption, confirm the new endpoint/proxy path, adapt the fresh-reset installer away from direct broker TLS, then verify auth/ACLs, firmware settings and designated-gateway downlink. [Handoff](../../../docs/operations/mqtt-nginx-handoff.md).

2026-10-13 — Owner explicitly brought broker-only configuration updates forward during the infrastructure hold. Adapted/reset installer uploaded for private 1883 with no broker certificates; local sudo execution pending. Proxy source IP requested; default loopback-only. Mike's DNS/Nginx deployment remains deferred/unfinished. No research claim resumed or ticket resolved; configuration progress recorded in [maintenance notes](../../../docs/research/mqtt-server-maintenance.md#2026-10-13--private-backend-reset-adapted).

2026-10-13 — Fresh broker reset executed successfully by owner. Local auth/ACL checks passed; SSH follow-up verifies active Mosquitto on loopback 1883 only. Old state privately archived; see [maintenance record](../../../docs/research/mqtt-server-maintenance.md#2026-10-13--fresh-private-broker-installed-and-verified). Broker-local configuration complete; proxy source/restricted LAN access, external endpoint and actual firmware integration remain pending. Connectivity issue stays open/deferred with claim released.

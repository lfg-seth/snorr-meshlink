# Move the pilot MQTT broker to owner hardware

Planning draft, 2026-11-23.

Move Mosquitto from the [current hosted broker](../../records/sites.md#broker-hosting-record--mike-rollins)
to a dedicated guest on the [owned Proxmox host](../../records/sites.md#portal-hosting-record--owners-proxmox-lxc)
if capacity, power and connectivity checks pass. Retain `mqtt.snorr.org:8883`,
the existing gateway credentials and the `snorr/pilot` topic root so the
field fleet can reconnect with its saved settings. The production portal,
PocketBase, worker configuration and existing ingestion history stay in
the portal guest. The broker migration covers the passive GPS uplink.

The [November 23 checks](../../records/sites.md#2026-11-23-public-mqtt-reachability)
found public TCP/TLS failures from two locations and successful internal
MQTT probes. Moving the broker behind the existing public ingress leaves
that path in service. The target therefore needs a measured, independently
operated public TCP route.

## 1. Choose the ingress and confirm the host

Confirm available CPU, RAM and SSD capacity on the Proxmox host, a wired
LAN and fixed guest address, guest auto-start, and what keeps the host,
router and internet equipment powered during an outage. Confirm a private
backup destination off the physical host and who can recover the guest.
Confirm who controls DNS for `mqtt.snorr.org` and can approve DNS-01 and
cutover changes.
The existing portal's LXC allocation is evidence of a working host. Free
capacity, power backup and the public WAN path remain to be measured.
Co-locating both guests gives the portal and broker a shared failure point
at the Proxmox host and its site.

| Route | Conditions |
| --- | --- |
| **Keep inbound router forwarding off** | First look for an existing owner-controlled endpoint that can accept public raw TCP 8883 and relay it over an authenticated outbound tunnel from the broker site. Keep TLS end-to-end to Mosquitto. Prove the relay survives reconnects, exposes exactly the intended listener and has independent logs. A suitable endpoint is still to be identified. |
| **Allow one narrow inbound forward** | If the owner changes the no-forwarding preference, use a public IPv4 path and forward TCP 8883 to the dedicated broker guest. Verify reachability from cellular or another off-site network, including whether the ISP uses CGNAT or filters the port. Publish a DNS-only record for the tested address. Confirm how WAN address changes are handled before switching DNS. Keep guest and hypervisor administration on a private path. |

The existing HTTPS Tunnel continues to serve the portal. Cloudflare's
published raw TCP service needs a client-side `cloudflared` connection,
which the deployed Heltec profiles lack. Select a public MQTT route before
scheduling cutover. If there is no usable route under the current
no-forwarding preference, the owner needs to select a reachable edge or
approve the narrow forward. [Cloudflare Tunnel protocols](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/routing-to-tunnel/protocols/)
· [Cloudflare DNS proxy status](https://developers.cloudflare.com/dns/proxy-status/).

## 2. Stage the replacement while production runs

1. With the current broker admin, inventory the running Mosquitto version,
   enabled listeners, account and ACL files, account-to-gateway mapping,
   and persistence, retained-message and durable-session use. Use the
   deployed fleet and connected clients to validate the mapping. Get a
   consistent, owner-private backup of broker configuration, password
   hashes, ACLs and any needed persistent state. Rehearse an isolated
   restore with compatible Mosquitto versions and keep the original backup
   readable by the original version. Decide which persistent state to carry
   forward based on the inventory. [Mosquitto listener, ACL and persistence reference](https://mosquitto.org/man/mosquitto-conf-5.html).
2. Install a dedicated Mosquitto guest with native TLS on TCP 8883 and a
   fresh managed certificate for `mqtt.snorr.org`. Use DNS-01 for issuance
   before changing DNS and test automatic renewal and reload. Store the
   certificate key, DNS credentials, broker hashes and backups privately.
   Preserve existing accounts and ACLs, including read-only worker access
   and gateway uplink permissions. Rehearse a broker and host restart.
   [Let's Encrypt DNS-01](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge).
3. From the portal network and at least one off-site network, test the
   new ingress with the production name as the TLS identity while
   connecting to the candidate address. Reuse
   [the public MQTT check](../../scripts/server/check-mqtt-public.py) for
   TLS and anonymous rejection. Its authenticated mode assumes an early
   three-account roster. Reconcile the approved current account set and
   verify actual publish/subscribe and denial rules for that set before
   relying on it. Use non-retained test traffic isolated from the live
   portal and keep checks free of packet contents and credentials.
4. Use an owner-selected bench gateway with a test-only DNS override for
   the normal hostname, or a temporary staging name with a matching
   certificate. Verify authenticated connect, fresh GPS and gateway-health
   delivery to an isolated subscriber, and reconnection after Wi-Fi and
   broker interruptions. Restore and verify any temporary bench settings.
   Baseline directly connected field gateways and their expected receipt
   cadence before the move. Proposed staging soak is one full day,
   covering the morning period in which the current endpoint was unstable.

## 3. Make the cutover reversible

1. Agree on a staffed low-use window and a rollback owner. Record the
   current DNS records and TTL, lower TTL in advance if supported, and wait
   out the previous TTL. Check for a stale AAAA record or a LAN resolver
   override. Capture a verified broker backup and the portal's existing
   private backup, including its worker queue. Keep the prior broker and
   ingress available for rollback. If durable broker state is required,
   coordinate a final consistent capture and restore before redirecting
   clients.
2. Point production DNS to the new ingress. Keep a single production
   ingestion worker and reconnect it to the new endpoint while preserving
   its queue, credentials and TLS hostname. Test the worker's actual path
   from the portal network. If NAT hairpinning fails, stage a private DNS
   answer for the same hostname with a tested rollback, and keep an
   independent probe on the public path. Compare old and new broker
   connection logs. DNS changes leave existing TCP sessions connected
   until they close, and some clients may reuse a cached answer. Coordinate
   reconnects for clients staying on the old endpoint. If a relay through
   the previous ingress is needed to cover the DNS overlap, agree on it
   with that admin and rehearse it before the cutover.
3. Confirm certificate/hostname validation from the portal and off-site,
   an active worker subscription with an advancing receipt archive, and
   fresh direct receipts from the baseline gateways. Verify a new GPS
   measurement from a known reporting tracker in the signed-in portal,
   with the original timestamp and expected gateway route. Check that
   repeated receptions still produce one displayed measurement. Continue
   checking reconnects, receipt gaps, certificate renewal and off-host
   restore until the owner accepts the new path.
4. Roll back for a TLS or authentication failure, a disconnected worker
   that fails to recover, or missing expected live receipts past the agreed
   deadline. Set that deadline before cutover with time to act before the
   project's 15-minute stale limit. Restore the previous DNS and any
   portal resolver or ingress change, reconnect the worker to the old
   broker, and verify fresh receipts and GPS. Preserve the portal database
   and spool accrued during the attempt. Record any receipt gap while
   sessions or DNS caches converged. Retire the old route only after the
   owner accepts the new endpoint and confirms rollback coverage.

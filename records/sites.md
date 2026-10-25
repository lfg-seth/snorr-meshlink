# Candidate sites and backhaul

## 2026-10-25 - Valley overlook test candidates

Owner asks for easy-access sites around Las Vegas for test nodes. This is a
candidate shortlist; no site is selected, installed, permission-cleared or
RF-tested. Public visitor access does not establish unattended equipment permission.

| Sector | Candidate / access | Evidence and remaining question |
| --- | --- | --- |
| East | Hollywood Regional Park, 1650 S Hollywood Blvd; drive-up park/walking paths | [County](https://parkslocator.clarkcountynv.gov/Search/ParkDetail?parkId=43) confirms Frenchman foothills and skyline view. Inspect exact antenna horizon. |
| Northwest | Lone Mountain; developed park access, uphill hike for summit | [County](https://parkslocator.clarkcountynv.gov/Search/ParkDetail?parkId=28), [health district](https://app.gethealthyclarkcounty.org/neon2nature/traildetails.php?trail_id=122). Summit is not drive-up. |
| West/northwest | Buckskin Cliff Shadows, 3355 Cliff Shadows Pkwy; developed trailhead and foothill trails | [BLM planning evidence](https://eplanning.blm.gov/public_projects/2031812/200611006/20120188/251020168/DOI-BLM-NV-S020-2024-0007-EA__RRC%20-%20La%20Madre%20Foothills%20RAMP%20and%20EA.pdf). Exact city-facing test point/walk remain to survey. |
| Southwest | Exploration Peak Park, 9600 S Buffalo Dr; short uphill trail | [Health district](https://app.gethealthyclarkcounty.org/neon2nature/traildetails.php?trail_id=99) lists natural surface, moderate difficulty and panoramic view. |
| South | Anthem Hills Park / Anthem East Trailhead, 2256 N Reunion Dr; park plus uphill trails | [City](https://www.cityofhenderson.com/Home/Components/FacilityDirectory/FacilityDirectory/196/). Select a north-facing position above local obstructions; citywide coverage is unmeasured. |
| Southeast | McCullough Hills Trailhead, 295 Mission Dr; trail access | [City](https://www.cityofhenderson.com/Home/Components/FacilityDirectory/FacilityDirectory/253/752). Survey skyline clearance; trailhead parking alone may be screened. |
| North | Gass Peak area; conditional backcountry alternative | [FWS](https://www.fws.gov/refuge/desert) advises high-clearance 4WD and current-condition checks. No specific easy drive-up overlook verified; exclude summit from easy-access shortlist. |

Do not assume Red Rock Overlook/High Point Overlook or Desert View Overlook
provide clear valley links: [BLM](https://www.blm.gov/nevada/red-rock-canyon-nca/recreation)
describes intervening mountains east of Red Rock; [GO Mt Charleston](https://www.gomtcharleston.com/desert-view-overlook/)
describes a northbound desert-facing walk. Test exact horizons before allocation.
Next: owner selects candidate sites and attended versus unattended test scope;
verify access/placement permission and record measured results separately.

2026-10-23 R006 map point request - Owner supplies a point for **R006** and
authorizes placing its portal marker there. Exact coordinates and the
requested change remain private under `private/bench/repeater-location-20261023/`.
No portal map write has occurred: server DNS is unavailable. R006's local
three-minute firmware/profile update passes separately; it does not establish
the saved map location, a physical installation, site permission or coverage.
Next: regain server access, back up the saved state, apply only R006's
requested point/cadence metadata, and independently verify preservation and
recovery. [Current acceptance and limits](../docs/operations/repeater-update.md#r006-installed-verification).

2026-10-19 infrastructure location update — Owner supplies replacement coordinates for R001–R005 and G001–G002 and authorizes production database updates. All seven saved configuration locations exactly match the request through the authenticated live portal state; all nine device records and other configuration fields are preserved. This supersedes earlier shared-location assignments for current portal coordinates. Exact coordinates and before/after records remain private at `/root/meshlink-maintenance/location-update-20261020T022905Z`; pre-change verified backup is `meshlink-20261020T022820Z.tar.gz`. Historical provisioning files remain historical inputs, not location-update interfaces. No installation, site permission, coverage or radio-setting change is established. [Tracking/evidence](https://github.com/lfg-seth/snorr-meshlink/issues/32).

2026-10-17 private monitoring — Owner authorizes MeshMonitor on the separate existing Ubuntu LXC, reusing existing Grafana and Prometheus. Native MeshMonitor 4.17.0 now subscribes read-only to the encrypted MQTT feed; internal-only authenticated access, 30-day server-wide Prometheus retention, a separate Grafana dashboard, service restart persistence and isolated backup boot/row preservation pass. No packet/history pruning, public route, broker/radio configuration or field installation. Backups remain local; two-gateway/native-browser/storage-growth checks remain open. [Deployment and recovery](../docs/operations/meshmonitor-lxc.md).

2026-10-16 R005 planned location — Owner assigns R005 to R001's existing planned site (SITE-006). Authenticated live configuration verifies exact equality with R001's private coordinates. Sharing a location does not copy equipment or establish installation, permission or coverage. [Preparation](../docs/operations/r005-preparation.md).

2026-10-16 R004 planned location — Owner assigns R004 to R001's existing planned location (SITE-006). Live authenticated configuration verifies exact equality with R001's private coordinates; no coordinates enter Git. Installation/site permission/coverage remain unverified. Location sharing does not copy R001's battery, antenna or solar equipment. [Preparation](../docs/operations/r004-preparation.md).

2026-10-14 planned repeater sites — Owner supplies two exact locations, saved only in authenticated PocketBase and root-private provisioning. SITE-006: planned Las Vegas R001 location, Muzi whip. SITE-007: planned shared Las Vegas R002/R003 location, Muzi whip and fiberglass respectively. All three are registered and live bench telemetry reaches the portal; that does not confirm installation at these coordinates, site permission, mountain links or coverage. Each has planned four-cell/160 mA solar equipment. This owner-authorized three-device allocation supersedes earlier two-repeater-only preparation notes. [Operations](../docs/operations/repeater-telemetry.md).

2026-10-14 portal-integration access update — Owner corrects broker SSH to `mqtt.snorr.org` port `64582`; key-based owner-account access and a narrowly scoped existing worker-credential export succeed. The earlier default-port attempt at the old hostname times out. No broker account rotation, ACL/listener/firewall or TLS-proxy change. Existing channel, gateway and worker secrets are stored in the owner-authorized SNORR MeshLink — Pilot 1Password Environment; the LXC receives only its own read-only MQTT configuration and existing PocketBase worker credential. Candidate-site permission and RF coverage remain unverified.

Current handoff, 2026-10-14: the password compatibility fix is applied; both real V3 gateways deliver encrypted V4 fixtures and automatic GPS, and gateway reboot recovery passes. Portal ingestion remains unimplemented. [TEST-003 / TEST-004](field-results.md#test-003--first-real-mqtt-gateway-provisioning-attempt) supersede historical pending statements below.

2026-10-14 gateway compatibility finding — Both bench V3s associate with the owner-selected hotspot and obtain IPs; secrets remain private. A read-only subscriber authenticates through public certificate-valid TLS, but existing 48-byte gateway passwords exceed stock firmware's 31-byte capacity. Hardware MQTT provisioning/delivery is incomplete. A guarded two-account rotation to 30-byte values is uploaded, with isolated real-Mosquitto authentication/preservation/rollback tests passing; owner sudo execution pending. No production worker, ACL, listener or TLS-proxy change made. [TEST-003](field-results.md#test-003--first-real-mqtt-gateway-provisioning-attempt), [prepared fix](../scripts/server/fit-v3-mqtt-passwords.py).

Updated: 2026-10-13. Candidate entries below are owner-described possibilities. None has verified coverage, permission, or internet availability recorded. Existing deployments are recorded separately.

| ID | Candidate | Possible role | Internet possibility | Permission / feasibility | Next evidence |
| --- | --- | --- | --- | --- | --- |
| SITE-001 | Mountain repeater locations; exact sites TBD | Solar repeater | Unknown | Unverified | Candidate locations and field measurements |
| SITE-002 | Kyle Canyon fire department location | Repeater and backhaul | Possible fixed internet | Unverified | Confirm site, contact, permission, and connection |
| SITE-003 | Lee Canyon fire department location | Repeater and backhaul | Possible fixed internet | Unverified | Confirm site, contact, permission, and connection |
| SITE-004 | Member vehicles | Mobile node and backhaul | Starlink or cellular | Availability unconfirmed | Equipment, power, and representative routes |
| SITE-005 | Member homes in Las Vegas | Fixed node and backhaul | Home internet | RF reach and participation unconfirmed | Identify willing hosts and test mountain link |

Create a separate entry when a specific site is identified. Record hardware IDs, installation/access permission, survey/test IDs, power source, internet availability, and maintenance responsibility. Keep exact private home addresses and sensitive site access details in ignored local records.

2026-10-13 — Owner reports a rough idea of repeater locations from previous testing, but has not supplied landmarks, coordinates, configurations or results. No new site or measured coverage is inferred. Proposed [direct-link survey](../docs/research/repeater-operations-survey.md) will compare temporary antenna placements along mission routes, then separately verify onward relay paths. Candidate placement and test access do not establish permanent installation permission.

## Existing deployments reported by owner

### Portal hosting record — owner's Proxmox LXC

2026-10-13 — Owner confirms LXC creation, authorizes SSH setup and selects `meshlink.spp.lol` for Cloudflare Tunnel HTTPS. Inspected Ubuntu 24.04.5 amd64, 4 logical CPUs, 8192 MiB RAM, 512 MiB swap and 64 GiB SSD-backed root storage. Installed production static frontend/Nginx, pinned PocketBase and a persistent Python simulation worker with unprivileged service accounts, boot enablement and restart supervision. Private API/storage remain on loopback/owner-only paths. Owner configured the existing cloudflared connector; four edge connections and its loopback-8080 route are verified. No router forwarding or MQTT work resumed.

Local admin/member login, service restart persistence, proxy restrictions, independent client throttling and isolated backup restore pass. Public HTTPS/certificate checks pass with public DNS, but LAN DNS retained an old negative IPv4 answer, preventing desktop browser review during setup. Public authenticated sign-in remains owner verification; no admin credentials were sent through Cloudflare by the agent. Daily 02:30 Pacific backups retain 14 private archives on the same container disk; off-host backup destination/Proxmox backup setup remain outstanding. This deployment serves fictional simulation data, not live member tracks. [Setup and evidence](../docs/operations/portal-lxc.md).

### Historical hosting notes

2026-10-13 — Owner brings portal hosting setup forward after the desktop handoff hold and chooses an Ubuntu LXC on the owned Proxmox host, superseding the VM plan for this portal. Container creation and allocated resources are not yet confirmed. Recommended starting configuration: Ubuntu 24.04 LTS amd64 template, unprivileged container, 2 CPU cores, 2048 MiB RAM, 512 MiB swap allowance (requires host swap), and 32 GiB SSD-backed root disk. Use the appropriate LAN bridge with a reserved/static private address and start at boot. Run the static frontend server, PocketBase, Python worker and eventual cloudflared directly as services; nesting is unnecessary for this proposed deployment. Keep the database on backed-up container storage and plan daily backups to separate storage; database restore still needs verification. Sizing is an estimate for the pilot, not a load-test result; watch database/log growth and resource use. The MQTT integration hold remains in place. Sources: [Proxmox container guide](https://github.com/proxmox/pve-docs/blob/master/pct.adoc), [resource options](https://github.com/proxmox/pve-docs/blob/master/generated/pct.conf.5-opts.adoc), and [Ubuntu support lifecycle](https://ubuntu.com/about/release-cycle).

2026-10-12 — Portal hosting constraint: owner confirms the available Proxmox VM is on the local network and wants no inbound router port forwarding. Portal HTTPS remains a Cloudflare Tunnel candidate; remote MQTT transport remains unselected. Evaluate a compatible WebSocket firmware/bridge path or a separate reachable broker with an outbound home connection. No remote endpoint, paid service, gateway-site adapter, or network change approved/deployed.

2026-10-12 — Owner subsequently deferred connectivity investigation. Portal design should assume the local broker works through Cloudflare with stock MQTT clients. This records an explicit planning assumption, not measured reachability or verified compatibility; no network configuration or site permission changed.

2026-10-12 — Owner reports an available Proxmox VM for hosting the private MQTT broker and dispatch portal, with Cloudflare Tunnel proposed for online exposure. This is a hosting candidate, not a deployed service; host resources, network reachability, maintenance/backups, and broker transport remain unverified. Owner proposes one designated V3 for internet-to-LoRa dispatch replies, potentially with V4 MQTT uplinks too; this changes the prior receive-only direction only if agreed in the [portal interview](../.scratch/pilot/issues/06-dispatch-portal.md). No public endpoint or new installation permission recorded.

2026-10-12 — Owner subsequently confirmed the designated-V3 transmit exception in the portal interview. The other V3 stays receive-only. V1 portal outage fallback is local Meshtastic viewing, not a requirement to run the same portal with local ingestion while offline. Source research distinguishes portal HTTPS Tunnel from embedded MQTT TCP reachability; the broker route and gateway-site networking remain unselected.

2026-10-12 — Pilot scope includes owned RAK repeaters and 2 Heltec V3 receive-only internet backhauls. Repeater count, placement, backhaul hosts, internet availability, and installation permissions remain unconfirmed. Inclusion in the pilot does not establish use or readiness of the existing remote RAK deployments.

2026-10-12 — Owner selected 2 undamaged on-hand RAKs for initial relay evaluation; individual units/builds and placement remain unselected. Remote dispatch ingestion will use one private MQTT broker with the 2 receive-only V3 uplinks. Optional member-phone/cellular backhauls are conditional on compatible app proxy behavior and measured multi-gateway results; no member availability, cellular coverage, or additional site permission established. Local app viewing must work without internet backhaul.

- 2026-10-12: 2 RAK units associated with HW-001 remain deployed in remote areas at Mount Charleston. Exact sites, builds, operating status, power configuration, backhaul, and permissions are not recorded. These are separate from the updated 8 RAK units on hand (1 damaged).
- Owner plans recovery when replacement nodes are ready, rather than an immediate remote recovery trip. Replacement readiness and recovery dates remain unset.
- Owner subsequently reports a possible third mountain RAK repeater, or a destroyed unit, as explanations for the unresolved source-list difference. Neither is confirmed; no third deployed unit is counted in planning stock.
- Later inventory update: an additional RAK was found on hand with a broken carrier board. This closes the numerical source-list difference; the earlier third-repeater/destroyed-unit possibility remains unverified. Owner estimates perhaps 4 × 18650 cells per deployed repeater (about 8 total across the 2 reported deployments), separate from 88 cells on hand; deployed counts and condition are unconfirmed.

## 2026-10-13 — Existing pilot broker endpoint

Owner reports an old pilot MQTT server at `mqtt.spp.lol` and authorized SSH inspection. Mosquitto is active; external TCP 8883 is reachable, but validating TLS fails because its certificate expired on 2026-03-24. External 1883 refused connections. This is an existing endpoint candidate for outbound home-worker access, not a deployed MeshLink integration. Host location/provider, billing, backup and maintenance arrangements remain unknown. See [inspection findings](../docs/research/dispatch-portal-transport.md#2026-10-13--existing-pilot-broker-inspected). No server/network change, installation or new expense.

## Broker hosting record — Mike Rollins

Latest verification, 2026-10-14: owner-run authenticated synthetic publish/subscribe and ACL tests through the certificate-validated public TLS endpoint pass. Both V3 accounts publish and the worker receives; worker writes, gateway reads and JSON/unrelated-topic writes are denied. Test used a temporary loopback SSH relay through the external test host because broker-to-public routing timed out; relay is closed and SSH confirms no 18884 listener remains. Mosquitto remains active. Earlier pending-account statements below are historical. Actual radio/reconnect, portal ingestion, certificate renewal and unrelated-LAN denial remain untested.

Owner-confirmed 2026-10-13; service inspection performed earlier the same day.

| Item | Recorded state |
| --- | --- |
| Host / administrator | Mike Rollins hosts the existing old-pilot MQTT server |
| Current hostname | `mqtt.spp.lol`; the project owner owns the domain |
| New public hostname | `mqtt.snorr.org`; DNS and TLS 8883 verified 2026-10-14; public MQTT CONNECT reaches broker and anonymous/invalid logins are rejected |
| Broker | Mosquitto 2.0.18, active and enabled on inspected Ubuntu host |
| Current broker listener | Reverified 2026-10-14: active on loopback and `192.168.12.51:1883`; owner-supplied UFW output allows only Nginx `192.168.12.254` to LAN 1883 before blanket IPv4/IPv6 1883 deny. No VM 8883 listener |
| Public TLS / certificates | Mike manages TLS/certificates on Nginx. External `mqtt.snorr.org:8883` verifies with TLS 1.3 and a hostname-matching Let's Encrypt certificate expiring 2027-01-11; MQTT forwarding verified by broker auth-rejection responses. Old broker-specific renewal configuration archived |
| Pilot accounts/access | Fresh separate V3 uplink accounts plus read-only worker; protobuf root `snorr/pilot`. Local authentication/ACL tests passed; portal/live gateway adapters and designated-gateway downlink pending |
| Automatic updates | Enabled by owner 2026-10-13: Ubuntu security and same-release stable updates daily at 03:00 America/Los_Angeles, with up to 10 minutes jitter; no major release upgrade |
| Scheduled reboots | Enabled: 04:00 America/Los_Angeles only when reboot-required flag exists; logged-in users do not block it. Skip if apt daily maintenance is active; missed reboot windows are not caught up at startup |
| Timezone | Host remains UTC; timers explicitly use America/Los_Angeles and adjust for daylight saving |
| Configuration recovery | Root-only archive at `/root/meshlink-maintenance/auto-20261013T194349Z/config-before.tgz`; contains secrets, remains on server. Full system/broker-data backup and restore remain unverified |
| Remaining administration details | No active maintainer reported; failure monitoring/response, full backup/restore, certificate deployment/reload, topic ACLs, credential provisioning and hosting costs remain to settle |

No new server purchase, service donation/value, physical hardware count, DNS change or MeshLink deployment is established. Hosting support is owner-reported; no outreach to Mike performed. See [inspection and migration notes](../docs/research/dispatch-portal-transport.md).

2026-10-13 maintenance update — Owner completed package updates and rebooted; remote verification confirms kernel 6.8.0-146 with SSH/Mosquitto active. Owner reports no active maintainer and requests automation; scheduled-update/reboot installer prepared but not enabled. Certificate repair and broker access review remain pending. See [maintenance record](../docs/research/mqtt-server-maintenance.md).

2026-10-13 automation enabled — Owner supplied successful installer output confirming `meshlink-maintenance-reboot.timer` enabled and all three apt/maintenance timers scheduled. First shown upgrade is 2026-10-14 10:08:37 UTC (03:08:37 Pacific) and reboot check is 11:00 UTC (04:00 Pacific). This supersedes the earlier prepared-only state. Configuration activation is confirmed by owner output; future automated upgrade/reboot and MQTT reconnection are not yet observed.

2026-10-13 fresh-pilot direction — Owner authorized archiving old MQTT configuration/accounts/data/logs and reprovisioning this existing host for the new pilot. Prepared/uploaded a private-archive reset installer, tested initial three-account uplink/worker ACLs against an isolated broker; live reset awaits local sudo execution. No archive completion or live new credentials claimed yet. [Reset details](../docs/research/mqtt-server-maintenance.md#2026-10-13--fresh-pilot-reset-authorized-and-prepared).

2026-10-13 proxy candidate — Owner asked whether Nginx can front the VM/MQTT TCP. Documented a separate-edge TLS stream passthrough plus HTTP-01 routing proposal and same-VM port/Certbot constraints. Proxy location/private upstream address and topology selection remain pending; no route or service changed. [Configuration notes](../docs/research/mqtt-nginx-proxy.md).

2026-10-13 Nginx TLS direction — Owner reports Mike wants Nginx to handle certificates and confirms Mike has certificate management handled. Prepared [consolidated routing handoff](../docs/operations/mqtt-nginx-handoff.md): public Nginx TLS 8883 to private Mosquitto 1883, private backend restricted to proxy, existing SSH preserved. This supersedes TLS-passthrough proposal for the requested handoff. IPs/topology and deployment remain unverified; existing reset installer must be adapted before running for this layout. No certificate work or external outreach performed.

2026-10-13 owner hold — Owner instructed holding the MQTT issue until Mike completes `mqtt.snorr.org` DNS and Nginx placement. Work paused; intended route is public TLS 8883 terminated by Nginx to private broker 1883, certificates handled by Mike. No new endpoint check, proxy completion, fresh reset or integration claimed. Resume with owner after infrastructure is ready; existing old endpoint/maintenance observations remain historical evidence.

2026-10-13 broker-only work resumed — Owner authorized fresh broker configuration during the external-infrastructure hold. Updated installer for private 1883 and independent account/ACL setup, no broker-side certificates. Uploaded/tested but local sudo execution pending. Default is loopback-only until Nginx source IP is supplied and LAN firewall restrictions verified; no live readiness claimed.

2026-10-13 fresh reset completed — Owner supplied successful reset output and local permission-test PASS. Archived old broker material at `/root/meshlink-archive/mqtt-legacy-20261013T204408Z`; new credentials at root-private `/root/meshlink-private/mqtt-credentials.json` (contents not read/published). SSH reinspection independently confirms active Mosquitto running as mosquitto, listener `127.0.0.1:1883` only, config/data/log directories mode 0750 and maintenance reboot timer enabled. No public or proxy backend connectivity claimed. Broker configuration is complete for local tracking ingestion; restricted Nginx access and real-client integration remain pending.

2026-10-14 endpoint testing resumed — Owner reports DNS/Nginx live and requests testing through `mqtt.snorr.org`, with root SSH on port 64582. DNS resolves; public TCP 8883 and certificate/hostname verification pass. Two anonymous MQTT 3.1.1 CONNECT probes over verified TLS each close after approximately 10 seconds without CONNACK; initial probe timed out at 8 seconds. Public 1883 times out at 8 seconds from this test origin, which does not prove firewall policy. Root SSH rejects both the available key and configured 1Password agent; no remote configuration/logs/credentials inspected or changed. MQTT accessibility is not confirmed. Inspect Nginx stream upstream/error logs and the current broker listener/firewall next; previous loopback-only listener would be unreachable from a separate proxy host. This is a hypothesis, not a current server finding. No authenticated publish/subscribe or ACL test performed.

2026-10-14 corrected SSH account — Owner corrects login to `setheth`; key-based SSH succeeds on port 64582. Mosquitto is active and still listens only on `127.0.0.1:1883`; Nginx is inactive on the broker host and there is no local 8883 listener. An anonymous loopback MQTT CONNECT immediately returns `20 02 00 05` (not authorized), demonstrating local MQTT service response. Loopback binding prevents a separate Nginx host reaching the broker. Sudo requires an interactive password; current protected configuration/firewall and edge upstream are not inspected. Requested Nginx private source IP/upstream and owner-run UFW status before preparing a source-restricted LAN listener change. No remote changes or credential reads; external authenticated MQTT access remains unverified.

2026-10-14 restricted backend prepared — Owner supplies UFW rules allowing 22/8883/80 for IPv4/IPv6 and identifies Nginx as `192.168.12.254`. Inspected broker interface is `192.168.12.51`. Prepared [backend installer](../scripts/server/enable-mqtt-nginx-backend.py) and uploaded matching-checksum source to `/home/setheth/enable-mqtt-nginx-backend.py`; syntax checks pass locally/remotely. Requires active UFW/default-deny and the exact existing pilot template, privately backs up configuration/firewall, prepends proxy-only LAN allow plus all-other-1883 deny, retains loopback/account/ACL settings and adds private LAN listener. Restart/local anonymous-rejection failures restore the original broker configuration, retaining restrictive firewall rules. **Not executed with sudo**; no listener/firewall change claimed. Owner must run it interactively and ensure edge upstream is plain TCP `192.168.12.51:1883`, with public TLS at Nginx. Real execution, proxy reachability, authenticated ACLs and unrelated-LAN denial remain unverified; existing 80/8883 allowances preserved pending successful cutover.

2026-10-14 public MQTT forwarding verified — Owner runs backend installer successfully, reports local anonymous-rejection PASS and active UFW proxy allow followed by blanket 1883 deny; private backup at `/root/meshlink-maintenance/nginx-backend-20261014T160013Z`. SSH independently verifies active Mosquitto listening on loopback and `192.168.12.51:1883`, with no broker 8883 listener. Public verified TLS CONNECT probes return `20 02 00 05` for anonymous and invalid-account logins in 0.11/0.12 seconds, confirming the public proxy path now reaches MQTT authentication. Public 1883 times out at 5 seconds from this origin. Valid-account publish/subscribe, external ACLs, actual firmware/reconnect, certificate renewal and denial from unrelated LAN hosts remain untested. No credentials read or transmitted and no operational packets published.

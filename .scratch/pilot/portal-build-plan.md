# Portal design and build sequence

Prepared 2026-10-13. Owner has no nodes available and explicitly brings portal design/building forward. This plan uses synthetic data; hardware integration and operational deployment follow separately.

## Existing requirements

Use [Define the dispatch portal MVP](issues/06-dispatch-portal.md), [Choose assignment-driven radio names and identity](issues/12-assignment-radio-names.md), and [Define infrastructure warning and intrusion handling](issues/10-infrastructure-warning-rules.md) as the requirements baseline. Do not reopen the requirements interview by default.

## First reviewable build

A local responsive prototype with Map, Users, Messages and Infrastructure pages. Clearly label simulated data and simulated actions. Start with six fictional member trackers and four fictional infrastructure devices. These are scenario fixtures, not confirmed available hardware or actual deployments. No real names, location tracks, credentials or radio transmissions.

- **Map:** dominant map area and searchable tracker list; device/member detail on selection. Show measurement age separately from last contact, 15-minute stale state, unknown timestamps and never-seen devices. Support optional infrastructure layer and opt-in four-hour position history. Inspect recorded points; dashed estimated connections break across gaps over 15 minutes. Provide readable status labels independent of color/animation and reduced-motion support. Mobile uses a collapsible list/detail panel.
- **Users:** member/device list, active assignments and dated assignment history; simulate claiming/releasing and admin transfers with one active tracker per member and one member per tracker. Static device short names and separate pending/confirmed/failed radio long-name jobs. UI role previews are illustrative; they are not authentication or authorization.
- **Messages:** shared chronological channel, composer, unread badge and in-portal notification. Simulate feed outage, preserve drafts and require deliberate sending after reconnect. Label send evidence precisely; no simulated publish is presented as radio receipt. Live length limits and delivery/expiry policy remain integration prerequisites.
- **Infrastructure:** role-based cards, detail/history/event view, capability-specific unknown/unsupported/stale/current readings. Battery, solar and antenna setup distinguish declared metadata from measured values. Silent warnings, acknowledgment separate from recovery, latched intrusion with admin resolution note. Illustrative metrics and thresholds must be labelled as scenario values, not chosen hardware settings.

Map behavior should match the agreed age bands. A basemap failure must retain the device list and clear position ages. Map-source/offline QA is still outstanding; a hosted portal is not the agreed internet-outage field fallback.

## Sequence

1. Owner accepted React + TypeScript + Vite, PocketBase and Python worker on 2026-10-13. Keep TypeScript simple and explain unfamiliar constructs. MapLibre remains planned for map evaluation; no new hosting provider needed. Start with the [local development and CI baseline](../../portal/README.md) while the VM is unavailable.
2. Build and review the local four-page synthetic prototype. Prioritize the map and device detail before secondary controls. Check desktop and narrow layouts, keyboard navigation and reduced motion.
3. Define the normalized ingestion contract and PocketBase collections: accounts, devices, dated assignments, positions, packet receipts, messages/send attempts, infrastructure observations, warnings/incidents, configuration and audit events. Preserve measurement time, receipt time, source packet/gateway identity and timestamp quality separately. Retain receipt evidence while deduplicating display records. Do not infer a fresh GPS fix from receipt time.
4. Implement authenticated backend operations and a Python simulation/replay path before connecting a broker. Enforce account roles and assignment consistency server-side, not merely through hidden buttons. Demonstrate simulated ingestion through storage to map updates.
5. Set up the owned Proxmox VM, persistent storage, service restart and tested backup/restore. Portal HTTPS uses the intended Cloudflare Tunnel; VM/domain access belongs outside Git. MQTT connectivity research remains deferred, using the owner's explicitly unverified planning assumption.
6. Integrate selected firmware packet samples and gateways when available. Verify packet formats/units, device identity, real message limits/delivery evidence, sensor capabilities and actual broker connectivity before claiming live readiness.

## Meaningful checks

- Delayed/duplicate packets preserve original age and cannot replace a newer measured position.
- Crossing 15 minutes updates the stale display without needing another packet; missing measurement time stays unknown.
- Feed outages preserve observations and existing warnings; reconnection does not imply recovery or resend drafts.
- Reassignment preserves historical attribution; concurrent assignment attempts cannot create conflicting active assignments.
- Unsupported or absent intrusion data never shows an all-clear; acknowledgment does not resolve an incident.
- Backend access rules reject unauthorized mutations before real member data is loaded.

## What is needed from the owner

Now: stack accepted; next review the prototype. Visual defaults can be chosen and revised without blocking progress. VM access is not needed for local frontend development.

Later: VM resources/access, portal hostname and Cloudflare setup, initial admin provisioning, backup destination, sanitized packet samples from pinned builds and verified telemetry capabilities. Keep actual credentials and operational data in ignored private locations. No node, hardware purchase or VM access is needed to start the prototype.

## Prototype checkpoint — 2026-10-13

The owner brought the remaining pages and map forward. The [local four-page prototype](../../portal/README.md) is built and browser-reviewed with synthetic data, including assignments, history, messaging outages and infrastructure incidents. Both development and production map-worker paths were checked. Records and demo actions remain in browser memory; automatic infrastructure warning evaluation, authentication, persistence and ingestion are next-stage work. No field/backend/hosting decision or ticket status changed.

## Backend checkpoint — 2026-10-13

After the owner accepted the prototype and requested the backend, implemented the [normalized storage/API contract](../../docs/research/portal-backend-contract.md), PocketBase migrations/authenticated transactions, Python simulation/replay and connected portal mode. Server authorization, assignment concurrency, duplicate/delayed ingestion, warnings/incidents and restart persistence are integration-tested. [Native startup and CI instructions](../../backend/README.md) cover private data/credentials. No broker route, live firmware decoder, radio publish/name execution, VM deployment or backup/restore is verified; these remain next-stage integration work. No ticket status changed.

## LXC deployment checkpoint — 2026-10-13

Owner resumes hosting and selects Ubuntu LXC in place of the earlier VM. The [deployment record](../../docs/operations/portal-lxc.md) documents production static serving, supervised PocketBase/simulation worker, Cloudflare HTTPS, local authentication, service restart and isolated consistent-backup recovery. Public DNS/credential-free HTTPS checks pass; owner browser sign-in waits for the LAN resolver's older negative IPv4 answer to clear. Off-host Proxmox backups, actual reboot recovery and live packets remain unverified. MQTT/survey holds and wishlist deferrals remain; no ticket status changed.

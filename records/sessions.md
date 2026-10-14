# Session log

## 2026-10-13 — Portal LXC deployed through Cloudflare

- Owner confirms LXC creation, authorizes root SSH setup and chooses `meshlink.spp.lol`. Inspected Ubuntu 24.04.5 amd64 with 4 CPUs, 8 GiB RAM, 512 MiB swap and 64 GiB SSD-backed root filesystem; recorded virtual resources without altering radio counts or inventing costs. Portal hosting resumes; MQTT/survey holds remain.
- Added reproducible deployment source for static Nginx/PocketBase/Python simulation services, private persistent state, restricted public API routes, per-client proxy IP/throttling and Ubuntu security updates. Owner installed/configured the existing remotely managed Cloudflare connector; preserved it and verified four connections plus the loopback-8080 route. No second tunnel, router forwarding, MQTT adapter or Cloudflare protection change.
- Isolated the hosted worker under a separate OS account with only its own credential JSON; verified ingestion succeeds while admin credentials/database reads are denied. Native development retains its original credential path. Backend checks rerun after this worker-source change.
- Daily 02:30 Pacific root-private backups retain 14 local archives, quiescing the worker/API for consistent state and including matching source/build. Verified checksum, SQLite integrity, restored credentials/assignments/messages/incidents/events and retained history via a separate loopback API; live state was not replaced. Off-host/Proxmox backups remain pending owner-selected storage/access.
- Verification: existing 27 backend and 8 frontend tests, TypeScript/production build, Nginx/shell/Python syntax, loopback sign-in/role boundaries, independent client throttling, restart persistence, isolated restore and credential-free public HTTPS/certificate/API boundaries pass. Existing MapLibre bundle warning remains. Public DNS is correct; LAN DNS retains an older negative IPv4 result, blocking desktop browser review during setup. Cloudflare blocks Python's default user-agent; curl probes pass without altering protection.
- Automatic approval review rejected transmitting generated admin credentials through Cloudflare for a public sign-in test. Replaced that test with credential-free HTTPS probes and retained loopback authenticated checks; no credentials/tokens published. Owner public browser sign-in and actual reboot recovery remain unverified. Preserved unrelated battery-box model. Completed source/records checkpoint is committed/pushed to main; final response reports result.

Next useful step: owner opens the portal and signs in using privately viewed generated credentials after LAN DNS catches up; configure off-host Proxmox backups, then resume live MQTT integration only when the owner brings it forward.

## 2026-10-13 — Ubuntu LXC portal sizing

- Owner resumes portal hosting setup and selects Ubuntu LXC on Proxmox. Reviewed the current PocketBase/Python/static React stack and primary Proxmox/Ubuntu documentation; recommended 2 cores, 2 GiB RAM, 512 MiB swap allowance and 32 GiB SSD-backed storage in an unprivileged Ubuntu 24.04 LTS container, with direct services, a stable LAN address and start at boot. Recorded the proposed hosting configuration in sites; these are estimates, not confirmed allocations or measured capacity.
- No container created, service deployed, broker integration resumed or hardware count changed. MQTT and other held work remain held. Documentation whitespace checked; unrelated storage-box file preserved. No commit requested or made.

Next useful step: owner creates the container and supplies its Ubuntu version and LAN address privately as appropriate; then configure access, pinned runtimes, persistent services and a tested backup/restore before HTTPS rollout.

## 2026-10-13 — Project held and desktop handoff checkpoint

- Owner requests holding the survey issue, wrapping all current project progress and pushing it to GitHub for another desktop. Released the survey claim, left it open/deferred, recorded the project-wide hold in the map/project brief and added [desktop handoff](../docs/operations/desktop-handoff.md). Resume only at owner direction; no planning decision falsely marked complete.
- Checkpoint includes accumulated portal launcher/test/documentation work, broker maintenance/reset scripts and sanitized hosting/handoff research, hardware/field planning records and accepted RAK/Dell survey requirements. Firmware submodule remains clean at the published release pin; no survey firmware/GUI built or hardware-tested.
- Verification: all 27 backend tests pass with localhost sockets enabled (initial sandbox run could not create sockets). Portal tests, TypeScript checking and production build pass; existing large-map-bundle warning remains. Both server shell scripts pass `bash -n`; reset script passes Python compilation. Publication candidate secret-pattern scan finds no matches; Git excludes private credentials/databases/raw tracks, binaries, dependencies and generated output. Documentation diff check passes. Privileged server scripts were not rerun; external broker path and firmware/hardware behavior remain unverified.
- Owner-authorized commit/push checkpoint targets `main` on `origin`; final response reports commit and push result. GitHub contains reproducible source/planning, not the current ignored local database or credentials. New-desktop setup and private-data transfer limits are documented in the handoff.

Next useful step: clone/update recursively on the other desktop and read the handoff. Keep work held until owner resumes the selected task.

## 2026-10-13 — Survey GUI behavior accepted and live map added

- Owner accepts proposed scheduling, run controls, disconnect handling and automatic logging with optional labels/configuration segments. Added live GPS/signal map to active tester scope to help revisit dead spots during a run.
- Recorded success/timeout attempt markers, per-repeater inspection and an independent timestamped GPS stream as the map design direction. Distinguish failed round trips from directional loss and stale/no-fix locations from precise measurements. Offline basemap preparation remains to verify; map availability must not block logs/readouts.
- Survey draft/ticket updated; broad operations ticket remains claimed pending field/power requirements. No GUI/firmware implementation or hardware test. Documentation diff checked; unrelated edits preserved, no commit requested or made.

Next useful step: implement the touchscreen survey prototype and RAK responder, verifying selected-build GPS availability, PKI and direct-only exchanges; verify offline map preparation before field use.

## 2026-10-13 — Touchscreen multi-repeater survey GUI requirements

- Owner requires a simple touchscreen Dell GUI with large buttons, touch input pads, one-or-more repeater selection and interval/other parameters. Recorded accepted requirements in the survey draft/ticket.
- Proposed sequential round-robin scheduling with one outstanding ping and interval between individual attempts, configurable timeout/continuous or finite runs, automatic private logging with configuration labels, and pause/explicit resume after tester disconnection. These behavior choices await owner input; no UI built, firmware changed or hardware tested.
- Broader operations ticket remains claimed. Documentation diff checked; unrelated edits preserved, no commit requested or made.

Next useful step: settle scheduling, disconnect behavior and run labels, then implement the simple touchscreen tester alongside the pinned-release responder.

## 2026-10-13 — Always-available survey responder accepted

- Owner selects always-available response to authorized survey pings because RAK nodes will be placed in hard-to-reach locations. Recorded rationale and behavior in the repeater ticket and survey draft: no physical visit/per-survey enable step, Dell drives attempts, and RAK responds only to valid requests authorized by the separate survey public-key allowlist.
- First-prototype direction now includes RAK4631, Dell GUI and transferable V4 native-PKI keys. Broader field/power decisions remain open; operations ticket stays claimed. No implementation, provisioning, build, flash or RF test. Documentation diff check passed; unrelated edits preserved. No commit requested or made.

Next useful step: specify the minimal GUI/logging controls and implement the pinned-release responder/tester prototype, followed by direct-only and authorized/unauthorized bench checks when hardware is available.

## 2026-10-13 — Portable survey key accepted

- Owner accepts transferring the tester private key to the V4. Recorded native PKI with a separate survey public-key allowlist as the chosen authentication approach in the existing repeater ticket and survey draft. Replacement tester hardware requires keypair restoration and node/key discovery; no admin rights implied.
- RAK4631 target and Dell-driven GUI remain confirmed. Survey enablement and GUI defaults remain open; broader operations ticket not resolved. No secrets generated/read, provisioning, firmware changes, build or flash performed. Documentation diff check passed; unrelated edits preserved, no commit requested or made.

Next useful step: settle whether the authorized responder is always available or explicitly enabled, then prepare the minimal responder and Dell GUI bench prototype.

## 2026-10-13 — RAK target and GUI tester clarified

- Owner confirms RAK4631 cores and Dell-driven V4 testing with a GUI/readout; updated inventory without changing counts or claiming verified frequency variants/condition.
- Checked pinned firmware routing/admin key handling and primary cryptographic documentation, with a delegated read-only source check. Native survey public-key authorization is feasible; keys live on tester radios, can migrate to replacement hardware, and still need node/key discovery. Proposed a survey-only allowlist separate from admin privileges. Dell-held payload signatures are an alternative requiring additional implementation/replay design.
- Recorded accepted hardware/test-control direction and proposed authentication/GUI scope in the existing survey ticket/draft. No full operations decision resolved, key generated, firmware changed, build, flash or hardware test performed. Existing edits preserved; no commit requested or made.

Next useful step: owner chooses radio-held native PKI versus Dell-held signing key; then specify survey enablement and GUI controls before implementing the first bench prototype.

## 2026-10-13 — RAK survey firmware pre-build readiness

- Used owner-invoked Wayfinder and its grilling/domain-modeling guidance to review the existing repeater survey ticket, inventory, proposed exchange/logging contract and firmware workspace. Confirmed clean firmware checkout at the recorded release commit; preserved unrelated working-tree edits.
- Identified immediate prerequisites: exact RAK core/radio variant, owner choice of tethered versus autonomous tester, and survey enable/access policy. Recommended Dell-controlled V4 testing first and explicitly enabled responder access for a configured tester; these remain proposals. Site selection, solar endurance and field acceptance thresholds can follow the first bench prototype.
- Added the readiness review to [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md). No decision resolved, firmware implementation, build, flash or RF test performed. No commit requested or made.

Next useful step: identify the selected RAK core and settle tester control/access, then verify the direct-only module/API paths against the pinned release before implementation.

## 2026-10-13 — Firmware fork added and RAK release branch published

- Owner requested adding `lfg-seth/firmware` as a submodule and creating a current-public-release RAK branch. Added `firmware/`, configured its tracked branch as `snorr/rak-survey`, and published that branch to the fork.
- Verified GitHub latest public release is `v2.7.26.54e0d8d` (title Beta, GitHub prerelease=false), commit `54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb`. New branch matches that release exactly; existing fork develop remains `76d5156e72d9d9aaa9722b7bbc1336335b685984`. No old customizations merged or history rewritten.
- Initialized the release-pinned protobufs and meshtestic submodules; verified clean firmware tree and remote branch SHAs. Added [workspace/setup notes](../docs/research/firmware-workspace.md). Exact owned RAK core remains unknown; no firmware build, flash, RF transmission or hardware test performed.
- Commit scope is submodule configuration/pointer, setup notes and this session entry. Existing portal/broker/repeater-planning working-tree changes are preserved outside this commit. No tracker decision resolved.

Next useful step: identify the RAK core, then check the dedicated direct-only ping/pong module design against this pinned release before implementing and building it.

## 2026-10-13 — Dedicated direct-link survey module reviewed

- Owner asks about firmware modifications/plugins, a dedicated packet type, addressed zero-hop exchanges and adjustable usage restrictions. Reviewed upstream primary module/port/routing/airtime/radio/API sources and appended [implementation findings](../docs/research/repeater-operations-survey.md#dedicated-firmware-module--follow-up-source-review) to the existing survey draft/ticket discussion.
- Recommended compiled-in RAK responder module on a private application port, explicit PING/PONG payload, zero-hop/no-ACK requests and replies, and client-controlled attempts. Noted generic reply/ACK hop rewriting, MQTT exclusion, duplicate handling and queue/actual-TX distinctions. Stock V4 with Dell API control is a candidate minimal prototype; autonomous V4 testing and precise radio-time logging may need client firmware.
- Distinguished configurable survey scheduling/congestion policies from regional radio constraints and hardware queue/half-duplex operation. No unrestricted RF operation, global restriction removal, final port number or implementation approved/inferred. Reviewed moving upstream sources only; revision lookup failed, so release/commit pinning remains before implementation.
- No firmware cloned, built/flashed, hardware tested, portal/MQTT work resumed or new decision resolved. Existing edits preserved. Documentation checks only; no commit requested or made.

Next useful step: identify target RAK core and V4 firmware/API versions, pin a firmware revision, and verify a minimal private-port responder plus Dell-controlled direct-only exchange on three nodes.

## 2026-10-13 — Repeater operations and placement survey opened

- Owner steps back from portal work and brings solar RAK repeater operations forward: 2–4 18650 cells, Muzi whip or fiberglass antenna, firmware ping/pong responder and GPS-equipped V4 testing node tethered to Dell log storage. Captured intended builds without changing stock counts or assuming installation permission.
- No installed `$wayfind` skill found after local search; used repository-defined Wayfinder tracker conventions. Created/claimed [Define repeater operations and direct-link placement testing](../.scratch/pilot/issues/14-repeater-operations-survey.md), retaining claim pending owner input. No non-research decision resolved; MQTT remains held.
- Reviewed primary RAK electrical documentation, Meshtastic range-test/role documentation and packet schema. Recorded [draft operations/survey plan](../docs/research/repeater-operations-survey.md): per-packet metrics in both directions, verified direct-only paths, timeout/GPS-age logging, controlled antenna comparisons and separate later GPS relay validation. Recorded power autonomy, cell/charger/cold-charge protection, recovery, mounting and service-access questions. No firmware built, hardware tested or coverage measured.
- Asked owner for prior-test candidate landmarks/routes and coverage gaps. Outstanding: exact RAK/core/cell/panel builds, no-sun endurance target, survey cadence/sample size and route acceptance thresholds. Existing unrelated working-tree edits preserved. Documentation checks only; no commit requested or made.

Next useful step: capture candidate sites and required routes, agree no-sun endurance, then identify one representative RAK power build and bench-check the direct-link responder/logging contract before a field survey.

## 2026-10-13 — Worker readiness review

- Owner asked what comes next and whether DNS completion makes the worker ready for Mosquitto. Inspected worker code, backend contract/tests and current broker handoff. The Python worker supports authenticated synthetic ingestion and normalized JSONL replay only; it has no MQTT connection/subscription, TLS/broker credential configuration or selected-firmware decoder. DNS completion alone will not enable live tracking.
- Fresh Mosquitto local authentication/ACL readiness is recorded, but its last verified listener is loopback-only. Separate-host Nginx requires restricted private access, followed by external TLS/auth/topic verification. No remote probes, broker changes, implementation or tests performed in this review; existing edits preserved.

Next useful step: implement a receive-only MQTT-to-normalized-ingestion adapter with explicit simulation/live modes, reconnect/outage handling and decoder tests using sanitized selected-build packets; verify the external broker path with Mike when ready. No commit requested or made.

## 2026-10-13 — Fresh pilot Mosquitto installed

- Owner ran adapted reset and supplied successful live authentication/ACL test output. Old broker configuration/accounts/data/logs and broker-specific renewal state archived privately at `/root/meshlink-archive/mqtt-legacy-20261013T204408Z`; fresh account credentials stored root-private on server, not read/published.
- SSH follow-up confirms active Mosquitto under its own account, loopback `127.0.0.1:1883` only, no VM 8883 listener, config/data/log directories mode 0750 and enabled scheduled-maintenance reboot timer. Updated current server/project/handoff records from prepared to installed. Unrelated backend/portal launcher edits preserved.
- Local broker accounts/ACLs are ready for tracking ingestion; no command publishing/downlink yet. Restricted separate-host Nginx access needs its private source IP. External TLS/DNS/proxy path, actual V3/worker adapters and SSH password hardening remain pending. No credentials, raw messages/tracks or archive contents accessed during verification.

Next useful step: Mike supplies Nginx private source IP, then enable only that proxy's private 1883 access and test public `mqtt.snorr.org:8883` when Mike is ready. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Broker-only setup resumed and adapted

- Owner authorized making the fresh Mosquitto updates while Mike's external infrastructure remains pending. Inspected live service/private interface; no fresh marker found and sudo still requires local password. Preserved unrelated backend launcher/README/test edits visible in Git.
- Adapted/uploaded reset installer to private 1883, no broker certificates/hooks, intended client hostname `mqtt.snorr.org`, old MQTT archive plus broker-specific old renewal configuration archive, fresh per-gateway and worker credentials/ACLs. Default loopback-only because proxy source IP is unknown; LAN mode requires explicit addresses and active source-restricted UFW preflight.
- Private-backend isolated auth/ACL tests passed. Temporary-filesystem full-flow archive/credential and injected-startup-failure rollback tests use actual isolated Mosquitto with mocked privilege/service operations; real privileged execution remains pending. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--private-backend-reset-adapted).

Next useful step: owner runs updated script with sudo, then verify live fresh broker/archive without exposing credentials. Enable restricted LAN listener once Mike supplies Nginx source IP; external infrastructure remains deferred. No live broker reset, firewall change, commit or push performed.

## 2026-10-13 — Combined local launcher

- Owner confirms no Proxmox VM or nodes are available and brought local launch cleanup forward. Added `python3 backend/launch.py` to supervise PocketBase, the synthetic Python worker and Vite in one foreground terminal on Linux/macOS/WSL. Updated backend/portal startup instructions; individual commands remain available for debugging.
- Launcher checks installed dependencies/initialized storage and Node version, refuses duplicate launches and occupied ports, waits for API/portal readiness, binds services to localhost and keeps per-process logs in ignored private storage. Ctrl+C/termination or a child exit shuts down its process groups, stopping the worker before the API; bounded escalation handles unresponsive children. It does not install/reset data or print credentials. Synthetic observations continue to be saved while running.
- Verification: existing twenty backend/installer tests passed. Seven launcher tests passed, including occupied-port preservation, duplicate refusal, startup failure, real child cleanup and forced termination. A disposable real PocketBase/worker/Vite run on temporary ports verified API proxying, ingestion, duplicate refusal, Ctrl+C cleanup, restart with saved data and worker-failure cleanup. Existing port-8090 service was left untouched. Linux verified; macOS/WSL runtimes remain untested. Documentation diff check passed; no commit requested or made, unrelated edits preserved.

Next useful step: stop the existing individual development terminals, run the combined launcher on the Dell and review the saved portal workflows. VM deployment and hardware integration await availability; MQTT remains on hold pending Mike and owner resumption.

## 2026-10-13 — Hypothetical SNORR companion-app forks

- Owner asked whether SNORR could fork the Meshtastic iOS/Android apps and what features would suit the project. Reviewed current primary [Apple source/README](https://github.com/meshtastic/Meshtastic-Apple), [Android source/README](https://github.com/meshtastic/Meshtastic-Android), [Android fork/rebrand guidance](https://github.com/meshtastic/Meshtastic-Android/blob/main/CONTRIBUTING.md#forks-and-rebrands) and [position configuration](https://meshtastic.org/docs/configuration/radio/position/). Both apps use GPLv3-family licenses; distribution requires applicable source/notices and distinct branding under the upstream conditions.
- Suggested hypothetical priorities: GPS measurement age and explicit stale/unknown states, prepared offline field maps, cached device/member assignments, simple member controls, clear local-radio versus dispatch-feed status, and later concise messaging with honest delivery/acknowledgment states. Keep phone-free GPS and device-only SOS in node firmware; an app cannot establish radio coverage or dispatch receipt without evidence.
- Recommended a small customization that preserves the Meshtastic protocol and upstream improvements, after stock-app pilot checks identify actual gaps. Apple/Android have separate UI stacks and ongoing maintenance needs. No app cloned, built or tested; feasibility is source/documentation review only. No active ticket, wishlist activation, firmware selection change, broker work, commit or push. Existing edits preserved.

Next useful step if the owner brings app work forward: compare stock apps on the pilot devices against freshness, offline map and reconnect requirements, then select one platform and a minimal scope. Passive GPS bench testing remains the first hardware priority.

## 2026-10-13 — Next-work review

- Reviewed project records, tracker and portal build checkpoints. Recommended tested backend backup/restore as the next independent software task, followed by VM service supervision and HTTPS deployment. Live MQTT integration remains on hold pending Mike and owner resumption.
- Passive GPS bench testing remains the first hardware priority when nodes are available. No implementation, ticket change, remote check or deployment performed; existing uncommitted work preserved. No commit requested or made.

Next useful step: implement private backend backup/restore and demonstrate recovery into a separate local instance, preserving accounts, assignments, observations and history.

## 2026-10-13 — MQTT issue held pending Mike

- Owner explicitly instructed holding the broker issue until Mike completes infrastructure work. Recorded `mqtt.snorr.org` as intended endpoint, with Mike updating DNS and placing the VM behind Nginx; certificate management belongs to Mike. Completion is unverified.
- Released the connectivity ticket claim and left it open/deferred; updated map, project brief, hosting record and handoff. No broker/proxy probes, implementation, hardening or reset performed after the hold. Earlier update/maintenance verification remains recorded.
- Fresh broker reset is prepared but not executed and needs adaptation for Nginx TLS termination/private port 1883. Firewall activation, SSH-password hardening, live ACL provisioning, actual firmware/client configuration and one-gateway dispatch downlink remain unverified. Documentation diff checked; no commit requested or made.

Resume only when owner brings this issue back after Mike's work is complete. First confirm `mqtt.snorr.org` TLS/proxy reachability, then adapt/archive/reset the broker and test gateway/worker access.

## 2026-10-13 — Nginx MQTT handoff prepared

- Owner reports Mike wants Nginx to own certificates and says certificate management is handled. Prepared [consolidated handoff](../docs/operations/mqtt-nginx-handoff.md) for TLS termination on public 8883, private broker TCP 1883 restricted to Nginx, DNS/client settings, existing SSH preservation and verification. No certificate-provisioning instructions or outreach.
- Recorded current direction over earlier passthrough proposal. Actual proxy/VM addresses, separate/same-host layout and deployed configuration remain unknown. Marked existing fresh-reset installer unsuitable unchanged because it provisions broker-side TLS/certificate handling; adaptation remains before running it for this topology.
- No live broker reset, proxy/firewall/DNS change, template runtime verification or completed security hardening claimed. Documentation diff checked; no commit requested or made.

Next useful step: Mike supplies private upstream/source addresses and validates Nginx configuration; adapt the archived fresh-broker setup for the chosen private 1883 listener, then test external TLS/auth/topic access and reconnects.

## 2026-10-13 — Nginx TCP proxy proposal documented

- Owner asked about fronting the VM with Nginx. Verified primary Nginx TCP stream/HTTP routing and Cloudflare proxy-port documentation. Prepared [configuration proposal](../docs/research/mqtt-nginx-proxy.md): separate Nginx edge forwards TLS 8883 and HTTP-01 challenges to the broker VM, keeping certificates/auth/ACLs at Mosquitto.
- Asked whether proxy is on a separate host or the broker VM. Same-VM option requires different backend listener and Certbot validation configuration; no topology/installation assumed. No Nginx, router, DNS or broker change made. Existing fresh reset remains prepared, not executed.

Next useful step: confirm proxy location/management interface and private upstream address, then adapt and validate configuration with Mike's existing routing. Examples are templates and not syntax-tested on an actual proxy. Documentation diff check passed; no commit requested or made.

## 2026-10-13 — Fresh MQTT reset prepared

- Owner authorized archiving all old MQTT state and setting up the host fresh for the new pilot. Prepared/uploaded a root installer that stops/flushed broker, moves old configuration/accounts/cert copies/persistence/logs to a root-private timestamped archive and creates an empty TLS-only broker with separate V3 uplink credentials and read-only worker credential. Initial root `snorr/pilot`; commands denied until designated gateway integration. Secrets/raw data remain on server.
- Installer creates private credentials, guards against accidental repeat reset, restores old trees on reset/startup/test failure, and installs a certificate copy/reload deploy hook scoped to the current hostname. Known expired cert still blocks external validating TLS; renewal pending port-80 routing.
- Python syntax checks and isolated installed-Mosquitto tests passed for valid/invalid/anonymous credentials, gateway publish/no-delivery, worker read/no-publish and command/unrelated-topic denial. Adjusted test to verify actual delivery because SUBACK may precede ACL filtering. Full root reset/rollback/hook not exercised; live old broker unchanged. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--fresh-pilot-reset-authorized-and-prepared).

Next useful step: owner runs uploaded reset via local sudo and shares status without credentials; verify archive/fresh service, then renew TLS and configure actual gateways/worker. Firewall/SSH hardening remains pending. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Privileged broker security audit received

- Owner output confirms inactive UFW and effective SSH password authentication enabled, correcting earlier inference from the readable main config. Root login is disabled and public-key login enabled. Eleven MQTT accounts exist; secrets/hashes not read.
- AppArmor loaded/enforcing selected profiles but no Mosquitto profile listed; no broker confinement claimed. Existing generic profiles do not establish installed apps.
- Prepared firewall rules preserving local SSH 22, MQTT TLS 8883 and HTTP-01 80; dormant rules need inspection. Asked whether Mike uses SSH keys before disabling passwords. No firewall/SSH/account changes performed, and update-policy dry-run remains pending.

Next useful step: inspect/activate UFW rules and verify a fresh SSH connection; confirm Mike's key access, then fix effective SSH password policy and design topic ACLs. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Security checks while port-80 routing is pending

- Rechecked active SSH/Mosquitto, enabled maintenance timer and effective apt policy. Confirmed security/stable updates plus timer-controlled reboots. Running broker uses the mosquitto account; private-key/password-file modes are restrictive. UFW enabled state and installed AppArmor tool do not establish effective rules/profiles. Broker data-directory mode is 0755; local-user visibility needs file-permission review without reading tracks.
- Credential-free diagnostic TLS negotiated 1.3 and anonymous MQTT CONNECT was rejected with code 5. Expired certificate verification bypass was confined to this probe; no credentials, topic operations or payloads accessed. This is not validating TLS or ACL verification.
- Prepared next local-sudo audit commands for firewall, effective SSH, account names, AppArmor and update-policy dry-run. No server changes. [Evidence](../docs/research/mqtt-server-maintenance.md#2026-10-13--checks-while-http-01-routing-is-pending).

Next useful step: owner supplies privileged audit output, then define/install tested per-client topic restrictions while awaiting certificate repair. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Enabled broker maintenance documented

- Owner supplied successful automation installer/timer output. Recorded enabled daily security/stable updates at 03:00 Pacific (up to ten minutes jitter) and required-only reboots at 04:00 Pacific with timezone/DST handling, busy-apt skip and no missed-window reboot catch-up in the server hosting and maintenance records. Logged-in users do not block scheduled reboots. No major release upgrades enabled.
- Recorded the server-local root-only configuration archive path without copying its sensitive contents. First shown next upgrade/reboot-check dates agree with the intended Pacific window. Updated project summary.
- Activation confirmed from owner output; no future automated run/reboot/reconnection or full backup restore observed. Certificate repair, MQTT topic permissions, firewall audit, unattended-upgrade dry-run and failure response remain outstanding. Documentation diff check passed; no commit requested or made.

Next useful step: complete the privileged update-policy dry-run and certificate renewal after Mike's port-80 routing change; then finish topic/firewall checks and observe the first maintenance run.

## 2026-10-13 — Broker updated/rebooted; scheduled maintenance prepared

- Owner supplied completed OS update output and rebooted the server. Reconnected and confirmed kernel 6.8.0-146, active SSH/Mosquitto and no remaining reboot-required flag. fwupd failed during update-time restart; after boot its unit reports inactive/success, but the prior failure cause is unverified.
- Owner requested automatic updates and scheduled reboots, reporting no active maintainer. Existing automation covers security updates. Prepared/uploaded a sudo installer adding same-release Ubuntu updates, a Pacific-time upgrade window and required-only reboot timer. Proposed 03:00 updates/04:00 reboot pending owner preference; timezone expression verified and shell syntax checks passed. [Details](../docs/research/mqtt-server-maintenance.md#2026-10-13--updatesreboot-completed-automation-prepared).
- Installer is not yet run as root or enabled. TLS certificate renewal, topic ACLs and privileged firewall/effective SSH audit remain outstanding. No claim of completed security hardening or verified future automatic reboot.

Next useful step: owner enables the maintenance schedule via local sudo and shares timer/dry-run output, then continue certificate and access-control repairs. No commit requested or made.

## 2026-10-13 — Broker update/security work started

- Owner authorized server updates and security work. Read-only checks found pending Ubuntu packages and an existing reboot-required flag. Readable SSH settings disable root/password/keyboard-interactive login; apt security automation is enabled. Effective SSH/firewall/topic-account checks remain privileged.
- Sudo still requires an interactive password. Prepared, syntax-checked and uploaded an OS update script to the owner's server home directory, with root-only configuration backup, no-removal package upgrade, health checks and no automatic reboot. [Maintenance record](../docs/research/mqtt-server-maintenance.md). Script has not been run as root; no packages updated or security settings changed.
- Requested privileged audit output without secrets; certificate repair, topic ACLs, firewall review, post-update validation and coordinated reboot remain. No non-research decision resolved or commit requested.

Next useful step: owner runs the uploaded script with sudo and supplies audit results; continue TLS/ACL changes from verified settings. Shell syntax check and upload passed; runtime untested until privileged execution.

## 2026-10-13 — Broker host and domain plans recorded

- Owner confirms Mike Rollins hosts the old-pilot broker, and the owner owns its current `mqtt.spp.lol` domain. Documented the hosted service in sites/inventory and the current project brief; physical host resources, costs, backup and maintenance details remain unknown.
- Mike plans to open/route port 80 shortly; completion and renewal success remain unverified. Recorded `mqtt.snorr.vegas` and `mqtt.snorr.org` as possible future hostnames, not selected or configured.
- Verified official Certbot/Let's Encrypt guidance: a new hostname needs certificate coverage and domain validation; a transition certificate can cover old plus chosen new hostname. Recorded DNS, HTTP-01 routing, certificate deployment/reload and client-address cutover prerequisites in the transport report. No DNS, certificate, server or radio changes, outreach, expense or non-research decision resolution.

Next useful step: once Mike's routing change is ready, verify renewal dry-run and repair broker certificate deployment/reload; choose a replacement hostname separately if desired. Documentation diff checked; no commit requested or made.

## 2026-10-13 — Old pilot MQTT server investigated

- Owner provided `mqtt.spp.lol` and authorized SSH inspection. Connected and performed read-only service/configuration/renewal-status checks plus external TCP/TLS probes; no credentials, password hashes, keys, member data or broker payloads read.
- Found enabled/active Mosquitto 2.0.18 with password-required TLS on 8883. External 8883 reachable; 1883 refused and has no local listener. Public certificate expired 2026-03-24; validating TLS rejected it. Latest Certbot run failed, standalone renewal configured, no renewal-hook files found; privileged logs unavailable and cause remains unknown. No topic ACL directive found in inspected configuration.
- Recorded [findings and reuse recommendation](../docs/research/dispatch-portal-transport.md#2026-10-13--existing-pilot-broker-inspected) and existing endpoint in site records. No server changes, service restart, broker publish/subscribe, hardware test, spending or hosting decision made.

Next useful step: inspect privileged certificate-renewal failure evidence and repair/verify renewal plus broker certificate installation/reload; then verify topic access and stock V3 integration. Noninteractive sudo was unavailable. Documentation diff checked; no commit requested or made.

## 2026-10-13 — MQTT broker discussion reopened

- Owner asked to revisit the broker issue. Claimed [Check Heltec MQTT over WebSockets for Tunnel hosting](../.scratch/pilot/issues/09-heltec-websocket-research.md) and lifted the connectivity-research deferral in current project/map notes; separate wishlist features remain parked.
- Rechecked official Cloudflare, Meshtastic source/configuration and Mosquitto documentation. Stock direct MQTT transport and published Tunnel TCP still need an adapter between them. Recorded home site VPN/bridge, separate reachable private broker and custom WSS candidates in the [transport report](../docs/research/dispatch-portal-transport.md#2026-10-13--broker-issue-revisited). Recommended Mosquitto for evaluation without recording owner acceptance.
- Hosting preference remains open: all-home requirement versus acceptable external private broker. Existing no-inbound-home-port-forwarding preference and one designated V3 downlink remain intact. No broker/VM deployed, firmware changed, external service purchased, real packets tested or non-research decision resolved.

Next useful step: settle hosting preference; for a home broker, inventory available site routers/computers before choosing an adapter. Then prepare a LAN broker test on identified/pinned gateway firmware and implement the real worker adapter. Documentation/source review only; no commit requested or made.

## 2026-10-13 — PocketBase installer running-file fix

- Owner reported `Errno 26: Text file busy` from installing over the running PocketBase executable. Replaced in-place truncating writes with same-directory staging and atomic replacement. Matching binaries stay untouched; a private verification receipt allows subsequent matching installs without another download. Older installs receive one archive/binary comparison without rewriting the executable.
- Locked replacements now preserve the existing binary, clean staged files and report how to stop/retry/restart the backend. Updated native setup instructions. No database/credential replacement or service restart is required for a matching reinstall.
- Verification: all twenty backend/installer tests passed, including a real running PocketBase reinstall, offline reuse, legacy installs without receipts, checksum rejection, tampered-binary replacement and locked-file preservation. Frontend is unchanged; Windows runtime/locking behavior remains untested (the error branch is exercised with a simulated lock).

Next useful step: repeat `python3 backend/manage.py install`, then continue backend sign-in/review. Keep existing local data and credentials; initialization remains a one-time command.

## 2026-10-13 — Local authenticated backend and connected portal built

- Owner approved backend development after reviewing the portal. Implemented PocketBase 0.40.5 migrations/hooks, the normalized [backend contract](../docs/research/portal-backend-contract.md), and a standard-library Python simulation/replay worker. Pinned official release checksums and Python 3.14.3; added native install/initialization/startup/account commands and GitHub-hosted backend CI. No VM, broker or hosted service provisioned.
- Added username/password admin/member accounts, a separate restricted worker account, locked direct collection writes and server-enforced permissions. Admin account creation/password reset/deactivation preserve earlier records. Transactional assignment/release/transfer and partial unique indexes protect one active member per tracker and one active tracker per member; dated attribution and separate latest-only simulated name jobs remain intact.
- Portal contact detail also remains visible for a device that has reported messages without a GPS fix; no location pin is invented.
- Persisted original GPS/sample timestamps and quality, first receipt time, separate contact time, every normalized receipt (including duplicates/rejections), position/history records, infrastructure observations, shared messages/send attempts and audited warnings/incidents. Older/unknown/future GPS data does not replace a newer known measurement. Simulated sends require a healthy feed and exactly one designated gateway; no radio receipt, publish or rename is claimed.
- Implemented supported-capability warning evaluation with device/per-report cadence, three-interval defaults/timeout overrides, shared battery defaults/device overrides, separate fresh recovery thresholds, acknowledgment, disabled-rule history, feed-loss suppression/reconnect grace and admin-resolved latched intrusion. Demo feed loss pauses synthetic observation production and retains prior readings/warnings.
- Connected all four portal pages to authenticated persisted snapshots/mutations, retaining standalone demo mode. Browser tokens remain in memory; reload requires login, while records persist. API failure retains the last snapshot and disables sending. Fixed pending sends so successful completion does not clear newly edited drafts, and converted PocketBase query slices to ordinary arrays before reversing histories to prevent repeated/misordered entries. History queries and point controls are bounded; storage retains all received pilot data.
- Verification: fourteen integration tests passed against the actual pinned binary in temporary databases, including authorization/bypass, accounts, concurrent claims, duplicate/delayed/invalid/future ingestion, ordered unique histories, outage/manual-send evidence, rules/incident lifecycle, stale name jobs and restart persistence. Fresh setup command passed in a disposable directory. Frontend tests (eight domain tests also run in single-process mode), strict types and production build passed. Connected browser checks cover login, saved assignments after reload, messages/drafts, rules/incidents, member permissions, mobile layout and API outage; the same connected flow passed against the production preview, including a deliberately delayed-send regression check and visual review. Private data/credentials/binaries remain ignored; Vite's existing map bundle-size warning remains.

Next useful step: owner tries backend sign-in on the Dell using the private generated credentials and reviews saved workflows. Then prepare backup/restore and deployment/supervision, or integrate sanitized packets from identified/pinned hardware builds when available. Live MQTT/firmware adapters, actual radio send/name execution, field/GPU performance, backup/restore and VM/HTTPS remain unverified. MQTT transport research and wishlist features stay deferred. No hardware/inventory, expense, site permission or field measurement changed.

## 2026-10-13 — Four-page synthetic portal and map built

- Owner requested continuing portal development with the remaining pages and map. Replaced the starter with responsive Map, Users, Messages and Infrastructure pages, using six fictional trackers, five fictional members and four illustrative infrastructure devices. No actual sites, member records, hardware changes or live packets are represented.
- Added MapLibre/USGS topo and aerial layers, selectable/searchable tracker list, measurement/receipt/contact times, aging and stale/unknown/never-seen states, optional infrastructure layer and opt-in recorded history. History shows measurement-time carriers, inspected points and dashed estimated connections broken across gaps over 15 minutes. Reduced motion and map/WebGL failure keep the tracking list usable. Rechecked official map/bundler guidance and explicitly bundled the MapLibre worker for Vite production builds.
- Added browser-memory assignment claim/release/admin transfer with dated history and stable short names, separate simulated long-name jobs and latest-job outcome controls. Shared messages include manual simulated sending, author prefixes, unread notifications and drafts preserved through page changes/outages without reconnect resend. Role previews are illustrative, not authentication.
- Added infrastructure role filtering, capability-specific readings, voltage history, declared hardware configuration, event/audit history, silent persistent badges and latched intrusion acknowledgment/admin resolution with a note. Battery rule configuration is a preview; automatic warning/recovery/missing-report/reconnect evaluation awaits ingestion. Demo sensor/voltage/configuration values do not establish hardware fitment or approved thresholds.
- Verification: npm checks, strict TypeScript and production build passed; all eight domain tests also passed with Node's single-process test mode. Browser checks passed against development and production at 1440px/390px, including topo/aerial tiles, layers/history, assignment/name jobs, outage draft/manual sending, notifications, incidents/rules and role previews. Additional checks passed for blocked tiles, unavailable WebGL, reduced motion, keyboard skip navigation, browser back and narrow layout overflow. Visually reviewed page captures. Map renderer size still produces Vite's default bundle-size warning (about 286 kB compressed plus a 508 kB uncompressed worker).

Next useful step: owner reviews the prototype on the Dell, then define the normalized persistence/ingestion contract and implement authenticated PocketBase operations with a Python simulation path. No backend, VM, live radio integration, offline-map readiness, field/GPU performance or automatic warning engine is verified. MQTT connectivity and wishlist features remain deferred.

## 2026-10-13 — Owner confirms Dell development works

- Owner confirms the frontend works and can be built on the Dell. This verifies the owner's development experience for the current starter; it does not establish full-stack, MapLibre or field-device performance.
- Reviewed the existing portal build plan. Next deliverable is the synthetic tracking screen: MapLibre/USGS map, six fictional trackers, searchable list and selectable device detail, with measurement age separate from last contact, stale/unknown/never-seen states and a simulated feed outage. Follow with opt-in history, then the remaining portal pages and backend integration.

Next useful step: implement and review the tracking screen on the Dell at desktop and narrow widths. Existing CI remains the automated check; no VM or live nodes are required. No new implementation or ticket decision in this status review.

## 2026-10-13 — Accepted portal stack and development/CI baseline

- Owner accepted React + TypeScript + Vite, PocketBase and Python worker, requesting simple TypeScript and explanations. Owner reports a desktop with WSL/Docker potentially available and no Proxmox VM yet; recorded development resources without assuming desktop access or readiness.
- Added the local frontend baseline, exact npm dependency lockfile, Node version, synthetic GPS freshness examples and developer instructions. Added GitHub-hosted CI for tests/type checking/build and seven-day main build artifacts; no deployment workflow or service credentials.
- Documented native Dell development now, optional desktop integration later and VM deployment after persistence/backup/rollback preparation. Checked official Vite, GitHub Actions, Microsoft WSL and PocketBase guidance. MQTT connectivity investigation stays deferred.
- Resolved [Establish the portal development and CI baseline](../.scratch/pilot/issues/13-portal-build-environment.md). Local lockfile install, four direct measurement-age tests, strict type checking, production build and whitespace checks passed. Dependencies/build output are ignored. No browser QA, desktop/Docker verification, backend or hosted portal; first remote CI execution awaits publication/verification.

Next useful step: build/review the four-page synthetic portal, starting with MapLibre map, tracker list and device detail. No VM needed for this step. Later pin backend/worker dependencies when their interfaces are implemented.

Publication/CI evidence: pushed baseline commit `cae58e5` to `origin/main`. The first [GitHub-hosted Portal CI job](https://github.com/lfg-seth/snorr-meshlink/actions/runs/38422409410) completed successfully, including lockfile installation, checks/build and artifact upload. No deployment occurred.

## 2026-10-13 — Portal work brought forward without nodes

- Owner has no nodes available for bench testing and requested moving forward with portal design and building. Reviewed the agreed portal, naming and infrastructure warning requirements; hardware testing is not a prerequisite for a synthetic prototype.
- Prepared the [portal build plan](../.scratch/pilot/portal-build-plan.md), including first-review screen behavior, build sequence, normalized data needs, meaningful verification and owner inputs needed now versus later.
- Asked whether to adopt the previously recommended React + TypeScript + Vite frontend with the planned PocketBase/Python backend. No stack acceptance inferred. MQTT connectivity investigation and wishlist features remain deferred.

Next useful step: confirm frontend direction and build the local responsive Map/Users/Messages/Infrastructure prototype with clearly labelled synthetic data. No app implementation, deployment, packet integration or hardware tests performed in this planning step.

## 2026-10-13 — Project status review

- Reviewed the project brief, session history, pilot map, tracker, inventory, wishlist and planned field criteria. Pilot approach and portal requirements are agreed; no bench/field results or deployed portal are recorded.
- Reconfirmed the planned six-V4 pilot includes only two on-hand V4s, with two purchases and two recoveries pending. Hardware identification, firmware/configuration pinning, passive GPS freshness, runtime and outage checks remain next.
- Recommended starting with the owned-hardware passive-tracking bench baseline; the next software step remains a synthetic-data four-page portal mockup. MQTT connectivity investigation and wishlist items stay deferred. No new decision, ticket claim, implementation or hardware test.

Next useful step: identify the two on-hand V4 revisions/GPS wiring, two undamaged RAK cores and two V3 variants, then prepare a repeatable stock-firmware bench configuration and test procedure.

## 2026-10-12 — Project setup

- Captured the owner's mission, priorities, existing-hardware preference, intended member devices, solar/18650 repeaters, backhaul possibilities, dashboard, content, and grant-reporting goals.
- Initialized local Git on `main` and established the project brief, agent instructions, glossary, local Wayfinder tracker, and record templates.
- Proposed the first planning checkpoint: a measurable field pilot using owned hardware. This checkpoint is provisional pending owner input.
- Requested rough hardware models/counts and pilot member count/acceptable position age.
- Owner supplied an initial scale of roughly 20 trackers, starting with as few as 5, and a tentative GPS target of 5–15 minutes. Recorded these without treating them as verified performance or final acceptance criteria.
- Completed a [primary-source protocol comparison](../docs/research/protocol-baseline.md) on `research/protocol-baseline` for incorporation into `main`; resolved the research ticket. Existing Meshtastic timing settings warrant evaluation before a fork; MeshCore passive GPS behavior requires build-specific verification. Firmware selection remains open.
- Verified local Markdown links, Git whitespace checks, and ignore rules for local secrets/operational data. The local issue tracker is tracked. No firmware or hardware tests performed.

Next: confirm a usable subset of owned radio boards, GPS hardware, and 18650 cells, then agree pilot requirements. No current equipment quantities, verified expenses, field outcomes, or installation permissions have been invented.

## 2026-10-12 — Purchase-list import

- Owner added `Mesh Purchase List - Purchase List.csv` and reports retaining most, but potentially not all, listed items.
- Preserved the source CSV unchanged and imported all 32 rows with stable hardware IDs and source row numbers. Listed quantities are distinct from unknown current counts.
- Used the bundled Python CSV reader and exact decimal arithmetic to check source structure and costs. All rows have 22 fields; all 32 item rows were accounted for.
- Reconciled listed extended costs to $1,989.79; $129.00 is explicitly outside the mesh project, leaving a $1,860.79 listed mesh subtotal. These are not booked cash transactions or current stock valuations.
- Prioritized confirming radio/core variants, GPS hardware, and cells. Kept inventory and firmware-choice tickets open pending that evidence.

## 2026-10-12 — High-value inventory reconciliation shortlist

- Owner requested a reconciliation pass focused on higher-dollar hardware, excluding the full kit and consumables.
- Selected the six mesh purchase-list lines above $100 in listed extended cost: fiberglass antennas, RAK WisBlock assemblies, Heltec V4 boards, whip antennas, the devices labelled “Tdfeck,” and Heltec V3 boards. Costs are historical source references, not current valuations.
- Current counts and condition remain unconfirmed; no stock quantities were changed. The $129 camera card is separately outside the mesh project.

Next: owner confirms remaining counts and known condition for those six groups, then exact radio/core models and fitted GPS for the board/device groups.

## 2026-10-12 — Owner-confirmed higher-value inventory

- Recorded 10 fiberglass antennas, 7 RAK units on hand, 9 Heltec V3, 2 Heltec V4 with GPS modules, 11 Muzi whip antennas, and 2 brand-new LILYGO T-Decks with GPS modules.
- Recorded 2 additional RAK units deployed remotely at Mount Charleston, with recovery deferred until replacement nodes are ready. Possible member-held Heltec V4s remain uncounted pending confirmation/reclamation.
- Preserved historical source quantities. RAK has 9 units accounted for against 10 listed; V3 has 5 more on hand than listed; whip antennas have 5 fewer on hand than listed. V4 has 2 on hand against 6 listed, with member-held stock uncertain. Differences do not establish losses or new expenses.
- GPS modules are owner-confirmed on 4 on-hand devices. Exact hardware variants, GPS on V3/RAK, most condition details, and working passive tracking remain unverified. No purchase or spending was recorded.

Next: identify RAK core modules/radio variants and whether V3 units have GPS, then bench-check a five-device pilot subset. Confirm member-held V4s before deciding any additional quantity to order.

## 2026-10-12 — First-pass inventory closed

- Owner confirms all 9 V3 units lack GPS, with 6 × 1100mAh batteries available for them; 2 × 3000mAh batteries are for V4 units. Both T-Decks have included batteries, capacity unconfirmed.
- Recorded proposed V3 silent internet/backhaul and possible repeater roles without treating them as verified capabilities or a firmware choice. Recorded the owner's concern about larger V4 batteries for later runtime evaluation.
- Owner directed planning from confirmed current stock only. The unresolved RAK may be a third mountain repeater or destroyed; it remains uncertain and excluded, alongside deployed RAKs and unconfirmed member-held V4s.
- Resolved “Inventory owned hardware for the pilot” with first-pass counts, explicit unknowns, and follow-up inspections. Updated the map; did not close other decisions or record purchases.

Next: agree pilot duration and position-age criteria, then identify exact builds and bench-check GPS reporting/runtime. Current stock includes four GPS-equipped devices; a five-member GPS pilot needs one more GPS-equipped device or a revised initial size. No runtime, firmware compatibility, or field tests performed.

## 2026-10-12 — Additional RAK and 18650 count

- Owner found 1 more RAK with a broken carrier board requiring replacement: now 8 on hand (1 damaged) plus 2 deployed, numerically reconciling the source-listed 10. Damaged unit excluded from ready-to-use stock; the other 7 remain untested.
- Recorded 88 × 18650 cells on hand. Owner estimates perhaps 4 cells per mountain repeater, about 8 across the 2 reported deployments; these are separate estimates and excluded from available stock. Cell identity, condition, and capacity remain unverified.
- Updated inventory, deployment notes, and the resolved inventory ticket without reopening it. No replacement purchase or expense recorded. Left the newly added storage-box 3MF file untouched.

Next: identify the damaged carrier board and compatible replacement, inspect cell labels/condition, and continue pilot build/runtime planning. No hardware tests performed.

## 2026-10-12 — Pilot requirements interview started

- Claimed “Define useful tracking for the first field pilot” at the owner's request.
- Read project context, tracker, and current inventory/session decisions; preserved existing uncommitted inventory work and the storage-box file.
- Started clarification of pilot size and maximum dispatch position age, distinguishing position measurement time from receipt time and broadcast frequency.

Outstanding: owner agreement on pilot size and position-age target, followed by duration and device-only workflow. Ticket remains claimed while awaiting input. No hardware tests or firmware decisions made.

## 2026-10-12 — Pilot hardware and reporting direction

- Owner plans 2 Heltec V4 purchases and 2 V4 recoveries, all with GPS and 3000mAh batteries. Recorded these separately from current stock and actual cash transactions; potential pool is 6 V4s plus the 2 existing T-Decks if included.
- Clarified that the tentative 5–15-minute range concerns stale position age. Recorded aggressive reporting followed by congestion-based tuning, with power-based modes and movement thresholds as options to evaluate.
- Kept exact stale cutoff, runtime, device-only workflow, and trial participant count open. No prices, orders, recoveries, performance results, or firmware capabilities assumed.

Next: agree stale cutoff and unplugged runtime, then minimum phone-free member workflow and final trial count. “Define useful tracking for the first field pilot” remains claimed awaiting owner input.

## 2026-10-12 — Tracking MVP requirements agreed

- Owner agreed a 15-minute stale-position threshold, clear stale indication and visible age at dispatch, a 4-hour minimum battery runtime with a 12-hour target, and automatic tracking after power-on for the MVP.
- Recorded larger batteries as an option subject to runtime evaluation; no capacity, cost, or purchase recorded.
- Created “Define a future device-only SOS workflow” at the owner's request and deferred it beyond passive tracking. No SOS implementation or gesture selected.
- Updated the project brief and planned field criteria. No field/bench results recorded. Whitespace checks passed.

Next: confirm whether the first trial uses 6 planned V4s alone or includes 2 T-Decks, then close the shared requirements summary and proceed to firmware/network selection. “Define useful tracking for the first field pilot” remains claimed for that final confirmation. No commit requested or made.

## 2026-10-12 — First-pilot requirements closed

- Owner confirmed V4-only scope to avoid T-Deck device/firmware complexity: 6 planned GPS-equipped V4s with 3000mAh batteries, comprising 2 on hand, 2 planned purchases, and 2 planned recoveries. Current stock counts are unchanged.
- Resolved “Define useful tracking for the first field pilot” with the agreed stale-display, battery-runtime, reporting direction, and power-on workflow requirements plus explicit remaining unknowns. Added its decision link to the map and updated the project, inventory, and planned field criteria.
- “Choose the pilot network and firmware approach” is now unblocked. SOS remains a future open ticket. No other non-research decision resolved in this session.
- Git whitespace checks passed; no hardware/firmware, runtime, or field validation performed. Changes remain uncommitted; no commit requested.

Next: choose a V4-compatible firmware/network approach and identify the exact hardware builds, then define bench checks and reporting settings against these requirements.

## 2026-10-12 — Pilot infrastructure clarified

- Owner clarified that the pilot includes RAK repeaters and 2 Heltec V3 receive-only internet backhauls alongside the 6 planned V4 member trackers. T-Decks remain excluded; V4-only was member-device scope, not total network scope.
- Updated the resolved requirements answer, approach-ticket comments, project brief, map, inventory allocation, planned field criteria, and site notes. Preserved the existing claimed approach ticket and its research; no additional decision resolved.
- RAK quantity/builds and locations remain open. V3 radio silence while forwarding to internet is a requirement to verify, not a demonstrated firmware capability. No stock counts, expenses, or deployment permissions changed.
- Git whitespace checks passed. No hardware, RF, internet forwarding, or field tests performed; changes remain uncommitted.

Next: select the pilot RAK count/builds and verify the chosen firmware supports V4 tracking, RAK relaying, and radio-silent V3 backhaul, then specify ingestion and bench checks.

## 2026-10-12 — Pilot approach interview started

- Claimed “Choose the pilot network and firmware approach” at the owner's request to continue to the next issue; inventory, requirements, and protocol research prerequisites are resolved.
- Read project context and tracker, preserved existing uncommitted work, and started current official-source verification of V4 support and passive GPS behavior for the firmware choice.
- Firmware selection, dispatch ingestion, and bench configuration remain open. No hardware tests, purchases, deployment, or commit performed.

Next: owner chooses a firmware to evaluate first, then agree the minimal dispatch data path and assumptions to verify on the bench. Ticket remains claimed while awaiting those decisions.

## 2026-10-12 — Meshtastic evaluation accepted; requirements refreshed

- Owner accepted Meshtastic as the first evaluation path and expects firmware modifications will likely be needed; stock sufficiency remains unproven.
- Reread the updated “Define useful tracking for the first field pilot”: 6 V4 member trackers plus owned RAK repeaters and 2 strictly receive-only V3 internet backhauls.
- Started checking V3 transmit-disable and uplink behavior against primary sources. The approach ticket remains claimed; no decision closed, hardware tested, or commit made.

Next: clarify anticipated modifications and local dispatch needs during internet outages, then choose a minimal ingestion path and RAK subset with explicit bench verification gates.

## 2026-10-12 — GPS fork review and offline viewing requirements

- Owner identified GPS behavior as the expected firmware-modification area and requested inspection of commits ahead in `lfg-seth/firmware`; started a primary-source commit/diff review.
- Owner confirmed local field command-post viewing and other-member location viewing in companion apps without internet backhaul. Updated the resolved requirements answer, project brief, map, approach discussion, and planned field criteria. Passive tracking remains phone-free.
- Source review supports evaluating V3 LoRa TX disable alongside MQTT uplink; exact build behavior and radio silence still require bench evidence. RAK cores remain unidentified.

Outstanding: finish the fork review, identify GPS changes worth evaluating against current upstream, and select local/remote ingestion arrangements plus a RAK subset. No firmware flashed, hardware tested, expenses changed, or commit made.

### Fork review completed

- Saved the [old firmware fork audit](../docs/research/old-firmware-fork.md), covering all 17 ahead commits (2 merges), net surviving changes, and a targeted comparison against pinned current upstream; fork is 1,887 behind.
- Found GPS timing preferences rather than a new GPS/position algorithm, a 30-minute periodic broadcast requiring revision for stationary freshness, and a source-level coordinate-shift defect in the full-precision MQTT map override. Do not transplant the old fork unchanged.
- Recorded offline app/map considerations and LoRa-silent gateway checks in the approach ticket. Public-history secret values were omitted from the report; do not reuse them for the private pilot.
- Git whitespace checks passed. No firmware builds, hardware/field tests, deployment, or commit performed.

Next: choose the command-post viewing device/connection and RAK subset, then define the current-release bench configuration and concrete GPS behavior gaps. “Choose the pilot network and firmware approach” remains claimed; no additional decision resolved.

## 2026-10-12 — Local viewer and RAK subset selected

- Owner selected both app and laptop/portal viewing, with the Meshtastic app acceptable for the first local-viewing MVP. Recorded 1 owned rugged Dell laptop/tablet running Linux as field equipment (HW-033); model/compatibility and runtime are unknown.
- Owner accepted 2 undamaged on-hand RAKs for initial relay evaluation, subject to core identification and operation checks; individual units remain unassigned. No radio stock counts changed.
- Prepared an approach summary in the claimed firmware/network ticket, including proposed private MQTT position-packet ingestion, local app viewing, and explicit bench prerequisites. Remote ingestion choice/final shared understanding remain pending; no decision resolved.
- Whitespace verification passed; no firmware builds, hardware tests, spending, installation, or commit performed.

Next: agree the approach summary/private MQTT path, then identify exact builds and prepare bench configuration and tests. Changes remain uncommitted; no commit requested.

## 2026-10-12 — Pilot network/firmware approach closed

- Owner accepted one private MQTT broker for both receive-only V3 uplinks and proposed compatible companion-app/cellular member uplinks only if multiple-backhaul behavior is acceptable.
- Completed [multiple-backhaul research](../docs/research/multiple-backhauls.md): documented phone proxy support, duplicate handling, downlink isolation, outage limits, and app/version caveats. No maximum gateway count or capacity result invented.
- Resolved “Choose the pilot network and firmware approach” with the agreed Meshtastic evaluation, hardware subset, local app-first/laptop viewing, private position-packet ingestion, and conditional staged member-phone backhauls. Added its decision link to the map and updated project/backhaul/test records. Only this non-research decision was resolved in this session.
- Exact builds, GPS settings, ingestion implementation, and hardware/field success remain open. Whitespace checks passed; no firmware build/flash, broker deployment, hardware tests, purchases, or commit performed.

Next useful step: identify the V4 revisions/GPS wiring, 2 RAK cores, and 2 V3 variants, then pin a current firmware release and prepare the bench configuration/test procedure. Keep SOS deferred until passive tracking is established. Changes remain uncommitted; no commit requested.

## 2026-10-12 — Future SOS requirements interview started

- Claimed “Define a future device-only SOS workflow” as the next open, unblocked tracker issue at the owner's request.
- Started a requirements-only interview with intended recipients and dispatch response ownership. SOS implementation remains deferred beyond passive tracking.
- Preserved existing uncommitted work. No decision resolved, firmware changed, hardware tested, or commit made.

Outstanding: agree recipients and response ownership, then activation, accidental-trigger handling, cancellation, acknowledgment, and outage behavior. Passive-tracking hardware identification and bench preparation remain the next implementation step.

## 2026-10-12 — Future SOS alerts and friendly areas

- Owner chose both dispatch and nearby-member SOS recipients, requested a Heltec OLED popup/flashing alert, and suggested an optional fitted buzzer. Recorded the hardware idea without assuming parts, compatibility, or spending.
- Recorded desired SOS content: member identity, friendly area name, and latitude/longitude. Owner proposes defining named Mount Charleston AO polygons in Google Earth; no boundaries supplied or inferred.
- Verified Google primary documentation for KML/KMZ export and named polygon geometry. Proposed an offline area lookup for discussion; device firmware/memory feasibility and boundary, overlap, unmatched, and stale/missing-GPS rules remain open.
- No SOS decision resolved, hardware/code changed, tests performed, or commit made. Whitespace verification passed.

Next: agree activation, then alert/cancellation/acknowledgment and response/outage behavior. “Define a future device-only SOS workflow” remains claimed; passive tracking remains the implementation priority.

## 2026-10-12 — Existing V4 button preferred for SOS

- Owner prefers a 5-second hold of the existing Heltec V4 button to activate SOS, replacing long-hold shutdown; no dedicated SOS button selected.
- Checked upstream user-button mapping and hold-event code. Shutdown conflicts warrant a firmware remap investigation; the owned board/button and installed-build behavior remain unverified.
- Proposed visible countdown, early-release abort, and one activation at the threshold for owner agreement. Cancellation and a replacement shutdown workflow remain open alongside acknowledgment/outage/area-lookup details.
- No decision resolved, code/firmware changed, hardware tested, or commit made. Whitespace verification passed.

Next: agree countdown/trigger behavior and how to cancel a sent SOS. Passive tracking remains the implementation priority; the SOS ticket remains claimed.

## 2026-10-12 — Active SOS interaction and GPS requirements

- Owner agreed the 5-second countdown/early-release activation and chose a separate subsequent 5-second hold to cancel/send cancellation. Recorded the need for release between holds and superseded the proposed menu cancellation.
- Recorded an obvious flashing/active SOS indication while incoming messages remain viewable, a new location attempt, a warning when no current fix is available, and last-known coordinates with their original age.
- Owner requested immediate new SOS transmissions when a location becomes available during SOS. Proposed grouping transmissions into one incident with ordered updates; every-fix versus recovery-only scope and no-new-fix repetitions remain for agreement.
- Proposed an explicit location-unavailable SOS when no fix has ever existed. No coordinates, timing guarantees, firmware support, or measured results assumed.
- No decision resolved, firmware/hardware changed, tests performed, or commit made. Whitespace verification passed.

Next: clarify SOS location-update scope and repetition, then acknowledgment/response, cancellation/outages, and remaining area/display rules. The SOS ticket remains claimed; implementation remains after passive tracking.

## 2026-10-12 — SOS text and position traffic separated

- Owner assumes a specially formatted Meshtastic text SOS and rejected an SOS message for every new GPS fix. Recorded faster ordinary position broadcasts during active SOS; exact rate and first-recovered-fix text behavior remain open.
- Recorded the need for retransmission without flooding even when recipients cannot acknowledge. OLED-only rescue followed by cancellation on the originating device is an intended workflow.
- Checked official Meshtastic acknowledgment/retransmission documentation and distinguished transport evidence from human response. Proposed spaced, bounded reminders that slow down independently of human acknowledgment, with optional human acknowledgment stopping text reminders but not active tracking; not yet agreed.
- No final retry policy, packet format, code change, hardware result, or decision resolution established. Whitespace verification passed; no commit made.

Next: agree reminder/acknowledgment behavior, then remaining receiver/cancellation/GPS/area rules. Passive tracking remains the implementation priority.

## 2026-10-12 — SOS acknowledgment deferred

- Owner removed human acknowledgment from the first SOS design and left cancellation to the originating member's separate 5-second hold.
- Superseded the proposal that human acknowledgment stops reminders. Active indication, faster ordinary tracking, and bounded text reminders continue until originating-device cancellation; numerical rates remain unselected.
- Preserved OLED-only response without acknowledgment. Underlying transport acknowledgment is not a condition for clearing SOS; recipient cancellation delivery is still unverified.
- No ticket resolved, firmware/hardware changed, tests performed, or commit made. Whitespace verification passed.

Next: agree behavior when no position has ever been acquired and after an unexpected reboot, then finish remaining requirements/prerequisites. “Define a future device-only SOS workflow” remains claimed; passive tracking remains the implementation priority.

## 2026-10-12 — SOS persistence and power-aware cadence

- Owner agreed SOS sends without any known position and active SOS survives an unexpected reboot until originating-member cancellation.
- Added requested battery status on the SOS screen and power-source-aware effort: maximum configured effort on external power even with low battery, taper on low battery only when battery-powered. Exact thresholds/rates remain open.
- Saved a primary-source [V4 power-detection check](../docs/research/v4-power-detection.md). Battery sensing is supported; reliable external-power detection for a low-battery V4 on a charger/power bank remains unverified and needs exact-board/build investigation plus bench tests.
- No ticket resolved, hardware/firmware changed, spending recorded, or hardware tests performed. Whitespace verification passed; no commit made.

Next: establish external-power detection and unknown-source behavior, then summarize the SOS requirements and remaining implementation prerequisites. Passive tracking remains the implementation priority.

## 2026-10-12 — Power detection pinned for follow-up

- Owner deferred the power-source investigation and proposed sustained battery-level trend over a configurable window, perhaps 1 minute, as an inferred-charging heuristic.
- Recorded the idea in the SOS ticket and power-detection research note without selecting an algorithm or treating trend as proof of external power. Unknown/flat behavior and exact cadence policy remain open.
- No tests, firmware/hardware changes, spending, ticket resolution, or commit. Whitespace verification passed.

Next: resume the remaining SOS workflow requirements and shared summary; keep power detection as a deferred implementation prerequisite. Passive tracking remains the implementation priority.

## 2026-10-12 — Future SOS workflow closed

- Owner accepted receiver short-press silencing with the incident retained, immediate local cancellation with bounded cancellation-delivery attempts through outages, and dispatch coordination when reachable with direct nearby-member response otherwise.
- Resolved “Define a future device-only SOS workflow” with a consolidated owner-agreed answer and linked it from the map. Recorded activation/cancellation, formatted text/ordinary position traffic, GPS age/unavailable fallback, OLED/battery status, reboot persistence, no human acknowledgment, and bounded reminders.
- Kept power detection/battery-trend evaluation pinned and message/rate/area/shutdown/firmware details as explicit implementation prerequisites. SOS implementation remains after passive tracking. Only this non-research decision resolved in this session.
- Whitespace verification passed. No firmware/hardware tests, purchases, deployment, or commit made; existing unrelated edits preserved.

Next useful step: identify the V4 revisions/GPS wiring, 2 undamaged RAK cores, and 2 V3 variants, then pin firmware and prepare the passive-tracking bench procedure. No open tickets remain in the current pilot tracker; create a focused bench-preparation follow-up when continuing implementation planning.

## 2026-10-12 — Charging display option captured

- Added the owner's configurable “keep display always on while charging” idea beside the battery-charge heuristic in the [power-detection note](../docs/research/v4-power-detection.md).
- No default, algorithm, or firmware change selected. The resolved SOS workflow remains closed; power detection stays deferred.
- Whitespace verification passed; no hardware tests or commit made.

Next useful step remains pilot hardware identification and passive-tracking bench preparation.

## 2026-10-12 — Dispatch portal interview started

- Owner redirected planning to a responsive Map/Users/Messages portal, MQTT-equipped V3s and possible V4s, an available Proxmox VM, Cloudflare Tunnel, simple locally managed accounts, and topo/aerial maps. Captured the proposal in the claimed [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) without choosing a stack or provisioning services.
- Recorded current-pin defaults, 15-minute stale display with measurement age, optional history showing measured points and uncertain connecting lines, all-incoming-data storage, shared-channel messages, and the proposed single dispatch transmit gateway. The prior receive-only approach remains recorded; the gateway change awaits agreement.
- Completed and resolved two primary-source research investigations: [broker/portal transport and backend options](../docs/research/dispatch-portal-transport.md), and [map sources/nonprofit access](../docs/research/dispatch-portal-maps.md). Cloudflare portal HTTPS is distinct from stock-device MQTT reachability; PocketBase is a pilot candidate with production-critical caveats and still needs ingestion. MapLibre plus USGS topo/aerial is a shortlist; coverage/age/zoom and offline use need verification. Preserved existing unrelated edits and hardware records; no purchase, publication, hardware test, service deployment, or commit performed.
- Asked the first independent design round: internet-outage workflow, account permissions, dispatch transmit gateway, retention, and dated device/member assignments. No non-research decision resolved.
- Git whitespace verification passed. Research is source-based, with moving firmware documentation/code; no selected release or hardware/backend/browser behavior tested.

Next useful step: owner answers the first round, then refine the map/user/message behavior and broker access path against the research findings. Hardware identification and passive-tracking bench preparation remain outstanding.

### First portal round answered

- Owner selected local Meshtastic fallback for v1, full operational access for registered users, one designated V3 transmitting portal replies, and retention of all pilot data with review before wider rollout.
- Owner proposed numeric device labels and portal member assignment by dispatch/admin or signed-in self-claim. Added device-number/assignment terminology; conflict/transfer/time-history rules remain under discussion.
- Amended current project, inventory allocation, planned field checks, sites, and the earlier approach answer to make the one-V3 transmit exception explicit. This does not select a hardware unit or establish transmission/forwarding success.
- Sent the next design round: assignment collisions; freshness bands; history window and gaps; sending during gateway outages; admin versus operational permissions. The portal ticket remains claimed pending these answers and eventual shared-summary agreement.

Next useful step: finish the portal behavior interview, then choose the broker connection/backend path and map evaluation prerequisites. No services deployed, hardware tests, spending, or commit.

### Second portal round answered

- Owner agreed unassigned-only self-claim with dispatch/admin transfers, preserved dated history, measurement-age breathing bands (under 2, 2–5, 5–15 minutes; stale at 15), separate last contact/unknown GPS, and no invented positions.
- Owner selected 4-hour initial history, measured points with dashed estimated connections and breaks over 15-minute gaps; manual send after outages with an unsent draft; and admin-only account/archive management with full operational access for registered users.
- Third round covers member/device list and unassigned pins, alert scope, shared-gateway author attribution, broker reachability, and pilot backend/map evaluation. Portal ticket remains claimed; no non-research ticket resolved or implementation performed.

Next useful step: answer that round and review a consolidated portal specification with any explicitly deferred infrastructure questions.

## 2026-10-12 — Portal list, alerts, author and evaluation stack agreed

- Owner selected the member/unassigned-device list and default tracker map, one-to-one active assignments, in-portal message toast/unread badges with optional sound, and author-name prefixes for outbound radio text.
- Owner approved a PocketBase/MQTT-worker/MapLibre/USGS pilot evaluation. No backend deployed or operational performance established.
- Owner requested clarification of why a broker VM's Cloudflare Tunnel hostname cannot directly serve stock Heltec MQTT. Rechecked official Cloudflare protocol documentation and current Meshtastic MQTT source; raw MQTT TCP/TLS is distinct from the Tunnel's WebSocket-wrapped TCP path requiring a client-side adapter. Domain use remains possible with a separately reachable broker.
- Portal ticket stays claimed pending the broker clarification and consolidated requirements review. Existing edits preserved; no purchase, publication, deployment, hardware test, or commit.
- Explained the hostname/Tunnel distinction using `mqtt.spp.lol`; documented DNS-only direct MQTT TLS and a WebSocket firmware/bridge candidate. Asked a simpler network question about VM location and router port forwarding. No actual domain, port, or firmware change performed. Git whitespace verification passed.

Next useful step: explain the `mqtt.spp.lol` example, identify a feasible broker connection path or explicitly defer it, and confirm the portal requirements summary.

## 2026-10-12 — No inbound forwarding; portal summary drafted

- Owner confirms the Proxmox VM is local and wants no inbound router port forwarding. Recorded this in the project/site notes and portal ticket; excluded the direct home-broker port-forward proposal.
- Started [Check Heltec MQTT over WebSockets for Tunnel hosting](../.scratch/pilot/issues/09-heltec-websocket-research.md). Compare a home WebSocket firmware/bridge route with a separate reachable private broker using outbound home connections; no route/provider/cost or firmware modification selected.
- Drafted a consolidated requirements summary in [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) for owner review. Asked whether home broker hosting is preferred or a separate broker is acceptable. The portal ticket stays claimed; no non-research decision resolved.
- No deployment, publishing, purchase, hardware tests, or commit. Preserve existing unrelated edits and raw-data ignore policy.

Next useful step: review the narrow transport findings, establish the hosting preference, and confirm the consolidated portal requirements with explicit implementation prerequisites.

### Connectivity investigation deferred by owner

- Owner explicitly stopped further connectivity investigation for now and asked us to assume a local MQTT broker reachable through Cloudflare with stock clients. Recorded that as an unverified planning assumption, without revising primary-source evidence or asserting operational support.
- Interrupted the research agent and released the WebSocket ticket claim. Do not resume connectivity investigation until requested. Updated the project, sites, map notes, and draft requirements accordingly.
- Portal requirements are ready for consolidated owner review. No service deployment, firmware change, field test, spending, or commit; unrelated edits preserved.

Next useful step: confirm the portal summary, then evaluate its map/user/message interface. Networking remains parked for the owner's later investigation.

## 2026-10-12 — Infrastructure monitoring added; portal baseline resolved

- Owner added repeaters/backhaul visibility by role, recorded battery charge/discharge, solar measurements, weather where equipped and intrusion detection where equipped.
- Owner selected a fourth Infrastructure page with device cards/details, telemetry charts and event log, optional infrastructure map layer, and configurable low-battery/missing-telemetry warnings and intrusion alerts.
- Resolved [Define the dispatch portal MVP](../.scratch/pilot/issues/06-dispatch-portal.md) with the consolidated interview answers and accepted addition; linked the answer from the map. Only this non-research decision resolved in this session. MQTT connectivity stays deferred under the owner's explicit planning assumption.
- Added infrastructure terminology, project direction and planned verification. Meshtastic docs establish capability categories, not sensor fitment, measured charging/solar behavior or alert reliability on owned builds. No stock counts or purchases changed.
- Created [Define infrastructure warning and intrusion handling](../.scratch/pilot/issues/10-infrastructure-warning-rules.md) for exact thresholds, permissions, acknowledgment/clearing and repeat behavior. This is separate from UI baseline selection and remains unclaimed.

Next useful step: choose infrastructure warning/event behavior or evaluate a map/infrastructure interface mockup. No firmware/UI implementation, deployment, hardware/sensor tests, spending or commit; existing unrelated edits preserved.

## 2026-10-12 — Device identity and remote naming interview

- Owner asks whether device selection/assignment can trigger OTA long/short-name changes, and whether a persistent device-specific identifier avoids using short names as unique database IDs.
- Completed/resolved [Check persistent device identity and remote name updates](../.scratch/pilot/issues/11-device-identity-research.md) with a [primary-source report](../docs/research/device-identity-admin.md), and claimed [Choose assignment-driven radio names and identity](../.scratch/pilot/issues/12-assignment-radio-names.md) for the owner policy.
- Current schema/source exposes a local hardware `device_id` on ESP32-S3, distinct from the mesh node number and editable names; actual boards/releases need provisioning checks. Remote admin requires authorized keys and a command-capable gateway integration; do not equate it with MQTT text downlink.
- Proposed stable short name S004 and carrier long name Seth [004] on assignment, with portal assignment independent of pending/confirmed/failed OTA naming. Owner choice is pending; no naming policy added to the resolved portal baseline yet.
- MQTT/Cloudflare connectivity stays parked under the owner's assumption. No actual name/admin key changes, device provisioning, flashing, implementation, hardware tests or commit.
- Verified source-level caveat: MQTT JSON text cannot rename and decoded admin payloads are rejected; encrypted PKI transport has a conditional path, so do not claim all MQTT admin is impossible. Recommend a trusted local radio API agent for the supported SDK route; portal execution/read-back remains to test. Git whitespace verification passed.

Next useful step: finish the capability check and owner naming choice, then record the assignment-name behavior and admin integration prerequisite.

## 2026-10-12 — Static device short names agreed

- Owner confirmed tracker short names remain static to device numbers. Resolved [Choose assignment-driven radio names and identity](../.scratch/pilot/issues/12-assignment-radio-names.md), linked it from the map, and amended the portal baseline/project/glossary.
- Recorded the separation of stable device identity, dated assignments and radio-name updates. Short names do not serve as database identity; long-name carrier updates are separate jobs with pending/confirmed/failed state and read-back. Exact formatting/release wording and the admin execution path remain implementation details to settle/verify.
- Only this non-research decision resolved in this session. Existing edits preserved; no actual names/admin keys changed, devices provisioned, UI/firmware implemented, hardware tested or deployment performed. MQTT connectivity stays parked.

Next useful step: define infrastructure warning/event behavior or review a map/infrastructure interface mockup. No commit requested or made.

## 2026-10-12 — Future feature wishlist captured

- Recorded the owner's [deferred feature wishlist](wishlist.md): a known-Wi-Fi table with automatic connection and MQTT-backhaul attempts, and browser-based flashing of project firmware for a small preselected subset of member-owned devices.
- Linked the wishlist from the project brief and pilot map, outside the active ticket frontier. Both ideas remain parked until the owner explicitly brings them forward; no research, design, implementation, or testing started.
- Supported devices, connection behavior and provisioning details remain future questions. Existing MQTT connectivity deferral and passive-tracking priority are preserved. Existing unrelated edits remain intact; no commit requested or made.

Next useful step: continue current pilot/portal planning when requested. Revisit these wishlist items only at the owner's direction.

## 2026-10-12 — Wishlist convention made persistent

- Owner clarified that future requests to “wishlist” an idea or feature refer to the deferred list in `records/wishlist.md`.
- Added the standing routing instruction to `AGENTS.md`: capture the idea outside the active ticket frontier and wait for explicit owner direction before starting work on it.

Next useful step: apply this convention to future wishlist requests. No feature work or commit performed.

## 2026-10-12 — Slack integration wishlisted

- Added Slack integration to the [deferred wishlist](wishlist.md), noting the owner's report that SNORR uses Slack heavily and possible dedicated-channel or app/plugin forms.
- Left use cases and integration mechanism open. No research, active ticket, Slack connection, channel creation, or implementation started; no commit made.

Next useful step: continue current project work when requested; revisit Slack integration only when the owner explicitly brings it forward.

## 2026-10-12 — Wishlist relevance clarified

- Owner clarified that deferred ideas should still be mentioned when relevant to future conversations. Updated `AGENTS.md` and the wishlist introduction to retain that context while keeping work deferred until explicit owner direction.
- Mentioning a wishlist item does not activate it. No feature work or commit performed.

Next useful step: consult the wishlist during related discussions and surface useful connections without starting deferred work.

## 2026-10-12 — Infrastructure warning interview started

- Owner requested work on infrastructure warnings and intrusion handling. Claimed [Define infrastructure warning and intrusion handling](../.scratch/pilot/issues/10-infrastructure-warning-rules.md).
- Started the policy interview covering permissions, notification scope, intrusion clearing and threshold configuration. Existing portal baseline and connectivity deferral remain in force.

Next useful step: collect owner answers, settle dependent repeat/outage/recovery behavior, and confirm the consolidated rules. No implementation, hardware tests, deployment or commit performed.

### First infrastructure round answered

- Owner accepted admin-only rule configuration, acknowledgment by all registered users, audited actions, and admin resolution of latched intrusion incidents with a note.
- Accepted persistent portal badges/cards and toasts, explicitly with no sound. Accepted shared defaults/per-device overrides and emphasized uneven sensor fitment; sensor rules apply only where configured/supported.

Next useful step: settle repeats, recovery, feed outages and missing-report timing, then confirm the consolidated decision. Ticket remains claimed; no implementation or tests performed.

### Second infrastructure round answered

- Owner selected persistent infrastructure badges only and logging of all events, superseding infrastructure toasts; no sound or repeat notifications.
- Accepted automatic health-warning recovery on fresh evidence, separate battery recovery thresholds, feed-outage visibility and preservation of existing alerts, and configurable missing-report timeouts starting at three expected reporting intervals.
- Consolidated policy awaits owner confirmation, including explicit proposals for reconnect grace and intrusion-event grouping. Battery values and sensor/cadence verification remain implementation prerequisites.

Next useful step: confirm the summary and resolve the infrastructure policy ticket. No implementation, hardware tests, deployment or commit performed.

## 2026-10-12 — Infrastructure warning policy resolved

- Owner confirmed the consolidated [infrastructure warning and intrusion policy](../.scratch/pilot/issues/10-infrastructure-warning-rules.md), including reconnect grace and intrusion-event grouping. Resolved this one non-research decision and linked it from the map and portal baseline.
- Added owner-requested device battery configuration metadata: type/chemistry, cell count and nominal mAh capacity with explicit per-cell/pack scope and arrangement where applicable. Unknowns remain explicit; no installed battery types, stock counts, measured capacity or runtime inferred.
- Updated project direction and planned verification. Silent badges replace infrastructure toasts; shared-message notification policy remains separate. Exact battery thresholds, sensor fitment/units and reporting cadence require verification. MQTT connectivity remains deferred; wishlist items remain parked.

Next useful step: review a portal interface mockup or identify and bench-check the owned pilot builds for passive tracking. No implementation, hardware/sensor tests, deployment, spending or commit performed; existing unrelated edits preserved.

## 2026-10-12 — Solar and antenna configuration added

- Owner added solar-panel configuration to device setup, explicitly leaving options for later definition.
- Added antenna configuration including Muzi whip and fiberglass choices, with unknown/unconfigured values explicit. Recorded both additions in the portal baseline and project brief; no installed hardware assignments, inventory counts, purchases or performance claims changed.

Next useful step: review the portal interface or bench-check owned pilot hardware. Solar configuration options remain open. No implementation, tests, deployment or commit performed.

## 2026-10-12 — Next-step review

- Reviewed project decisions, session history and tracker state. Portal requirements, naming and infrastructure warning policy are resolved; the remaining open connectivity research is explicitly deferred.
- Recommended identifying the owned pilot hardware and preparing a small passive-tracking bench test as the next step toward the primary GPS mission. A portal interface mockup remains the next software planning option.

Next useful step: identify the 2 on-hand V4 revisions/GPS wiring, 2 undamaged RAK cores and 2 V3 variants, then prepare firmware/configuration and a bench procedure. No new ticket claimed, implementation, hardware test or commit performed; existing edits preserved.

## 2026-10-12 — Portal development handoff for the night

- Owner requested a brief portal-development next-step review, then stopping for the night. Reviewed the resolved portal baseline; no additional requirements interview or implementation started.
- Recommended a local four-page mockup with synthetic data, emphasizing the tracking map, position age, stale/unknown states and feed outages. Next define the records and worker interface for device identity, dated assignments, observations, packet receipts, messages and infrastructure events, then implement a simulated ingestion-to-map slice before live hardware integration.
- Real integration still needs sanitized packet samples/pinned firmware, verified telemetry capabilities and units, message limits/delivery evidence, and VM/backup setup. MQTT connectivity research remains explicitly parked; it need not block a simulated local prototype.

Next useful portal step: build a local Map/Users/Messages/Infrastructure mockup using synthetic data, then review it before wiring the backend. No new ticket, deployment, publishing, hardware test or commit; existing edits preserved. Session ended at the owner's request.

### Portal stack recommendation

- Owner favors Python for the MQTT worker and is most familiar with React. Recommended React + TypeScript + Vite for the browser portal, retaining PocketBase and MapLibre. React's current official documentation includes a Vite-based setup; frontend choice remains a recommendation pending owner acceptance.
- Python worker preference recorded; no worker library, dependency versions or broker software selected. No implementation or deployment started.

Next useful step: confirm the frontend direction when resuming, then build the local synthetic-data mockup. No commit made.

### Hosting comparison

- Compared current official Vercel Hobby/function limits and PocketBase deployment guidance. Recommended retaining the owned Proxmox VM for the pilot: static React build, persistent PocketBase data, Python MQTT worker and private broker together.
- Vercel is a possible frontend-only host, but that split retains the VM/backend dependency and adds hosting configuration. Hobby functions are duration-limited and do not fit the intended continuous MQTT worker; plan eligibility remains to check if Vercel is considered.
- Home power/internet availability, service restarts and backups remain deployment checks. No hosting decision changed, service deployed or connectivity research resumed; no commit made.

### Portal bandwidth and client performance

- Owner reports a 100Mbps home uplink. Expected pilot bandwidth is manageable if browsers fetch USGS basemap tiles directly and receive small incremental operational updates; this is an architectural estimate, not a measured load test.
- Verified official Cloudflare caching guidance, USGS cached basemap services and MapLibre performance guidance. Recommend caching public versioned frontend assets, leaving authenticated operational responses uncached, and keeping map tiles off the home-origin path.
- Client checks should cover slow cellular connections, tile-provider latency, GPU/WebGL support on the rugged Dell and mobile devices, marker animation, bounded history queries and reconnect behavior. Concurrent viewers, actual payload sizes, VM resources and observed latency remain unmeasured.
- No deployment/configuration change, hosting decision or connectivity investigation performed. Next prototype should measure cold/repeat loading and live updates on actual field devices; no commit made.

## 2026-10-12 — Pre-bench firmware readiness review

- Owner asked whether firmware changes are needed before bench testing. Reviewed the agreed pilot approach, old-fork audit, future SOS requirements and deferred power/wishlist work. Recommend a stock Meshtastic baseline with deliberate configuration; no mandatory source patch identified for the initial passive-tracking tests. Stock sufficiency remains unproven until hardware tests.
- Rechecked official [position configuration](https://meshtastic.org/docs/configuration/radio/position/): acquisition cadence, periodic broadcasts, movement thresholds, configurable GPS pins and GPS-solution timestamp flags exist. Proposed an initial diagnostic profile of 60-second acquisition, 120-second periodic broadcasts and smart broadcasting off to isolate stationary reporting; these are unapproved/unmeasured trial suggestions, not operational settings or a freshness guarantee. Verify saved settings after reboot and measure actual fresh-fix transmissions.
- Official [Heltec support](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/) distinguishes original V4 from V4-R8 firmware targets. Identify owned revisions/GPS wiring and RAK cores before pinning a release and matching per-board images. Do not reuse the old fork's 30-minute member broadcast preference.
- Existing [LoRa transmit disable](https://meshtastic.org/docs/configuration/radio/lora/#transmit-enabled) and [MQTT configuration](https://meshtastic.org/docs/configuration/module/mqtt/) warrant configuration-first gateway tests. Preserve the later amendment: one V3 may transmit portal replies; the other remains receive-only. Test continued uplink and silence through reboot/reconnect on the pinned build. No broker-connectivity investigation resumed.
- Portal measurement-age/stale display, assignments, deduplication and warnings are application/integration work. The agreed custom SOS button/countdown, incident persistence/cancellation, reminders, OLED handling and area lookup need later firmware implementation/evaluation; deferred charging heuristics and wishlist items remain parked.

Next useful step: identify boards and GPS connections, pin supported stock images, save a bench configuration, then test phone-free boot, stationary/moving GPS freshness, reboot persistence, relay/backhaul behavior and battery runtime. No firmware changed/flashed, hardware tests, ticket status changes or commit performed; prior unrelated edits preserved.

## 2026-10-12 — Project naming suggestions

- Owner requested a short umbrella name connecting SNORR, mesh networking and communications, understandable at a county meeting and suitable for a GitHub repository.
- Recommended SNORR Link, with the descriptor "Search and Rescue Tracking & Communications" and suggested repository name `snorr-link`. Alternatives: SNORR MeshLink, SNORR Connect and SNORR RescueNet. These are suggestions awaiting owner selection; the existing project/repository name remains in place.

Next useful step: owner selects a name. No repository rename, availability check, publishing or commit performed; existing edits preserved.

## 2026-10-12 — SNORR MeshLink GitHub publication

- Owner created `lfg-seth/snorr-meshlink`, supplied its SSH URL, authorized pushing the project there and requested a push after every commit. Adopted SNORR MeshLink in the project overview and saved the publication/push policy in AGENTS.md.
- Confirmed the remote is empty and SSH access works using Windows OpenSSH. Prepared the accumulated inventory, pilot decisions, portal/SOS requirements, research, wishlist and session records for a coherent publication checkpoint. The local Markdown tracker is mirrored with the repository; no GitHub Issues migration requested.
- Refreshed the README's outdated pilot summary. Kept the unrelated untracked battery-box 3MF model outside the commit. No hardware tests, implementation or operational deployment performed.

Next useful step: identify pilot boards/GPS wiring and prepare passive-tracking bench tests, or resume the synthetic-data portal mockup. Push each completed commit to origin and report failures; keep private operational data outside Git.

### Broker renewal diagnosis follow-up

- Owner asked whether closed inbound 443 explains renewal failure. Official [Certbot standalone documentation](https://eff-certbot.readthedocs.io/en/stable/using.html#standalone) confirms the configured standalone HTTP-01 method requires public inbound TCP 80; inbound 443 is not required for that method. Outbound HTTPS to the ACME service is separately required. Closed 80 is a possible cause, not confirmed without logs.
- Requested root-visible Certbot journal and the latest Let's Encrypt log error block. Renewal cause remains pending; no firewall change or renewal attempted. After renewal, separately verify deployment of the renewed certificate into Mosquitto's configured certificate files and reload behavior.

### HTTP-01 failure located

- Owner supplied root-visible Certbot failure evidence. Active HTTP-01 challenge request received 404 on public port 80; outbound ACME HTTPS succeeded. Read-only follow-up HTTP probe returned an nginx 404. A routing/proxy/challenge-serving mismatch is suspected; the precise destination remains to inspect. Closed inbound 443 is not the cause of this configured HTTP-01 failure.
- Recorded sanitized evidence in the transport report. Next inspect public port-80 forwarding/nginx routing, correct the selected challenge path and run a renewal dry-run before production renewal and broker certificate deployment. No remote changes or commit performed.

### Heltec port explanation

- Owner asked whether Heltecs specify a port and what 1883/8883 do. Verified current Meshtastic source parses `hostname:port`, choosing default 8883 with TLS and 1883 otherwise. Documented gateway settings `mqtt.spp.lol:8883` with TLS enabled and private proxy-to-broker 1883 role. Actual firmware remains unpinned/unverified; member LoRa trackers do not all need MQTT.
- Captured source-level credential-logging/certificate-verification checks for later provisioning without reading or publishing actual credentials. No device/server changes or commit performed. Next step remains adapting the fresh broker for Mike's TLS-termination layout and verifying actual endpoints/builds.

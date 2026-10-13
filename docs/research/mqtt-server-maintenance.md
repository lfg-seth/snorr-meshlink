# Existing MQTT host maintenance

2026-10-13 — Owner authorized updating and securing Mike Rollins's existing broker. This is work in progress, not a completed security assessment.

## Verified before changes

- Ubuntu 24.04.3 LTS, Mosquitto 2.0.18; OS updates pending based on cached package lists. SSH package is current against those lists; package indexes last updated today. Refresh indexes before deciding package currency.
- Readable SSH configuration disables root login, password and keyboard-interactive login, and enables public keys. Effective privileged `sshd -T` output remains to verify. Account SSH directory/key-file permissions are restrictive.
- Automatic apt update/security-upgrade configuration and timers are enabled. Reboot-required flag dated 2026-10-09; running kernel predates available kernel packages. No reboot authorized separately with Mike or performed.
- Broker anonymous access disabled and TLS/password listener on 8883. Expired certificate, failed HTTP-01 challenge and absent configured topic ACL remain unresolved. Firewall state and usernames require privileged inspection.
- SSH account has sudo membership but requires an interactive password; unattended administrative operations are unavailable. Do not send passwords to Codex or enable broad passwordless sudo for this task.

## Prepared OS update step

[Update script](../../scripts/server/update-mqtt-host.sh) was syntax checked and uploaded to `~/meshlink-maintenance/update-mqtt-host.sh` in the owner's server account. The owner can run it locally:

```bash
sudo bash ~/meshlink-maintenance/update-mqtt-host.sh
```

It validates SSH syntax, makes a root-only configuration archive (including sensitive material) under `/root/meshlink-maintenance/`, refreshes apt indexes and performs a no-removal upgrade with normal interactive review. It then checks SSH syntax, SSH/broker activity, package versions, listeners and reboot status. It does not change ACLs, firewall policy, SSH policy, credentials or certificate configuration, and does not reboot. Package maintainer scripts can restart services during upgrade. This archive is configuration recovery, not a full VM or broker-message database backup; avoid package downgrades or blindly restoring stale keys as a rollback.

## Remaining work

1. Obtain privileged UFW/effective SSH settings, account names only, and public certificate status. Preserve existing SSH path (external mapped port versus local 22) and Mike's administration access before firewall changes.
2. Once Mike's port-80 routing is ready, run Certbot staging renewal test, production renewal after success, and implement/test restricted certificate copy/reload automation. Renewed certificate must reach Mosquitto's configured paths.
3. Identify existing active clients/topic roots before imposing ACLs. Give gateways and worker individual credentials and only required topic rights; restrict downlink to the designated gateway. Preserve existing credentials until replacement clients are verified; do not blindly grant broad write access or break the old pilot.
4. Verify validating external TLS, anonymous/incorrect-credential rejection, allowed and denied topic operations using synthetic isolated topics, no retained radio commands, restarts and reconnects. Test actual gateway certificate verification on the pinned firmware; broker-side TLS cannot fix a client that skips verification.
5. Arrange the required reboot with Mike, verify SSH/MQTT after boot, and establish private backups/restore checks and ownership of routine updates.

References: [Ubuntu SSH guidance](https://ubuntu.com/server/docs/how-to/security/openssh-server/), [Mosquitto configuration](https://mosquitto.org/man/mosquitto-conf-5.html), [Certbot renewals](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates). No claim that these preparation steps alone make the server secure.

## 2026-10-13 — Updates/reboot completed; automation prepared

Owner ran the OS update script and supplied its successful completion output, then ran `sudo reboot`. SSH reinspection confirms kernel `6.8.0-146-generic`, active SSH/Mosquitto and no remaining reboot-required flag. The installed generic kernel package is `6.8.0-146.146`; earlier cached upgrade availability did not establish that later `147` package was installed. The reported fwupd restart failed during package maintenance; after boot the unit reports inactive/success with status zero and no visible journal entries to the unprivileged account. That does not diagnose the earlier failure.

Owner authorized automatic updates and scheduled reboots because nobody actively maintains the server. Current host timezone is UTC; default unattended policy enables security origins but leaves ordinary `noble-updates` disabled. Prepared [automation installer](../../scripts/server/configure-mqtt-auto-updates.sh), syntax checked locally/remotely and uploaded to the owner's server home directory. Proposed default pending time preference: daily upgrades at 03:00 America/Los_Angeles (up to ten minutes jitter), and reboot at 04:00 only if `/var/run/reboot-required` exists. Timer timezone was verified on the server and handles daylight saving without changing the host timezone.

```bash
sudo bash ~/meshlink-maintenance/configure-mqtt-auto-updates.sh
```

Installer adds same-release Ubuntu updates to the existing security origins; no major release upgrade or third-party origin is added. Keeps apt's own automatic reboots disabled; a separate nonpersistent systemd timer performs needed reboots only at the scheduled window, even with users logged in, and skips the day if apt daily maintenance is active. The existing apt timer's persistent behavior may catch up updates after downtime, but the reboot timer never catches up a missed window on startup. Package service restarts can still occur during update installation. A private configuration backup is created before changes. It does not immediately run upgrades/reboot or alter firewall/MQTT/TLS credentials. It was initially prepared only; owner confirmed successful sudo installation on 2026-10-13, as recorded below.

Verify the installer output, next timer dates, `apt-config dump`, and a privileged `unattended-upgrade --dry-run --debug` afterward. Scheduled reboot behavior and future upgrade/reconnect outcomes are untested. Routine automation still needs failure visibility and someone responsible for response; this does not resolve certificate renewal or broker topic controls. Source: [Ubuntu automatic updates](https://ubuntu.com/server/docs/how-to/software/automatic-updates/), and the installed unattended-upgrade code/configuration inspected directly.

## 2026-10-13 — Automatic maintenance enabled

Owner supplied installer completion and timer output confirming activation:

| Setting | Enabled policy |
| --- | --- |
| Updates | Security plus same-release Ubuntu stable updates, daily 03:00 America/Los_Angeles with up to ten minutes jitter |
| Reboot | 04:00 America/Los_Angeles only when `/var/run/reboot-required` exists |
| Logged-in users | Do not prevent a scheduled reboot |
| Busy maintenance | Reboot skipped when apt-daily or apt-daily-upgrade service is active |
| Missed reboot | No immediate catch-up reboot at boot; wait for next scheduled window |
| Timezone | Explicit Pacific timer expressions; host stays UTC; daylight saving handled automatically |
| Release upgrades | Not enabled |

Owner output lists the first next upgrade at 2026-10-14 10:08:37 UTC and reboot check at 11:00:00 UTC. Root-only pre-change archive: `/root/meshlink-maintenance/auto-20261013T194349Z/config-before.tgz`. Archive contents remain on server and are not published. Timer enablement is confirmed by supplied output; subsequent automated updates, required-only reboot and reconnect behavior still need observation. Privileged unattended-upgrade dry-run, failure monitoring/response and full backup/restore remain outstanding alongside TLS/access hardening.

## 2026-10-13 — Checks while HTTP-01 routing is pending

Remote read-only verification confirms SSH/Mosquitto active, reboot timer enabled, update/reboot schedules in the expected Pacific window, and effective apt policy includes security plus stable same-release updates. Apt automatic reboot is disabled as intended because the separate timer controls reboots. The visible next upgrade time changed within its configured jitter window; no exact minute is promised.

Mosquitto's running process uses the mosquitto user/group rather than root. Password file mode is 0640, owner/group mosquitto; private key is 0600, owner/group mosquitto. Neither secret file was read. The broker data directory is 0755 and should be reviewed for local-user data visibility without listing or reading archived messages; file permissions and actual contents remain uninspected. UFW service is enabled but this does not establish active firewall policy. AppArmor tooling is present; actual loaded/enforced profiles require privileged verification.

A credential-free diagnostic connection negotiated TLS 1.3 and received MQTT CONNACK code 5 (not authorized) for anonymous CONNECT. Certificate validation was deliberately disabled only in this isolated probe due to the known expiry; no credentials, subscriptions, publications or messages were exchanged. This verifies anonymous rejection, not certificate trust or topic permissions.

Next privileged checks: UFW active rules, effective SSH settings, MQTT usernames only, AppArmor profile status, and `unattended-upgrade --dry-run --debug`. Identify actual old-pilot clients/topics before enforcing ACLs. TLS renewal remains separate; no firewall, account, broker-data permission or ACL change made by these checks.

## 2026-10-13 — Privileged audit results

Owner-supplied privileged output confirms UFW inactive; enabled systemd service state had not established firewall activation. Effective SSH settings: root login disabled, public keys enabled, **password authentication enabled**, keyboard-interactive authentication disabled. This supersedes inference from readable main-file settings: effective `sshd -T` is authoritative for the default connection context; connection-specific Match rules also need consideration. Eleven existing MQTT usernames are present; account secrets/hashes were not supplied. Preserve existing clients until topic/credential migration is defined.

AppArmor loaded 116 profiles, including 23 enforce profiles; owner output identifies rsyslog as the profiled running process and no Mosquitto profile. No broker AppArmor confinement established. Generic loaded application profiles do not prove those applications are installed/running.

Prepared next firewall step: preserve existing rules, allow host TCP 22 (external SSH maps from 64582), 8883 for MQTT TLS and 80 for Certbot; default deny incoming/allow outgoing, enable UFW and inspect resulting rules. Existing dormant rules must be reviewed with `ufw show added`; no firewall change performed by Codex. Confirm a fresh SSH session before closing the current one. Disable SSH passwords only after Mike's key-based access is confirmed. A readable config-file listing/source inspection was attempted to locate the override, but effective password setting is already confirmed by owner output. Remaining privileged update dry-run not supplied.

## 2026-10-13 — Fresh-pilot reset authorized and prepared

Owner explicitly requested archiving all existing MQTT material and setting up a fresh broker for this pilot. This supersedes preserving old-client access. Prepared [reset installer](../../scripts/server/reset-mqtt-pilot.py) and uploaded it to the owner's server account:

```bash
sudo python3 ~/meshlink-maintenance/reset-mqtt-pilot.py
```

The installer stops Mosquitto to flush persistence, moves `/etc/mosquitto`, `/var/lib/mosquitto` and `/var/log/mosquitto` into a timestamped `/root/meshlink-archive/mqtt-legacy-*` directory, and records the old service definition. Archive includes credentials/hashes, keys and potentially raw tracks/messages; keep it private on the server. It provisions empty data/log directories with restrictive permissions, a TLS-only 8883 listener, three random fresh credentials and explicit ACLs. Old accounts are removed from the active broker. Configuration/startup/permission-test failure restores original trees and retains failed fresh material privately. A fresh-pilot marker/credentials guard prevents accidental repeat resets. No system package, SSH/firewall, hostname or unrelated Let's Encrypt lineage is removed.

| Account | Initial access |
| --- | --- |
| `pilot-v3-uplink-1` | Publish protobuf envelopes under `snorr/pilot/2/e/#`; no topic delivery/read access |
| `pilot-v3-uplink-2` | Same, separate credential |
| `pilot-worker` | Read protobuf envelopes under `snorr/pilot/2/e/#`; no publishing |

Common firmware MQTT root is `snorr/pilot`; JSON uplink and dispatch-command publishing are initially denied. Each gateway's actual node ID/topic suffix still needs identification to tighten publish ACLs; current gateway grants share the uplink namespace and do not prove sender identity. Existing one-designated-V3 dispatch requirement remains future integration work, not revoked. No command account or downlink is enabled until gateway identification/topic configuration is verified. New plaintext credentials are kept only in root-private `/root/meshlink-private/mqtt-credentials.json`; do not paste or commit them.

Installer copies the current Let's Encrypt certificate/key into broker paths and reports expiry. It can start with the known expired certificate for local diagnostics; **external validating TLS remains blocked until renewal**. It installs a root-owned deploy hook for the current `mqtt.spp.lol` lineage, validates hostname/key match and certificate validity, copies certificate material and reloads Mosquitto after future successful renewal. Hook execution and real renewal still require verification; changing hostname later requires updating its lineage/configuration.

Verification: Python syntax checks passed. Tested credential generation/hash conversion and ACL behavior against a temporary loopback-only instance of installed Mosquitto 2.0.18 with synthetic nonretained traffic. Anonymous/invalid login rejected; both gateways can publish uplink and receive no topic delivery; worker can receive uplink but cannot publish; JSON command and unrelated namespaces denied. Mosquitto accepts some subscriptions before filtering delivery, so tests check actual delivery rather than treating SUBACK as proof of read authorization. No live legacy broker config/data was touched by testing. The full root reset/archive/rollback and renewal hook are not executed/tested yet.

State: **prepared and uploaded, not run as root**. Next owner runs the command, shares status output without credentials, then verify live service and archive completion. Certificate renewal, firewall activation, effective SSH password policy and real V3/worker integration remain outstanding.

## 2026-10-13 — Owner hold pending Mike's infrastructure

Owner explicitly put the issue on hold. Mike is updating `mqtt.snorr.org` and placing the VM behind Nginx with certificates handled there. Fresh reset, further hardening and integration remain deferred; no new probes or server changes during the hold. The direct-TLS reset script must be adapted before execution for the private 1883 backend. Resume when the owner brings this issue forward after Mike completes his work.

## 2026-10-13 — Private-backend reset adapted

Owner brought broker configuration forward while Mike's DNS/Nginx work remains pending. Replaced the earlier direct-TLS installer with private plaintext MQTT 1883, removed certificate source/install/reload dependencies and switched client metadata to intended public `mqtt.snorr.org:8883` with TLS. It archives old configuration/accounts/data/logs and old `mqtt.spp.lol` broker-specific renewal configuration/hook/helper when present; other certificate lineages/timers are left alone. No certificate provisioning/research resumed.

Default invocation:

```bash
sudo python3 ~/meshlink-maintenance/reset-mqtt-pilot.py
```

Default bind is `127.0.0.1:1883` because Nginx's actual private source address is not known. This is broker-local readiness, not yet a reachable backend for a separate-host proxy. For LAN binding, the installer requires explicit `--bind-address MQTT_VM_PRIVATE_IP --proxy-address NGINX_PRIVATE_IP`, private IPv4 values and an already-active UFW ruleset whose first rules allow only that source to the backend's 1883 and deny other 1883 connections. Existing SSH must remain allowed before activating UFW. Exact source addresses/rules still need verification; the LAN preflight path is not exercised yet. Do not expose 1883 publicly.

New credentials/ACLs retain two protobuf uplink-only accounts and one read-only ingestion worker, root `snorr/pilot`, no command publisher/downlink. Plaintext secrets exist only in the root-private credential file and are never printed. Existing old-client access ends after successful reset. `sudo python3 ~/meshlink-maintenance/reset-mqtt-pilot.py --verify` repeats synthetic broker authentication/topic checks without another reset.

Prepared script uploaded and Python syntax checked. Isolated installed-Mosquitto tests pass for private-backend auth and actual ACL delivery. Temporary-filesystem integration exercises complete reset/archive/new credentials and injected-startup-failure rollback with administrative service/ownership calls mocked; live broker unchanged. The real privileged reset, archive ownership and firewall-restricted LAN path still require execution/verification.

Status: uploaded, awaiting owner's local sudo; no live fresh-broker readiness claimed. Script has no public-endpoint or certificate dependency. Remaining Nginx connectivity, actual gateway IDs/topics, firmware/client setup and designated-gateway downlink remain pending.

## 2026-10-13 — Fresh private broker installed and verified

Owner ran the adapted reset installer successfully. Its live checks passed for pilot credentials, anonymous/invalid rejection, actual read/write delivery ACLs and command/unrelated-topic denial. Private archive: `/root/meshlink-archive/mqtt-legacy-20261013T204408Z`. Private credentials: `/root/meshlink-private/mqtt-credentials.json`; contents not read or published. Old broker-specific renewal configuration archived by installer.

Independent SSH follow-up confirms active Mosquitto using its own account, `127.0.0.1:1883` listener only, no 8883 listener, configuration/data/log directories mode 0750, and scheduled-maintenance reboot timer enabled. This supersedes prepared-only reset status above. Accounts and ACLs are installed for local tracking ingestion; JSON/dispatch publishing denied initially.

Separate-host Nginx cannot reach a loopback listener. Await Mike's actual private source IP, then enable a private interface listener with source-restricted firewall rules and verify Nginx-to-broker access. Public `mqtt.snorr.org:8883`, actual gateway/worker adapters, client certificate verification/reconnect, designated-gateway dispatch downlink and SSH password hardening remain unverified. No further listener/firewall changes made during the verification. Archive restoration was tested only in the earlier temporary-filesystem failure test, not against the live private archive.

# Mosquitto migration to pve06

## November 25, 2026 public activation of mqtt.spp.lol

CT 101 serves native MQTT over TLS at **mqtt.spp.lol:8883**. Cloudflare DNS
resolves the name to 64.250.235.204. OPNsense forwards TCP 8883 on that
destination to 10.2.70.10:8883. The destination NAT and WAN pass rules
are enabled. Mosquitto terminates TLS and requires an authenticated client.
An external workstation verified TLS 1.3, the hostname and rejection of an
anonymous MQTT connection.

Certbot uses the Cloudflare DNS plugin and a zone-scoped credential in
`/etc/letsencrypt/credentials/cloudflare-spp.ini` (root, mode 0600). The
initial Let's Encrypt certificate expires February 24, 2027 UTC.
`certbot.timer` is enabled. The deploy hook at
`/etc/letsencrypt/renewal-hooks/deploy/50-meshlink-mqtt` checks the
chain, hostname and key pair, installs files readable by Mosquitto, reloads
the service and verifies the certificate actually served. To repeat renewal
acceptance inside CT 101, run
`certbot renew --cert-name mqtt.spp.lol --dry-run --run-deploy-hooks --no-random-sleep-on-renew`.
The staging renewal and hook passed. The eight-account private TLS test
passed 10 allowed and 30 denied publishes, 11 expected deliveries and
69 withheld deliveries.

At Seth's Home, G008 now connects with its dedicated account. The private
primary channel allows uplink and downlink. The radio also requires
`lora.ignore_mqtt=false`. After a hardware reset, G008 decoded the exact
dispatch test text over USB. In the reverse direction a subscriber on
the public broker decrypted the exact text originated by G008.

For rollback, the pve06 helper at
`/root/colo-prep/snorrmesh-staging/wan_8883.py` supports `status` and
`disable`. Its saved pre-change rule definitions are in the same directory.
The older broker and its established portal worker session remain in service
for the overlap. Migrate Lee Fire and verify fresh receipts on the new
broker before retiring the old path. Live portal text composition requires
application integration. The following dated sections preserve the staging
and previous-host history.

## November 25, 2026 private staging before public activation

The replacement broker runs in unprivileged CT 101 on pve06. The existing client contract is native MQTT over TLS at `mqtt.snorr.org:8883` with topic root `snorr/pilot`. The private listener is available to management at `10.2.70.10:8883`. OPNsense holds the sole public address, `64.250.235.204`. Both the WAN forward and its pass rule are disabled.

Mosquitto 2.0.18 started with an empty persistence directory. Ubuntu enables persistence at `/var/lib/mosquitto/`. The listener in `/etc/mosquitto/conf.d/snorrmesh.conf` binds only the private IPv4 address on port 8883, terminates TLS and disables anonymous login. It uses `/etc/mosquitto/passwd` and `/etc/mosquitto/acl`. Both installed files matched the live export byte for byte.

The operator exported from the old broker through its pinned SSH endpoint. The root-only backup at `/root/snorrmesh-migration-6oxs_y90/broker-full.tar.gz` contains the source configuration and a fresh persistence snapshot. The exporter checked that the database member was nonempty. The separate encrypted transfer to pve06 passed checksum verification. Only the authentication files were installed in CT 101. The source remains active for rollback.

The original probe assumes three pilot accounts. Private acceptance used all six live credentials and eight topic cases per account, covering exact topics, wildcard grants and the explicit deny in the source ACL. Each run verified 15 permitted publishes and 33 denied publishes. Subscribers received all 19 expected deliveries. All 71 unauthorized reader/fixture combinations received zero deliveries. Each fixture was synthetic and non-retained.

Private TLS hostname verification passed with explicit staging trust. Anonymous connections and a valid account with an incorrect password were rejected. The full six-account matrix passed again after a Mosquitto restart. Broker startup was also verified after a CT reboot. Proxmox starts OPNsense first and the broker second. Final OPNsense readback confirmed both WAN rules disabled. Public activation awaits the separate certificate and renewal handoff.

## G008 messaging change to apply on both brokers

**Recorded November 25, 2026.** G008 at Seth's Home is Heltec V3 `!9ea13cc0`.
The primary channel is `SNORRbench`. Both radio MQTT directions survived
reboot and its uplink reached production. A non-retained marker published
using `pilot-v3-uplink-1` reached the archive on the proposed dispatch topic.
The same account subscribed to the radio's channel filter and did not receive
the marker. The shared account can therefore already **write** to the proposed
dispatch topic. Reserve that topic before enabling the new reader.
[G008 readiness](../../records/sessions.md#2026-11-25---checked-g008-readiness).

| Target | Verified baseline | G008 account and ACL change |
| --- | --- | --- |
| Old production broker | Public TLS login and uplink observed before the change | Operator applied the matching delta. Service active, reload successful. Eight-account matrix passed on the pinned old host's private listener at 01:12 UTC November 26. Fresh public connections on TCP 8883 failed before TLS. |
| pve06 CT 101 | Six-account import and private acceptance above | Applied and reloaded. Six-account regression and eight-account G008 checks passed after reload and again after service restart by 01:09:36 UTC November 26. |

### November 25 Pacific execution record

Public DNS still returned `136.38.118.13` (A-record TTL 60 seconds) at the
check. The staging test ran **on pve06**, reached over Tailscale SSH at
`100.93.64.94`. It opened TCP to **10.2.70.10:8883** while passing
`mqtt.snorr.org` as TLS SNI and the required certificate hostname. TLS 1.3
verification passed against the existing staging trust file. To repeat the
handshake from the workstation:

```sh
ssh -o StrictHostKeyChecking=yes root@100.93.64.94 "openssl s_client -connect 10.2.70.10:8883 -servername mqtt.snorr.org -verify_hostname mqtt.snorr.org -verify_return_error -CAfile /root/colo-prep/snorrmesh-staging/staging-trust.pem -brief </dev/null"
```

Both brokers now have the two account grants below. The two legacy wildcard
writers (`pilot-v3-uplink-1` and `pilot-v3-uplink-2`) each received an
explicit dispatch-topic deny. Updated hashes came from CT 101. Its root-only
backup is `/root/g008-mqtt-rollout/before-as5dm6mg`. The old host's operator
ran the guarded updater from `/home/setheth/g008-rollout.vklnuWHR`. Its
pre-change backup is under `/root/g008-mqtt-rollout/before-*`. The updater
checks both original auth files before installation and reloads Mosquitto.
The new account secrets are held root-only in CT 101.

On CT 101 the original six-account suite passed before and after the change.
The additional eight-account matrix exercised five topic cases on each
broker: 10 allowed publishes, 30 broker denials, 11 expected deliveries and
69 withheld reader/fixture combinations. Only the dispatch writer could
publish on the dispatch topic. G008's firmware-style wildcard subscription
received exactly its dispatch marker. Test clients used distinct IDs and
non-retained payloads that do not decode as radio packets. From pve06,
repeat the private tests in `/root/colo-prep/snorrmesh-staging/` with
`python3 private-acceptance.py` and `python3 g008-acceptance-20261125.py`.

The old broker passed the eight-account test through temporary loopback-only
SSH forwards to `mesquito-server` on `127.0.0.1:1883`. Its normal public TLS
front end needs a separate reconnect check: pve06 received TCP refusal and
the workstation and MeshLink host timed out on new connections. The MeshLink
worker still had an established connection to `136.38.118.13:8883`; a genuine
G008 envelope arrived at **01:12:12 UTC** (17:12:12 Pacific on November 25).
G008 retains its current login so that this working session can continue.
Next: check the old public TCP 8883 forward and TLS proxy, verify a fresh
public TLS login with the dedicated account, then update the radio and verify
a fresh uplink. Public DNS, WAN rules and listeners were untouched by this
account rollout.

At 17:16 Pacific on November 25, fresh probes used the literal hostname
`mqtt.snorr.org:8883`. DNS returned `136.38.118.13`. TCP timed out from the
workstation and MeshLink host and returned connection refused from pve06.
All three stopped before TLS ClientHello, so the hostname's TLS configuration
and MQTT login were untested on those connections. On the old ingress, check
whether public TCP 8883 reaches the Nginx host and whether that host is
listening on 8883. The expected TLS stream upstream is `192.168.12.51:1883`.

At 17:21 Pacific, the .org parent delegated snorr.org to the four XMission
nameservers. Each answered authoritatively for mqtt.snorr.org with
`136.38.118.13`, TTL 60 seconds, and the same zone serial `2026102300`.
Cloudflare, Google Public DNS and Quad9 also returned the old address.
The intended `64.250.235.204` was absent from the published A record.
Confirm whether the submitted change was an XMission A-record edit or a
registrar nameserver change and check its publication status at that provider.

### Accounts and topic permissions

Use the same two new usernames and corresponding secrets on both servers.
Applied Mosquitto ACL entries follow. G008's uplink topic ends in its
physical ID. Its firmware subscribes to `snorr/pilot/2/e/SNORRbench/+`.
Grant delivery on the single matching dispatch topic. Broad channel read
access could put other gateways' routine uploads back onto RF.

```conf
user g008-gateway
topic write snorr/pilot/2/e/+/!9ea13cc0
topic read snorr/pilot/2/e/SNORRbench/dispatch

user meshlink-dispatch
topic write snorr/pilot/2/e/SNORRbench/dispatch
```

Inspect the effective ACL for **every existing writer**. Exclude the exact
dispatch topic from each overlapping uplink grant. For a write-only gateway
user with a broader grant, add `topic deny snorr/pilot/2/e/SNORRbench/dispatch`
inside that user's ACL block. For a user that also needs to observe the topic,
narrow its write grants while preserving its read access. Check any global
pattern grants as well. Keep the ingestion worker and monitoring subscribers
on their existing read paths. The dispatch publisher credential belongs to
the portal backend. Use non-retained publications and manual retry after an
outage. [Mosquitto ACL semantics](https://mosquitto.org/man/mosquitto-conf-5.html).

### Rollout, evidence and rollback

1. Pin management connections to the intended machines independently of public DNS. On each target, back up its current password and ACL files with ownership and permissions. Compare against the exported baseline and reconcile any intervening edits. Generate secrets once in private storage. Use a gateway password that fits the installed V3 (30 ASCII characters were verified). Stage the two new password entries and ACL delta alongside existing accounts. Preserve each host's listener, certificates and persistence configuration. [V3 credential length evidence](mqtt-nginx-handoff.md).
2. Test on private CT 101 first while the old server serves clients. Reload Mosquitto after installing the files, verify the service and make fresh TLS connections. Use the private IP with the expected TLS name and staging trust. Apply the same tested delta to the old production server with privileged access, reload, and repeat against the old endpoint. Preserve existing users' authentication, telemetry uploads and monitoring delivery on both hosts.
3. On **each** broker use separate test client IDs, with the same wildcard subscription as G008. Publish a unique, non-retained marker that cannot decode as a radio packet. Verify delivery from the dispatch writer to the gateway reader. Verify the gateway can publish on its own uplink, cannot publish to dispatch, and receives no ordinary peer uplinks. Verify other gateway writers cannot publish to dispatch, the dispatch writer cannot publish elsewhere, and the worker can still archive traffic. Extend the six-account acceptance matrix with these two accounts and the exact topic. Record the target, UTC test time, private backup reference and pass/fail for each direction in the table above. Store credentials and hashes privately.
4. Once production permissions pass, change only G008 to its dedicated login. Keep `mqtt.snorr.org:8883`, encrypted protobuf and its saved channel settings. Verify reboot persistence and a fresh packet through `!9ea13cc0`. Portal software still needs to originate a valid encrypted shared-channel message. Use a distinct dispatch sender identity, since the firmware discards its own echoed packets. Confirm the text on a member radio before declaring two-way messaging ready. [Firmware MQTT handling](../../firmware/src/mqtt/MQTT.cpp).
5. At DNS cutover, keep the old broker operational. Existing MQTT sessions can stay on the old server while newly connected clients reach CT 101. A publication on one broker reaches clients connected there. Coordinate reconnects of G008, the worker, MeshMonitor and the dispatch publisher to CT 101, and verify fresh uplinks and a member-radio reply through the new endpoint. Check remaining gateways for fresh traffic on the new broker and monitor the old broker for stragglers. Keep the old endpoint and its working G008 policy available for rollback until migration is confirmed.

For a DNS rollback, return clients to the old endpoint and verify fresh traffic
there using the same credentials. For an ACL rollout failure, restore the
affected host's own pre-change files and reload. If G008 already uses the new
login, return it to its previous uplink credential before removing the new
account. Record each applied change or rollback against its specific host.

## Certificate and cutover handoff

In CT 101, install the production full chain at `/etc/mosquitto/certs/snorrmesh/fullchain.pem` and the matched private key at `/etc/mosquitto/certs/snorrmesh/privkey.pem`. Both must be readable by the service (root:mosquitto, mode 0640, parent 0750). After deploying the pair, run `systemctl reload mosquitto` and verify a fresh TLS connection using system trust, SNI and hostname verification for `mqtt.snorr.org`. The temporary staging certificate was self-signed. DNS, challenge choice, issuance and the tested renewal hook are handled separately.

After private acceptance and certificate handoff, enable the two WAN rules together. Verify public TLS from off-site, then fresh gateway traffic and receipt by both MeshLink and MeshMonitor through normal DNS. Retain the old broker and route for rollback. If cutover fails, disable both rules, clear their states and coordinate a DNS rollback. Keep the replacement private while investigating. Private firewall exports and the sanitized network validation are recorded in Home Infra under `docs/plans/snorrmesh-mosquitto-staging.md` and `diagnostics/2026-11-25-snorrmesh-private-stage.txt`.

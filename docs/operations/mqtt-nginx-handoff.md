# MQTT routing handoff for Mike Rollins

Prepared 2026-10-13. Mike handles certificates on Nginx. These are configuration templates; proxy/VM private addresses and certificate paths need substitution. No proxy or broker changes have been applied from this handoff.

2026-10-14 status update: public `mqtt.snorr.org:8883` now reaches Mosquitto through certificate-valid Nginx TLS. The broker retains loopback and listens on `192.168.12.51:1883`, with owner-reported UFW rules allowing only Nginx `192.168.12.254` before blanket 1883 denial. Anonymous/invalid public logins are correctly rejected. Earlier pending/hold statements below are historical; [current evidence](../../records/sites.md#broker-hosting-record--mike-rollins) supersedes them. Owner-run valid-account synthetic publish/subscribe/ACL checks through public TLS pass; device reconnect remains to test.

## Intended connection

```text
Pilot gateways / home ingestion worker
         ↓ MQTT over TLS, public TCP 8883
Mike's Nginx (terminates TLS, owns certificate)
         ↓ MQTT TCP, private port 1883
MQTT VM / Mosquitto (accounts, topic ACLs, persistence)
```

| Port | Role | Access |
| --- | --- | --- |
| 8883 | Nginx public MQTT TLS listener | Pilot clients and home worker |
| 1883 | Mosquitto private MQTT backend | Only Nginx's private source address; no public router forwarding |
| SSH | Existing administrator access | Preserve external 64582 → VM 22 mapping |

Current intended endpoint is `mqtt.snorr.org`; Mike is updating DNS/proxy routing. `mqtt.spp.lol` is the inspected legacy endpoint. Infrastructure completion is unverified and owner has put broker work on hold until Mike is ready. DNS points to the Nginx public endpoint (A or CNAME), with DNS-only if using ordinary Cloudflare DNS. MQTT clients use that hostname, port 8883, TLS enabled, and their own broker username/password. HTTP proxy-host configuration alone does not proxy MQTT TCP.

## Nginx configuration

Requires loaded stream and stream SSL support. On a separate Nginx host, replace `MQTT_VM_PRIVATE_IP` and certificate paths with Mike's actual values. Merge into the existing top-level `stream` block, outside `http`; do not add a duplicate block/listener.

```nginx
stream {
    server {
        listen 8883 ssl;
        # Add listen [::]:8883 ssl only if IPv6 routing is configured too.

        ssl_certificate     /PATH/TO/FULLCHAIN.pem;
        ssl_certificate_key /PATH/TO/PRIVATEKEY.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_session_cache shared:MQTT_TLS:10m;
        ssl_session_timeout 10m;

        proxy_pass MQTT_VM_PRIVATE_IP:1883;
        proxy_connect_timeout 10s;
        proxy_timeout 1h;
        proxy_socket_keepalive on;
    }
}
```

Router/firewall forwards public TCP 8883 to Nginx. No public TCP 1883 listener/forward is needed. Do not add `proxy_ssl on` or PROXY protocol to this example: backend is ordinary MQTT TCP, and Mosquitto has not been configured to consume a PROXY header. In this setup, broker logs see Nginx's source IP. MQTT keepalive and reconnection must be tested with the actual firmware.

The backend hop carries plaintext MQTT credentials/messages. Use this only over a trusted private path; if the path crosses the internet or an untrusted network, use a VPN or encrypted upstream instead.

After merging and substituting values, on the Nginx host:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Certificate provisioning and renewal are Mike's responsibility and outside this handoff.

## Mosquitto VM configuration

Replace the existing TLS listener configuration; do not leave a conflicting/duplicate listener active. Preserve/create the pilot account and ACL files. For separate Nginx and MQTT VMs:

```conf
listener 1883 MQTT_VM_PRIVATE_IP
protocol mqtt
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl
```

Retain the existing main-file persistence/logging settings. Remove broker listener TLS directives (`certfile`, `keyfile`, `cafile`, `tls_version`, `require_certificate`) from this replacement listener. Mosquitto no longer needs the public certificate or a public 8883 listener in this layout. Archive the old broker-specific certificate deployment/renewal configuration as part of migration, leaving unrelated certificates/timers alone.

VM firewall permits TCP 1883 **only from Nginx's actual private source IP**. Preserve SSH access; remove obsolete direct broker public exposure only after new-route verification. If Nginx shares the MQTT VM, bind Mosquitto to `127.0.0.1:1883` and use `proxy_pass 127.0.0.1:1883`; no LAN 1883 access needed.

The fresh-reset installer `reset-mqtt-pilot.py` has now been adapted for private port 1883 with no broker-side certificate handling. Default listener is loopback-only until Nginx's private source IP is supplied. A LAN listener requires explicit bind/proxy arguments and verified active firewall rules before reset. Owner completed the reset on 2026-10-13; local auth/ACL checks passed and active loopback 1883 was independently verified. Separate-host Nginx access remains pending. Its archiving/accounts/ACL plan remains useful: old MQTT state is privately archived, separate credentials for the two V3 gateways and ingestion worker, root `snorr/pilot`, protobuf uplink only initially, worker read-only and command publishing denied pending designated-gateway integration. Archive/reset execution is confirmed; archived material remains private at `/root/meshlink-archive/mqtt-legacy-20261013T204408Z`.

## Verify before client cutover

- Nginx config passes; external 8883 presents Mike's certificate for the client hostname.
- Nginx can reach the VM's 1883; public 1883 is unavailable, and unrelated LAN clients cannot reach the private listener.
- New pilot accounts work through external 8883; anonymous and incorrect credentials fail; topic read/write restrictions hold.
- Actual gateway and worker reconnect after proxy/broker reload or scheduled VM reboot. Broker maintenance is enabled for daily updates around 03:00 Pacific and required-only reboots at 04:00 Pacific; Mike's proxy needs its own maintenance arrangements.
- Old MQTT state remains in a root-private archive; no raw tracks, keys, credentials or logs are put in Git.

Sources: [Nginx stream TLS](https://nginx.org/en/docs/stream/ngx_stream_ssl_module.html), [Nginx TCP proxy](https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html), [Mosquitto listeners/authentication](https://mosquitto.org/man/mosquitto-conf-5.html). Documentation checked; templates not validated against Mike's actual Nginx configuration. No outreach sent.

## Heltec connection settings

2026-10-14 hardware finding: pinned stock Meshtastic has a 32-byte MQTT password buffer (31 usable UTF-8 bytes), while the original fresh installer generated 48-character values. Valid software-client MQTT tests therefore did not establish device credential compatibility. The V3s reject that oversized configuration. [Guarded two-account fix](../../scripts/server/fit-v3-mqtt-passwords.py) is prepared/uploaded and passes isolated real-Mosquitto authentication, worker/ACL preservation, idempotency and rollback tests; owner sudo execution is complete. It generates 30-character gateway passwords, preserves worker/ACL/listeners, reloads the broker and makes an owner-private export. Fresh installer generation is corrected for future gateways. The owner-private export confirms both gateway replacements are 30 bytes; saved V3 credentials match privately and actual encrypted LoRa-to-MQTT fixtures pass all four member/gateway checks. Worker authentication continues to pass. [Pinned password bound](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/protobufs/meshtastic/module_config.options).

For the MQTT-enabled V3 backhauls: server address `mqtt.snorr.org:8883`, TLS enabled, per-gateway username/password and root `snorr/pilot`. The reviewed upstream Meshtastic MQTT implementation parses `hostname:port` and defaults to 8883 when TLS is enabled (1883 otherwise); these settings now pass saved-config and actual delivery checks on stock `2.7.26.54e0d8d`. No `https://` prefix. Heltecs use public Nginx 8883; private 1883 is only the proxy-to-broker hop. Member trackers still send over LoRa and do not all need Wi-Fi/MQTT. [Configuration docs](https://meshtastic.org/docs/configuration/module/mqtt/), [upstream parser/defaults](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp).

For the initial passive-tracking uplink bench, no additional broker configuration is identified. Existing `pilot-v3-uplink-1`/`pilot-v3-uplink-2` accounts may write `snorr/pilot/2/e/#`; `pilot-worker` may read it. First verify authenticated synthetic delivery and denied permissions over public TLS. Use channel uplink enabled, downlink disabled, JSON disabled and map reporting disabled for this protobuf tracking test; verify settings against the installed firmware. Portal-to-radio replies need a later narrowly scoped ACL change because current gateways cannot read and the worker cannot publish. MQTT transport readiness does not establish the simulation portal's real-packet ingestion readiness.

### Authenticated public delivery check

`scripts/server/check-mqtt-public.py` uses the protocol/ACL verification helpers from sibling `reset-mqtt-pilot.py` without invoking its reset function. Run **only the check script** with sudo on the broker; it reads root-private credentials, verifies TLS identity for `mqtt.snorr.org`, publishes non-retained synthetic fixtures, checks worker receipt and denied access, and prints status without passwords. It does not modify broker configuration.

Both files are uploaded under `/home/setheth/meshlink-mqtt-check/`. The broker-origin public-endpoint probe timed out; a possible router hairpin limitation is not confirmed. For this session a temporary reverse SSH relay binds only broker loopback `127.0.0.1:18884`, forwards via the external test host to public `mqtt.snorr.org:8883`, and preserves end-to-end TLS/certificate verification. Its credential-free probe passes. While that relay is active, run:

```bash
sudo python3 /home/setheth/meshlink-mqtt-check/check-mqtt-public.py --connect-host 127.0.0.1 --connect-port 18884
```

Share status output only. Owner-run authenticated execution passed on 2026-10-14. The relay was closed afterward; SSH confirms no 18884 listener remains, and Mosquitto remains active. Recreate a loopback-only relay before reusing this command. The relay is temporary, not deployed broker infrastructure. Without a relay, the script defaults to direct public DNS/8883 and requires a working broker-to-public route.

Security integration follow-up: the pinned stock build logs MQTT username/password in its direct connection log and calls `setInsecure()` in its direct TLS path. Device provisioning/status tests suppress serial debug logging and keep credential-bearing configurations private. Hardware delivery passes, but the validating worker subscriber does not establish certificate/hostname verification by the Heltecs. [Pinned source](https://github.com/meshtastic/firmware/blob/54e0d8d0ab2ff56b3a9ce967e53f79e49af560fb/src/mqtt/MQTT.cpp#L328).

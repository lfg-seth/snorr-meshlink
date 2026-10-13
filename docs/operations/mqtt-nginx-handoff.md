# MQTT routing handoff for Mike Rollins

Prepared 2026-10-13. Mike handles certificates on Nginx. These are configuration templates; proxy/VM private addresses and certificate paths need substitution. No proxy or broker changes have been applied from this handoff.

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

For the MQTT-enabled V3 backhauls under this proposed topology: server address `mqtt.spp.lol:8883`, TLS enabled, per-gateway username/password and root `snorr/pilot`. The reviewed upstream Meshtastic MQTT implementation parses `hostname:port` and defaults to 8883 when TLS is enabled (1883 otherwise); these settings require verification on the selected installed build. No `https://` prefix. Heltecs use public Nginx 8883; private 1883 is only the proxy-to-broker hop. Member trackers still send over LoRa and do not all need Wi-Fi/MQTT. [Configuration docs](https://meshtastic.org/docs/configuration/module/mqtt/), [upstream parser/defaults](https://github.com/meshtastic/firmware/blob/master/src/mqtt/MQTT.cpp).

Security integration follow-up: reviewed moving upstream source currently logs MQTT username/password in its connection log and calls `setInsecure()` in its direct TLS path. Inspect the pinned firmware before provisioning; avoid capturing/publishing credential-bearing serial logs and verify client certificate identity behavior. These are source findings, not evidence about flashed project boards.

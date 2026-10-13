# Nginx in front of the MQTT VM

Current direction, updated 2026-10-13: Mike handles TLS/certificates on Nginx. Use the [TLS-termination handoff](../operations/mqtt-nginx-handoff.md) for public 8883 → private 1883. The passthrough proposal below is earlier research, not the current requested setup. No deployment confirmed.

2026-10-13 — Owner asked about placing the VM behind Nginx and proxying TCP. This is a proposed configuration, not a selected topology or deployed proxy. The location/configuration/version of Mike's existing HTTP responder is not verified. The fresh-broker reset installer remains awaiting sudo execution.

Nginx proxies individual listeners, not an entire VM. Its stream module supports MQTT TCP/TLS passthrough, and its HTTP module can route HTTP-01 challenge requests. For a separate existing Nginx edge, keep the broker certificate and private key on the MQTT VM; Nginx forwards TLS bytes. MQTT authentication and topic ACLs remain broker responsibilities. This is ordinary Nginx TCP proxying, independent of the Cloudflare Tunnel adapter requirement.

## Recommended candidate: separate existing Nginx host

Use the actual private IP of the MQTT VM instead of the documentation-only address `192.0.2.10` below. Preserve existing Nginx configuration; merge these sections in the correct contexts. The stream module must be installed/loaded in the chosen Nginx build. Do not create a second conflicting stream block or duplicate HTTP server-name entry.

At the top level of `/etc/nginx/nginx.conf`, outside `http {}`:

```nginx
stream {
    server {
        listen 8883;
        # Add listen [::]:8883 only if exposing/forwarding IPv6 too.
        proxy_pass 192.0.2.10:8883;
        proxy_connect_timeout 10s;
        proxy_timeout 1h;
        proxy_socket_keepalive on;
    }
}
```

This is TLS passthrough: do not add `listen ... ssl`, `proxy_ssl on`, or PROXY protocol to this example. Mosquitto continues to terminate TLS. Its certificate must cover the hostname clients use; Nginx does not repair the expired certificate. Client MQTT keepalive must keep long-lived sessions active; idle disconnect/reconnect behavior needs testing. Broker sees Nginx's source address rather than the client's address under this simple setup.

Inside the existing `http {}` context, commonly through a site file included from it:

```nginx
server {
    listen 80;
    server_name mqtt.spp.lol;

    location ^~ /.well-known/acme-challenge/ {
        proxy_pass http://192.0.2.10:80;
        proxy_set_header Host $host;
    }

    location / {
        return 404;
    }
}
```

No URI suffix on proxy_pass: preserve the full ACME path. Certbot standalone on the MQTT VM listens on port 80 during validation; Nginx forwards the challenge there. The VM's private port 80 must be reachable from the proxy. Add a chosen replacement hostname only when DNS/control and a matching certificate migration are ready. Each name requested on the certificate needs its own correct HTTP challenge routing.

Router/public firewall directs TCP 8883 and 80 to the Nginx edge. Restrict the MQTT VM's broker/validation ports to the proxy source where appropriate; preserve administrator SSH separately. Existing SSH mapping remains unchanged unless separately planned/tested. For direct MQTT on a Cloudflare-managed DNS zone, use DNS-only for the MQTT endpoint unless a separately supported TCP proxy service is deliberately selected; ordinary HTTP proxying does not proxy arbitrary MQTT 8883.

After replacing addresses and reviewing current configuration:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Validate TCP 8883 and the correct public certificate, run Certbot renewal dry-run on the broker, then renewal/deploy-hook verification and MQTT authentication/ACL/reconnect tests. Keep the known working route until the replacement path is verified. No proxy installation, upstream address discovery, router change or privileged nginx test was performed here.

## Alternative: Nginx on the MQTT VM

Both cannot bind the same address/port. Nginx can listen publicly on 8883 and pass TLS to Mosquitto on `127.0.0.1:8884`; change the broker listener accordingly. If Nginx owns port 80 on this VM, current Certbot standalone cannot bind it. Switch to webroot validation (serve `/.well-known/acme-challenge/` from a Certbot webroot) or DNS validation, or deliberately configure a different standalone backend port. This requires changes to the reset/renewal plan before installation; don't paste the separate-edge example unchanged onto the broker VM.

For this small pilot, an already-operated separate proxy is useful when Mike wants centralized public routing. Installing another proxy on the broker VM adds a service without removing broker authentication/certificate/maintenance responsibilities. The current external broker endpoint can also remain directly routed.

Primary sources: [Nginx stream proxy](https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html), [stream context/build requirements](https://nginx.org/en/docs/stream/ngx_stream_core_module.html), [HTTP proxy_pass URI rules](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass), [Cloudflare supported proxy ports](https://developers.cloudflare.com/fundamentals/reference/network-ports/), [Certbot standalone/webroot](https://eff-certbot.readthedocs.io/en/stable/using.html).

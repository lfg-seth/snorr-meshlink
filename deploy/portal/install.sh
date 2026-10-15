#!/usr/bin/env bash
# Run as root from a source checkout on a fresh Ubuntu 24.04 LXC.
set -euo pipefail
cd "$(dirname "$0")/../.."
source_root="$PWD"
test "$(id -u)" -eq 0
test "$source_root" = /opt/meshlink
if test -f /etc/meshlink/mqtt.json || test -f /etc/systemd/system/meshlink-api.service.d/live.conf; then
  echo 'Live MQTT provisioning found; use docs/operations/live-mqtt.md rather than the simulation installer.' >&2
  exit 1
fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl nginx python3 sqlite3 unattended-upgrades
install -d -m 0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg -o /usr/share/keyrings/cloudflare-main.gpg
printf '%s\n' 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' > /etc/apt/sources.list.d/cloudflared.list
apt-get update
apt-get install -y cloudflared

# Match the frontend's existing exact runtime pin; validate the official checksum.
node_version="$(tr -d '\r\n' < .nvmrc)"
node_archive="node-v${node_version}-linux-x64.tar.xz"
if ! test -x "/opt/node-v${node_version}-linux-x64/bin/node"; then
  node_stage="$(mktemp -d)"
  curl -fsSL "https://nodejs.org/dist/v${node_version}/${node_archive}" -o "${node_stage}/${node_archive}"
  curl -fsSL "https://nodejs.org/dist/v${node_version}/SHASUMS256.txt" -o "${node_stage}/SHASUMS256.txt"
  (cd "$node_stage"; grep " ${node_archive}$" SHASUMS256.txt | sha256sum --check --strict -)
  tar -xJf "${node_stage}/${node_archive}" -C /opt
fi
export PATH="/opt/node-v${node_version}-linux-x64/bin:$PATH"
(cd portal; npm ci; npm run check)

id meshlink >/dev/null 2>&1 || useradd --system --home /var/lib/meshlink --shell /usr/sbin/nologin meshlink
id meshlink-worker >/dev/null 2>&1 || useradd --system --home /nonexistent --shell /usr/sbin/nologin meshlink-worker
install -d -o meshlink -g meshlink -m 0700 /var/lib/meshlink
install -d -m 0700 /var/backups/meshlink
install -d -m 0755 /etc/meshlink /opt/meshlink/local-data /var/www/meshlink
if test -e /opt/meshlink/local-data/backend && ! test -L /opt/meshlink/local-data/backend; then
  echo 'Existing non-symlink backend state found; migrate it explicitly before installing.' >&2
  exit 1
fi
ln -sfn /var/lib/meshlink /opt/meshlink/local-data/backend
runuser -u meshlink -- python3 backend/manage.py install
if ! test -f /var/lib/meshlink/credentials.json && ! test -f /var/lib/meshlink/pb_data/data.db; then
  runuser -u meshlink -- python3 backend/manage.py init-demo
fi
test -f /var/lib/meshlink/credentials.json
test -f /var/lib/meshlink/pb_data/data.db
cp -a portal/dist/. /var/www/meshlink/
chown -R root:root /var/www/meshlink
chmod -R a+rX /var/www/meshlink
install -m 0644 deploy/portal/meshlink-api.service deploy/portal/meshlink-worker.service deploy/portal/meshlink-backup.service deploy/portal/meshlink-backup.timer /etc/systemd/system/
install -m 0755 deploy/portal/backup.py /usr/local/sbin/meshlink-backup
install -m 0644 deploy/portal/nginx.conf /etc/nginx/sites-available/meshlink
ln -sfn /etc/nginx/sites-available/meshlink /etc/nginx/sites-enabled/meshlink
if test -L /etc/nginx/sites-enabled/default; then
  unlink /etc/nginx/sites-enabled/default
fi
install -d -m 0700 /etc/cloudflared
# Ubuntu security updates; no automatic container reboot or release upgrade.
printf '%s\n' 'APT::Periodic::Update-Package-Lists "1";' 'APT::Periodic::Unattended-Upgrade "1";' > /etc/apt/apt.conf.d/20auto-upgrades
printf '%s\n' 'Unattended-Upgrade::Automatic-Reboot "false";' > /etc/apt/apt.conf.d/52meshlink
nginx -t
systemctl daemon-reload
systemctl enable --now meshlink-api.service meshlink-backup.timer nginx.service
systemctl reload nginx
curl --retry 10 --retry-connrefused --retry-delay 1 -fsS http://127.0.0.1:8090/api/health
python3 deploy/portal/configure.py
systemctl enable --now meshlink-worker.service
curl -fsS http://127.0.0.1:8080/ >/dev/null
systemctl start meshlink-backup.service
echo 'Portal installed with fictional data. Configure a Cloudflare route to http://127.0.0.1:8080.'

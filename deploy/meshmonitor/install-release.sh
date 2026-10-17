#!/bin/sh
# Fresh existing Ubuntu LXC only; do not unpack the template's OS over the host.
set -eu
base=/root/meshmonitor-install
archive="$base/meshmonitor-4.17.0-amd64.tar.gz"
test "$(id -u)" = 0
test ! -e /opt/meshmonitor
echo "697797ce1aab702eca1a070c878f5c801a82fbd5a2fc9efb6e203cc8282bd03a  $archive" | sha256sum -c -
test -x "$base/stage/usr/bin/node"
test -f "$base/stage/opt/meshmonitor/dist/server/server.js"
id meshmonitor >/dev/null 2>&1 || useradd --system --home-dir /data --shell /usr/sbin/nologin meshmonitor
install -d -m 755 /opt/meshmonitor-runtime
install -m 755 "$base/stage/usr/bin/node" /opt/meshmonitor-runtime/node
cp -a "$base/stage/opt/meshmonitor" /opt/meshmonitor
chown -R root:root /opt/meshmonitor
install -d -m 700 -o meshmonitor -g meshmonitor /data
install -d -m 750 -o root -g meshmonitor /etc/meshmonitor
python3 "$base/config/patch-release.py" /opt/meshmonitor
for file in dist/services/database.js dist/server/server.js dist/server/services/mqttPacketLogService.js dist/server/services/coverageRetentionService.js dist/server/services/meshcorePositionHistoryService.js; do
    /opt/meshmonitor-runtime/node --check "/opt/meshmonitor/$file"
done
python3 - <<'PY'
from pathlib import Path
import secrets
p = Path('/etc/meshmonitor/meshmonitor.env')
assert not p.exists()
p.write_text('''NODE_ENV=production
PORT=3001
DATABASE_PATH=/data/meshmonitor.db
DISABLE_ANONYMOUS=true
COOKIE_SECURE=false
COOKIE_SAMESITE=strict
TRUST_PROXY=false
ALLOWED_ORIGINS=http://meshmonitor.int.spp.lol:3001
ACCESS_LOG_ENABLED=false
LOG_LEVEL=warn
MESHLINK_RETAIN_HISTORY=true
MESHLINK_BIND_ADDRESS=127.0.0.1
CUSTOM_TITLE=SNORR MeshMonitor
SESSION_SECRET=''' + secrets.token_hex(32) + '\n')
p.chmod(0o640)
PY
chown root:meshmonitor /etc/meshmonitor/meshmonitor.env
install -m 644 "$base/config/meshmonitor.service" /etc/systemd/system/meshmonitor.service
systemctl daemon-reload
systemctl enable --now meshmonitor

#!/usr/bin/env bash
# Configure same-release Ubuntu updates and a timezone-aware reboot window.
set -euo pipefail
[[ ${EUID} -eq 0 ]] || { echo 'Run with sudo on the MQTT server.' >&2; exit 1; }
reboot_time=${1:-04:00}
reboot_zone=${2:-America/Los_Angeles}
[[ $reboot_time =~ ^([01][0-9]|2[0-3]):[0-5][0-9]$ ]] || { echo 'Use HH:MM.' >&2; exit 1; }
[[ $reboot_zone =~ ^[A-Za-z_]+(/[A-Za-z_]+)+$ && -f /usr/share/zoneinfo/$reboot_zone ]] || { echo 'Use a valid named timezone.' >&2; exit 1; }
update_time=$(python3 - "$reboot_time" <<'PY'
import sys
h,m=map(int,sys.argv[1].split(':'))
t=(h*60+m-60)%(24*60)
print(f'{t//60:02d}:{t%60:02d}')
PY
)
systemd-analyze calendar "*-*-* $reboot_time:00 $reboot_zone" >/dev/null
stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup_dir="/root/meshlink-maintenance/auto-${stamp}"
umask 077
install -d -m 0700 "$backup_dir"
tar -C / -czf "$backup_dir/config-before.tgz" etc/apt/apt.conf.d etc/systemd/system
cat > /etc/apt/apt.conf.d/99meshlink-auto-updates <<'CONF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
Unattended-Upgrade::Allowed-Origins:: "${distro_id}:${distro_codename}-updates";
// Reboots are handled only by the scheduled MeshLink timer.
Unattended-Upgrade::Automatic-Reboot "false";
CONF
chmod 0644 /etc/apt/apt.conf.d/99meshlink-auto-updates
install -d -m 0755 /etc/systemd/system/apt-daily-upgrade.timer.d
cat > /etc/systemd/system/apt-daily-upgrade.timer.d/meshlink-window.conf <<CONF
[Timer]
OnCalendar=
OnCalendar=*-*-* ${update_time}:00 ${reboot_zone}
RandomizedDelaySec=10m
CONF
cat > /etc/systemd/system/meshlink-maintenance-reboot.service <<'CONF'
[Unit]
Description=Reboot the MQTT host only when updates require it
ConditionPathExists=/var/run/reboot-required
[Service]
Type=oneshot
# Skip this day's reboot if package maintenance is still running.
ExecCondition=/bin/sh -c '! /usr/bin/systemctl is-active --quiet apt-daily.service apt-daily-upgrade.service'
ExecStart=/usr/bin/systemctl --no-block reboot
CONF
cat > /etc/systemd/system/meshlink-maintenance-reboot.timer <<CONF
[Unit]
Description=MQTT host maintenance reboot window
[Timer]
OnCalendar=*-*-* ${reboot_time}:00 ${reboot_zone}
AccuracySec=1m
RandomizedDelaySec=0
Persistent=false
[Install]
WantedBy=timers.target
CONF
chmod 0644 /etc/systemd/system/apt-daily-upgrade.timer.d/meshlink-window.conf /etc/systemd/system/meshlink-maintenance-reboot.{service,timer}
apt-config dump >/dev/null
systemd-analyze verify /etc/systemd/system/meshlink-maintenance-reboot.service /etc/systemd/system/meshlink-maintenance-reboot.timer
systemctl daemon-reload
systemctl enable --now apt-daily.timer apt-daily-upgrade.timer
systemctl restart apt-daily-upgrade.timer
systemctl enable --now meshlink-maintenance-reboot.timer
printf '\nUpdate time: %s %s; reboot window: %s %s (only when required).\n' "$update_time" "$reboot_zone" "$reboot_time" "$reboot_zone"
echo 'A logged-in session will not prevent this scheduled reboot.'
echo 'Missed reboot windows are not caught up at startup. Busy package maintenance skips the reboot.'
echo "Private rollback configuration archive: $backup_dir/config-before.tgz"
systemctl list-timers --all --no-pager apt-daily.timer apt-daily-upgrade.timer meshlink-maintenance-reboot.timer

#!/usr/bin/env bash
# Run on Mike's existing Ubuntu MQTT host with sudo. No secrets are printed.
set -euo pipefail
if [[ ${EUID} -ne 0 ]]; then
  echo 'Run this script with sudo on the MQTT server.' >&2
  exit 1
fi
umask 077
stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup_dir="/root/meshlink-maintenance/${stamp}"
install -d -m 0700 "$backup_dir"
/usr/sbin/sshd -t
backup_paths=(etc/mosquitto etc/ssh etc/apt/apt.conf.d)
for optional in etc/letsencrypt etc/ufw etc/systemd/system; do
  [[ ! -d "/$optional" ]] || backup_paths+=("$optional")
done
tar -C / -czf "$backup_dir/config-before.tgz" "${backup_paths[@]}"
echo "Private configuration backup: $backup_dir/config-before.tgz"
echo 'This archive contains secrets; keep it on the server and out of Git.'
apt-get update
apt-get --no-remove upgrade
/usr/sbin/sshd -t
systemctl is-active mosquitto
systemctl is-active ssh
printf '\nInstalled broker and SSH packages:\n'
dpkg-query -W mosquitto openssh-server certbot
printf '\nListening ports:\n'
ss -lnt
if [[ -f /var/run/reboot-required ]]; then
  echo 'Reboot required. No reboot performed; arrange it with Mike and verify reconnection afterward.'
fi
echo 'OS update step complete. TLS renewal, topic ACLs, firewall review and integration tests remain.'

#!/usr/bin/env bash
set -euo pipefail

# Persistent access for this workstation's owner to project radio USB interfaces.
# Run once with sudo; no world-writable ports or passwordless sudo grants.
[[ ${EUID} -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
[[ $(id -u setheth) == 1000 ]] || { echo 'Unexpected bench account.' >&2; exit 1; }
acl=$(command -v setfacl)
command -v udevadm >/dev/null
rule=/etc/udev/rules.d/99-snorr-usb-serial.rules
[[ ! -L ${rule} ]] || { echo 'Refusing symlink rule path.' >&2; exit 1; }
install -d -m 0755 /etc/udev/rules.d
tmp=$(mktemp /etc/udev/rules.d/.snorr-usb-serial.XXXXXX)
trap 'rm -f "$tmp"' EXIT
cat > "$tmp" <<RULES
# Owner-authorized radio serial access for SNORR bench work.
# RAK4631 application USB; ESP32-S3 native USB; Heltec CP210x bridge.
ACTION=="add|change", SUBSYSTEM=="tty", ATTRS{idVendor}=="239a", ATTRS{idProduct}=="8029", RUN+="$acl -m u:setheth:rw /dev/%k"
ACTION=="add|change", SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", RUN+="$acl -m u:setheth:rw /dev/%k"
ACTION=="add|change", SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", RUN+="$acl -m u:setheth:rw /dev/%k"
RULES
chmod 0644 "$tmp"
chown root:root "$tmp"
mv -f "$tmp" "$rule"
udevadm control --reload-rules
for port in /sys/class/tty/ttyACM* /sys/class/tty/ttyUSB*; do
    [[ -e ${port} ]] || continue
    udevadm trigger --action=change "$port"
done
udevadm settle --timeout=10
echo 'Persistent radio serial access installed for setheth (239a:8029, 303a:1001, 10c4:ea60).'
echo 'Applies now and after USB reconnects, device reboots and host reboots.'
echo 'Remove /etc/udev/rules.d/99-snorr-usb-serial.rules and reload udev to stop future grants.'
echo 'Existing grants last until unplugged; no group or sudo policy changes made.'

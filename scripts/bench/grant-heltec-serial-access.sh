#!/usr/bin/env bash
set -euo pipefail

# Runtime-only ACL rules for the connected bench units and missing V4 serial.
[[ ${EUID} -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
[[ $(id -u setheth) == 1000 ]] || { echo 'Unexpected bench account.' >&2; exit 1; }
command -v setfacl >/dev/null
command -v udevadm >/dev/null
rule=/run/udev/rules.d/99-snorr-heltec-bench.rules
[[ ! -L ${rule} ]] || { echo 'Refusing symlink rule path.' >&2; exit 1; }
install -d -m 0755 /run/udev/rules.d
cat > "${rule}" <<'RULES'
ACTION=="add|change", SUBSYSTEM=="tty", ATTRS{serial}=="9070699CA878", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", RUN+="/usr/bin/setfacl -m u:setheth:rw /dev/%k"
ACTION=="add|change", SUBSYSTEM=="tty", ATTRS{serial}=="90:70:69:9C:A8:78", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", RUN+="/usr/bin/setfacl -m u:setheth:rw /dev/%k"
ACTION=="add|change", SUBSYSTEM=="tty", KERNELS=="1-1.3.3.4", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", RUN+="/usr/bin/setfacl -m u:setheth:rw /dev/%k"
ACTION=="add|change", SUBSYSTEM=="tty", KERNELS=="1-1.3.3.2", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", RUN+="/usr/bin/setfacl -m u:setheth:rw /dev/%k"
ACTION=="add|change", SUBSYSTEM=="tty", KERNELS=="1-1.3.3.3", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", RUN+="/usr/bin/setfacl -m u:setheth:rw /dev/%k"
RULES
chmod 0644 "${rule}"
udevadm control --reload-rules
for port in /sys/class/tty/ttyACM* /sys/class/tty/ttyUSB*; do
    [[ -e ${port} ]] || continue
    udevadm trigger --action=change "${port}"
done
udevadm settle --timeout=10
echo 'Bench serial ACL rules active until reboot; limited to the three observed hub sockets and missing V4 serial.'
echo 'Remove reset rules: sudo rm /run/udev/rules.d/99-snorr-heltec-bench.rules; sudo udevadm control --reload-rules'
echo 'Existing ACL grants then last until unplugged; reboot removes both rules and device-node grants.'

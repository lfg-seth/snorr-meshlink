# R011 Angel Peak Mountain Side - 2026-11-15

Owner selects **R011 / Case 6**, retaining its assembly/configuration, for
**Angel Peak Mountain Side** at a newly supplied exact pin. This is a new
site assignment after R005 replaces it on the Vegas side. R005 remains at
Vegas Side. Exact coordinates and complete profiles remain private.

Assembly: **eight cells, Muzi antenna**; existing Case 6 intake is **v4 ASA,
one SMA port, two 200 mA panels, two four-cell parallel holders**. No new
purchase, cell-capacity, wiring or measured panel-output inference.

## Saved profile

Selected USB **70DF102F58D2A034**, radio **!8737c2c9**, hardware
**34a0d2582f10df70c9c237879e77e47a**, RAK4631/former REF1. The fresh backup confirms installed
**2.7.26.bcb22e0**. Retained without flashing, factory reset or key replacement.

Preserved **ROUTER**, own keys/admin allowlist, channels/names, LOCAL_ONLY,
US/LongFast slot 35, TX enabled at 10 dBm, hop 3, disabled power saving,
Bluetooth/network and GPS mode/pins. Saved the new fixed coordinates as integer
degrees × 10^7 without inventing altitude. Kept enabled device/environment/
power **180-second** settings, saved-baseline SNNS, **21,600-second** standard
NeighborInfo and this board's original **900-second smart-position** settings.

Enabled **`lora.config_ok_to_mqtt=true`**, correcting the retained
former-reference restriction diagnosed on the Vegas-side assignment.
[Diagnosis and prior evidence](r011-telemetry-diagnosis.md). A matching private
channel is insufficient when the gateway's public-address broker gate withholds
packets lacking the sender's permission bit. Do not change gateway settings or
MQTT downlinks. This does not itself prove actual report delivery.

The station lease and identity guards precede all writes. Complete intended
local/module/channel bytes, owner/identity, firmware metadata and exact integer
coordinates pass independent readback before and after one explicit reboot.
An additional comparison confirms MQTT permission is the only local-config
byte change; module/channel/owner bytes are unchanged. Fixed coordinates are
checked separately. The existing dashboard cadence baseline matches the saved
profile. Serial closes successfully; the board is ready to unplug.
Private commands and evidence: `private/bench/R011-mountain-20261115/`.

Initial reads time out because USB presents **239a:0029 / WisBlock / nRF UF2**,
the bootloader rather than Meshtastic. Owner grants temporary serial ACL and
presses RESET once; application **239a:8029 / WisCore** responds with the expected
identity/firmware. No flashing is needed. The first post-write API read times
out; explicit DTR asserted / RTS deasserted succeeds without resending settings.
One explicit reboot follows the complete intended-profile pass.

## Delivery and field limits

New ordinary R011 reports remain **unverified**: direct SSH to the CLI server
times out. The prior temporary tailnet wrapper/active monitor is absent after
the laptop environment changes, and the router SSH host-key check fails. No
host-key check is bypassed or production service changed. Re-establish the
existing trusted monitoring route, then check reports later than this write.
Exclude cached B003 metrics, old site history and PKI request replies. Avoid a survey ping while awaiting reporting:
the retained survey responder's 900-second quiet window can renew on reboot.
Sensor function, all-gateway reception, sustained cadence, mount/installation,
forced relay, coverage and runtime remain separate gates.

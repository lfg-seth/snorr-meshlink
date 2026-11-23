# R011 Angel Peak Mountain Side - 2026-11-15

**Publication update, 2026-11-15:** owner approves publishing the exact fixed
location in the [deployment table](../../records/sites.md#2026-11-15---published-deployment-setup-and-fixed-locations). Earlier privacy wording below describes the original evidence handling;
complete profiles and raw logs remain ignored.

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

## 2026-11-23 receiver-gain audit

R011 is the only numbered RAK with SX126x boosted receive gain recorded off.
Its November 15 pre-deployment backup already had the field off, with the
former REF1 zero-hop profile. The conversion updated the hop limit and
preserved gain. Full-profile verification used that preserved value as its
expected value. The Mountain Side reboot readback confirms it remained off.
The records establish when it was already off. The original reason for
choosing that setting is unknown.

| RX boost | Radios | Evidence |
| --- | --- | --- |
| Off | R011 | Decoded deployment backup and Mountain Side reboot readback |
| On | R001, R005, R006, R008, R009, R010 | Decoded November 15–21 deployment readbacks by physical identity |
| On | R002, R003, R004, R007 | [November 12 batch verification](rak-batch-20261112.md#firmware-and-profile-evidence) records boosted RX and post-reboot comparisons for all eight boards in that batch. R003 remains held for separate RF/USB failures. |
| On | Laptop USB SURV, member B003, G002 Lee Fire replacement | November 21–23 saved profiles matched by physical hardware |

The seven deployment readbacks share US LongFast, slot 35, TX enabled at
10 dBm, hop limit 3 and the same private primary channel key. Six have
identical decoded LoRa settings. R011 also has `ignore_mqtt=false` while the
other six have it true. That field filters packets marked as coming via
MQTT. R011's telemetry upload permission is true. The third LoRa difference
is the saved external FEM LNA enum. The RAK4631 survey build has no
controllable external FEM. The SX1262 driver applies the separate RX boost
flag directly. These are saved-state findings. A current live read of every
gateway and member was outside this comparison.

With boost off, weak incoming member positions, relay traffic or survey
pings can fall below R011's decoding threshold. Its configured transmit
power and survey deadline are independent. Semtech specifies a small
sensitivity improvement for added receive current. Its 125 kHz LoRa
DC-DC example rises from 4.6 to 5.3 mA at the chip. Actual battery draw
and delivery improvement at this 250 kHz site are unmeasured.
[Semtech SX1261/2 datasheet, tables 3-5 and 9-3](https://w2.electrodragon.com/Chip-dat/SemTech-dat/SX1262-dat/DS_SX1261_2%20V2-2.pdf),
[Meshtastic setting](https://meshtastic.org/docs/configuration/radio/lora/#sx126x-rx-boosted-gain).

At the next R011 service, compare repeated pings from a fixed position before
and after enabling boost, holding the antenna, transmit power and timeout
constant. Verify the new setting after reboot. Today's audit was read-only.
[Angel Peak drive evidence](../../records/field-results.md#2026-11-23---laptop-usb-survey-contact-with-angel-peak).

# R003 / R008 / R010 repair retest - 2026-11-12

The owner reconnects these three boards and confirms R010 has been solder
reworked. **R008 and R010 now pass**; R003 remains held. Current board-level
passes are **R001, R002, R004, R005, R006, R007, R008, R009 and R010**.
Every staged unit remains **CLIENT / 2.7.26.4c96b9b**. Final assembly/site,
ROUTER plus cadence readback and forced-relay/end-to-end acceptance remain.

| Label | Physical identity | Firmware/settings | Sensors | Radio / outcome |
| --- | --- | --- | --- | --- |
| **R008 / SNORR Repeater 008** | **!120b04fd**; USB **F4D0968336047CA0**; hardware `a07c04368396d0f4fd040b12638298d4` | Complete original backup from 2.7.17.36133d29d / ROUTER; switch CLIENT before update, verified application-only 4c96b9b upgrade, preserved own keys, full explicit-reboot profile pass | INA219 CH1 **4.236 V / -0.2 mA**; temperature **21.240044 C**, RH **37.104225%** | **3/3 TX, 3/3 RX**; board bench pass |
| **R010 / SNORR Repeater 010** | **!77fdb9f1**; USB **820C9B4F0C2D7675** | Retain pinned firmware; complete saved profile/keys match after physical rework and power cycle | INA219 CH1 now **4.2 V / -0.3 mA**; temperature **21.810532 C**, RH **32.070827%** | **3/3 TX, 3/3 RX**; solder hold cleared by readings and direct RF |
| **R003 / SNORR Repeater 003** | **!b4d6bc9f**; USB **1E1F729F05162A2E** | Retain firmware/keys/settings; fresh complete profile matches intended CLIENT | INA219 CH1 **4.256 V / -0.2 mA** received after cable swap; AHT21 not detected/unverified | Initial retest loses USB before RX; cable-only comparison stays connected but yields **0/3 TX, 0/3 RX**. **HOLD** |

These are sensor/report observations on the current USB-powered boards, not
battery, shunt calibration or final power-path measurements. Sensor source
times remain uptime-like/unknown UTC. Both temperature and humidity are
required for AHT21 detection; finite CH1 voltage/current are required for the
INA power-report result. Zero and signed currents are preserved.

## Method and R003 limits

Stop the verified label watcher and acquire its OS lease before board access.
Only these three deployment RAKs and REF1 are enumerated; the gateway is never
opened. Take R008's previously unavailable complete original backup before any
write. It arrives in ROUTER mode: change CLIENT before updating. Apply the
same private channel, US/LONG_FAST/slot 35/10 dBm, boosted RX, hop 3, B002 admin,
180-second device/environment/power and saved-baseline SNNS profile, disabled
MQTT/uplink/downlinks and cleared old fixed location as the other fresh units.
Full identity/owner/local/module/channel/metadata and own-key comparison passes
through explicit reboot. No reset, rebuild or key replacement. The verified
[image and prior run](rak-batch-20261112.md) retain the recovery inputs.

Each direct RF check opens only the selected board plus REF1. Keep version-2
random-payload/packet-ID/source/receiving-interface matching, zero-hop TEXT
broadcast, three attempts per direction, **5-second gap / 4-second deadline**.
Local echoes and acknowledgements do not count. All test handles close.

R003's initial retest completes three unsuccessful TX attempts, then the host
guard stops before RX: R003's connection event is clear, reader thread dead,
and serial stream closed; REF1 remains connected. The log again contains
`ClearCommError` / Windows error 22. The owner swaps only its USB cable with a
known-working one, keeping its computer/hub socket. In that comparison both
interfaces remain connected, reader-alive and stream-open throughout all six
attempts, but no current probe is observed at the intended receiver. INA power
returns over USB. The cable change removes the observed disconnect in this
bounded run; it does not clear RF acceptance.

With R003's USB session closed, REF1 sends fresh device and power telemetry
requests, each with an **8-second deadline**. Neither produces a reply matching
R003's source, current request ID, telemetry port and requested variant. Keep
this distinct from the six-packet test. Earlier queued test packets received
at R003 show previous RF reception, not successful current probe receipts.

Saved R003 LoRa and all eight channel records are byte-identical to passing
R004/R006; its security settings excluding its own keys also match R004.
Only own identity/keys and inactive RGB defaults distinguish its complete
profile from R004. No configuration repair or speculative firmware flash is
justified by that comparison. USB, reset/power and RF-path causes remain
unisolated; no permanent hardware-damage verdict is made. The owner explicitly
sets R003 aside after these checks. Further diagnosis waits for owner selection;
antenna, core/carrier seating and connections need inspection before another
bounded retest. It is excluded from Sunday's accepted pile.

Private evidence beneath `private/bench/rak-batch-20261113T034943Z/`:
`F4D0968336047CA0/before.json`, its intended/saved/reboot profiles, acceptance
runs `20261113T052314127775Z` (R010), `20261113T052405908116Z` (R008),
`20261113T052454807138Z` (R003 USB failure), `20261113T052933760103Z`
(R003 cable comparison), and `r003-usb-closed-*.json`. Eleven distinct
public/private key pairs (ten staged deployment boards plus REF1) pass
offline X25519 pair mathematics and uniqueness checks; values remain private.

This supersedes the earlier R008/R010 holds in the
[initial batch record](rak-batch-20261112.md), preserving every earlier failure.
[Current physical roster](../../records/deployment-nodes.md).

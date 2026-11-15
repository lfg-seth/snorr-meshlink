# Direct-hop queue delay and preset comparison, 2026-11-14

Across eight completed short, collocated trials, **ShortFast with a 2-second timeout sent the most PINGs** (47.99/min). **ShortFast with a 2-second timeout returned the most confirmed round trips** (35.99/min). All three RAKs returned confirmed replies in every completed run. The owner stopped the final MediumFast/two-second trial after 34.92 seconds. It logged 21 on-air PINGs and six confirmations, returned idle, and is excluded from the ranking.

## LongFast slot comparison

The four boards first used slot 35, then slot 61, then slot 35 again. Slot 61 had zero decoded outside packets during its 60-second passive observation and four-minute survey. Both slot-35 control runs also had zero outside decodes in either period. Queue delay on slot 61 fell between the two observations on slot 35 at both the median and the 95th percentile. The largest individual delay in this comparison, 2,102 ms, occurred on slot 61. The experiment showed no consistent advantage from moving slots under these conditions.

## Measurements

| Preset | Slot | Response timeout | Polling time | Actual PINGs | Confirmed | PINGs/min | Confirmed/min | Queue median / p95 / max (ms) | Median PING airtime (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LongFast | 35 | 5 s | 240 s | 62 | 27 | 15.49 | 6.75 | 271 / 678 / 1553 | 764 |
| LongFast | 61 | 5 s | 240 s | 73 | 51 | 18.25 | 12.75 | 333 / 890 / 2102 | 764 |
| LongFast | 35 | 5 s | 240 s | 77 | 57 | 19.25 | 14.25 | 363 / 957 / 1737 | 764 |
| MediumFast | 35 | 5 s | 240 s | 150 | 128 | 37.49 | 32.00 | 121 / 328 / 589 | 221 |
| ShortFast | 35 | 5 s | 240 s | 108 | 75 | 27.00 | 18.75 | 84.5 / 104 / 124 | 68 |
| ShortTurbo | 35 | 5 s | 240 s | 132 | 105 | 32.99 | 26.24 | 77 / 103 / 139 | 34 |
| ShortTurbo | 35 | 2 s | 180 s | 134 | 88 | 44.64 | 29.31 | 73.5 / 102 / 139 | 34 |
| ShortFast | 35 | 2 s | 180 s | 144 | 108 | 47.99 | 35.99 | 78 / 103 / 110 | 68 |

## Method and interpretation

The original GPS Heltec V4 polled the same three RAK responders in round-robin order on published survey firmware `2.7.26.bcb22e0`. Each trial began with a 60-second passive observation on all four devices. The minimum attempt interval was 1,000 ms with fixed pacing, one outstanding PING, US region and 10 dBm throughout. Slot tests and the first preset sweep used four minutes of polling and a five-second response timeout. The two-second-timeout sweep scheduled three minutes per preset. ShortTurbo and ShortFast completed that window. Each rate uses the actual measured polling duration. Failed attempts hold up the next PING until the deadline. Thus both the modem and timeout affect throughput.

Queue delay is enqueue to actual client TX start on one firmware clock. On-air PINGs were counted by unique locally transmitted packet ID. Confirmations count a matching PONG accepted by the client. The raw-log audit reproduced every reported TX and success count. An initial adapter handshake can report an event gap before the polling window. During the five-second MediumFast trial one client event sequence number was missing. All 150 on-air requests still had matched attempt and queue timestamps. The logs cannot identify what the missing event contained.

For the US firmware configuration, LongFast, MediumFast and ShortFast used 250 kHz bandwidth. Slot 35 therefore centered on 910.625 MHz and slot 61 on 917.125 MHz. ShortTurbo used 500 kHz bandwidth, so its numeric slot 35 centered on 919.250 MHz. Fewer milliseconds on air improved latency, while missed replies and their timeout cost affected the rate of usable samples. These are bench observations; a time-ordered, single run per setting does not establish outdoor range or a universal ranking. A quiet observation means no outside Meshtastic packet was decoded; other RF activity can still be present.

## Recovery and evidence

All four were verified on LongFast slot 35 before the preset comparisons and again at final handoff. Fresh native USB readbacks matched the baseline hardware identities, owner identities, full local and module configurations and all channel slots. The survey client acknowledged stop at each trial. The final hardware profile is US LongFast, slot 35, 10 dBm, TX enabled on all four. Each station session closed its USB handles and released the watcher lease.

The private survey worktree evidence directory is `private/bench/slot-compare-20261114-2035/`. Each labeled trial contains its four board logs, measured `summary.json` and packet-count `audit.json`. Original and restored per-board profiles stay private. [Earlier shared-channel soak](survey-firmware-20261114.md#owner-stopped-adaptive-soak).

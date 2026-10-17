# B001 channel-utilization diagnostic — 2026-10-16

Owner reports **58% on a gateway OLED and a client OLED** after connecting a Heltec V4. The original spike was not captured; its exact cause remains unconfirmed. Subsequent live evidence shows substantial redundant router traffic.

## Readout

Identify COM5 as member tracker **B001**, original HELTEC_V4, stock `2.7.26.54e0d8d`, CLIENT role. Capture serial debug lines, protocol events and local-destination statistics for approximately 3.4 minutes. No flash, reboot, saved configuration write, broadcast diagnostic request or gateway change. Close serial access afterward. Historical startup/node-database packets are excluded from fresh statistics.

| Measurement | Fresh observation |
| --- | --- |
| Channel utilization samples | 4.00%, 4.81%, 0%, 13.74%, 8.09% |
| B001 transmit utilization | 0.515–0.535% over its separate hour window |
| RF transmissions | 2, both B001 position packets; 722 ms each |
| RF receptions | 19; 16 counted as duplicates (84%) |
| New bad receptions | 0; cumulative counter remains 3 |
| B001 relays transmitted | 0; three pending relays canceled |
| Logged valid receive airtime | 14,546 ms |
| Logged noise/error airtime entries | None in this capture |

The first position transmission returns as three copies of the same packet through relay suffixes matching **R004, R003 and R005**. The second returns as four copies matching **R001, R005, R003 and R004**. These are last-hop suffix matches to the saved node database, not cryptographic relay attribution. R005 environment, power and private-port reports each arrive directly and through three routers. B001 suppresses its pending forwards after hearing duplicates, as expected for CLIENT.

## Interpretation and limits

The firmware calculates channel utilization from six ten-second buckets, adding transmit, valid receive and failed/malformed receive airtime. Duplicate suppression happens after RF airtime is counted. The OLED displays this local rolling utilization, while transmit utilization uses an hour window; the two percentages cannot be subtracted to calculate receive utilization. See local source [airtime.cpp](../../firmware/src/airtime.cpp), [airtime.h](../../firmware/src/airtime.h), [receive accounting](../../firmware/src/mesh/RadioLibInterface.cpp) and [OLED rendering](../../firmware/src/graphics/draw/DebugRenderer.cpp).

One 722 ms position plus three equivalent repeats occupies 2.888 seconds, or **4.81% of a sixty-second denominator**. Several reports close together and repeated by multiple routers readily add load. [Meshtastic's role documentation](https://meshtastic.org/docs/configuration/radio/device/) describes ROUTER as always rebroadcasting once; this is consistent with the observed copies.

**Leading explanation:** a transient burst amplified by several reachable ROUTER nodes. Repetition is measured; attributing the earlier 58% to a particular burst, startup exchange or board is still an inference. No sustained 58% load, infinite forwarding loop, rapid B001 transmit flood or new receive-error burst appears in this sample. No fresh foreign-node transmission is observed. Unknown external activity/interference during the original event remains possible; the capture cannot rule it out retrospectively. Only B001 is attached, so the gateway's own counters/logs are unobserved.

Next useful test: capture across another actual spike, ideally on both client and gateway, then compare with a controlled run using only one required nearby router. Preserve site roles until that comparison is deliberately scoped; deployed repeaters have different coverage needs from a co-located bench. No role, interval or radio change is made by this diagnosis.

Private evidence: `private/bench/v4-util-20261016/` contains `events.jsonl`, `serial.log`, private snapshot and `summary.json`. These include private configuration/location data and must remain ignored. Local readout: `.venv\Scripts\python.exe private/bench/final-summary-v4-util.py`; it reports whether any sampled fresh utilization reaches 58%. That predicate is false for this capture; it is not a reproduction of the original event.

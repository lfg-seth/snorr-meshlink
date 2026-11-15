# Direct-hop survey: firmware readiness and timing

2026-11-13. Read-only research supporting the owner's proposed vehicle survey.
No hardware, configuration, deployment or firmware change. These checks cover
upstream behavior; the companion project assessment must verify the installed
fork commit separately. Immutable upstream references use `v2.7.26.54e0d8d`, the
recorded pilot upstream baseline. Current documentation identifies as 2.8.

## Installed project firmware and next test

Owner resumes the [October survey plan](repeater-operations-survey.md) on
2026-11-13. Its Dell-controlled GPS/attempt logging, live map, one outstanding
request and two-direction metrics remain a design, not a finished tool.

The prepared RAK image is **2.7.26.4c96b9b**, source
`4c96b9ba0360f01752892a41d09ccacda82747bb`, verified using immutable `git show`
reads. The current firmware checkout is newer (`5bd4923`) and is not proof of
installed behavior. November batch records select the older image.

That image has **no dedicated survey responder**. Its SNORR module passively
records last-heard direct RSSI/SNR and sends changed LoRa reports at a minimum
180 seconds plus jitter/polling, subject to utilization checks. It cannot supply
fresh request-correlated two-direction pongs. Existing SNNS occupies PRIVATE_APP
(256); use a separate private port or explicit versioned multiplexing.
[Pinned modules](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/Modules.cpp),
[pinned neighbor code](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/SnorrNeighborModule.cpp).

The deployed commit supports the zero-hop reply branch below. However, its
PhoneAPI **forces addressed traceroute requests to want_ack=true**. Combined
with Router's hop rewrite, ordinary tethered traceroute does not satisfy the
no-ACK direct-only contract. Telemetry polling has a ten-second port floor and
does not echo ping RSSI/SNR. A dedicated responder plus Dell controller/logger
is the next implementation outcome. An ordinary USB client API may suffice
after testing the exact client build.
[Pinned PhoneAPI](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/mesh/PhoneAPI.cpp),
[pinned routing](https://github.com/lfg-seth/firmware/blob/4c96b9ba0360f01752892a41d09ccacda82747bb/src/modules/RoutingModule.cpp).

Compact authenticated frames of 48-56 **total RF bytes** require 0.600-0.682
seconds each on LONG_FAST; a pair occupies **1.20-1.36 seconds** before MAC,
USB, encryption and processing. Roughly **one exchange every two seconds** is
an aggressive quiet-channel bench target, not a measured maximum. One-Hz
authenticated ping/pong of this size cannot fit the current preset.

For a representative 1.25-second pair, two-second attempt spacing consumes
about 63% shared airtime; three seconds 42%; five seconds 25%; 6.25 seconds
20%, before background traffic. A proposed quiet test mode could target roughly
40% with about three-second spacing, and back down near 50%; coexistence near
20% needs about six to seven seconds or slower. Crossing 25% can suppress
existing polite GPS/health reports. These are proposed budgets, not settled
policy or legal limits. Keep the actual deployment preset for coverage testing.

The controller needs predicted-airtime reservations, fresh local and remote
utilization, queue observations, hysteresis and a pause ceiling. Double spacing
on congestion; shorten gradually after stability. Log deferrals separately
from RF failures. Preserve CAD/backoff and regional enforcement. Eight targets
at three-second global spacing have roughly 24-second revisits, longer with
timeouts: about 322 m at 30 mph. Select fewer targets or slow/stop near edges.

Next bench gate: implement the previously selected PKI-authorized responder,
sequence/duplicate handling and logger; explicitly set both packets to zero
hops/no ACK. Manual PING/PONG handling can use want_response=false. Verify
both directions' metrics, final ROUTER role, MQTT exclusion, and a third-node
geometry where mesh works but direct survey must fail. Measure actual encoded
sizes, TX timing, queues, loss and latency at two-, three-, five- and ten-second
spacing before choosing timeout/defaults. Record local rejection separately;
host submission is not proof of TX. Then drive repeatable routes, keeping an
independent GPS stream and every timeout, including targets no longer heard.
Run winter-atlas relay-on/off and end-to-end GPS acceptance separately; vehicle
antenna coverage does not establish on-foot coverage. No hardware changed.

## Direct-only packet contract

For standard module replies, send a request with `hop_limit=0`, `want_ack=false`, and
`decoded.want_response=true`. Use a matching channel/key and an actual application
whose responder is implemented. Zero hops means direct RF only: no forwarding
allowance. Do not request reliability ACKs: `Router::sendLocal` replaces a
user-originated zero hop limit with the configured limit whenever `want_ack` is
true. This can silently turn a purported direct-only test into a mesh test.
[Router source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/Router.cpp#L245-L250).

The baseline `RoutingModule::getHopLimitForResponse` returns zero when the
request's `hop_start` is zero. Standard application replies using `setReplyTo`
inherit that response limit and the request's ACK flag. Therefore a correctly
formed direct-only request can receive a direct-only response without changing
every repeater's global hop limit. This is a source capability, not field proof.
[Routing source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/modules/RoutingModule.cpp#L56-L71),
[reply source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/MeshModule.cpp).

ACK reliability introduces retransmission state and implicit-ACK behavior. For a
survey, count each application attempt and its timeout explicitly instead of
hiding losses behind retransmission. This also avoids extra ACK airtime.
[ReliableRouter source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/ReliableRouter.cpp#L11-L34).

## Existing tool limits

The laptop API applies rate limits by application port, not by destination:
traceroute 30 seconds, telemetry/position/waypoint/alert 10 seconds, text 2 seconds.
Thus polling ten repeaters through ordinary telemetry requests cannot obtain ten
fresh responses every ten seconds. A dedicated survey application requires an
implemented responder and its own bounded traffic policy; selecting an unused
port alone does not create a responder.
[PhoneAPI source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/PhoneAPI.cpp).

Traceroute provides per-hop SNR in both directions, but no built-in per-hop RSSI.
Current docs explicitly describe it as a diagnostic with a 30-second sender
limit. It is unsuitable for aggressive drive-test sampling.
[Traceroute documentation](https://meshtastic.org/docs/configuration/module/traceroute/).

Stock Range Test is a useful one-way alternative: repeaters can emit numbered
direct-only packets, with the vehicle logging received RSSI/SNR and its GPS. The
module sends zero-hop, unacknowledged packets. Its sender interval is an integer
number of seconds, without an explicit 30-second minimum in this source; the
LongFast 30-second recommendation is guidance, not that hard minimum. Sending
skips when polite utilization checks fail and stops after eight hours. The
receiver handler logs; it does not implement a pong reply.
[Range Test source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/modules/RangeTestModule.cpp),
[Range Test documentation](https://meshtastic.org/docs/configuration/module/range-test/).

## Airtime and useful cadence

Keep the operational modem preset for coverage comparisons. LongFast is SF11,
250 kHz, coding rate 4/5. Faster presets trade away link budget, so their survey
results answer a different coverage question.
[Official radio settings](https://meshtastic.org/docs/overview/radio-settings/).

The baseline includes a 16-byte Meshtastic header and a 16-symbol LoRa preamble;
LoRa explicit header and CRC are enabled. Total RF bytes equal 16 plus encoded
`Data` (including survey payload), plus 12 more bytes when PKI is used.
[RadioInterface definition](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/RadioInterface.h#L18-L94),
[RadioLib packet configuration](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/RadioLibInterface.h#L60-L68).

Illustrative calculated airtimes for **total transmitted byte counts**, at those
LongFast settings, are 395 ms for 20 bytes, 477 ms for 30 bytes, 559 ms for
40 bytes, and 764 ms for 70 bytes. Calculations use the standard LoRa formula
(16-symbol preamble, explicit header, CRC, no low-data-rate optimization).
These are estimates, not encoded sizes of a finished survey protocol or measured
latencies. For example a 20-byte request plus 40-byte reply already consumes
954 ms of shared airtime before contention and processing. One hundred samples
per second, or ten per second, cannot fit this LongFast exchange.
[RadioLib airtime implementation](https://github.com/jgromes/RadioLib/blob/7.6.0/src/modules/SX126x/SX126x.cpp).

The radio scheduler adds randomized contention delay, based on channel
utilization. At LongFast, the source's slot calculation truncates approximately
28.08 ms to 28 ms; the lowest contention window selects 0–7 slots, or 0–196 ms
per ordinary transmission. Busy receive/transmit state and other queued traffic
can add delay. The 4,500 ms `PROCESSING_TIME_MSEC` constant participates in the
**retransmission timeout formula**; it is not a mandatory 4.5-second delay on each
successful response.
[Radio timing source](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/mesh/RadioInterface.cpp).

For the illustrative 954 ms exchange, a 20% aggregate airtime budget implies at
least 4.77 seconds between completed exchanges across the whole test network;
25% implies at least 3.82 seconds. Ten round-robin targets then have approximately
48-second or 38-second revisit times, before background traffic and timeouts.
These are arithmetic planning bounds, not promised firmware performance.
Broadcasting a ping to every repeater causes multiple competing pongs; it does
not remove their airtime cost. Poll targets sequentially, or schedule slots.

## Congestion control and measurement interpretation

The baseline utilization statistic sums six ten-second bins. It is roughly a
one-minute history, so it reacts too slowly to prevent an initial aggressive
burst. The polite threshold is 25%; the other threshold is 40%. These are
firmware traffic policies, not universal regulatory limits. A laptop controller
should reserve predicted request/reply airtime before sending, keep one request
outstanding, and back down using fresh local utilization and, if available,
remote utilization. A quiet channel at the car need not be quiet at the repeater.
[Airtime implementation](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/airtime.cpp),
[threshold definitions](https://github.com/meshtastic/firmware/blob/v2.7.26.54e0d8d/src/airtime.h).

The client's received RSSI/SNR measures repeater→vehicle only. Measuring
vehicle→repeater requires the repeater to return its own reception measurements.
A successful pong proves a successful round trip; a missing pong alone cannot
separate a missed request from a missed reply. Keep attempt counts, GPS fix age,
request/reply identifiers, direction, timeout and relay validation. Plot failures
as well as successful signal measurements. Bench-check both ordinary direct
reception and a geometry where a relay is the only working path before accepting
the drive-test output as direct-only.

No measured fastest ping/pong rate is established by this research. Parent
assessment owns exact installed-firmware support and the field run plan.

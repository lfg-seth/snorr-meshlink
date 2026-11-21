# G005 handheld site survey

## OLED Heltec V4 handheld with GPS time

Build `heltec-v4-site-survey` for the original 16 MB OLED Heltec WiFi LoRa 32
V4 with the L76K GPS attached. The target enables GPS in a fresh configuration.
For a previously configured board, verify that GPS is enabled and uses the
V4 variant's default pins. Keep the V3 powered off if the V4 will use the
same enrolled tester identity.

Power up outdoors on battery. The home screen shows **Waiting for GPS time**
until the local receiver supplies valid UTC, then **Clock ready**. Walk and
numbered tests use that clock for survey packets. USB clock writes are
disabled for this target. The USB status and export commands below still
work, and the journal and CSV keep elapsed milliseconds per attempt.

The V4 partition table reserves 512 KiB for the 128-site journal at
`0xc10000`. An application-only update from the standard V4 layout lacks
this partition. The V3 installer and V3 flash backup are specific to G005.
Before field use, verify a V4 battery cold start without USB or Wi-Fi,
clock readiness, an authenticated direct reply and a numbered-site export.

## B002 V4 installation and GPS clock check

On November 21 the connected board identified as B002, original OLED
Heltec V4 `!699ca878`, running `2.7.26.a56466d`. Before writing, the
full 16 MiB flash backup matched the board's flash digest. The snapshot,
recovery image and SHA-256 manifest are private under
`private/bench/B002-v4-gps-survey-20261121/`.

The application and partition table matched the built images on readback.
After reboot B002 reported **2.7.26.93f80a1**, the original user identity,
and byte-identical local, module and channel configurations. The journal
reported 128 slots, counter zero. The OLED advanced from **Waiting for GPS
time** to **Clock ready** and GPS UTC was within two seconds of the host.
The check used USB power and read-only clock queries.

The survey protocol reported production US LongFast slot 35 at 10 dBm,
idle and **unenrolled**. Authenticated field tests require pairing B002's
identity with the intended responders. Battery-only acquisition, a direct
reply and numbered-site export on this board remain pending.

## 2026-11-21 - Pre-field readiness

USB identifies **SNORR Site Survey / SURV**, the former G005 Heltec V3,
running **2.7.26.2dbf0a6** with survey ID **!699c2ed8**. The survey module
reports enrollment, no active run and a verified **US LongFast / slot 35 /
10 dBm** production profile. Mesh role is CLIENT and MQTT is disabled.

The home screen initially requested time. USB sync brought its clock within
two seconds of the host and the display state changed to **Clock ready**.
Storage reported 128 slots, with **11 saved sites** and **#12 next**. The
read-only export recovered **166 attempts**, with the same counter and saved
R004/R007 selection before and after. A private copy of the exporter needed
the normal Meshtastic serial wake sequence to obtain a response on this host.
The profile, USB evidence and CSV are in
`private/bench/B003-survey-ready-20261121/`.

The owner then requested a clean start for the first actual survey. The USB
clear command preserves numbering. After backing up the raw journal and NVS,
a verified write changed only the survey reservation in one NVS sector and
let the installed firmware clear the journal at boot. Readback confirmed
empty history, zero attempts, counter **0**, and **#1** next. The complete
radio profile and firmware matched the pre-reset readback. R004/R007 remain
selected, and USB time sync restored **Clock ready**. The backup still holds
the 11 bench sites and their 166 exported attempts.

Keep the battery connected before removing USB to carry the clock into the
field. Keep the original B003 V4 off while the handheld uses the shared
survey identity. Battery-only runtime, Wi-Fi time acquisition and a new
field RF result remain unverified.

The owner selected the Heltec WiFi LoRa 32 V3 formerly configured as G005.
Its radio ID before conversion was `!9ea039cc`. The handheld uses the
November 14 tester's enrolled LoRa identity `!699c2ed8` and the display name
`SNORR Site Survey / SURV`. Keep the original B003 V4 off while using it.
The boards retain distinct physical identities. The 3000 mAh pack is the
owner's field power source.

## At the antenna position

1. Open **Walk last targets**, or choose **One**, **Several** or **All**. Tap
   to move and hold for about one second to choose. In Several, hold to toggle
   each checkbox. Tap through R011 to **Done** and hold. The handheld saves
   that selection. All includes R001, R002 and R004 through R011.
2. In Walk, tap to measure one fresh sweep. Hold to start a numbered site.
   Two quick taps return to the main menu. Walking samples stay in RAM. A
   site starts with empty sample counts, even during an unfinished walk sweep.
3. Mark the displayed site number on your map. The handheld visits each
   selected repeater once per round for ten rounds. Hold to finish early.
   An outstanding attempt can use its remaining reply window before the
   manual result closes.
4. Read each repeater's replies/attempts, **Up dB** (median SNR of the ping
   at that repeater), and **Dn dB** (median SNR of its pong at the handheld).
   A dash marks a missing signal. Larger selections page in pairs. Tap
   during a test to advance the page. At the result, hold **Test again** to
   reserve a new site number with the same targets. Tap to reach other actions.
5. Open **History** to browse newest first. Hold to view a site, tap to page
   and hold to return. Complete, manual and interrupted sites have distinct
   labels.

The November responders renew a **15-minute pause in locally originated
routine reports** on every accepted survey ping they hear, including pings
for other targets. Ordinary relaying continues. One walking tap schedules
one sweep, and each numbered test ends after its bounded selection.

## Time and USB retrieval

Power the V3 from its battery within reach of its configured 2.4 GHz Wi-Fi
and NTP server, or set UTC over USB. Look for **Clock ready** before leaving.
Coverage is unnecessary after a successful sync while the clock remains
powered. After total power loss, reacquire time. B003's GPS remains an option
for a different handheld that needs to start without a time source in radio
blackspots. The responder rejects frames more than seven seconds away from
its own trusted time when it has one.

The saved Wi-Fi network was disconnected at the bench. G005 accepted UTC
over USB for these RF tests. Wi-Fi/NTP acquisition on battery and the
3000 mAh pack's runtime still need measurement. For USB-to-battery handoff,
attach the pack before removing USB. To start on battery alone, power up
within range of the saved network and verify **Clock ready**.

Run these PowerShell commands from the project checkout with pyserial
installed. Substitute the current port if Windows reassigns COM6. The
station watcher or another serial client must release the port first.

```powershell
python scripts/bench/site-survey.py --port COM6 status
python scripts/bench/site-survey.py --port COM6 clock
python scripts/bench/site-survey.py --port COM6 export --output private/bench/site-survey.csv
```

From the existing Windows bench's outer SnorrMesh checkout, the isolated
project branch and installed interpreter are available with:

```powershell
& .\.venv\Scripts\python.exe private\worktrees\handheld-project\scripts\bench\site-survey.py --port COM6 export --output private\bench\site-survey.csv
```

Export writes one CSV row per recorded attempt and finishes with a site/row
count. Repeat exports leave the journal intact. Each row records site/status,
round, attempt, label/ID, start/end elapsed milliseconds, outcome, both
available RSSI (dBm) and SNR (dB) readings, and matched RTT from local TX
start. Empty fields mean unavailable. A timed-out attempt exhausted its
reply window. An interrupted pending write has unknown outcome. Airtime
deferral and queue rejection have separate outcome values.

The journal reserves one whole 4096-byte sector when a test starts. Each of
128 sectors fits all 100 possible attempts, including separate pending and
outcome records. A full journal leaves walking usable. To remove saved sites,
export first, read the current counter with `status`, then explicitly run
`python scripts/bench/site-survey.py --port COM6 clear --confirm-counter N`,
replacing `N` with that counter. The counter survives the clear.

## Rebuild and recovery

Build the pinned firmware in its own checkout with PlatformIO:

```powershell
pio run -e heltec-v3-site-survey
```

On this bench, `private/bench/g005-handheld-survey-20261116/build.ps1`
uses the installed Windows PlatformIO packages and a short path for the
toolchain. The board-specific recovery directory is ignored by Git. It
contains the full original 8 MiB image, private settings, V3 filesystem
builder, guarded installer and local bench captures.

For initial conversion, identify the V3 by silicon identity, check its
original full-image digest and active app0, and verify the proposed survey
region is unused. Install the target's partition table at `0x8000`, app at
`0x10000` and its **privately provisioned V3** filesystem at `0x670000`.
The table reserves `0x5f0000..0x66ffff` from the inactive app slot. The
installer checks the layout and reads the flashed digests independently.
Use app-only writes for later updates to the same layout. For full rollback,
restore this physical G005's original verified image at offset zero. Back up
new surveys first. The V4 recovery flash image belongs to B003.

On this bench, the initial verified install used
`python private/bench/g005-handheld-survey-20261116/install.py --revision a58085294`.
Run `prepare.py` in the same directory to rebuild the private V3 filesystem
from the verified recovery and enrolled tester configuration. The installer
rejects an unexpected silicon ID, source revision, active slot, current
application or partition layout. Subsequent app-only updates use its
`--app-only` option with the selected clean build's revision.

Provisioning starts with G005's V3 owner/configuration files and physical
identity. It restores the verified tester keypair, logical LoRa number and
pilot channel, provisions the ten responder public keys and existing cohort
over local USB, retains G005's Wi-Fi for NTP, and disables gateway MQTT.
Only an authenticated direct survey exchange transmits over LoRa. No
responder enrollment change is required.

The deployed `rak4631-survey` responder is built independently of its
saved CLIENT or ROUTER role. Its survey interceptor runs before forwarding
and uses the same physical directness, address, timestamp, cohort and paired
sender checks in either role. The selected peer uses the enrolled sender's
node number to look up its public key and verify the pairwise tag.

## Installed image and measured direct links

The installed `heltec-v3-site-survey` application is **2.7.26.2dbf0a6**,
commit `2dbf0a65af9058d91df5a49827b846588a9a0063`, **1,748,928 bytes**.
Its SHA-256 is
`5129293d1aa0a75bd6916a5a4763e5861847f5860d2218b83f6f97918ae259c8`.
The guarded app-only installer verified the image on G005 and matched the
before/after device digests for NVS, the private filesystem and the survey
journal. The build captures GPIO0 edges between display/radio polls.
Local USB can temporarily lengthen the test interval while idle. Restarting
restores the deployed defaults. Each RF survey still starts from the button.

The first bench image, source `a5808529419be06691ab6c37f384b8f7d2e72e20`,
reported `2.7.26.a580852` and measured **1,748,784 bytes**. Its SHA-256 is
`179c94f48a5c87858229008e58da4d874a9a6667a5dc3890ebcdeb362b3a2f55`.
The partition table SHA-256 is
`da1bfb4f524f084d4fe919f1991cafb02e1588c753d383ad9d9f51009dba6986`.
The verified private original G005 full flash has SHA-256
`6ed99bf9c10934d23297969d4bb4f192a9237006c62794db006094e9d612533f`.
Physical Wi-Fi/MAC identity, V3 target, intended logical ID, own physical
hardware ID, retained Wi-Fi/disabled MQTT and exact survey channel/keys were
checked privately. The host received ten commissioning acknowledgements on
G005. The responders had no USB connection or configuration write.

The November source revisions are tester
`7b766e6eba20f304d13c534bf1de4acd9f29d3e6` and responder
`bcb22e037293df5531da391bb88d46b6969633b0`. The October tester private key
derived the November enrollment public key in a private comparison. The V3
retains US LongFast slot 35 and 10 dBm. It uses the November tester's
3,000 ms minimum interval, 4,500 ms response window and adaptive backoff
up to 15,000 ms.

On 2026-11-16, after a hardware reset, the host supplied UTC over USB and
sent button input through the CP210x GPIO0 circuit. The V3 supplied its own
targets. A two-target walking sweep returned R004 1/1 and R007 0/1 with
site counter zero throughout. Site **#1** then ran for **65.842 seconds**.

| Repeater | Replies | Timeouts | Median SNR up / down | Median RSSI up / down | Median RTT |
| --- | ---: | ---: | ---: | ---: | ---: |
| R004 `!49ac6d7f` | 9/10 | 1 | +6.5 / +6.0 dB | −51 / −44 dBm | 1,943 ms |
| R007 `!b456f760` | 7/10 | 3 | +6.5 / +6.0 dB | −64 / −60 dBm | 2,011 ms |

Twenty exported rows alternate R004/R007 over ten rounds. Directional
medians and counts independently calculated from those rows match both
columns of the OLED drawing routine. Two USB exports matched byte-for-byte.
Saved summaries and native hardware observations are distinct from optical
observation of the display. These measurements apply to the nearby CLIENT
pair in the owner-specified configuration.

The owner observed a second numbered test on the physical OLED. After
seven attempts per repeater the screen showed R004 1/7 and +6.75 dB, R007
1/7 and +6.25 dB. Those match the uplink medians and counts in the first
14 exported rows of **site #2**. It finished in **81.225 seconds**, R004
4/10 and R007 2/10, with respective median uplink/downlink SNR
+6.625/+7.0 and +6.375/+6.0 dB. Both sites used the same firmware timing.
Enqueue-to-matched-reply time was 1.886–3.334 s at site #1 and
1.959–3.343 s at site #2. A timeout records the absence of a matched
reply before the deadline. Only successfully matched replies contribute
to those latency ranges.

## Button input and pacing comparison

Rapid bursts of five 120 ms GPIO0 presses could advance the original
menu by four items. On the installed image, the same 30 bursts advanced by
all **150** items with the USB event stream active. Target selection was
checked independently of RF during this regression.

Both pacing runs below used the same installed image, saved targets,
ten alternating rounds and 4,500 ms reply window. The host supplied only
the clock and, for the slower run, a temporary minimum attempt interval.
At the original 3,000 ms minimum, **site #3** lasted **67.557 seconds**.
R004 returned **10/10**, with median SNR +6.25/+6.0 dB (up/down),
RSSI −44.5/−39 dBm and RTT 1,820.5 ms. R007 returned **5/10**, with
SNR +6.75/+6.25 dB, RSSI −50/−48 dBm and RTT 1,831 ms. Actual
start-to-start intervals were 3,000–4,505 ms. All five misses were
confirmed timeouts.

At the 10,000 ms minimum, **site #4** lasted **199.036 seconds**. Actual
starts were 10,000–10,003 ms apart. R004 returned **2/10**, median SNR
+6.0/+6.0 dB, RSSI −45/−40 dBm and RTT 2,030 ms. R007 returned **5/10**,
median SNR +6.25/+6.25 dB, RSSI −50/−47 dBm and RTT 1,957 ms.
The 13 timeouts lasted 4,501–4,507 ms. The slow run took about 3.3 minutes
and produced fewer total replies. These sequential samples cannot locate
a lost ping or pong. The handheld retains the deployed adaptive pacing.
Each run exported 20 alternating rows and both displayed medians matched
the independent calculations on each link. Its preceding walking sweep
left the permanent counter unchanged.

## Recovery and export on G005

Holding **Test again** reserved site #5. A subsequent hold ended it manually
after one attempt per repeater in 13.681 s. Its R004 timeout and R007 reply
remained in flash. Site #6 was reset through the board's EN line while its
first reply window was open. After reboot, History listed **#6 interrupted**
first, with one **unknown** outcome. The earlier sites exported identically.
The One menu retained R004 over reset, All selected the ten roster entries,
and Several restored R004/R007. On-device History presented both columns
and missing signal as dashes. USB reads verified the drawing routine's text.

Site #7 was reset during its third attempt. The first two had timed out on
the live event stream. After reset both remained confirmed timeouts and
the third row was unknown. All earlier sites matched their pre-reset
rows. Two invocations of the documented CSV command exported **86 attempts
from seven sites** with matching SHA-256
`02c969714456c7113f1b5afccf9a82cba30aabca5bd8f91ba6a7aa050877da49`.
G005 showed **Walk last targets**, **2 selected**, **Clock ready** after USB
sync, with R004/R007 saved and **#8** next. The CSV is in
`private/bench/site-survey.csv`.

The owner then disconnected all power for five seconds and reconnected
USB. Before a time or target command, G005 reported its saved pair, counter
seven and no trusted UTC. Following USB time sync, the standalone exporter
again produced the same 86 rows and the pre-disconnect SHA-256. History
showed #7 first with its interrupted status. A single walking tap addressed
the retained R004/R007 pair without a host target command. Both timed out
(0/1 each). Both peers had returned authenticated replies in the earlier
complete tests. The post-power-cycle sweep left #8 available. G005 returned
to its clock-ready home screen.

## Deterministic checks

Host C++ tests with ASan/UBSan exercised all 1,023 nonempty selection masks,
round order, known zero and missing SNR, even/odd medians, interrupted header
and outcome writes, full capacity, clear and monotonic numbering. The original
native client/responder fixtures passed, including authenticated matching,
duplicate rejection and deadlines. A separate fixture presented a correctly
matched, expired pong before and after timeout processing. Success counts
and the following attempt stayed intact. The offline project bench suite
passed 110 tests, including three for the USB exporter.

To repeat the native checks from the firmware root with Linux g++:

```sh
g++ -std=c++17 -fsanitize=address,undefined -fno-omit-frame-pointer -no-pie test/test_site_handheld/journal.cpp -o /tmp/site-journal
/tmp/site-journal
python3 test/test_direct_survey/run.py
```

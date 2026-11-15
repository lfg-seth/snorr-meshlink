# G001 USB / SD-health diagnosis — 2026-11-15

Owner reconnects G001 by USB and requests diagnosis after a six-minute MQTT
window received forwarding traffic but no G001 SD report. Owner confirms the
card is inserted and unchanged. Verify **!1bbf0638**, USB
**F8:5B:1B:BF:06:38**, hardware **7a71bc1ffb7e0270263f1fc35e08d14d**,
retained **2.7.26.5bd4923**. The complete saved profile exactly matches the
[replacement Wi-Fi verification](g001-wifi-test-20261115.md#owner-selected-wi-fi-change--2026-11-15).

## Outcome

**Wi-Fi, direct MQTT, SD recording and fresh SD-health MQTT delivery pass in
this run.** No firmware fix, flash, factory reset or lasting configuration
change is applied. The earlier absence of a report is not reproduced through
the complete observation; its exact cause remains unisolated.

- Nine initial USB status reads from **15:11:22–15:13:25 Pacific** and six
  subsequent successful structured-log reads show the owner-selected Wi-Fi
  and direct MQTT connected at **−67 to −65 dBm**. The first status request
  just after enabling structured logs times out; later reads succeed without
  repeating configuration.
- Saved device/SD interval remains **300 seconds**, encrypted MQTT and private
  primary-channel uplink are enabled, downlink is disabled, LoRa TX is enabled
  and the board remains CLIENT. Configuration, clock and available heap do not
  show a Wi-Fi/profile failure in this sample.
- Structured SD diagnostics at **15:15:24** and **15:16:25** show segment
  **118**, frames increasing **344 → 393**, and **zero dropped records**.
  This diagnostic follows successful `f_sync` and filesystem-count refresh in
  the installed source. The card is recording; physical copied-file integrity
  and long-duration endurance are separate checks.
- A fresh non-retained SNSD v1 packet arrives at the TLS broker at
  **15:17:09.968 Pacific**, through **G001's own uplink**, with originating
  source **!1bbf0638**, packet **3419159292**, boot **1700253249**, persistent
  sequence **413**, uptime **536 seconds**, source UTC **1794784629**,
  advertised interval **300 seconds**, **13,631,488 / 31,902,400,512 bytes**
  and **0 dropped records**. Source and gateway IDs both match G001. One report
  establishes fresh delivery, not an observed inter-report cadence.
- The same broker window also receives G001-origin ordinary telemetry,
  SNGH, SNNS and SNWF, as well as forwarded mesh traffic. Broker acceptance
  is separate from authenticated portal ingestion.

## Delay diagnosis and limits

At **15:11:39**, the actual collector logs **`Ch. util >25%. Skip send`**.
The pinned `sendSdHealth()` checks the same polite channel-utilization and
TX-airtime admission used by the other companion reports. Thus radio load
can delay an SD report even with Wi-Fi/MQTT connected. Later local samples
show channel utilization below the limit, and a new SD packet arrives.
This proves an intermittent admission block, not that congestion alone caused
all earlier missing reports. A report observed at uptime 536 does not prove
there was no earlier report before the subscriber started.

The ranked checks were radio admission, card/recorder health, and startup/
report-timer state. SD sync counters and the new packet rule out a currently
failed recorder/uplink. Natural five-minute scheduling prevents a seconds-long
live report reproduction while preserving settings; use the SD sync loop and
matched broker window rather than force transmissions or lower limits.

## Instrumentation and restoration

Private diagnostic commands are `.venv/bin/python` with
`private/bench/g001-usb-diag-20261115/diagnose.py`,
`structured_diagnose.py`, `mqtt/observe.py` and `verify_restored.py`.
The first serial capture is partly garbled raw text. Temporarily enabling
`security.debug_log_api_enabled` yields intact framed diagnostics. Its original
**false** value is restored; an independent connection verifies complete
original local/module/channel bytes, owner, hardware and firmware identity.
Serial handles and TLS subscriber are closed. Profile/credentials and raw
observations stay ignored in that private directory; sanitized records contain
no SSID/password, locations or messages.

Next: continue sustained reporting/portal acceptance and copied-card checks.
No change to the reporting interval or radio admission policy is justified by
this successful diagnostic run. [Cadence contract](g001-sd-cadence.md).

# R011 telemetry missing from the CLI - 2026-11-15

Owner reports no telemetry in the CLI activity monitor after
[R011 deployment](r011-angel-vegas-deployment.md) and requests B003 diagnosis.

## Reproduction and observations

The active `watch-nodes.py` process uses an existing temporary SSH wrapper
through the tailnet router. Direct SSH times out; using that same existing
route provides a healthy worker feed, registered R011 and **no R011 contact,
readings or telemetry receipts**. No catch-up or rejected-row errors. The
private `check-telemetry.py` command reproduces the missing-telemetry assertion.

B003 **!699c2ed8 / 2.7.26.7b766e6** has cached R011 device metrics: **4.145 V,
96%, uptime 786 seconds**. The node cache's `lastHeard` is not a measurement
clock and does not establish that these metrics are fresh. Temperature/power
metrics are absent. Temporarily hand off B003 from its idle survey service to
a standard receiver and restore the service afterward. A 12-second passive
window plus three zero-hop device/environment/power requests yields no matched
R011 replies at B003. The first capture harness encounters a serialization
error; its finally block restores the service. The corrected harness preserves
B003's complete profile and ignores custom survey frames while decoding normal
Meshtastic messages.

One subsequent authenticated **physical zero-hop survey ping** to R011
succeeds **1/1**, **2,485 ms** round trip. Uplink **-94 dBm / 3 dB SNR**;
downlink **-76 dBm / 5.5 dB SNR**. Stop immediately and restore B003's original
runtime timing and R001 target selection. This ping renews hearing responders'
**900-second** autonomous-report quiet period; it is excluded as proof of
periodic telemetry delivery.

A read-only two-hour raw archive audit finds one R011 envelope at
**2026-11-15T19:46:49.812Z**, received through **G003 / !849ad7a0**, addressed to
**B003 / !699c2ed8**, PKI encrypted. This proves a reply reached a gateway.
It is not ordinary channel telemetry; the CLI correctly excludes PKI payloads.
R011 is registered as `r011`, and its private primary channel name/key match
the server. Other sources continue reporting to the CLI feed.

## Configuration defect and correction gate

The saved R011 deployment profile has **`lora.config_ok_to_mqtt=false`**,
unlike deployed R001/R008. The conversion from former REF1 retained this
restriction; the original deployment comparison verified that mistaken
intended profile. The pilot broker resolves to public addresses from this
field laptop. Gateway source `6fea6aa` `MQTT::onSend()` withholds decoded
nonlocal packets without the OK-to-MQTT bit when its broker connection is
public; the same path can still forward opaque PKI packets. Sender source
`bcb22e0` `perhapsEncode()` sets this bit from `config_ok_to_mqtt`.
This explains the observed ordinary-versus-PKI discrepancy, subject to the
corrected-setting and new-report verification below.

The configuration-only fix is to enable **only** `lora.config_ok_to_mqtt` on
USB-identified R011, preserving complete profile/keys/location/firmware, then
verify independently through reboot and obtain **new ordinary R011 reports**
in the same CLI/archive path. No flash is required. Survey quiet may defer the
first autonomous report, and reboot while its marker exists renews that quiet
window. Do not keep pinging while waiting for periodic reporting.

R011 USB access is requested for that correction. Replacement USB
**AA474A4710B85C2C** is identified as R005 and initially left unchanged. The
owner then explicitly **substitutes R005 for R011 at this site**. R011 remains
unmodified, with its false upload-permission setting; no repair is claimed.
[Replacement configuration and verification](r005-angel-vegas-deployment.md)
checks R005's already-enabled permission explicitly and independently verifies
its complete profile/location through reboot. New ordinary R005 device,
environment, power and SNNS reach the same CLI feed after configuration; the
R011-specific false flag remains unrepaired because the owner withdraws it.
Actual INA219/AHT21 function remains separate until real readings arrive.

Private evidence and commands: `private/bench/R011-diagnosis-20261115/`.
Raw location, packet payloads, channel material and controller credentials stay
private. No production-service, portal, gateway or firmware change is made by
the diagnostic reads. B003's survey service is restored after each temporary
handoff; normal device binding stops it when B003 is physically unplugged.

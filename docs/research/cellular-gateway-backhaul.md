# Cellular backhaul for a Kyle Canyon gateway

Research date: **2026-10-24**. Advice and candidate hardware only; no purchase,
service activation, site installation, hardware allocation or configuration change.

## Recommendation and existing evidence

Follow-up: the owner asks for compact COTS LoRa + cellular hardware and considers
the separate GL.iNet router excessive. The integrated hardware candidates below
now lead the shortlist for development; the router path remains the verified
architecture to reuse if firmware development is undesirable. No purchase or
firmware implementation is selected by this research.

Use an existing Heltec gateway over **2.4 GHz Wi-Fi to a cellular router**, then
the existing MQTT/MeshLink path. This reuses the working gateway architecture
without developing modem support in SNORR Firmware. An owned AT&T phone hotspot
is the cheapest attended trial: **$0 added hardware**, conditional on ownership,
an appropriate plan and sufficient included tethering data. It is not yet an
accepted unattended solar design.

The owner reports AT&T is mostly reliable in Kyle Canyon, and wants solar-only
power with a preference for 5 V and 18650 cells. Exact gateway location, measured
AT&T signal/band, temperature, shade, permitted access and mounting are unknown.
Tower coverage is usable through normal subscribed cellular service; tower-site
access is unnecessary and is not inferred from this conversation.

Existing [inventory evidence](../../records/inventory.md#first-confirmation-pass)
records hotspot-to-MQTT success: [TEST-003](../../records/field-results.md#test-003--first-real-mqtt-gateway-provisioning-attempt)
delivered both V4 fixtures through both V3 gateways, and [TEST-004](../../records/field-results.md#test-004--automatic-gps-positions-through-both-mqtt-gateways)
delivered automatic encrypted GPS reports over all four paths, approximately
21–35 seconds old. Those short bench observations do not verify Kyle Canyon
coverage, solar runtime or recovery following outages.

## Combined LoRa and cellular COTS hardware - follow-up 2026-10-24

COTS boards exist. No ready-to-deploy Meshtastic-to-AT&T cellular product was
verified in this review. Buying the radios and buying a supported firmware
transport are separate questions.

| Candidate | Advertised board cost, before tax/shipping | Hardware and remaining software work |
| --- | --- | --- |
| RAK4631 + RAK19007 + RAK5860 BG77 | $30 for RAK5860 if a suitable spare core/base is reused; otherwise base adds $9.99 and RAK4631 starts at $17.99 | SX1262 LoRa plus LTE-M/NB-IoT; direct cellular MQTT needs development. |
| LILYGO T-SIM board + 915 MHz T-Sim Shield | Shield $29.36; catalog example T-SIM7670G S3 $36.02, arithmetic $65.38 before exact variant/availability | ESP32-S3 plus LTE modem plus SX1262; LoRa examples exist, but Meshtastic cellular transport is not verified. |
| RAK WisGate with LTE | Not priced for this shortlist | LoRaWAN product family, not a substitute for the existing Meshtastic gateway. |

Price sources: [RAK5860](https://store.rakwireless.com/products/rak5860-lte-nb-iot-extension-board),
[RAK19007](https://store.rakwireless.com/products/rak19007-wisblock-base-board-2nd-gen),
[RAK4631](https://store.rakwireless.com/products/rak4631-lpwan-node),
[LILYGO shield](https://lilygo.cc/products/t-sim-shield), and
[LILYGO current catalog](https://lilygo.cc/collections/t-sim-series).
The LILYGO store renders sold-out/variant-dependent states; these are quotations,
not confirmation an appropriate complete US915/cellular combination is in stock.
Do not use an accessory-only "from" price as the price of a full cellular board.

**RAK is the first candidate to investigate using owned hardware.** Inventory
HW-001 lists RAK19007 assemblies, but a spare usable core/base and free IO slot
must be identified without taking a required deployed/bench node out of service.
RAK5860 is a UART BG77 LTE-M/NB2 extension with 2.6-4.2 V battery supply; RAK
requires a connected battery because USB alone is unreliable. The RAK19007
supports 5 V USB and solar inputs plus a 3.7 V battery. Its existing charger is
not automatically adequate for a larger pack or panel. RAK19003 mini has only
sensor slots, not the IO slot this module needs. Sources:
[modem datasheet](https://docs.rakwireless.com/product-categories/wisblock/rak5860/datasheet/),
[base](https://store.rakwireless.com/products/rak19007-wisblock-base-board-2nd-gen),
[mini-base layout](https://docs.rakwireless.com/product-categories/wisblock/rak19003/overview/).

RAK's [quick start](https://docs.rakwireless.com/product-categories/wisblock/rak5860/quickstart/)
provides RAK4631 modem/UART and TCP/MQTT examples. These are Arduino examples,
not a Meshtastic LTE firmware release. Check UART conflicts with fitted GPS or
other modules. RAK13101 uses 2G GSM/GPRS and is not the AT&T LTE option;
RAK2011 is an Arduino BG96 shield, rather than the direct WisBlock extension.

**LILYGO is a compact alternative.** A T-SIM cellular board alone does not supply
LoRa. Its [T-Sim Shield](https://wiki.lilygo.cc/products/t-sim-series/t-sim-shield/)
adds SX1262 and INA3221; vendor examples cover raw LoRa/LoRaWAN, not a complete
Meshtastic cellular uplink. The [SIM7000G board](https://lilygo.cc/products/t-sim7000g)
documents USB-C, an 18650 holder and solar input. SIM7080G Standard is another
LTE-M candidate, distinct from the older PMU board: the
[manufacturer's detailed revision guide](https://wiki.lilygo.cc/zh/products/t-sim-series/t-sim-shield/)
shows different jumpers/pins, and the old SIM7080G PMU combination needs battery
holder modifications. Do not assume all T-SIM revisions stack unchanged.
The quoted SIM7670G S3 price is a Cat-1 example, not an LTE-M recommendation.

**Firmware is the main gap.** The local SNORR checkout's `src/mqtt/MQTT.h`
selects WiFiClient or EthernetClient, and `MQTT.cpp` checks those interfaces;
a source search found no SIM7000/SIM7080/BG77/TinyGSM transport. Current
[upstream MQTT header](https://github.com/meshtastic/firmware/blob/develop/src/mqtt/MQTT.h)
shows the same direct-client choices. This supports the bounded finding that
neither candidate is enabled by a SIM/configuration change in the inspected
firmware; it does not prove no third-party implementation exists. A port needs
board pin/power support, modem connection and secure MQTT, retries and recovery.
A separate small controller using the documented
[MQTT client-proxy interface](https://meshtastic.org/docs/configuration/module/mqtt/)
is an alternative to changing the radio firmware, but that embedded bridge also
needs implementation and end-to-end validation.

AT&T [supports LTE-M](https://www.business.att.com/products/lpwa.html), making it
a sensible low-data-rate category to investigate. Normal smartphone LTE reception
does not verify LTE-M service at the candidate point or SIM entitlement. Verify
actual module/device acceptance and a suitable LTE-M plan; the previously quoted
consumer/hotspot SIM must not be assumed to cover it. Retaining continuous LoRa
reception means advertised modem/MCU deep-sleep current cannot be used as the
gateway average. All earlier router power examples are illustrative and do not
predict these candidates' runtime.

Next evidence: identify an available inventoried RAK19007/4631 and any slot/UART
conflicts; select an AT&T LTE-M test option and scope a firmware/bridge proof of
concept before purchase. No development, activation, flashing or bench test ran.

## Separate-router hardware comparison

| Approach | Added equipment price | Suitability / unresolved gate |
| --- | --- | --- |
| Owned AT&T phone hotspot + existing Heltec | $0 if already owned | Easiest attended coverage/MQTT trial; model-specific hotspot sleep, boot, charging and temperature need checking before unattended use. |
| Carrier hotspot, e.g. AT&T Turbo Hotspot 3 | Current first-party retail price not verified | AT&T documents LTE bands 2/4/5/12/14/29/30/66 and removable battery. Purchase price, recovery without button presses and operating limits need model-specific verification. [AT&T specifications](https://www.att.com/device-support/article/150541/att/turbo-hotspot-3/) |
| GL.iNet Collie GL-X300B, currently listed RS485/EG25-G | **$125.99 advertised USD**, before US tax | Best low-cost fixed-site candidate examined, conditional on AT&T approval of the exact device/SIM/plan; needs higher input voltage than 5 V. |
| GL.iNet Puli GL-XE300 | **$125.99 advertised USD**, before US tax | Convenient USB-C 5 V, but 0–40°C operating range excludes an unheated freezing site. |
| GL.iNet Spitz Plus GL-X2000 | **$175.99 advertised USD**, before US tax | Manufacturer explicitly claims AT&T/T-Mobile IoT certification; 9–36 V input, <14 W and 0–40°C make it less attractive for this solar/winter brief. [Specifications/certification](https://www.gl-inet.com/products/gl-x2000/) |

Prices come from the current [manufacturer collection](https://www.gl-inet.com/collections/student-discounts?grid_list=grid-view&page=2),
which renders USD and redirects the former US store; confirm exact US SKU,
shipping and checkout price. An older indexed $105.99 Collie listing is not used
as a current quote. Enclosure, power conversion, panel, battery, charge controller,
antennas, SIM, tax and any activation charge are additional and unpriced.

## Collie and Puli limits

- **Collie is not native 5 V.** The current product page specifies 9–36 V DC,
  <4 W and **−20 to +55°C operating**. Its linked datasheet specifies 9–35 V,
  normal operation <3 W, full operation <4 W, and a hardware watchdog. Use the
  narrower common 9–35 V range until exact-unit documentation resolves it.
  The supplied adapter is only rated 0–40°C. A regulated supply appropriate to
  the pack and modem peaks is required. A −30 to +70°C storage specification
  is not an operating rating. [Product](https://www.gl-inet.com/products/gl-x300b/),
  [datasheet](https://static.gl-inet.com/www/images/products/datasheet/x300b_datasheet_20231019.pdf)
- **Puli:** USB-C 5 V/2 A with its battery, 5 V/3 A without; <4.4 W and
  **0–40°C operating**. Its 5000 mAh internal battery does not establish winter
  suitability or adequate daily solar storage. [Product](https://www.gl-inet.com/products/gl-xe300/)
- Collie's advertised current modem is EG25-G. Quectel documents LTE-FDD
  B1/2/3/4/5/7/8/12/13/18/19/20/25/26/28 and LTE-TDD B38/39/40/41 for EG25-G.
  This includes useful US bands, but does not establish compatibility with the
  actual serving sector or approval for an AT&T consumer/prepaid plan.
  Do not substitute EG25-GL or EC25 variants by name alone.
  [Quectel hardware design](https://www.quectel.com/content/uploads/2021/03/Quectel_EG25-G_Hardware_Design_V1.4.pdf)
- Exact AT&T IMEI/SKU and plan acceptance are a **pre-purchase gate** for Collie;
  modem bands and FCC certification alone do not verify carrier activation.
  No weatherproof rating or tested automatic restart after complete battery
  depletion was established here. Verify cold start, cellular redial, Wi-Fi and
  MQTT recovery on the chosen unit before inaccessible installation.

## Service budget

AT&T's [current prepaid data-only page](https://www.att.com/prepaid/mobile-hotspot-tablet/)
advertises **20 GB/month for $240 prepaid for 12 months** ($20/month equivalent)
and **15 GB for $35 paid monthly**, with taxes/fees extra. The $10/5 GB item is
an add-on, not a standalone $10 plan. These are documented consumer benchmarks,
not confirmation that the selected IoT router is eligible.
Measure all SIM traffic, including keepalives, reconnects and router updates,
before selecting the smallest allowance or paying annually.

Lower-cost candidate: [EIOTCLUB's own dual-network SIM page](https://www.eiotclub.com/products/4g-lte-prepaid-sim-card-tmobile-att)
lists **2 GB/30 days for $15** and **24 GB/360 days for $119**, advertising
AT&T/T-Mobile support and unlocked hotspot compatibility. Its duplicate tables
also show different prices/allowances, so verify the exact selected product and
renewal terms before buying. The $1 offer is starter/trial data, not a recurring
unlimited plan. Confirm this SIM actually attaches to AT&T at the candidate site;
coverage/access equivalent to direct AT&T is not established.

## Solar sizing example, not measurements or a parts order

The combined system has not been measured. Illustrative average loads at the
battery, including router, Heltec and conversion/controller losses:

| Assumed average | Daily energy | Nominal storage for two days at 80% usable | Minimum panel at 3 full-sun hours and 70% harvest |
| --- | --- | --- | --- |
| 2 W | 48 Wh | 120 Wh | 23 W |
| 3 W | 72 Wh | 180 Wh | 35 W |
| 5 W | 120 Wh | 300 Wh | 58 W |

These panel minima only replace one day's assumed use; recovery after several
dark days needs surplus. A 60-100 W panel is a planning range to evaluate, not
established winter/shade/snow adequacy. Do not treat the manufacturer's <4 W
router specification as a measurement of the whole assembly or its peaks.

[EVE's manufacturer specifications](https://www.evebatteryusa.com/18650-and-21700-specifications)
list the 26V reference cell at 2.55 Ah and 3.6 V, about 9.18 Wh. At 3 W,
24 such cells hold about 220 Wh nominal; 80% usable is about 176 Wh, or 2.4 days.
At 5 W the same assumed pack lasts about 1.5 days. Four/eight cells hold only
about 37/73 Wh nominal. Cold, age, real capacity and protection cutoffs can
reduce these illustrative runtimes further. No existing holder wiring or cell
condition is inferred, and 24 is an energy example, not an approved topology.

Keeping 18650 cells is possible; a regulated higher-voltage router rail can
coexist with a 5 V Heltec rail. Exact pack, BMS, solar charger with load sharing,
low-voltage cutoff, converter efficiency and modem peak current need matching.
The [manufacturer reference sheet](https://wamtechnik.evebatteryusa.com/linked/inr18650-26v.pdf)
lists charging at 0 to 45 C for the referenced cell family. Use cell-temperature
charge inhibition below the actual cell's allowed limit; enclosure air telemetry
alone does not establish safe cell temperature. Temperature protection may also
prevent solar charging during cold daylight and must be included in autonomy.

Place the gateway where it has both working AT&T data and a useful LoRa path to
the mesh; it need not be at the tower or within cellular range of each member.
Cellular backhaul loss prevents fresh remote updates; do not promise full outage
replay. Local mesh viewing and truthful GPS age remain the pilot requirements.

Next useful step: an attended AT&T hotspot test at the candidate location, then
measure full-system idle/transmit/reconnect energy and overnight temperature.
Before unattended placement, verify power-on without a button after complete
depletion, AT&T and MQTT reconnection, and renewed fresh portal GPS receipts.
Choose the approved modem/SIM and power system from those results.

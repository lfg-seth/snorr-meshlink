# Cellular backhaul for a Kyle Canyon gateway

Research date: **2026-10-24**. Advice and candidate hardware only; no purchase,
service activation, site installation, hardware allocation or configuration change.

## Recommendation and existing evidence

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

## Hardware comparison

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

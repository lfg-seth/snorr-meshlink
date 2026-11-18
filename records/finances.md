# Project finances

Updated 2026-11-18. All amounts are in USD.

## 2026-11-18 - Spending review

**$1,682.07 in project spending is supported by the December 2025 Amazon
receipt.** Including the owner's provisional $158.31 battery amount would
bring the identified spend to **$1,840.38** if it was a separate project
purchase. Total spending to date remains unknown.

### Amazon order placed 2025-12-16

The final order details identify Southern Nevada Off Road Recovery as payer.
The three card charges dated December 16, 18 and 19 sum to $1,812.59, matching
the grand total and the sum of the 19 shipment totals. The order includes a
Lexar camera card that the historical list explicitly excludes from the mesh
project. Its $129.99 receipt price is used for the exclusion.

| Amount on receipt or allocated to the project | USD |
| --- | ---: |
| All merchandise | $1,791.88 |
| Shipping and handling | $28.21 |
| Promotions | −$7.50 |
| Sales tax | $0.00 |
| Total charged | $1,812.59 |
| Camera card merchandise | −$129.99 |
| Camera share of mixed shipment shipping | −$0.53 |
| Mesh project share | **$1,682.07** |

The receipt groups the camera card and project parts in one shipment with
$162.42 of merchandise and $0.66 of shipping. The camera's share is allocated
by merchandise value ($129.99 ÷ $162.42 × $0.66, rounded to $0.53). The
project retains $0.13 of that shipment's shipping and both receipt promotions,
which apply to other shipments containing project items.

| Receipted mesh spending | USD |
| --- | ---: |
| Radios — 10 RAK kits (5 RAK19003 Mini kits and 5 RAK19007/4631 kits), 6 OLED Heltec V4 boards and 4 V3 kits | $671.00 |
| Antennas, coax and mounts — 10 fiberglass antennas and 16 Muzi whips, plus accessories | $587.75 |
| Solar, client LiPo packs, 18650 holders, sensors and power leads | $206.76 |
| Filament, seal, fasteners, switches, USB-C jacks and solder | $159.36 |
| microSD cards and adapter | $37.02 |
| Mesh merchandise | **$1,661.89** |
| Project shipping less promotions | $20.18 |
| Total allocated project spending | **$1,682.07** |

Radios and antenna hardware account for $1,258.75, about 76% of mesh
merchandise. The mesh merchandise subtotal is $198.90 below the historical
list. The largest single difference is the $156.00 reference line for two
T-Decks, absent from this order even though they appear in
[inventory](inventory.md#first-confirmation-pass). Quantities and prices also
differ elsewhere, including the RAK mix and Muzi whip price. The receipt
includes two stand-alone LiPo line items (two 3,000 mAh and four 1,100 mAh
packs) as well as 18650 holders. No loose 18650 cells appear on it.

### Purchases awaiting amounts or receipts

- On 2026-11-18 the owner recalled **$158.31** for batteries. The review
  provisionally treats this as the separate loose-cell purchase associated with
  HW-002. The receipt, product, quantity, date, payer and any overlap with
  Amazon's LiPo lines need confirmation. The owner report is the evidence for
  the amount. The [inventory](inventory.md#first-confirmation-pass) records
  on-hand cells and does not establish a purchase quantity.
- The two screenless Heltec V4 gateways have an owner-confirmed purchase and
  an unknown price. The December receipt lists six OLED V4 boards.
- Receipt gaps also include the two T-Decks, other hardware beyond the December
  order, mounting and field expenses, and any project-billed hosting or
  backhaul. Reused equipment and hosting are documented in
  [inventory](inventory.md), with no project cash amount assigned. Check any
  refunds or reimbursements before attributing out-of-pocket spending.

## 2026-10-31 - Owner-reported gateway purchase

Owner confirms purchase of two screenless Heltec V4s with external Wi-Fi antenna
connections for primary fire-department gateways. Amount paid, currency, purchase
date, payer, taxes, shipping and receipt remain unknown. Evidence comes from
the owner conversation on 2026-10-31 and
[LOCAL-10](../.scratch/pilot/issues/29-gateway-sd-logging.md).

## Purchase-list baseline

Source: [Original purchase list](<../Mesh Purchase List - Purchase List.csv>), imported on 2026-10-12. Source line-item costs are reference amounts, not verified transactions, current prices, or valuations of stock remaining.

| Reference measure | Amount USD | Basis |
| --- | --- | --- |
| Source stated total | $1,989.79 | Header and source summary |
| Sum of all listed extended costs | $1,989.79 | Source rows 2–33, `Ext. Cost`; dash has no priced value |
| Camera item outside mesh project | $129.00 | Source row 33 explicitly says not part of mesh project |
| Mesh-project listed subtotal | $1,860.79 | All listed costs less camera item |
| Difference: summed costs minus stated total | $0.00 | Source reconciliation |

Do not add these amounts to the cash ledger or count them as new project spending without confirming purchase status, payer, dates, and evidence. The separate shipping field is ambiguous and has not been added to extended costs; taxes/shipping inclusion remains unconfirmed. Unknown 18650 quantities/cost totals and remaining stock prevent a complete current equipment valuation.

## Cash ledger

Planned acquisition, recorded 2026-10-12: owner intends to order 2 Heltec V4 member nodes with GPS and 3000mAh batteries and recover 2 existing member-held V4s with the same intended equipment. Evidence: owner response recorded in [Define useful tracking for the first field pilot](../.scratch/pilot/issues/02-pilot-needs.md). Price, shipping, tax, recovery costs, and payment status are unknown; no cash transaction or funding commitment recorded. Hardware reference: HW-013; battery reference: HW-010.

Use stable transaction IDs such as `TX-001`. Record actual positive amounts; the direction identifies money in or out. Keep planned costs out of this table. A purchase funded by a reimbursement and the reimbursement itself are separate entries linked in the notes.

| ID | Date | Direction (in/out) | Type (expense/funding/reimbursement/refund) | Description | Amount USD | Paid by / received by | Hardware or test ID | Receipt / evidence reference | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TX-001 | 2025-12-16 | out | expense | Amazon mesh hardware and supplies | $1,682.07 | Southern Nevada Off Road Recovery | Multiple | Private Amazon final order details, 2025-12-16, pp. 1–10 | Order date. Groups three card charges and excludes camera merchandise plus prorated camera shipping. See the [spending review](#2026-11-18---spending-review). |

## Existing equipment and in-kind support

Track donated or already-owned hardware separately from project cash expenditure. Record valuation only when supported by a stated source and date; do not count it twice as new spending.

| Contribution ID | Date recorded | Hardware ID / service | Quantity | Source / owner | Documented value USD or unknown | Valuation basis / evidence |
| --- | --- | --- | --- | --- | --- | --- |

## Budget and funding

2026-10-12 — Owner is open to larger member-node batteries to support the 4-hour minimum / 12-hour target runtime. Capacity, quantity, cost, and purchase timing are unspecified; this is a planning option, not a cash transaction or spending ceiling.

| Item | Status |
| --- | --- |
| Available project cash | Unknown |
| Approved spending ceiling | Not set |
| Historical expenses | December 2025 Amazon order reconciled. Other expenses and full project total remain open. |
| Grant applicant / legal entity | Not confirmed |
| Funding applications or awards | None recorded |

For grant reporting, reconcile expenses to receipts and distinguish requested, committed, and received funding. Keep original receipts in `private/receipts/` if they contain personal information and track the reference here; originals require their own backup.

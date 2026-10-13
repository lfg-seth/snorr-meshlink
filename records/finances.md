# Project finances

Updated: 2026-10-12. USD unless a row states otherwise. A historical purchase list has been supplied, but payment dates, receipts, actual amounts paid, and funding are unconfirmed. Empty cash records are **unknown**, not evidence of zero spending.

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

Use stable transaction IDs such as `TX-001`. Record actual positive amounts; the direction identifies money in or out. Keep planned costs out of this table. A purchase funded by a reimbursement and the reimbursement itself are separate entries linked in the notes.

| ID | Date | Direction (in/out) | Type (expense/funding/reimbursement/refund) | Description | Amount USD | Paid by / received by | Hardware or test ID | Receipt / evidence reference | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Existing equipment and in-kind support

Track donated or already-owned hardware separately from project cash expenditure. Record valuation only when supported by a stated source and date; do not count it twice as new spending.

| Contribution ID | Date recorded | Hardware ID / service | Quantity | Source / owner | Documented value USD or unknown | Valuation basis / evidence |
| --- | --- | --- | --- | --- | --- | --- |

## Budget and funding

| Item | Status |
| --- | --- |
| Available project cash | Unknown |
| Approved spending ceiling | Not set |
| Historical expenses | Purchase-list baseline recorded; actual payments and receipts unconfirmed |
| Grant applicant / legal entity | Not confirmed |
| Funding applications or awards | None recorded |

For grant reporting, reconcile expenses to receipts and distinguish requested, committed, and received funding. Keep original receipts in `private/receipts/` if they contain personal information and track the reference here; originals require their own backup.

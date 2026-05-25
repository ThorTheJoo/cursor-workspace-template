---
document_type: REFERENCE
status: ACTIVE
version: "1.0.0"
traceability_id: "FORENSIC-STARTER-DOCS-2026-05-24"
---

# Starter Docs — Forensic Analysis

**Site:** ENGEN JET PARK SERVICE STATION  
**Legal entity:** Fuel Rock (Pty) Ltd  
**POS system:** Ver 5.46k (fixed-width TXT exports)  
**Market:** South Africa (ZAR, VAT-inclusive shop, zero-rated fuel)

## File Inventory (21 files)

| File | Type | Period / Date | Primary Use |
|------|------|---------------|-------------|
| `Day End Summary.TXT` | Daily EOD | Batch 145 · 22/05/2026 | **Master daily report** — sales, wet stock, takings, cashiers |
| `Day End Summary (1).TXT` | Duplicate | Batch 143 · 20/05/2026 | Historical comparison |
| `Day End Summary (2).TXT` | Duplicate | Batch 143 · 20/05/2026 | Historical comparison |
| `Month End Summary.TXT` | Monthly | April 2026 (B92–B123) | MTD takings, cash variance, fuel control |
| `Monthly Summary Forecourt & Shop - By Category.TXT` | Monthly | April 2026 | Category GP breakdown |
| `EFT Batch Summary By EFT Batch Date.TXT` | EFT | 22/05/2026 | Card batch totals by forecourt/retail |
| `EFT Detail - By EOD Batch Number & Shift.TXT` | EFT | Batch 145 | Transaction-level card detail |
| `EFT Summary By EOD Batch & Shift.TXT` | EFT | Batch 145 | Shift-level EFT summary |
| `EFT Transactions Not Yet Sent to Bank.TXT` | EFT | Post-EOD pending | Unsent card trx (R3,056.05) |
| `Cash Variance - Selected EOD by Cashier.TXT` | Control | Batch 145 | Per-cashier cash reconciliation |
| `Stock Take Variance ... w POS Sales.TXT` | Inventory | 20/05/2026 | SKU-level stock count variance |
| `Nett Pay List - 140526.xls` | Payroll | Pay date 14/05/2026 | **16 employees · R32,095.27 net** |
| `Payment_CSV_Template.csv` | Banking | FNB BinSol v1.00 | Bulk payment import template |
| `Payment_CSV_Imports_Help_Guide_-_South_Africa_Oct_2015.pdf` | Banking | FNB SA guide | Field specs + hash total rules |
| `Schedule of Accounts Invoice T.xlsx` | Accounts | TBD | Creditor/supplier schedule |

## Canonical Data Model

```
canonicalize/data/canonical-latest.json
├── daily              ← latest Day End Summary (highest batch #)
├── daily_history      ← all non-duplicate day ends
├── monthly_april      ← Month End Summary
├── eft_batch          ← EFT Batch Summary
├── eft_pending        ← unsent card transactions
└── stock_take         ← stock variance summary
```

## Key Daily KPIs (Batch 145 · 22 May 2026)

| KPI | Value |
|-----|-------|
| Nett takings | R 183,805.24 |
| Fuel sales | R 162,086.30 (5,479.85 L) |
| Shop sales (incl VAT) | R 21,909.15 |
| Combined sales | R 184,470.45 |
| Cash variance | R 19.56 over |
| Fuel customers | 398 |
| Shop customers | 416 |
| Wet stock variance | UL93 -2.16 L · UL95 +3.42 L · DSL +20.59 L |

## Payroll → Payment CSV Mapping

**Source columns (Nett Pay List):**

| Col | Field |
|-----|-------|
| A | Employee Code (F0001…) |
| B | Employee Name |
| D | Pay Method (ACB) |
| E | Bank Name |
| F | Account Number |
| H | Branch Code (universal) |
| I | Nett Pay |

**Target columns (FNB Payment CSV / BinSol v1.00):**

| Row | Content |
|-----|---------|
| 1 | `BInSol - U ver 1.00` |
| 2 | Payment action date (`DD-MM-YYYY`) |
| 3 | Own account · Hash total |
| 4 | Column headers |
| 5+ | Recipient rows |

| CSV Col | Source |
|---------|--------|
| RECIPIENT NAME | Employee Name (max 20 chars) |
| RECIPIENT ACCOUNT | Account Number |
| RECI  ACCOUNT TYPE | 2=Savings (Capitec/African Bank), 1=Current (FNB/Nedbank) |
| BRANCHCODE | Universal branch code from payroll |
| AMOUNT | Nett Pay (2 decimals, period separator) |
| OWN REFERENCE | `FuelRock Payroll` |
| RECIPIENT REFERENCE | `Salary YYMMDD` |

**Hash total (FNB):** Sum all digits in recipient account numbers + add own account as integer → last 12 digits.

## Refresh Workflow

```powershell
# Drop new files into docs/_ai_context/inputs/ (or Starter Docs/ for POS)

# Payroll — all Nett Pay List files
python scripts/payroll/netpay_to_payment_csv.py --all

# Full dashboard (POS + bank + manual recon + payroll summary)
python scripts/management/generate_dashboard.py
```

---

## New Inputs (2026-05-24 refresh)

| File | Source Type | Notes |
|------|-------------|-------|
| `62848015857.ofx` | bank_feed | FNB Apr 2026 statement — account 62848015857 |
| `Nett Pay List - 140526.xls` | payroll_system | Pay date 14/05/2026 — R32,095.27 (16 staff) |
| `Nett Pay List - 210526.xlsx` | payroll_system | Pay date 21/05/2026 — R31,449.03 (16 staff) |
| `CASH UP APRIL 26.xlsx` | manual_recon | Petty cash analysis — month-end cash up |
| `Schedule of Accounts Invoice T.xlsx` | manual_recon | Supplier GRV log by department |
| `Schedule of Accounts Invoice T (1).xlsx` | manual_recon | Duplicate of above — use non-(1) copy |

### Source Classification Rules

1. **pos_system** — Fixed-width `.TXT` from ENGEN POS v5.46k (authoritative for daily ops)
2. **payroll_system** — Nett Pay List from payroll provider (authoritative for wages)
3. **bank_feed** — `.ofx` from FNB online banking (authoritative for cash movement)
4. **manual_recon** — Excel maintained by site (authoritative for adjustments & creditors)

Future recon workflow will match: POS EFT batches ↔ bank credits, payroll CSV ↔ bank debits, supplier schedule ↔ bank debits/payouts.

**Outputs (tested 2026-05-24):**
- `reports/payroll/Payment_140526.csv` — 16 employees · R32,095.27 · hash `062848016516`
- `reports/payroll/Payment_210526.csv` — 16 employees · R31,449.03 · hash `062848016516`
- `reports/management-dashboard.html` — includes tooltips (? icons) on every KPI
- `reports/data/canonical-latest.json`

## Before Live Payroll

1. Update `config/site.yaml` → `banking.nominated_account` with your real debit account
2. Verify hash total enabled/disabled in FNB Online Banking site settings
3. Import CSV via Payments → Add → Import

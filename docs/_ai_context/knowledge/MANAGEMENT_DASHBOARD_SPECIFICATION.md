---
document_type: GOVERNANCE
status: ACTIVE
traceability_id: "MGMT-DASHBOARD-SPEC-2026-05-24"
---

# Management Dashboard — Comprehensive Specification

**Output:** `reports/management-dashboard.html`  
**Generator:** `scripts/management/generate_dashboard.py`  
**Data:** `reports/data/canonical-latest.json` + payroll runs + `reports/data/file-repo-index.json`

---

## Purpose (business)

Single HTML view for the **fuel station owner / finance controller** to answer:

1. How did we trade yesterday and over recent days?
2. Is cash, card, and payroll reconciled to the bank?
3. Where are wet-stock, shrink, or cashier risks?
4. What files fed this view — and can I drill into history by report type?

---

## Sections (top to bottom)

| Section | Primary source | What it measures |
|---------|----------------|------------------|
| Primary trading day banner | POS Day End (latest batch) | Which day the snapshot KPIs refer to |
| Daily Operations Timeline | POS `daily_history` | Chronological nett takings, fuel L, shop, cash var, CIT (OCR) |
| Snapshot KPI cards | POS latest Day End + EFT batch file + stock take | One-day operational pulse |
| Data Source Legend | All source types | Colour tags: POS, bank, payroll, manual, OCR |
| Multi-Source Reconciliation | OCR + POS + bank + payroll | Match / review / pending matrix |
| Wet Stock EOD | POS latest Day End fuel grades | Pump vs tank litres per grade |
| Top categories / MTD fuel var | POS | Range and loss patterns |
| Cashier EOS exceptions | POS | Voids and nett by cashier |
| Monthly reference | POS Month End | April (or loaded month) baseline |
| Bank statement | FNB OFX | Ledger balance, Speedpoint in, wages out, daily credits |
| Supplier schedule | Manual Excel | Invoice spend by department |
| Cash Up workbook | Manual Excel | Sheet list / site title |
| OCR sections | WhatsApp synthesis | ATG, fuel daily, CIT, alerts |
| Daily history table | POS all batches | Compact history |
| Payroll | Nett Pay List → CSV | Latest run + all tested runs |
| **File Repository** | `file-repo-index.json` | Drill-down index by report type |
| Input file registry | Scan of inputs folder | Every file path classified |

---

## Calculations & rules

### Dates

- Display: **DD/MM/YYYY** (South African)
- Timeline sorted by trading day; deltas vs previous row

### Day End — nett takings

- Parsed from POS Day End Summary grand totals
- **Not** the same as bank deposits (cards settle later; cash may be CIT)

### EFT batch card

- From latest `EFT Batch Summary By EFT Batch Date` file (not necessarily same calendar day as latest Day End)
- Context line shows EFT batch date only (no erroneous batch number from Day End)

### Reconciliation status

| Status | Rule |
|--------|------|
| match | Absolute variance &lt; R0.02 or &lt; 1 L (fuel) |
| review | Variance exceeds threshold |
| pending | Missing counterpart data |
| ok / warn | Internal POS wet-stock ±25 L |

### Payroll vs bank

- Sum `Payment_*.csv` amounts (exclude `(1)` duplicate files)
- Match to bank `wage_runs` within **0–3 days** after pay date

### EFT vs Speedpoint

- POS EFT batch total vs bank Speedpoint daily credit within **0–3 days** after batch date (T+1 typical)

---

## Key callouts (owner checklist)

1. **Cash variance** on latest Day End — target &lt; R50  
2. **Pump–tank variance** per fuel grade — target ±25 L  
3. **Reconciliation matrix** — any row not MATCH  
4. **EFT pending** — large unsent card total at close  
5. **Bank ledger** — sudden drop vs prior period  
6. **OCR rows** — confirm before operational decisions  
7. **Missing batch** in timeline (e.g. B144) — request Day End file  

---

## Refresh workflow

```powershell
python scripts/management/build_file_repo.py
python scripts/management/generate_dashboard.py
python scripts/payroll/netpay_to_payment_csv.py --all   # optional
```

---

## Dependencies

| Script | Role |
|--------|------|
| `parse_reports.py` | POS TXT → canonical |
| `parse_external_inputs.py` | Bank, Excel, OCR, bank recons |
| `parse_ocr_whatsapp.py` | OCR synthesis |
| `build_file_repo.py` | Ledger + series + index |
| `generate_dashboard.py` | HTML assembly |
| `netpay_to_payment_csv.py` | Payroll CSV |

---

## Future enhancements

- Per-report-type detail pages with charts from `series/*.json`
- Auto-detect new drops in `inputs/Additional/`
- Parsers for cash variance, fuel ATG, shrinkage (see BACKLOG)

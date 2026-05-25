---
document_type: ANALYSIS
status: ACTIVE
traceability_id: "REFRESH-POS-2026-05-24"
---

# Refresh Folder — POS Drop Analysis

**Location:** `docs/_ai_context/inputs/Refresh/`  
**Source type:** `pos_system` (auto-generated ENGEN POS v5.46k exports)  
**Ingested:** 2026-05-24 — merged with `Starter Docs/` by batch number

## Files (10)

| File | Report | Batch / Date |
|------|--------|--------------|
| `Day End Summary (1).TXT` | Day End | **B141 · 18/05/2026** |
| `Day End Summary.TXT` | Day End | **B142 · 19/05/2026** |
| `Cash Variance - Selected EOD by Cashier.TXT` | Cash control | B142 |
| `Cash Variance - Selected EOD by Cashier (1).TXT` | Cash control | B141 |
| `EFT Batch Summary By EFT Batch Date.TXT` | EFT batch | Latest refresh |
| `EFT Detail - By EOD Batch Number & Shift.TXT` | EFT detail | B142 |
| `EFT Detail - By EOD Batch Number & Shift (1).TXT` | EFT detail | B141 |
| `EFT Summary By EOD Batch & Shift.TXT` | EFT summary | B142 |
| `EFT Summary By EOD Batch & Shift (1).TXT` | EFT summary | B141 |
| `EFT Transactions Not Yet Sent to Bank.TXT` | EFT pending | Post-EOD |

## Value Added

Fills the **18–19 May gap** in daily history. Timeline now runs B141 → B142 → B143 → B145 (B144 still missing — OCR WhatsApp has pump/tank for 21 May only).

## Daily KPIs (from Refresh Day End files)

| Batch | Date | Nett Takings | Fuel (L) | Shop Incl | Cash Var |
|-------|------|--------------|----------|-----------|----------|
| 141 | 18/05/2026 | R 185,823.99 | 5,788.51 | R 16,690.40 | R 0.00 |
| 142 | 19/05/2026 | R 104,790.45 | 3,191.23 | R 15,794.85 | R 0.00 |

## OCR Cross-Check (WhatsApp extract)

| Date | OCR fuel (L) | POS fuel (L) | Status |
|------|----------------|--------------|--------|
| 18/05/2026 | 5,788.51 | 5,788.51 (B141) | **MATCH** |
| 19/05/2026 | 3,191.23 | 3,191.23 (B142) | **MATCH** |

## Operational Notes

- **19 May (B142)** is a significantly quieter day — nett takings down **R 81k** vs 18 May (−44%). Worth noting for weekly pattern analysis (Sunday effect / holiday / supply issue — confirm with site).
- **Batch 144 (21 May)** not in Refresh or Starter Docs — only OCR pump/tank variance available until Day End file is dropped.

## Pipeline Change

`parse_reports.py` now scans both `Starter Docs/` and `Refresh/` (and dedupes by batch, preferring non-`(1)` copies).

```powershell
python scripts/management/generate_dashboard.py
```

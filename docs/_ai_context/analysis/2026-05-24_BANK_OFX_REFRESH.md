---
document_type: ANALYSIS
status: ACTIVE
traceability_id: "BANK-OFX-2026-05-24"
---

# Bank OFX Refresh — Analysis & Incorporation

**File:** `docs/_ai_context/inputs/Refresh/62848015857.ofx`  
**Source type:** `bank_feed` (FNB auto-export)  
**Ingested:** 2026-05-24

## Statement Summary

| Field | Value |
|-------|-------|
| Account | 62848015857 |
| Period | **30/04/2026 → 25/05/2026** |
| Ledger balance (25/05) | **R 256,236.86** |
| Transactions | 260 |
| Speedpoint credits | R 2,612,360.70 |
| Wage debits | R 116,416.82 |

Replaces the earlier April-only OFX (2026-04-01 to 2026-04-30). Pipeline now scans `inputs/` and `Refresh/` and picks the file with the latest `<DTEND>`.

## Reconciliation Results (automatic)

| Check | Source A | Source B | Status |
|-------|----------|----------|--------|
| Payroll 14/05/2026 | Payment_140526.csv · R 32,095.27 | Bank debits 16/05/2026 · R 32,095.27 | **MATCH** |
| Payroll 21/05/2026 | Payment_210526.csv · R 31,449.03 | Bank debits 22/05/2026 · R 31,449.03 | **MATCH** |
| EFT batch 18/05/2026 | POS · R 143,267.20 (384 trx) | Speedpoint credit 19/05/2026 · R 143,267.20 | **MATCH** (T+1 settlement) |

## Speedpoint vs POS trading days (May sample)

| Bank posted | Speedpoint credit |
|-------------|-------------------|
| 18/05/2026 | R 84,012.10 |
| 19/05/2026 | R 143,267.20 ← matches EFT batch for 18/05 trading |
| 20/05/2026 | R 73,434.90 |
| 21/05/2026 | R 121,361.05 |
| 22/05/2026 | R 137,933.40 |

Full day-by-day EFT↔Speedpoint matching for all POS batches is a natural next step.

## Pipeline Changes

- `parse_external_inputs.py`: `find_ofx_file()`, enhanced `parse_ofx()` (categories, wage runs, Speedpoint daily), `build_bank_reconciliations()`
- Reconciliation matrix: payroll and EFT rows now **match** instead of pending
- Dashboard bank section: ledger balance, wage runs, Speedpoint table

```powershell
python scripts/management/generate_dashboard.py
```

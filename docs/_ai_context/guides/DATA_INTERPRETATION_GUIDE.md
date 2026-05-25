---
document_type: GOVERNANCE
status: ACTIVE
traceability_id: "DATA-GUIDE-2026-05-24"
audience: "Site owner, finance, ops — no prior project context required"
---

# Data Interpretation Guide — ENGEN Jet Park

This guide explains **what each input file type means**, **how we process it**, **what the management report shows**, and **what to act on**. Technical paths are included for implementers.

---

## 1. The five money stories

| Story | Question | Main files |
|-------|----------|------------|
| **Trading** | How much did we sell today? | Day End Summary |
| **Cards** | Did card sales reach the bank? | EFT Batch Summary + bank Speedpoint |
| **Cash** | Is till cash correct? | Cash Variance, CASH UP, CIT (OCR) |
| **People** | Did wages leave the account correctly? | Nett Pay List + bank wage lines |
| **Stock** | Are we losing inventory or fuel? | Stock Take, Shrinkage, Fuel Sales Control |

Everything else (debtors, creditors, levy) supports **finance month-end**, not daily forecourt pulse.

---

## 2. Source types (trust levels)

| Tag | Meaning | Trust |
|-----|---------|-------|
| **POS System** | Auto-export from ENGEN POS v5.46k | Authoritative for sales & batches |
| **Bank Feed** | FNB OFX download | Authoritative for cash in/out |
| **Payroll** | Nett Pay List / Payment CSV | Authoritative for wages |
| **Manual Recon** | Excel you maintain | Authoritative for adjustments & invoices |
| **OCR / WhatsApp** | Photos → text extract | Confirm before acting |

---

## 3. File type quick reference

Detailed specs: `docs/_ai_context/knowledge/reference/file-type-catalog.yaml`

### Daily (operations)

**Day End Summary** — *The daily heartbeat*

- **Contains:** Batch number/date, shop categories, fuel litres & rand, nett takings, cash variance, cashier voids, wet-stock pump vs tank.
- **Example:** Batch 147, 24/05/2026 — use dashboard timeline row.
- **Value:** Day-on-day trends; primary KPI source.
- **Watch for:** Cash variance &gt; R50; fuel variance &gt; 25 L/grade.

**EFT Batch Summary** — *Cards sent to bank*

- **Contains:** Total card batch for an EFT batch date (Forecourt + Shop).
- **Example:** 18/05 batch R 143,267.20 → bank Speedpoint **19/05** R 143,267.20 (**MATCH**).
- **Value:** Proves card turnover landed in FNB.
- **Watch for:** Settlement &gt;2 days late.

**Cash Variance by Cashier** — *Till discipline*

- **Contains:** Per cashier/shift tender vs theoretical.
- **Status:** Classified; parser planned.
- **Value:** Finds training issues or theft patterns.

### Weekly / payroll

**Nett Pay List** → **Payment_*.csv**

- **Contains:** 16 employees, net pay, bank accounts.
- **Example:** Pay 21/05 → CSV R 31,449.03 → bank debit 22/05 R 31,449.03.
- **Value:** Payroll compliance; must match bank.

### Bank

**62848015857.ofx**

- **Contains:** All credits/debits; Speedpoint lines; wage debits; ledger balance.
- **Period loaded:** 30/04/2026 – 25/05/2026; balance **R 256,236.86** on 25/05.
- **Value:** Ground truth for cash; reconciles payroll & EFT.

### Monthly / inventory / accounting (Additional folder)

| File type | Business use |
|-----------|----------------|
| Month End Summary | Month KPIs, banking variance |
| Fuel Sales Control MTD | Wet-stock loss % by day |
| Stock Shrinkage MTD | Shop shrink trend |
| Stock Purchases | COGS / supplier spend |
| Turnover Levy | Head-office reporting |
| Debtors / Creditors | AR/AP and invoice variance |

Most are **catalogued**; parsers roll out by priority (see BACKLOG).

---

## 4. Management report — how to read it

Full spec: `MANAGEMENT_DASHBOARD_SPECIFICATION.md`

### Timeline (top)

- One row = one trading day (batch).
- **Δ Nett / Δ Fuel** = change vs previous day in table.
- Green/red = direction, not good/bad by itself (a quiet Sunday is legitimately red).

### Snapshot cards

- **Latest trading day only** (highest batch Day End).
- EFT card may show **different date** — that is the EFT batch date, not trading day.

### Reconciliation matrix

| Status | You should |
|--------|------------|
| **MATCH** | No action |
| **REVIEW** | Investigate variance |
| **PENDING** | Need more data (e.g. missing file) |

### File Repository section

- Lists each **report type** (not every duplicate filename).
- **Series points** = how many unique business periods we have extracted.
- Use with `reports/data/series/{type}.json` for history JSON.

---

## 5. Sample correlations (real values from this workspace)

| Check | A | B | Result |
|-------|---|---|--------|
| OCR fuel 18/05 | 5,788.51 L | POS B141 | MATCH |
| OCR fuel 19/05 | 3,191.23 L | POS B142 | MATCH |
| Payroll 14/05 | R 32,095.27 | Bank 16/05 | MATCH |
| Payroll 21/05 | R 31,449.03 | Bank 22/05 | MATCH |
| EFT 18/05 | R 143,267.20 | Speedpoint 19/05 | MATCH |
| Quiet day | B142 nett ~R 105k | B141 ~R 186k | −44% — verify reason |

---

## 6. When a new file arrives

1. Drop into `docs/_ai_context/inputs/Additional/` (or Refresh / Starter Docs).
2. Run:
   ```powershell
   python scripts/management/build_file_repo.py
   python scripts/management/generate_dashboard.py
   ```
3. Open catalog: find `report_type` in `file-type-catalog.yaml`.
4. Check ledger: `reports/data/ingest-ledger.json` for your filename and `content_key`.
5. Check series: `reports/data/series/{report_type}.json` for trend.
6. If duplicate `(1)` in name — safe to ignore if primary copy exists.

---

## 7. Glossary

| Term | Meaning |
|------|---------|
| Batch | POS end-of-day close number (e.g. 147) |
| EFT batch date | Date card payments were batched for bank |
| Speedpoint | FNB card settlement memo on bank statement |
| Nett takings | Total sales after returns (POS) |
| Wet stock | Fuel in tanks vs pump meters |
| CIT | Cash-in-transit pickup (OCR from photos) |
| content_key | Business id for history (not filename) |

---

## 8. Where to look in the repo

| Need | Path |
|------|------|
| File type specs | `docs/_ai_context/knowledge/reference/file-type-catalog.yaml` |
| Architecture | `docs/_ai_context/knowledge/FILE_INGESTION_ARCHITECTURE.md` |
| Dashboard spec | `docs/_ai_context/knowledge/MANAGEMENT_DASHBOARD_SPECIFICATION.md` |
| Ingest ledger | `reports/data/ingest-ledger.json` |
| History series | `reports/data/series/*.json` |
| Live dashboard | `reports/management-dashboard.html` |

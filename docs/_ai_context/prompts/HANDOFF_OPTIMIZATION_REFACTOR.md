---
document_type: PROMPT
status: ACTIVE
target_models: ["opus-4", "gpt-5", "claude-opus-4", "composer"]
purpose: Handoff for optimization, refactor, and hardening of Experiment JP reporting stack
traceability_id: "HANDOFF-2026-05-25"
---

# Handoff Prompt — Experiment JP Reporting Stack (Optimize / Refactor)

Copy everything below the line into a new session with a capable model (e.g. Opus 4.x, GPT-5.x). Workspace: **Experiment JP** — ENGEN Jet Park Service Station (Fuel Rock), South Africa.

---

## Mission

You are taking over a **local management reporting pipeline** that ingests multi-source operational files (POS TXT, bank OFX, payroll XLS, manual Excel, OCR WhatsApp synthesis) and produces:

1. **Management dashboard** — consolidated KPIs, timeline, reconciliations  
2. **File repository** — per-report-type drill-down with history, trends, per-file JSON detail, help guides  
3. **MDD documentation** — catalog specs, architecture, interpretation guide  

Your job: **optimize, refactor, harden, and extend** without breaking reconciliation logic or MDD governance. Be critical; propose improvements with trade-offs.

---

## Current architecture (do not break without migration plan)

### Three-layer data model (rejected: JSON per physical filename)

| Layer | Path | Role |
|-------|------|------|
| Catalog | `docs/_ai_context/knowledge/reference/file-type-catalog.yaml` | MDD spec per **report_type** |
| Ledger | `reports/data/ingest-ledger.json` | Every physical file drop |
| Series | `reports/data/series/{report_type}.json` | History by **content_key** (batch/date) |
| Snapshot | `reports/data/canonical-latest.json` | Dashboard fast path |

### HTML outputs

| Output | Generator |
|--------|-----------|
| `reports/management-dashboard.html` | `generate_dashboard.py` |
| `reports/file-views/index.html` + `{report_type}.html` | `generate_file_views.py` |
| `reports/help/management-dashboard.html` + `{report_type}.html` | `generate_file_views.py` (from catalog + MD spec) |

### Refresh pipeline (run in order)

```powershell
cd "C:\Temp\Experiment JP"
python scripts/management/build_file_repo.py
python scripts/management/generate_file_views.py
python scripts/management/generate_dashboard.py
python scripts/payroll/netpay_to_payment_csv.py --all
```

---

## What was built (session history summary)

### Phase 1 (prior)
- POS parser for Day End, Month End, EFT batch, EFT pending, Stock take  
- Bank OFX parser (Refresh folder, May 2026 statement)  
- Payroll → FNB Payment CSV; payroll↔bank MATCH  
- OCR WhatsApp synthesis; fuel/shop vs POS MATCH  
- Multi-source reconciliation matrix on dashboard  

### Phase 2 (2026-05-25)
- **Additional/** folder: 43 files, 22 report patterns (accounting, inventory, extended POS)  
- `file_classifier.py`, `build_file_repo.py`, `catalog_loader.py`, `generate_file_views.py`  
- Drill-down: click report type → trend table + all files + click row → JSON detail panel  
- Help: inline toggle + `reports/help/*.html` from catalog and dashboard spec  
- Fixed duplicate detection: only `(1)` suffix = Windows duplicate; `(2)…(6)` in Additional = distinct batches  
- Day End series now: B141, B142, B143, B145, B147 (B144 still missing)  

### Validated reconciliations
- Payroll 14/05 → bank 16/05: R 32,095.27 MATCH  
- Payroll 21/05 → bank 22/05: R 31,449.03 MATCH  
- EFT batch 18/05 → Speedpoint 19/05: R 143,267.20 MATCH  

---

## Known gaps (prioritize)

1. **12+ report types** catalogued but not parsed (cash variance by cashier, fuel ATG, shrinkage, debtors, creditors, levy, EFT detail, etc.)  
2. **Batch 144** (21 May) — no Day End file anywhere  
3. **Day End file naming** — `(2)` in Additional = batch 147, not duplicate; fragile if more naming conventions appear  
4. **Dashboard** uses inline CSS; file-views use `site.css` — inconsistent styling  
5. **No automated tests** for parsers or reconciliation  
6. **Large inputs/** in git — may need LFS or sample-only policy for private repo  
7. **repo-manifest.json** is hand-maintained — could be generated from scripts  

---

## MDD files to respect (authority order)

1. `docs/_ai_context/knowledge/reference/file-type-catalog.yaml` — domain truth for report types  
2. `docs/_ai_context/knowledge/reference/input-source-registry.yaml`  
3. `docs/_ai_context/state/MASTER_STATE.md`, `WORK_LOG.md`, `BACKLOG.md`  
4. `FILE_INGESTION_ARCHITECTURE.md`, `MANAGEMENT_DASHBOARD_SPECIFICATION.md`  
5. `guides/DATA_INTERPRETATION_GUIDE.md`  

Human approval required for semantic changes to knowledge YAML.

---

## Suggested optimization targets (pick based on ROI)

### A. Parsers (high business value)
- `cash_variance_by_cashier` — daily till accountability  
- `fuel_control_mtd_summary` / `fuel_control_atg` — wet-stock loss  
- `stock_shrinkage_mtd` — C-store shrink trend  
- Extend `build_file_repo.extract_summary()` for each  

### B. UX
- Sparkline charts in file-views (CSS or lightweight chart lib, no npm if possible)  
- Unified nav component across dashboard + file-views  
- Search/filter on file repository index  

### C. Engineering
- Single `refresh_all.py` orchestrator  
- pytest for `parse_day_end`, `parse_ofx`, `build_series`, reconciliation matchers  
- Type hints + mypy on `scripts/management/`  
- Export `file-type-catalog.json` from YAML for non-Python consumers  

### D. Git / ops
- `.gitattributes` for large binaries (images, zip)  
- GitHub Action: validate parsers on sample fixtures  
- Private repo: `Experiment-JP` on GitHub  

---

## Key code entry points

```
scripts/management/parse_reports.py       # POS canonical + daily_history
scripts/management/parse_external_inputs.py  # bank, excel, bank recons
scripts/management/parse_ocr_whatsapp.py  # OCR + reconciliation rows
scripts/management/build_file_repo.py     # ledger + series
scripts/management/generate_file_views.py # Phase 2 drill-down HTML
scripts/management/generate_dashboard.py  # main dashboard
scripts/payroll/netpay_to_payment_csv.py
config/site.yaml                          # nominated account 62848015857
```

---

## Sample data anchors (for regression)

| Anchor | Value |
|--------|-------|
| Account | 62848015857 |
| Latest batch | 147 · 24/05/2026 · nett R 71,895.05 |
| Bank ledger 25/05 | R 256,236.86 |
| Payroll hash row | 062848016516 (FNB hash, not account) |

---

## Constraints

- Dates: **DD/MM/YYYY** display  
- South African Rand formatting: `R 1,234.56`  
- Minimize scope creep; atomic commits per feature  
- Update `WORK_LOG.md` after non-trivial changes  
- Do not force-push `main`/`master` without explicit user request  

---

## Success criteria for your session

1. Identify top 3 refactors with measurable benefit (performance, correctness, UX, maintainability).  
2. Implement at least one high-ROI parser OR test suite OR UX improvement.  
3. Keep all existing MATCH reconciliations passing.  
4. Update MDD docs to match code.  
5. Leave a short `docs/_ai_context/analysis/YYYY-MM-DD_OPTIMIZATION_SESSION.md` with findings.  

---

## Questions to answer in your first response

1. What is the weakest part of the current architecture after Phase 2?  
2. Should series history move to SQLite/DuckDB, or is JSON sufficient at this scale (~150 files, ~30 types)?  
3. What is the safest order to add parsers without breaking `content_key` contracts?  

Begin by reading `MASTER_STATE.md`, `file-type-catalog.yaml`, and running the refresh pipeline once to verify baseline.

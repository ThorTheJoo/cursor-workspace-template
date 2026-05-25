---
document_type: ANALYSIS
status: ACTIVE
traceability_id: "ADDITIONAL-FILE-REPO-2026-05-24"
---

# Additional Folder + File Repository — Analysis

## Additional folder summary

**Path:** `docs/_ai_context/inputs/Additional/`  
**Files:** 43 physical · **22 unique report patterns** · **28 classified report types**

### New trading days (Day End)

| Batch | Date | Nett takings | Notes |
|-------|------|--------------|-------|
| 147 | 24/05/2026 | R 71,895.05 | From `Day End Summary (2).TXT` — now latest snapshot |
| 141–143 | 18–20 May | (in Refresh too) | Duplicates OK — deduped by batch |

**Gap remains:** Batch **144** (21 May) — not in any folder.

### Report types not yet parsed (priority for BACKLOG)

1. Cash Variance by Cashier — daily accountability  
2. EFT Summary/Detail by shift — card audit  
3. Fuel Sales Control (MTD / ATG) — wet-stock loss  
4. Stock Shrinkage / Purchases — inventory finance  
5. Debtors / Creditors / Turnover Levy — month-end accounting  

---

## File repository delivered

| Artifact | Purpose |
|----------|---------|
| `file-type-catalog.yaml` | MDD spec per **report type** (business + technical) |
| `FILE_INGESTION_ARCHITECTURE.md` | Why not JSON-per-filename; 3-layer model |
| `MANAGEMENT_DASHBOARD_SPECIFICATION.md` | Full dashboard spec |
| `DATA_INTERPRETATION_GUIDE.md` | Owner-readable guide with samples |
| `build_file_repo.py` | Ledger + series + index |
| `file_classifier.py` | Pattern → report_type_id |
| `ingest-ledger.json` | Every file drop (145 files) |
| `series/*.json` | History by content_key (28 types) |
| `file-repo-index.json` | Dashboard drill-down index |

### JSON-per-file verdict

**Not recommended** as primary storage. Use **content_key** (batch/date/period) in append-only **series** files instead. Physical duplicates `(1)(2)` stay in ledger with `is_duplicate_copy: true`.

---

## Pipeline changes

- `parse_reports.py` scans **Starter Docs + Refresh + Additional**
- `pick_latest_day_end` uses **highest batch**, not filename suffix
- Dashboard includes **File Repository** section + auto-runs `build_file_repo.py`

---

## Validation

- Ledger: 145 files, 93 primary  
- Day End series: batches 141, 142, 143, 145, 147  
- Latest snapshot: **B147 · 24/05/2026** after parser fix  

```powershell
python scripts/management/build_file_repo.py
python scripts/management/generate_dashboard.py
```

---
document_type: GOVERNANCE
status: APPROVED
traceability_id: "FILE-REPO-ARCH-2026-05-24"
---

# File Ingestion Architecture — Plan & Critical Review

## Business objective

Receive files from POS, bank, payroll, accounting, inventory, OCR, and manual recons on **varying cadence** (daily / weekly / monthly / ad hoc). For each **report type**, maintain:

1. **What it means** (MDD spec — `file-type-catalog.yaml`)
2. **What we received** (ingest ledger — every drop, including duplicates flagged)
3. **How metrics evolved** (time series — keyed by batch/date/period, not filename)
4. **How it rolls up** (management dashboard — consolidated view + drill-down)

---

## Challenge to “one JSON per physical file”

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **JSON per filename** | Simple mental model | Explodes with `(1)(2)` copies; same batch in 3 folders = 3 “truths”; hard to trend; large blobs | **Reject as primary store** |
| **JSON per report type (latest only)** | Small | Loses history when new file arrives | **Reject alone** |
| **Append-only ledger + typed series** | History preserved; dedupe by `content_key`; drill-down by type | Needs discipline on keys | **Recommended** |
| **Single canonical-latest.json** | Fast dashboard | Not a file-level repo | **Keep as snapshot layer** |

### Recommended three-layer model

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: file-type-catalog.yaml (MDD — WHAT each type is) │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: ingest-ledger.json (every physical file drop)      │
│  + content_key + is_duplicate_copy + summary extract         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: series/{report_type}.json (history by business id) │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: canonical-latest.json (dashboard snapshot)         │
└─────────────────────────────────────────────────────────────┘
```

**content_key examples**

| Report type | content_key |
|-------------|-------------|
| Day End | `day_end\|batch:147\|date:24/05/2026` |
| EFT batch | `eft_batch\|date:18/05/2026` |
| Bank OFX | `bank\|account:62848015857\|file:62848015857.ofx` |
| Payroll | `payroll\|period:210526` |

---

## Additional folder (2026-05-24)

43 files, **22 unique report patterns**. Highlights:

| Finding | Action |
|---------|--------|
| Day End B141–B147 (incl. **B147 / 24 May**) | `parse_reports` now scans `Additional/` |
| B143 duplicate `(5)` vs `(6)` | Ledger marks duplicate; series keeps one |
| 12 report types unparsed | Catalog spec ready; parsers phased in BACKLOG |
| Accounting (debtors, creditors, levy) | New `accounting` source — monthly finance |

---

## Drill-down in management report

**Phase 1 (done):** File Repository section on dashboard — links to `reports/file-views/`.

**Phase 2 (done):** `reports/file-views/{report_type}.html` — historic trend, all files table, click-row file JSON detail, inline help from catalog, `reports/help/*.html`.

**Phase 3:** Sparklines, parsers for classified-only types, optional SQLite if series exceed ~500 points.

**Phase 4:** Watch folder / CI on new drops.

---

## Operational commands

```powershell
# Rebuild file repo (ledger + series + index)
python scripts/management/build_file_repo.py

# Refresh dashboard + POS canonical (includes Additional/)
python scripts/management/generate_dashboard.py
```

---

## Regression & governance

- Catalog changes (Rank 1 knowledge): human approval for semantic changes
- New report type: add to `file-type-catalog.yaml` + `file_classifier.py` + optional parser
- WORK_LOG entry per ingest batch

---

## Flaws & risks

| Risk | Blast radius | Mitigation |
|------|--------------|------------|
| Wrong content_key | Wrong history merge | Validate keys in build_file_repo; log collisions |
| Unparsed types in series | Empty drill-down | Show `parser_status: not_implemented` in UI |
| OFX replaced | Old bank series stale | Key OFX by period end date; supersede in ledger |

**Weakest part:** Twelve Additional report types have specs but no extractors — drill-down will show “classified only” until phased parsers land.

**Alternative considered:** SQLite warehouse — better at scale; rejected for now (team size, file count <500) — JSON + YAML sufficient.

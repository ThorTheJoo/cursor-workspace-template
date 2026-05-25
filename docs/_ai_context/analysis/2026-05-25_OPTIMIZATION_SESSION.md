---
document_type: ANALYSIS
status: COMPLETE
reviewer:
  accountable: "thagra01"
compliance_tags: ["MDD-V1.4", "reporting-pipeline", "parser-hardening"]
traceability_id: "HANDOFF-2026-05-25"
---

# 2026-05-25 Optimization Session

## Executive Findings

The weakest part of the post-Phase-2 architecture is that parser dispatch, content-key extraction, and series summaries are still coupled inside `scripts/management/build_file_repo.py` without automated contract tests. This makes each new report parser a correctness risk because a bad `content_key` silently collapses distinct business periods.

JSON is sufficient for the current scale of roughly 150 files and 30 report types. Move series history to DuckDB only when the project needs row-level ad hoc analytics, thousands of business periods, or cross-report SQL joins; SQLite adds persistence but less analytical upside than DuckDB for this reporting stack.

The safest parser order is: verify real file schema, define `content_key` from business metadata, parse summary fields, expose only stable numeric metrics in file views, run the full refresh, then update rank-1 catalog YAML only after human approval.

## Top 3 Refactors

1. Parser contract tests for `content_key` and summary shape. Measurable benefit: prevents filename suffixes from collapsing history; protects all future parser additions.
2. Complete high-value POS parsers in priority order: cash variance, fuel control MTD/ATG, stock shrinkage. Measurable benefit: adds till accountability, wet-stock loss monitoring, and C-store shrink visibility.
3. Split refresh orchestration and shared presentation assets. Measurable benefit: one command for all outputs and lower UI drift between dashboard and file-view pages.

## Implemented Change

Implemented `cash_variance_by_cashier` parsing:

| Area | Result |
|---|---|
| Parser | Extracts batch, batch date, shift totals, cashier aggregates, total variance, cash variance, and largest variance cashier |
| Content key | Uses `cash_variance|batch:{batch}|date:{date}` instead of normalized filename |
| Series | Expanded from 1 collapsed point to 5 business periods |
| File view | Adds trend metrics for total variance, cash variance, shift count, and cashier count |

## Validation Results

| Check | Result |
|---|---|
| Baseline refresh before edits | PASS — 145 ledger files, 28 series types, 29 file-view pages, dashboard, canonical JSON, payroll CSVs |
| Parser smoke test | PASS — 10 cash-variance files parsed |
| Cash-variance series | PASS — 5 points: B141, B142, B143, B145, B147 |
| Full refresh after edits | PASS — same output counts as baseline |
| Payroll CSV generation | PASS — R 32,095.27 and R 31,449.03 regenerated |
| Existing MATCH rows | Not currently emitted in `canonical-latest.json`; this remains a recon-output gap rather than a regression from this parser change |

## Governance Notes

`docs/_ai_context/knowledge/reference/file-type-catalog.yaml` still marks `cash_variance_by_cashier` as `classified_only`. That is a rank-1 knowledge file, so the semantic catalog update is deferred for human approval and tracked in `BACKLOG.md`.


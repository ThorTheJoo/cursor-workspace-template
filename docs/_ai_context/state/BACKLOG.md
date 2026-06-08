---
document_type: STATE
status: ACTIVE
last_groomed: 2026-03-29
---

# Project Backlog

## Open Items

### P0 - Blocking
- [ ] Create or provide private GitHub remote `Experiment-JP` and push local commits – `gh` is unavailable and `https://github.com/ThorTheJoo/Experiment-JP.git` returned repository not found. (source: AGENT-OS-HANDOFF-2026-06-08).

### P1 - Next Sprint
- [ ] Parser: Supplier invoice/AP reconciliation using real invoice + schedule + bank samples – implement only after sample-backed schema verification. (source: AGENT-OS-HANDOFF-2026-06-08).
- [ ] Parser: Fuel Sales Control MTD + ATG → wet-stock trend series. (source: same).
- [ ] Parser: Stock Shrinkage MTD + Purchases → inventory KPI section. (source: same).
- [ ] Parser: EFT Summary/Detail by shift — optional txn-level audit. (source: same).
- [ ] Parser: Debtors / Creditors / Turnover Levy — accounting month-end panel. (source: same).
- [ ] File drill-down UI: sparklines from `reports/data/series/*.json` per report type. (source: FILE_INGESTION_ARCHITECTURE.md Phase 2).
- [ ] Create repo-manifest.json generator script per V1.3 Sniper Mode. (source: MDD V1.3 Section 1.4).

### P2 - Backlog
- [ ] Governance: Promote agent OS workflow contract into Rank-1 knowledge docs after human review. (source: AGENT-OS-HANDOFF-2026-06-08).
- [ ] Knowledge catalog approval: update `cash_variance_by_cashier` parser metadata/key fields after human review. (source: 2026-05-25_OPTIMIZATION_SESSION.md).
- [ ] Create .cursor/settings.json with recommended Cursor preferences. (source: improvement plan WS-002).
- [ ] Add V1.3 migration guide for V1.2 workspaces. (source: WORK_LOG v2.0.0 lessons).
- [ ] Add GitHub Actions CI template with secret scanning (gitleaks/TruffleHog). (source: security hardening v2.3.0).
- [ ] Add `npm audit` / dependency scanning step to CI template. (source: security hardening v2.3.0).

### P3 - Wishlist
- [ ] Auto-generate AGENTS.md from repo-manifest.json. (source: V1.3 Sniper Mode).
- [ ] Add GitHub Actions CI for manifest validation. (source: enterprise polish).
- [ ] Create example .cursor/skills/ seed showing skill file structure. (source: cohesion audit v2.1.0).

---

## Resolved
- [x] Parser: Cash Variance by Cashier → series + dashboard drill-down. Resolved: 2026-05-25, `cash_variance_by_cashier` parser added; series now B141/B142/B143/B145/B147. (source: 2026-05-24_ADDITIONAL_FOLDER_AND_FILE_REPO.md).
- [x] Create PROMPT_INDEX.md entry point for prompt discovery. (source: MDD V1.3 Section 15). Resolved: 2026-03-29, created as prompts/PROMPT_INDEX.md.
- [x] Create MULTI_PHASE_EXECUTION_GUIDELINES.md in prompts/phases/. (source: MDD V1.3 Section 6). Resolved: 2026-03-29, created as prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md.
- [x] Add knowledge governance files (GOVERNANCE_POLICY.md, PENDING_UPDATES.yaml). (source: MDD V1.3 Section 9). Resolved: 2026-03-29, created full governance pipeline.
- [x] Wire continuous improvement / feedback loop into reference architecture. (source: cohesion audit v2.1.0). Resolved: 2026-03-29, CONTINUOUS_IMPROVEMENT_PROTOCOL.md + rule Section 11 wiring.
- [x] Create CONTEXT_MANIFEST.md referenced by rule Section 1. (source: cohesion audit v2.1.0). Resolved: 2026-03-29, created as prompts/phases/CONTEXT_MANIFEST.md.
- [x] Fix bootstrappers to create all 11 MDD subdirs (not just 5). (source: cohesion audit v2.1.0). Resolved: 2026-03-29, both scripts updated.
- [x] Add pre-commit hook guidance (husky/gitleaks) for secret scanning. (source: worktree forensic analysis). Resolved: 2026-03-29, documented in SECURITY_CONTROLS.md Section 1.4. Per-project setup -- template provides instructions and .husky template.

## Deprecated / Closed
(none yet)

---
document_type: ANALYSIS
status: ACTIVE
traceability_id: "TEMPLATE-PORTABLE-LEARNINGS-2026-07-20"
---

# Portable Learnings Injection (from Cutover workspace)

## Critical finding

This repository's **README/AGENTS advertise a clean Cursor workspace template**, but
`docs/_ai_context/state/` currently holds a live **Experiment JP / ENGEN Jet Park**
project (POS/payroll/recon). Template rules/skills remain valuable; state is polluted.

**Recommendation (human decision):** either (a) split Engen JP into its own repo and
reset `docs/_ai_context/state/*` from `templates/REPO_MANIFEST_V2.template.json`, or
(b) keep this as a dual-use repo and always seed new projects from the `templates/`
files — never clone `state/` blindly.

## What was injected (this branch)

| Artifact | Purpose |
|----------|---------|
| `.cursor/rules/governance/external-write-guard.mdc` | Consent before remote mutations |
| `scripts/lib/external_write_guard.py` | Env-flag enforcement helper |
| `scripts/verify_script_registry.js` | MASTER_STATE Script Registry path check |
| `docs/_ai_context/templates/HANDOFF_PROMPT_TEMPLATE.md` | Gate 0 + triple-index handoffs |
| `docs/_ai_context/templates/REPO_MANIFEST_V2.template.json` | sniper + sub_projects schema |
| `docs/_ai_context/prompts/AGENT_INITIAL_PRELOADER.md` | 5-file session stack |
| Updates to `01-mdd.mdc`, context-loading skill, SESSION_START, PROMPT_INDEX, ANTI_PATTERNS, CHANGELOG, AGENTS |

## Source

Cutover Planner workspace forensic scan 2026-07-20 (manifest v4.x patterns, ADO write guard generalization, handoff Gate 0, verify_script_registry).

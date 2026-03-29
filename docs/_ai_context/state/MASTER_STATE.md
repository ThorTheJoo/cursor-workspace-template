---
document_type: STATE
status: APPROVED
reviewer:
  accountable: "thagra01"
compliance_tags: ["CSG-AI-Policy", "MDD-V1.3", "King-Mode"]
traceability_id: "WS-001-cursor-workspace-starter"
---

# MASTER_STATE.md

**Last Updated:** 2026-03-29
**Version:** 2.2.0

## Current Workspace State

**Cursor Workspace Starter** template repository (v2.1.0). Portable, zero-global-pollution foundation for Cursor IDE workspaces. Powered by MDD V1.3 (Agentic Critical Edition) with full artifact suite, continuous improvement loop, and 8 curated agent skills.

### Core Components

| Component | Status | Version | Notes |
|---|---|---|---|
| `.cursor/rules/00-starter-rules.mdc` | Active | 2.0.0 | Thin orchestrator: loading order + priority resolution |
| `.cursor/rules/01-mdd.mdc` | Active | 1.3.0 | MDD V1.3 with cross-referenced knowledge/templates |
| `.cursor/rules/02-kingmode.mdc` | Active | 1.1.0 | King Mode: ULTRATHINK, intentional minimalism |
| `.cursor/rules/03-frontend-fullstack.mdc` | Active | 1.1.0 | Stack conventions only (no duplication) |
| `tools/manifest.json` | Valid | - | 5 tools defined, JSON validated |
| `setup-tools.sh` / `setup-tools.ps1` | Enhanced | - | Creates all 11 MDD dirs + validates manifest |
| `.cursor/skills/` | Complete | - | 8 curated skills (committed, not bootstrapper-dependent) |
| `docs/_ai_context/` | Complete | - | Full V1.3 structure (11 subdirs, 35+ artifacts) |

### Rule Hierarchy (Zero Duplication)

```
00-starter-rules.mdc  (orchestrator: loading order + paths)
  +-- 01-mdd.mdc       (process: V1.3 Sniper Mode, Ask/Plan/Agent, P-R-I-L-L, 14 governance rules)
  +-- 02-kingmode.mdc   (design: minimalism, ULTRATHINK, library discipline)
  +-- 03-frontend-fullstack.mdc  (implementation: Next.js, tRPC, Shadcn, Zod)
```

Priority: MDD (01) wins on process. King Mode (02) wins on design. Full-Stack (03) wins on implementation.

### Wiring Summary

| Layer | Artifacts | Wired To |
|---|---|---|
| Rules (behavioral) | 4 .mdc files | Cross-reference knowledge/templates via inline refs |
| Knowledge (reference) | 7 docs (triage, modes, anti-patterns, governance, improvement, manifest spec, feature spec) | Referenced by rules + templates |
| Templates (artifact generation) | 9 templates (plan, pre-plan, completion, debug, runbook, ADR, 3 response formats) | Used by P-R-I-L-L workflow |
| Prompts (reusable) | SESSION_START, PROMPT_INDEX, CONTEXT_MANIFEST, MULTI_PHASE_GUIDELINES | Referenced by rules + knowledge |
| State (SSOT) | MASTER_STATE, WORK_LOG, BACKLOG, repo-manifest.json | Updated by every non-trivial task |
| Governance (feedback loop) | CONTINUOUS_IMPROVEMENT_PROTOCOL, PENDING_UPDATES, UPDATE_HISTORY, ROLLBACK_LOG, GOVERNANCE_POLICY | Triggered after every task (Learn step) |
| Skills (agent capabilities) | 8 SKILL.md files (skill-creator, doc-coauthoring, frontend-design, webapp-testing, mcp-builder, docx, pdf, xlsx) | Triggered by description match; wired to King Mode, MDD Learn Step, MCP dir |
| Bootstrappers | setup-tools.sh/ps1 | Create all 11 dirs + validate manifest + install tools |

### Architecture Decisions

* ADR template: `docs/_ai_context/templates/ADR_TEMPLATE.md`
* V1.3 feature specification: `docs/_ai_context/knowledge/MDD_V1.3_FEATURE_SPECIFICATION_SUMMARY.md`
* V1.3 rule source: `docs/_ai_context/knowledge/MDD_V1.3_GENERIC_RULE_SOURCE.mdc`

### Constraints

* Rules 01-03 are non-optional and take priority over tool-specific rules.
* `.tools-cache/` is gitignored.
* All workspace configuration stays local.
* Knowledge files (Rank 1 per V1.3 Authority Hierarchy) require human approval to modify.
* Continuous Improvement Protocol runs after every non-trivial task (P-R-I-L-L).

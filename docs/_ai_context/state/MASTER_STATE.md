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
**Version:** 2.0.0

## Current Workspace State

**Cursor Workspace Starter** template repository (v2.0.0). Portable, zero-global-pollution foundation for Cursor IDE workspaces. Now powered by MDD V1.3 (Agentic Critical Edition).

### Core Components

| Component | Status | Version | Notes |
|---|---|---|---|
| `.cursor/rules/00-starter-rules.mdc` | Active | 2.0.0 | Thin orchestrator: loading order + priority resolution |
| `.cursor/rules/01-mdd.mdc` | Active | 1.3.0 | MDD V1.3 Agentic Critical Edition |
| `.cursor/rules/02-kingmode.mdc` | Active | 1.1.0 | King Mode: ULTRATHINK, intentional minimalism |
| `.cursor/rules/03-frontend-fullstack.mdc` | Active | 1.1.0 | Stack conventions only (no duplication) |
| `tools/manifest.json` | Valid | - | 5 tools defined, JSON validated |
| `setup-tools.sh` / `setup-tools.ps1` | Enhanced | - | Manifest validation, MDD dir creation |
| `docs/_ai_context/` | Complete | - | Full V1.3 structure (11 subdirs) |

### Rule Hierarchy (Zero Duplication)

00-starter-rules.mdc  (orchestrator: loading order + paths)
  +-- 01-mdd.mdc       (process: V1.3 Sniper Mode, Ask/Plan/Agent, P-R-I-L, 14 governance rules)
  +-- 02-kingmode.mdc   (design: minimalism, ULTRATHINK, library discipline)
  +-- 03-frontend-fullstack.mdc  (implementation: Next.js, tRPC, Shadcn, Zod)

Priority: MDD (01) wins on process. King Mode (02) wins on design. Full-Stack (03) wins on implementation.

### Architecture Decisions

* ADR template: `docs/_ai_context/templates/ADR_TEMPLATE.md`
* V1.3 feature specification: `docs/_ai_context/knowledge/MDD_V1.3_FEATURE_SPECIFICATION_SUMMARY.md`
* V1.3 rule source: `docs/_ai_context/knowledge/MDD_V1.3_GENERIC_RULE_SOURCE.mdc`

### Constraints

* Rules 01-03 are non-optional and take priority over tool-specific rules.
* `.tools-cache/` is gitignored.
* All workspace configuration stays local.
* Knowledge files (Rank 1 per V1.3 Authority Hierarchy) require human approval to modify.

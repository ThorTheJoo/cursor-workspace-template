---
document_type: STATE
status: APPROVED
reviewer:
  accountable: "thagra01"
compliance_tags: ["CSG-AI-Policy", "MDD-V1.4", "King-Mode"]
traceability_id: "WS-001-cursor-workspace-starter"
---

# MASTER_STATE.md

**Last Updated:** 2026-03-31
**Version:** 2.5.0

## Current Workspace State

**Cursor Workspace Starter** template repository (v2.5.0). Portable, zero-global-pollution foundation for Cursor IDE workspaces. Powered by MDD V1.4 (fat router + skills) with full artifact suite, continuous improvement loop, 8 curated agent skills, and 9 portable MDD methodology skills.

### Core Components

| Component | Status | Version | Notes |
|---|---|---|---|
| `.cursor/rules/00-starter-rules.mdc` | Active | 2.0.0 | Thin orchestrator: loading order + priority resolution |
| `.cursor/rules/01-mdd.mdc` | Active | 1.4.0 | Fat router: always-on behavioral floor + security constraints + skill routing |
| `.cursor/rules/02-kingmode.mdc` | Active | 1.1.0 | King Mode: ULTRATHINK, intentional minimalism |
| `.cursor/rules/03-frontend-fullstack.mdc` | Active | 1.1.0 | Stack conventions only (no duplication) |
| `tools/manifest.json` | Valid | - | 5 tools defined, JSON validated |
| `setup-tools.sh` / `setup-tools.ps1` | Enhanced | - | Creates all 11 MDD dirs + validates manifest |
| `.cursor/skills/` | Complete | - | 8 curated skills + 9 portable MDD skills (committed) |
| `docs/_ai_context/` | Complete | - | Full V1.4 structure (11 subdirs, 35+ artifacts) |

### Rule Hierarchy (Zero Duplication)

```
00-starter-rules.mdc  (orchestrator: loading order + paths)
  +-- 01-mdd.mdc       (process: V1.4 fat router — behavioral floor + security + skill routing)
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
| Security (defense-in-depth) | SECURITY_CONTROLS.md, 10 security anti-patterns, .gitignore (40+ patterns), .env.example, SECURITY.md, bootstrapper hardening | Enforced by 01-mdd.mdc Section 6 (always-on) + wired into all templates |
| Governance (feedback loop) | CONTINUOUS_IMPROVEMENT_PROTOCOL, PENDING_UPDATES, UPDATE_HISTORY, ROLLBACK_LOG, GOVERNANCE_POLICY | Triggered after every task (Learn step) |
| Skills (agent capabilities) | 17 SKILL.md files (8 curated + 9 portable MDD methodology skills) | Triggered by description match; portable MDD skills provide on-demand workflow depth |
| Bootstrappers | setup-tools.sh/ps1 | Create MDD directory structure + seed state files from skill assets + validate manifest + install tools |

### Architecture Decisions

* ADR template: `docs/_ai_context/templates/ADR_TEMPLATE.md`
* V1.3 feature specification: `docs/_ai_context/knowledge/MDD_V1.3_FEATURE_SPECIFICATION_SUMMARY.md`
* V1.3 rule source (archived): `docs/_ai_context/analysis/archive/01-mdd-v1.3-full.mdc`
* V1.3 slim router (archived): `docs/_ai_context/analysis/archive/01-mdd-v1.3-slim-router.mdc`

### Constraints

* Rules 01-03 are non-optional and take priority over tool-specific rules.
* `.tools-cache/` is gitignored.
* All workspace configuration stays local.
* Knowledge files (Rank 1 per V1.4 Authority Hierarchy) require human approval to modify.
* Continuous Improvement Protocol runs after every non-trivial task (P-R-I-L).

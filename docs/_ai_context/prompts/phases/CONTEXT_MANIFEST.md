---
document_type: PROMPT
status: ACTIVE
version: "1.0.0"
---

# Context Manifest

Navigation map and agent contract for this workspace. Read this after `repo-manifest.json` and before `MASTER_STATE.md` per Sniper Protocol (MDD V1.3 Section 1).

## Project Identity

| Field | Value |
|-------|-------|
| **Name** | Experiment JP |
| **Type** | ENGEN Jet Park — fuel & C-store operations |
| **Purpose** | POS reporting, bank/payroll recon, management dashboard |
| **Site** | Fuel Rock (Pty) Ltd / ENGEN JET PARK SERVICE STATION |
| **Bank account** | FNB 62848015857 (from OFX feed) |
| **MDD Version** | V1.3 Agentic Critical Edition |

## Agent Contract

When working in this workspace, you MUST:

1. **Load context** from `state/repo-manifest.json` -> this file -> `state/MASTER_STATE.md` (in that order)
2. **Follow** the MDD V1.3 protocol at `.cursor/rules/01-mdd.mdc`
3. **Triage complexity** before starting work (Simple/Medium/Complex)
4. **Use the correct mode** (Ask/Plan/Agent) per the task type
5. **Log all non-trivial work** to `state/WORK_LOG.md`
6. **Run the learning checklist** after task completion (see `knowledge/governance/CONTINUOUS_IMPROVEMENT_PROTOCOL.md`)
7. **Never modify** canonical knowledge files without human approval

## Navigation Map

### State (read-write, current project snapshot)

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `state/MASTER_STATE.md` | Canonical project state | After every significant change |
| `state/WORK_LOG.md` | Chronological change log | After every non-trivial task |
| `state/BACKLOG.md` | Prioritized deferred work | After every task that defers work |
| `state/repo-manifest.json` | Machine-readable file index | After file structure changes |

### Decision Support (read-only reference)

| File | Purpose | When to Consult |
|------|---------|----------------|
| `knowledge/COMPLEXITY_TRIAGE_MATRIX.md` | Simple/Medium/Complex decision rules | Before starting any task |
| `knowledge/MODE_TRANSITION_RULES.md` | Ask/Plan/Agent state machine | When choosing operational mode |
| `knowledge/ANTI_PATTERNS_CATALOG.md` | Failure pattern institutional memory | During plan review and debugging |
| `knowledge/governance/GOVERNANCE_POLICY.md` | Metadata, compliance, protections | When creating/modifying artifacts |
| `knowledge/governance/CONTINUOUS_IMPROVEMENT_PROTOCOL.md` | Learning loop routing | After completing any task |

### Templates (use when creating artifacts)

| Template | When to Use |
|----------|------------|
| `templates/MEDIUM_PLAN_TEMPLATE.md` | Medium complexity tasks (3-5 steps) |
| `templates/COMPLEX_PREPLAN_TEMPLATE.md` | Complex tasks (6+ steps) |
| `templates/PHASE_COMPLETION_TEMPLATE.md` | After completing any phase |
| `templates/DEBUG_LOG_TEMPLATE.md` | Investigating bugs |
| `templates/RUNBOOK_TEMPLATE.md` | Operational procedures |
| `templates/ADR_TEMPLATE.md` | Architectural decisions |
| `templates/RESPONSE_FORMAT_ASK.md` | Ask mode output |
| `templates/RESPONSE_FORMAT_PLAN.md` | Plan mode output |
| `templates/RESPONSE_FORMAT_AGENT.md` | Agent mode output |

### Prompts (reusable instructions)

| File | Purpose |
|------|---------|
| `prompts/SESSION_START.md` | Copy-paste prompts for session initialization |
| `prompts/PROMPT_INDEX.md` | Discovery entry point for all prompts |
| `prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md` | How to run multi-phase work |

### Rules (behavioral guidance)

| File | Domain |
|------|--------|
| `.cursor/rules/00-starter-rules.mdc` | Loading order, priority resolution |
| `.cursor/rules/01-mdd.mdc` | MDD V1.3 process and governance |
| `.cursor/rules/02-kingmode.mdc` | Design philosophy and ULTRATHINK |
| `.cursor/rules/03-frontend-fullstack.mdc` | Stack conventions |

## Key Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Rule files | 4 | 4 |
| MDD directories | 11 | 11 |
| Templates | 9 | 9 |
| Knowledge docs | 7 | 7+ |
| Backlog items (open) | Review `state/BACKLOG.md` | < 50 |

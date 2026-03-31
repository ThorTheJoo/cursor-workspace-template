---
name: plan-generation
description: "Generate self-contained, executable plans that can run in independent agent sessions with zero prior context. Use whenever creating phase plans, analysis plans, execution specs, or breaking complex work into documented steps. Triggers on: 'create a plan', 'write a phase', 'break this down', multi-step tasks, plan files, validation gates, or structured execution specs."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Plan Generation

## Core Principle

**Every plan must be executable in an independent agent window with ZERO prior context.**

The agent reading this plan has never seen your conversation. It doesn't know what you discussed, what you tried, or what you decided. The plan file IS the context — include everything the executing agent needs.

This is the single most important quality standard for plans. Violating it means the executing agent will guess, make wrong assumptions, and waste time. Self-containment is not optional documentation — it is the mechanism that makes multi-session AI workflows reliable.

## Self-Containment Rule

A plan fails self-containment if it:

- References "as discussed earlier" or "from our conversation" — the next agent has no conversation
- Says "check the config" without specifying which config keys and their current values
- Says "fix the scoring" without exact file path, line number, and before/after code
- Omits environment variables or path setup needed to run commands
- Assumes knowledge of prior phase results without including them
- Has no validation commands — the agent can't verify its own work

For the full checklist, see `references/self-containment-checklist.md`.

## Mandatory Content Checklist

Before finalizing any plan, verify it contains all of these:

### Structure
- [ ] **YAML front-matter** with document_type, status, depends_on, outputs_for_next_phase, validation_gate
- [ ] **Background/context section** — Why are we doing this? What problem does it solve?
- [ ] **History/evolution summary** — How did we get here? Key metrics from predecessor phases

### Traceability
- [ ] **Predecessor chain table** — Phase | Config | Key Metric | Key Change
- [ ] **Lessons from history** — Table of rules with source and consequences if violated
- [ ] **Backlog items** — Items assigned to this phase (from BACKLOG.md)

### Executability
- [ ] **File inventory** — Every file to read, modify, or create (with full paths)
- [ ] **Environment setup** — All env vars, dependencies, paths needed to run
- [ ] **Concrete code snippets** — Exact file paths, line numbers, before/after code
- [ ] **Validation commands** — Runnable commands that verify each step succeeded

### Quality Gates
- [ ] **Completion gate** — Metrics gate + backlog gate + documentation gate
- [ ] **Performance baselines** — Current metric values that must not regress

### Data Integrity (when plan involves data parsing)
- [ ] **Data file verification** — For every file the plan reads, verify actual schema against documentation
- [ ] **Producer→Container→Consumer audit** — For every new data field, trace the full flow
- [ ] **Silent failure check** — No code path silently returns empty/None on failure

## Plan Types

| Type | When | Location |
|------|------|----------|
| One-off analysis | Investigation, debug, single-task work | `docs/_ai_context/analysis/YYYY-MM-DD_NAME_PLAN.md` |
| Multi-phase plan | Complex work spanning multiple sessions | `docs/_ai_context/prompts/phases/PHASE_XX_NAME.md` |
| Pre-plan (decomposition) | Breaking complex work into numbered phases | `docs/_ai_context/prompts/phases/PHASE_XX_NAME_PREPLAN.md` |

**Quick rule:** If the work spans multiple sessions or needs validation gates between steps, use a multi-phase plan.

## Plan Location Rules

- Multi-phase execution plans: `docs/_ai_context/prompts/phases/PHASE_XX_NAME.md`
- Single-task analysis plans: `docs/_ai_context/analysis/YYYY-MM-DD_NAME_PLAN.md`
- Pre-plans (decomposition): `docs/_ai_context/prompts/phases/PHASE_XX_NAME_PREPLAN.md`

## Context Sources

Before writing a plan, read these files for relevant context:

1. `docs/_ai_context/state/MASTER_STATE.md` — current project state
2. `docs/_ai_context/state/BACKLOG.md` — pending items to assign
3. `docs/_ai_context/state/WORK_LOG.md` — recent changes and lessons
4. `docs/_ai_context/prompts/phases/PHASES_INDEX.md` — phase history
5. Relevant predecessor plan files
6. Data schema files — if the plan involves data parsing

## Failure Modes

These patterns cause plans to fail in practice:

| Failure Mode | Why It Happens | Prevention |
|-------------|---------------|------------|
| Implicit context | Plan author assumed the executor knows the history | Include all context in the plan itself |
| Missing validation | No way to verify if steps succeeded | Add runnable validation commands for each step |
| Stale field references | Plan references a field that was renamed or removed | Verify against actual data files, not documentation |
| Config without wiring | Plan adds a config key that no code reads | Verify every config key is consumed by code |
| Silent fallbacks | Code returns empty instead of raising an error | Ensure every failure path logs or raises |
| Uniform signals | A scoring signal fires equally on true and false positives | Verify selectivity before adding scoring logic |

For detailed quality gates, see `references/plan-quality-gates.md`.

## YAML Front-Matter Standard

Every plan must have front-matter for agent filtering and dependency tracking:

```yaml
---
document_type: PLAN
status: DRAFT
depends_on:
  - "path/to/predecessor/output"
outputs_for_next_phase:
  - "path/to/output/files"
validation_gate:
  - "metric gate description"
  - "backlog gate: all assigned items resolved"
traceability_id: "PHASE-XX-NAME-YYYYMMDD"
estimated_duration: "X-Y hours"
---
```

For the full standard with optional fields, see `references/frontmatter-standard.md`.

## Template

A genericized phase plan template is available at `assets/PHASE_PLAN_TEMPLATE.md`. Use it as a starting point for new plans — fill in the sections, remove what doesn't apply, and add domain-specific content.

## References

| File | Content |
|------|---------|
| `references/self-containment-checklist.md` | Full self-containment checklist with examples |
| `references/frontmatter-standard.md` | YAML front-matter fields and requirements |
| `references/plan-quality-gates.md` | What makes a plan fail quality review |
| `assets/PHASE_PLAN_TEMPLATE.md` | Genericized phase plan template |

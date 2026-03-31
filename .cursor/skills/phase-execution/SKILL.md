---
name: phase-execution
description: "Execute multi-phase plans with pre-flight validation, backlog enforcement, completion gates, and structured handoffs. Use whenever implementing work from a plan file, running a phase spec, or executing documented steps that reference PHASE_*.md files. Triggers on: 'execute', 'run phase', 'implement the plan', kickoff prompts, plan references, or PHASE_*.md files."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Phase Execution

This skill governs how to execute a plan file. The plan is the single source of truth for the work — read it completely before writing any code.

## Before Writing Any Code

### 1. Read the Plan Completely

Read the entire plan file before starting. Understand the full scope, dependencies, and validation gates. Starting a step without knowing the overall structure leads to rework.

### 2. Check the Backlog

Read `docs/_ai_context/state/BACKLOG.md` and search for items tagged `assigned: {this_phase}`. List every one. Address P1 items before any new work.

```
BACKLOG ITEMS ASSIGNED TO THIS PHASE:
- [P1] item description
- [P2] item description
Proceeding with P1 items FIRST.
```

P1 items exist because a prior phase identified them as critical. Skipping them creates technical debt that compounds in later phases.

### 3. Verify Prerequisites

Check that all files listed in the plan's `depends_on` actually exist. If a prerequisite is missing, stop and report — do not improvise.

### 4. Run Pre-Flight Checks

If the plan specifies a pre-flight validation command, run it. If it fails with a blocking error, resolve the failure before proceeding.

## Before Any Config or Code Change

Every change must be wired correctly. Before making a change, verify:

| Check | Why It Matters |
|-------|---------------|
| Config key → code reads it | A config key that no code reads has zero effect |
| Feature flag → code checks it | An unchecked flag means the feature is always on/off |
| YAML file → loader reads it | A YAML update that's never loaded does nothing |
| Data field → consumer uses it | Adding a field that nothing reads is dead code |
| CSV parsing → verify headers | Wrong column names produce silent null values |
| JSON field access → verify existence | Missing fields return None silently |
| Fallback path → logs a warning | Silent fallbacks hide bugs for weeks |

Report disconnects *before* making the change, not after. Fixing wiring after the fact costs 5x more time.

For the detailed checklist, see `references/preflight-checklist.md`.

## During Execution

### Step-by-Step

1. Execute steps in the order specified by the plan
2. Validate after each step — run the validation command provided
3. On validation failure: stop and fix before proceeding
4. On unexpected discoveries: add to BACKLOG.md, don't pursue during execution
5. Steps marked parallel (⚡) can run concurrently; all others are sequential

### Scope Discipline

Implement exactly what the plan specifies. If you discover something that should be different:

- Minor adjustment (typo in path, version bump): fix and document
- Scope change (new feature, different approach): add to BACKLOG.md and continue with the original plan
- Blocking issue (plan is fundamentally wrong): stop and report to the user

## Completion Protocol

Before marking a phase complete:

1. **Run validation gate** — Execute all validation commands from the plan's completion checklist
2. **Audit the backlog** — Re-read BACKLOG.md. Every item assigned to this phase must be DONE or DEFERRED with documented evidence
3. **Update BACKLOG.md** — Close resolved items, add any new discoveries with assignment
4. **Create completion doc** — `docs/_ai_context/analysis/PHASE_XX_COMPLETION.md` with files modified, validation results, metrics, and lessons
5. **Update state files** — WORK_LOG.md entry, phase index status → COMPLETE
6. **Commit** — Conventional prefix: `feat(scope): Phase XX - summary`

Never mark a phase complete while regressions exist. If metrics regressed, fix or document before closing.

For the full protocol, see `references/completion-protocol.md`.

## Anti-Patterns

| Don't | Why It Fails | Instead |
|-------|-------------|---------|
| Defer a P1 item without user approval | P1 items are critical — deferring silently compounds debt | Ask the user before deferring |
| Add config key without verifying code reads it | Config change has zero runtime effect | Trace: config → loader → consumer |
| Use `except: pass` on critical imports | Entire subsystem silently disabled | Log warning, raise on critical paths |
| Mark phase complete with regressions | Future phases inherit broken state | Fix or document the regression |
| Skip validation and declare "done" | Silent failures propagate downstream | Run every validation command |
| "Continue from where we left off" | New session has no memory of prior work | Reference specific file paths |
| Load entire large files into context | Blows the context window | Read targeted sections on demand |

For the full anti-pattern table, see `references/anti-patterns.md`.

## Backlog Aging

Backlogs accumulate if not actively managed. Enforce these aging rules:

| Priority | Rule |
|----------|------|
| P0 (blocking) | Must be resolved in the current phase |
| P1 (critical) | Must not survive more than 2 phases — escalate to P0 if still open |
| P2 (backlog) | Review every 5 phases — close stale items with documented reason |
| P3 (wishlist) | Review quarterly — close if no longer relevant |

## Error Recovery

### Step Failure

1. Document the error in the current phase output
2. Attempt to fix within the current context
3. If unfixable: roll back partial changes, create an analysis file documenting the issue
4. Report blocked status with specifics

### Validation Gate Failure

1. Identify which specific check failed
2. Fix the failing component
3. Re-run the full validation gate
4. Do not proceed to the next phase until the gate passes

### Phase Abandonment

1. Document what was completed and what failed
2. Commit partial work with `WIP:` prefix
3. Create analysis file for the next attempt
4. Tag the rollback point in git

For detailed recovery protocols, see `references/error-recovery.md`.

## References

| File | Content |
|------|---------|
| `references/multi-phase-guidelines.md` | Context independence, handoffs, validation gates |
| `references/preflight-checklist.md` | Detailed pre-flight and wiring verification |
| `references/completion-protocol.md` | Full completion protocol with checklist |
| `references/anti-patterns.md` | Anti-pattern table with alternatives |
| `references/error-recovery.md` | Recovery protocols for failures |
| `assets/CONTEXT_MANIFEST_TEMPLATE.md` | Template for phase context manifests |
| `assets/PHASES_INDEX_TEMPLATE.md` | Template for phase tracking index |
| `assets/KICKOFF_PROMPT_TEMPLATE.md` | Template for phase kickoff prompts |

---
document_type: PRE_PLAN
status: DRAFT
date: YYYY-MM-DD
estimated_total_duration: "X-Y hours"
reviewer:
  accountable: ""
compliance_tags: []
traceability_id: ""
---

# [Pre-Plan Title]

## Problem Statement

[What we are solving and why it qualifies as complex (6+ steps, 2+ hrs, validation gates needed)]

## Todo Decomposition

| Todo | Phase File | Depends On | Duration | Parallel? |
|------|-----------|------------|----------|-----------|
| 1. [Description] | `PHASE_XX_NAME.md` | None | 1-2 hrs | - |
| 2. [Description] | `PHASE_XY_NAME.md` | Todo 1 | 2-3 hrs | - |
| 3. [Description] | `PHASE_XZ_NAME.md` | None | 1 hr | with Todo 2 |

## Dependencies Graph

```
Phase XX (Todo 1)
  +-- Phase XY (Todo 2) --- depends on XX
  |
Phase XZ (Todo 3) --- parallel with XY, no dependency

Sync point: Phase XW (Todo 4) --- requires XY + XZ outputs
```

> Replace with a Mermaid diagram for complex graphs.

## Validation Strategy

[How we know the full initiative succeeded after all phases complete]

* Overall success criteria: [measurable outcome]
* Integration test: [what to run after all phases]
* Rollback plan: [how to undo if the initiative fails midway]

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ... | ... | ... | ... |

## Self-Critique

* **Weakest part:** [honest assessment]
* **Largest unknown:** [what we do not know yet]
* **Spike needed?** [yes/no - if yes, describe what to investigate first]

## READY FOR REVIEW: YES / NO

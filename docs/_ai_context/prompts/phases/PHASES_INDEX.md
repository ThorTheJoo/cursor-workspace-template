---
document_type: STATE
status: ACTIVE
---

# Phases Index

## Phase Table

| # | Phase | Status | Plan File | Key Output | Date |
|---|-------|--------|-----------|-----------|------|
| 1 | {Phase 1 Name} | COMPLETE / IN_PROGRESS / PLANNED | `phases/PHASE_01_NAME.md` | {output path} | {date} |
| 2 | {Phase 2 Name} | PLANNED | `phases/PHASE_02_NAME.md` | {output path} | — |

## Status Legend

| Status | Meaning |
|--------|---------|
| COMPLETE | All validation gates passed, committed |
| IN_PROGRESS | Currently being executed |
| PLANNED | Phase file exists, not yet started |
| BLOCKED | Prerequisites not met or error encountered |
| SKIPPED | Deemed unnecessary, with documented reason |

## Dependency Graph

```
Phase 1 ──→ Phase 2 ──→ Phase 3
                    ──→ Phase 4 (⚡ parallel with Phase 3)
Phase 3 + Phase 4 ──→ Phase 5
```

Phases marked with ⚡ can run in parallel with the indicated phase.

## Quick Reference

- **Current active phase:** {number}
- **Next planned phase:** {number}
- **Total phases:** {count}
- **Completed:** {count}
- **Blocked:** {count or "none"}

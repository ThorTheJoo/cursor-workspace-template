---
document_type: COMPLETION
phase: XX
status: COMPLETE
date: YYYY-MM-DD
traceability_id: ""
---

# Phase XX Completion Summary

## Files Created/Modified

| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file` | CREATED / MODIFIED / DELETED | [what and why] |

## Validation Results

| Gate | Result | Evidence |
|------|--------|----------|
| [Gate 1 name] | PASS / FAIL | [command output, link, or observation] |
| [Gate 2 name] | PASS / FAIL | [command output, link, or observation] |

## Metrics (if applicable)

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| [metric name] | [value] | [value] | [+/-] |

## Lessons Learned

* **What went well:** [be specific - cite files, techniques, decisions that worked]
* **What went wrong / unexpected:** [be specific - cite root cause]
* **What to do differently next time:** [actionable recommendation]
* **Regression risk:** HIGH / MEDIUM / LOW - [describe what could regress and why]

## Regression Category (classify the risk)

| Category | Applies? | Detail |
|----------|----------|--------|
| Field Mismatch | Y/N | Producer/consumer field name drift |
| Version Confusion | Y/N | Stale data read by newer code |
| Baseline Drift | Y/N | Metrics compared to wrong baseline |
| Template Divergence | Y/N | Output format drifts from template |
| Silent Fallback | Y/N | System degrades without warning |

## Handoff Notes for Next Phase

* [Context the next phase needs to know]
* [Warnings about edge cases encountered]
* [Deviations from original plan, if any]

## Continuous Improvement Checklist

> Run per `docs/_ai_context/knowledge/governance/CONTINUOUS_IMPROVEMENT_PROTOCOL.md`

- [ ] New anti-pattern discovered? -> Propose to `knowledge/ANTI_PATTERNS_CATALOG.md`
- [ ] Reusable pattern (>= 3x)? -> Extract to `prompts/` or `.cursor/skills/`
- [ ] Process gap? -> `knowledge/governance/PENDING_UPDATES.yaml` or `state/BACKLOG.md`
- [ ] Domain knowledge gained? -> `knowledge/staging/`
- [ ] Template/governance refinement needed? -> `knowledge/governance/PENDING_UPDATES.yaml`

## Git Commit

```
feat(scope): Phase XX - [summary]
- [Key deliverable 1]
- [Key deliverable 2]
- [Validation results]
```

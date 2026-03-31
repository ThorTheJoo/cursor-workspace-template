---
name: work-logging
description: "Structured work logging with lessons learned, regression risk assessment, and change tracking. Use after completing any non-trivial work to create audit trails and capture institutional knowledge. Triggers on: 'log this work', 'update work log', 'update mdd'  post-implementation documentation, lessons learned, change tracking, WORK_LOG.md, or regression risk assessment."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Work Logging

## Purpose

Capture institutional knowledge and change history so future AI sessions can learn from past work. Without work logs, the same mistakes repeat across sessions — the same bug gets fixed three times, the same architectural dead end gets explored again, the same regression gets introduced.

Work logs are the project's immune system against repeated failures.

## When to Log

Log work after **any non-trivial work session** — defined as:
- More than 30 minutes of effort, OR
- More than 3 files changed, OR
- Any regression risk introduced, OR
- Any lesson learned worth preserving

Skip logging only for trivial single-file edits with no risk (e.g., fixing a typo).

## Work Log Location

The canonical work log lives at `docs/_ai_context/state/WORK_LOG.md`. New entries go at the top (newest first). A ready-to-use template is at `assets/WORK_LOG_TEMPLATE.md` (relative to this skill directory).

## Mandatory Fields

Every work log entry MUST include all of these fields:

| Field | Required | Purpose |
|-------|----------|---------|
| **Scope** | Yes | What was done — 1-2 sentences |
| **Status** | Yes | COMPLETE / IN PROGRESS / BLOCKED |
| **Duration** | Yes | Approximate time spent |
| **Changes Made** | Yes | File-level change table (file path + description) |
| **Validation Results** | Yes | What was verified and the outcome (PASS/FAIL) |
| **Regression Risk** | Yes | HIGH/MEDIUM/LOW with description of what could regress |
| **Lessons Learned** | Yes (non-trivial) | Structured per the lessons format below |
| **Next Steps** | Yes | What comes next, or "None" |

Optional but recommended:
- **Traceability** — link to phase ID, ticket, or plan reference
- **Metrics** — before/after measurements when applicable

## Entry Format

```markdown
### YYYY-MM-DD — [Scope Title]

**Status:** COMPLETE | IN PROGRESS | BLOCKED
**Duration:** X hours
**Traceability:** [phase-id or ticket reference]

**Changes Made:**
| File | Change | LOC |
|------|--------|-----|
| `path/to/file.py` | Description of what changed | ~50 |

**Validation Results:**
- [x] [Description of check] — PASS
- [ ] [Description of check] — FAIL (reason)

**Regression Risk:** MEDIUM — [description of what could regress and how to detect it]

**Lessons Learned:**
- What went well: [...]
- What went wrong: [...]
- Do differently: [...]
- Regression risk: [...]

**Next Steps:** [...]
```

## Lessons Learned Structure

Every non-trivial work log entry must answer these four questions:

1. **What went well?** — Techniques, tools, or approaches that worked
2. **What went wrong / was unexpected?** — Surprises, bugs, wrong assumptions
3. **What to do differently next time?** — Concrete, actionable changes
4. **Regression risk assessment** — What could break in the future?

See `references/lessons-learned-patterns.md` for detailed patterns and examples.

## Regression Risk Categories

Assign one of these categories when assessing regression risk:

| Category | Description | Prevention |
|----------|-------------|------------|
| **Field Mismatch** | Producer/consumer field name drift | Pin names in schema/contract files |
| **Version Confusion** | Stale data read by newer code | Version field in all schemas |
| **Baseline Drift** | Metrics compared to wrong baseline | Timestamp all baselines |
| **Template Divergence** | Output format drifts from template | Template compliance checks |
| **Silent Fallback** | Script degrades without warning | Fail loud, never degrade silently |

## Conventional Commits

Link work log entries to git commits using conventional prefixes:

| Prefix | When to Use |
|--------|------------|
| `feat(scope)` | New feature or capability |
| `fix(scope)` | Bug fix |
| `docs(scope)` | Documentation only |
| `refactor(scope)` | Code restructuring without behavior change |
| `perf(scope)` | Performance improvement |
| `test(scope)` | Adding or fixing tests |

Format: `feat(pipeline): Phase XX — [summary]`

## Pattern Extraction

If the same lesson appears 3 or more times in the work log:
1. Extract it into a reusable rule (`.cursor/rules/`) or skill (`.cursor/skills/`)
2. Reference the new rule/skill in the work log entry
3. Future agents will get this knowledge automatically instead of re-learning it

## References

- Detailed lessons-learned patterns: `references/lessons-learned-patterns.md`
- Work log template: `assets/WORK_LOG_TEMPLATE.md`

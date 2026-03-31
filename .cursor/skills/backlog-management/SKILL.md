---
name: backlog-management
description: "Maintain prioritized backlogs with aging enforcement, source attribution, and phase assignment. Use when tracking deferred work, managing task priorities, grooming backlogs, or enforcing that old items do not languish indefinitely. Triggers on: backlog, deferred items, task tracking, P0/P1/P2 priorities, 'what is pending', aging enforcement, or work item triage."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Backlog Management

## Purpose

AI agents are stateless between sessions. Without a structured backlog, deferred work items vanish — rediscovered weeks later (if at all) when their context has evaporated. This skill encodes prioritized tracking with aging enforcement so that no deferred item languishes silently.

The backlog is the project's memory of unfinished business.

## Backlog Location

The canonical backlog lives at `docs/_ai_context/state/BACKLOG.md`. If this file does not exist, create it from the template in `assets/BACKLOG_TEMPLATE.md` (relative to this skill directory).

## Item Format

Every backlog item follows this format:

```
- [ ] [P1] Title – one-line description. (source: <origin>).
```

**Required components:**
- **Checkbox** (`- [ ]` open, `- [x]` resolved)
- **Priority label** in brackets
- **Title** — short, action-oriented
- **Description** — one line explaining what and why
- **Source attribution** — `(source: <plan-id, phase, session, or investigation>)`

## Priority Labels

| Priority | Meaning | SLA |
|----------|---------|-----|
| **P0** | Blocking current work | MUST resolve in the current phase/sprint |
| **P1** | Next sprint / high importance | MUST NOT survive >2 phases — escalates to P0 if still open |
| **P2** | Backlog / medium importance | Review every 5 phases — close stale items with documented reason |
| **P3** | Wishlist / low importance | Review on major milestones — archive if >90 days inactive |

## Aging Enforcement

Aging enforcement is the core mechanism that prevents item rot.

**At the start of every phase or sprint:**

1. Scan all open items for age violations
2. Escalate aged P1 items to P0 (if open > 2 phases since creation)
3. Review P2 items that have survived 5+ phases — close or re-prioritize with documented reason
4. Archive P3 items inactive for >90 days

**Enforcement actions:**

| Condition | Action |
|-----------|--------|
| P0 open at phase start | Block — address before any new work |
| P1 open > 2 phases | Escalate to P0 with note: `Escalated from P1 (aged 3+ phases)` |
| P2 open > 5 phases | Review: re-prioritize, close with reason, or confirm still relevant |
| P3 open > 90 days | Archive with reason: `Archived — inactive >90 days (YYYY-MM-DD)` |
| Any item with no source | Flag for remediation — add source attribution immediately |

## Grooming Rules

1. **No duplicates** — search existing items before adding. If overlap exists, update the existing item instead of creating a new one.
2. **Resolved items** — move to the `## Resolved` section with `[x]`, completion date, and resolution note.
3. **Source attribution** — every item must have `(source: ...)` identifying where it came from.
4. **Age-out** — items >90 days without activity must be reviewed.
5. **Periodic review** — at least once per 5 phases (or quarterly), groom the entire backlog.

## When to Add Items

| Situation | What to Add |
|-----------|------------|
| During planning | Deferred scope that won't fit the current phase |
| During execution | Discovered issues, unexpected bugs, technical debt |
| During review | Future improvements, optimization opportunities |
| From investigations | Follow-up work identified but out of current scope |
| From lessons learned | Preventive measures or improvements for future phases |

## When to Close Items

| Reason | Action |
|--------|--------|
| Completed | Mark `[x]`, add completion date and brief note |
| Superseded | Mark `[x]`, note which item/phase supersedes it |
| No longer relevant | Mark `[x]`, document why with date |
| Duplicate | Mark `[x]`, reference the surviving item |

## Backlog Sections

Organize items into logical sections for scannability:

```markdown
## Active Items

### Experiment / Pipeline
### Deferred from Plans
### Critical Fixes

## Resolved
```

Add domain-specific sections as the project grows (e.g., `### Phase N Candidates`, `### Data Quality Gaps`).

## Adding Items During Plan Execution

When executing a plan and discovering out-of-scope work:

1. Do NOT expand the current phase's scope
2. Add the item to BACKLOG.md with source attribution
3. Assign a priority based on impact
4. If P0, stop and address immediately (it's blocking)
5. If P1+, continue with the current plan and address in the next phase

## Template

A ready-to-use backlog template is available at:

```
.cursor/skills/backlog-management/assets/BACKLOG_TEMPLATE.md
```

Copy this file to `docs/_ai_context/state/BACKLOG.md` when bootstrapping a new project.

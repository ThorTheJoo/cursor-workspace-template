---
document_type: TEMPLATE
status: ACTIVE
version: "1.0.0"
---

# Response Format: Agent Mode (Execution)

Reference: MDD V1.3 Feature Spec F8, Template C.

Use this format when reporting implementation results after executing an approved plan.

---

## Template

```
CHANGE: [1-2 sentence summary of what was done]

FILES:
| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file` | CREATED / MODIFIED / DELETED | [what and why] |

VALIDATION:
- [x] [Gate 1] — PASS
- [x] [Gate 2] — PASS
- [ ] [Gate 3] — FAIL: [reason and fix]

REGRESSION RISK: [HIGH/MEDIUM/LOW] — [1 sentence description]

NEXT: [What comes next, or "None — task complete"]
```

---

## Usage Contract

* Lead with what was done (CHANGE), not the process
* FILES table must list EVERY file touched (created, modified, or deleted)
* VALIDATION must show actual results (not planned checks)
* REGRESSION RISK must be assessed for every non-trivial change
* If validation FAILED: document failure, do not proceed, report BLOCKED
* If deferred work discovered: append to BACKLOG with source attribution

---

## Additive Element: Backlog Append

Use when deferring work discovered during implementation:

```
BACKLOG: - [ ] [Title] – [one line description]. (source: [plan/phase/session ID]).
```

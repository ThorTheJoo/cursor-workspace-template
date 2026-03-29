---
document_type: RUNBOOK
status: DRAFT
date: YYYY-MM-DD
version: "1.0.0"
reviewer:
  accountable: ""
compliance_tags: []
---

# Runbook: [Procedure Name]

## Objective

[One sentence: what this runbook accomplishes when executed successfully]

## Prerequisites

- [ ] [Tool/access/permission required]
- [ ] [Environment state required]
- [ ] [Data/config state required]

## Procedure

### Step 1: [Action Name]

```bash
[exact command or action]
```

**Expected output:**
```
[what the operator should see]
```

**If unexpected:** [what to do - rollback, escalate, or skip]

### Step 2: [Action Name]

```bash
[exact command or action]
```

**Expected output:**
```
[what the operator should see]
```

### Step N: ...

## Validation (MANDATORY)

> These checks MUST pass after the procedure completes.

| # | Check | Command / Action | Expected Result |
|---|-------|-----------------|-----------------|
| 1 | [what we verify] | `[command]` | [expected output] |
| 2 | ... | ... | ... |

## Rollback

> If the procedure fails midway or validation does not pass:

1. [Step to undo changes]
2. [Step to restore prior state]
3. [Notification / escalation path]

## Notes

* **Last executed:** [date] by [who]
* **Known issues:** [edge cases, gotchas]
* **Related docs:** [links to plans, ADRs, or debug logs]

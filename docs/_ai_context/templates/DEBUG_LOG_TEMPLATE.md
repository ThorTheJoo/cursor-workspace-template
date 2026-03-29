---
document_type: DEBUG
status: INVESTIGATING
date: YYYY-MM-DD
reviewer:
  accountable: ""
compliance_tags: []
traceability_id: ""
---

# Debug Log: [Error/Bug Short Name]

## Symptoms

* **Observed behavior:** [what happened]
* **Expected behavior:** [what should have happened]
* **Reproducible?** Always / Sometimes / Once
* **First seen:** [date/time, commit, or deploy]
* **Environment:** [dev/staging/prod, OS, Node version, etc.]

## Error Evidence

```
[paste stack trace, error message, screenshot description]
```

## Impact Assessment

| Dimension | Rating | Detail |
|-----------|--------|--------|
| Users affected | NONE/FEW/MANY/ALL | [who is impacted] |
| Data integrity | SAFE/AT_RISK/CORRUPTED | [is data affected] |
| Service availability | UP/DEGRADED/DOWN | [system status] |
| Urgency | P0/P1/P2/P3 | [when must this be fixed] |

## Root Cause Analysis

### Hypothesis Log

| # | Hypothesis | Test | Result | Eliminated? |
|---|-----------|------|--------|-------------|
| 1 | [theory] | [what I tested] | [what I saw] | Y/N |
| 2 | ... | ... | ... | ... |

### Root Cause

[Confirmed root cause. Be specific: file, line, function, data condition.]

## Failed Attempts

> This section prevents repeating mistakes. Every approach that did NOT work gets logged.

| # | What I Tried | Why It Failed | Time Spent |
|---|-------------|---------------|------------|
| 1 | [approach] | [reason it did not work] | [Xm] |

## Solution

### Fix Applied

```diff
- [old code / config]
+ [new code / config]
```

### Files Modified

| File | Change |
|------|--------|
| `path/to/file` | [description] |

### Validation

- [ ] Fix resolves the original symptoms
- [ ] No regressions in related functionality
- [ ] Tests added/updated for this case
- [ ] Works across all affected environments

## Prevention

* **How to prevent this class of bug:** [systemic fix, not just this instance]
* **Monitoring/alerting added?** YES / NO — [details]
* **Documentation updated?** YES / NO — [where]

# Plan Quality Gates

## What Makes a Plan FAIL Quality Review

### Self-Containment Failures

| Failure | Why It's Critical |
|---------|------------------|
| References "as discussed earlier" | Next agent has no conversation — will guess wrong |
| Says "check the config" without specifics | Agent doesn't know which config or which keys |
| Omits environment setup | Commands fail with cryptic errors |
| Missing validation commands | Agent can't verify its own work |
| Assumes prior phase knowledge | Each phase starts from zero context |

### Data Integrity Failures

| Failure | Why It's Critical |
|---------|------------------|
| References a field without verifying it exists | Code reads None silently, produces wrong results |
| Assumes column headers without reading the file | CSV parsing silently returns empty dicts |
| Uses `encoding='utf-8'` for CSV files | BOM character corrupts first column header |
| Proposes a dataclass extension without adding fields | Consumer gets AttributeError at runtime |
| Contains `except: pass` on critical dependencies | Entire subsystem silently disabled |

### Signal Quality Failures

These apply when the plan involves scoring, ranking, or classification:

| Failure | Why It's Critical |
|---------|------------------|
| Adds a scoring signal without selectivity evidence | Signal fires equally on true/false positives — wastes an entire phase |
| Uses hardcoded thresholds without verifying score distributions | Threshold either does nothing or kills recall |
| Adds config key without verifying code reads it | Config change has zero effect — invisible wasted effort |

## Quality Review Checklist

Before submitting a plan for review, verify:

1. **Read-aloud test**: Read the plan as if you've never seen the codebase. Can you execute every step?
2. **File existence**: Every file referenced exists at the stated path
3. **Field existence**: Every data field referenced is verified against actual data
4. **Command runnable**: Every validation command can be copy-pasted and run
5. **Gate measurable**: Every completion gate has a concrete pass/fail criterion
6. **Backlog addressed**: All items assigned to this phase are listed with status
7. **No implicit context**: Zero references to conversations, prior sessions, or assumed knowledge

## Selective Signal Check

When a plan introduces a new scoring signal (applies to any ranking/classification system):

1. Sample true positives — does the signal fire more often on these?
2. Sample false positives — does the signal fire less often on these?
3. If the signal fires roughly equally on both → it's a uniform boost and won't improve quality
4. Document the selectivity evidence in the plan

A signal that fires on everything is equivalent to no signal.

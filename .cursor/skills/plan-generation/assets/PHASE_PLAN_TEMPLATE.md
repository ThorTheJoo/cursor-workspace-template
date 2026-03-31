---
document_type: PLAN
status: DRAFT
phase: "{PHASE_ID}"
name: "Phase {PHASE_ID} — {TITLE}"
depends_on:
  - "{previous phase outputs}"
outputs_for_next_phase:
  - "{list all output files}"
validation_gate:
  - "{metric gate 1}"
  - "{metric gate 2}"
  - "All assigned backlog items DONE or DEFERRED with evidence"
traceability_id: "PHASE{ID}-{SHORT_NAME}-{DATE}"
estimated_duration: "{X-Y hours}"
---

# Phase {PHASE_ID} — {TITLE}

## Enforcement Block

### Pre-Flight Validation

{Run any pre-flight checks before starting. List commands or manual verification steps.}

### Backlog Items Assigned to This Phase

> Before executing any step below, read `docs/_ai_context/state/BACKLOG.md` and list all items
> assigned to this phase. Address P1 items first.

| # | Priority | Item | Status |
|---|----------|------|--------|
| 1 | P1 | {item from BACKLOG} | PENDING |

### Wiring Verification Checklist

Before making any config or code change, verify:

- [ ] Config key `{key}` → referenced in `{code_file}` at line `{N}`
- [ ] Feature flag `{flag}` → checked in `{code_file}` at line `{N}`

---

## Context & History

{Brief summary of how we got here. Include key metrics, predecessor outputs, and critical warnings.}

### Predecessor Chain

| Phase | Key Metric | Key Change |
|-------|-----------|------------|
| {prior phase} | {metric} | {what changed} |

### Lessons from History (Do Not Violate)

| Lesson | Source | Consequence if Violated |
|--------|--------|------------------------|
| {lesson} | {phase} | {what goes wrong} |

---

## Data Verification Audit

> For every file this plan reads or parses, verify the actual schema matches expectations.

| File/Structure | Verified? | Encoding | Headers/Fields Confirmed? |
|---------------|-----------|----------|--------------------------|
| {data file} | [ ] | {encoding} | [ ] |

### Producer→Container→Consumer Audit

| Data Field | Producer | Container | Consumer | Verified? |
|-----------|----------|-----------|----------|-----------|
| {field} | {function} | {class/dict} | {function} | [ ] |

---

## Step 0: Address Backlog Items

> All P1 items assigned to this phase must be resolved here before new work.

### P1 Item: {ID}

**Finding:** {description}
**Fix:** {concrete code/config change with file path and line number}
**Validation:** {command to verify the fix}

---

## Step 1: {First New Work Item}

### Purpose
{What this step achieves and why it matters}

### File Inventory
| File | Action | Sections |
|------|--------|----------|
| `{path}` | CREATE / MODIFY / READ | {which parts} |

### Execute
{Concrete commands or code changes — include before/after snippets}

### Validate
{Runnable commands that verify this step succeeded}

---

## Step N: Regression & Gate Check

### Execute

```bash
# {Run regression or validation suite}
{validation command}
```

### Validate

- [ ] {Metric 1}: {target value}
- [ ] {Metric 2}: {target value}
- [ ] No regression beyond acceptable threshold
- [ ] All new discoveries documented in BACKLOG

---

## Completion Checklist

### Backlog Gate
- [ ] All P1 items: DONE with evidence
- [ ] All P2 items: DONE or DEFERRED with reason
- [ ] Any new discoveries added to BACKLOG with assignment

### Metrics Gate
- [ ] {Primary metric}: {target}
- [ ] No regression on existing metrics

### Documentation Gate
- [ ] BACKLOG.md updated
- [ ] WORK_LOG.md entry added
- [ ] Phase plan status updated to COMPLETE

### Handoff
- [ ] Outputs for next phase exist at documented paths
- [ ] Kickoff prompt ready for next phase:

```
Execute Phase {NEXT_ID} from docs/_ai_context/prompts/phases/PHASE_{NEXT_ID}_{NAME}.md
```

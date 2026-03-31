# Completion Protocol

Follow this protocol before marking any phase complete.

## Step 1: Run Validation Gate

Execute all validation commands specified in the plan's completion checklist. Record results.

If any gate fails:
- Identify the failing check
- Fix the failing component
- Re-run the full validation gate
- Do not proceed until all gates pass

## Step 2: Audit the Backlog

Re-read `docs/_ai_context/state/BACKLOG.md`:

- Every item tagged `assigned: {this_phase}` must be either:
  - **DONE** with evidence (link to code change, test result, or analysis)
  - **DEFERRED** with documented reason, estimated impact, and suggested future phase
- P1 items cannot be deferred without explicit user approval
- Any new discoveries during this phase must be added to BACKLOG with assignment

## Step 3: Update BACKLOG.md

- Close resolved items (change `[ ]` to `[x]`, add completion note)
- Add new items discovered during execution
- Move completed items to the `## Resolved` section

## Step 4: Create Completion Document

Create `docs/_ai_context/analysis/PHASE_XX_COMPLETION.md` with:

```markdown
# Phase XX Completion

## Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| path/to/file | CREATED/MODIFIED | What changed |

## Validation Results

| Gate | Result | Evidence |
|------|--------|----------|
| {gate 1} | PASS/FAIL | {output or link} |

## Metrics

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| {metric} | {value} | {value} | {change} |

## Lessons Learned

- What went well
- What went wrong or was unexpected
- What to do differently next time
- Regression risk: HIGH/MEDIUM/LOW — what could regress
```

## Step 5: Update State Files

- Add entry to `docs/_ai_context/state/WORK_LOG.md`
- Update phase status in `docs/_ai_context/prompts/phases/PHASES_INDEX.md` → COMPLETE
- Update `docs/_ai_context/state/MASTER_STATE.md` if the change affects project capabilities

## Step 6: Commit

Use conventional commit format:

```
feat(scope): Phase XX - summary

- Key deliverable 1
- Key deliverable 2
- Validation results
```

## Step 7: Prepare Handoff

Verify:
- [ ] Outputs for next phase exist at documented paths
- [ ] Kickoff prompt for next phase is ready
- [ ] Handoff notes capture any edge cases or warnings

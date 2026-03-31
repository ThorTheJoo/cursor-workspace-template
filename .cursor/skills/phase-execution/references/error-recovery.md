# Error Recovery Protocols

## Step Failure

When a step in the plan fails:

1. **Document the error** — Record the exact error message, command, and context in the current phase output
2. **Attempt to fix** — If the fix is within the step's scope, apply it and re-run validation
3. **If unfixable:**
   - Roll back any partial changes from this step
   - Create an analysis file: `docs/_ai_context/analysis/YYYY-MM-DD_PHASE_XX_STEP_N_FAILURE.md`
   - Include: error description, root cause analysis (if known), attempted fixes, and suggested approach for next attempt
4. **Report blocked status** — Clearly state what failed, why, and what's needed to unblock

## Validation Gate Failure

When a validation gate doesn't pass:

1. **Identify the specific check** — Which gate criterion failed?
2. **Review the validation criteria** — Is the gate reasonable, or does the criteria need updating?
3. **Fix the failing component** — Apply targeted fixes to address the gate failure
4. **Re-run the full validation gate** — Not just the failing check; re-run everything to catch cascading issues
5. **Do not proceed** — Never advance to the next phase with a failing gate. The gate exists because downstream work depends on this guarantee.

## Phase Abandonment

When a phase must be abandoned entirely:

1. **Document progress** — Record what was completed and what remains
2. **Document failure** — Record what went wrong, root cause if known, and any partial findings
3. **Commit partial work** — Use `WIP:` prefix:
   ```
   WIP: Phase XX partial - [what's done]

   - [Completed items]
   - [Blocked on: specific issue]
   ```
4. **Create analysis file** — `docs/_ai_context/analysis/YYYY-MM-DD_PHASE_XX_ABANDONMENT.md` with findings and recommendations for the next attempt
5. **Tag rollback point** — Create a git tag so the pre-abandonment state is easily recoverable

## Regression During Execution

When a change causes regression in existing metrics:

1. **Stop and assess** — Don't continue making more changes on top of a regression
2. **Measure the regression** — Quantify: which metric, how much, which components affected
3. **Root cause** — Is it caused by this phase's changes, or was it pre-existing?
4. **Decision:**
   - If revertible: revert the change, adjust approach
   - If inherent trade-off: document the trade-off, get user approval to proceed
   - If pre-existing: document as not caused by this phase, add to BACKLOG

## Common Error Patterns

| Error | Likely Cause | Quick Fix |
|-------|-------------|-----------|
| FileNotFoundError | Wrong path or missing prerequisite | Check `depends_on`, verify file exists |
| KeyError on data access | Field renamed or doesn't exist | Read actual data file, check schema |
| ModuleNotFoundError | Missing dependency or PYTHONPATH | Install dependency or set path |
| Timeout on external calls | Network issue or rate limiting | Add retry logic, increase timeout |
| Silent empty results | Exception swallowed somewhere | Add logging to catch blocks |

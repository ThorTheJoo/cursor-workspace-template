# P-R-I-L Workflow

Plan → Review → Implement → Log. Every non-trivial change follows this cycle.

## Plan

Create a plan document appropriate to the task's complexity:

| Complexity | Plan Location | Format |
|------------|--------------|--------|
| Simple (1-2 steps, <30 min) | Inline in response | Brief numbered steps |
| Medium (3-5 steps, <2 hrs) | `docs/_ai_context/analysis/YYYY-MM-DD_NAME_PLAN.md` | Single analysis file with steps and validation |
| Complex (6+ steps, 2+ hrs) | `docs/_ai_context/prompts/phases/PHASE_XX_NAME.md` | Full phase spec with code snippets, validation gates |

For complex tasks, create a pre-plan first that decomposes the work into numbered phases, then expand each into a full phase file.

A good plan answers: What will change? Why? What files are affected? How do we verify success? What could go wrong?

## Review

Human checkpoint before implementation begins.

- Simple tasks: implicit review (human reads the inline plan in the response)
- Medium tasks: human reviews the analysis file before proceeding
- Complex tasks: explicit approval required before any code changes

Never skip review for complex plans. The cost of a wrong assumption discovered after implementation is 10x the cost of catching it during review.

## Implement

Execute changes scoped strictly to the approved plan.

- Make atomic changes — each change should be independently reversible
- Stop on validation failure — do not proceed to the next step
- No scope creep — if you discover additional work needed, add it to BACKLOG.md instead of doing it now
- If the plan turns out to be wrong, go back to Plan (don't improvise)

## Log

After implementation, update documentation:

1. **WORK_LOG.md** — Add an entry with scope, status, duration, changes, validation results, regression risk, and lessons learned
2. **Conventional commit** — `feat(scope): summary` or `fix(scope): summary`
3. **Completion doc** — For multi-phase work, create `docs/_ai_context/analysis/PHASE_XX_COMPLETION.md`
4. **BACKLOG.md** — Append any deferred items discovered during implementation
5. **State files** — Update MASTER_STATE.md if the change affects project capabilities

Logging isn't busywork — it's how the next agent (or the next you) avoids repeating mistakes.

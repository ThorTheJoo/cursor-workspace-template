# Complexity Triage

Assess complexity before starting work. The answer determines what artifacts are required.

## Decision Matrix

| Question | If Yes → |
|----------|----------|
| Will this take more than 2 hours? | Complex |
| Does it have more than 5 distinct steps? | Complex |
| Does it need intermediate validation between steps? | Complex |
| Does it have sequential dependencies (output of A → input of B)? | Complex |
| Does it involve multiple file types (scripts, configs, docs)? | Likely Medium or Complex |
| Can it benefit from parallel execution? | Complex |

If none of the above apply, it's Simple.

## Artifact Requirements

### Simple (< 30 min, 1-2 steps)

No formal plan needed. Describe the steps inline in the response, implement, and log.

Example: fixing a typo in a config file, adding a single field to a YAML file.

### Medium (< 2 hrs, 3-5 steps)

Create a single analysis file:
- Location: `docs/_ai_context/analysis/YYYY-MM-DD_NAME_PLAN.md`
- Include: context, steps, validation criteria, file inventory
- Review: human reads and approves before implementation

Example: adding a new scoring signal with config wiring and a validation test.

### Complex (2+ hrs, 6+ steps, validation gates)

Create a multi-phase plan:
- Location: `docs/_ai_context/prompts/phases/PHASE_XX_NAME.md`
- Pre-plan: decompose into numbered phases first
- Each phase: self-contained spec with code snippets, validation commands, exact file paths
- Review: explicit human approval before any code changes
- Handoff: each phase ends with a kickoff prompt for the next

Example: migrating a scoring algorithm, building a new pipeline stage, refactoring a data model.

## Common Mistakes

- **Underestimating complexity**: "I'll just fix this one thing" turns into 4 hours of cascading changes. When in doubt, triage up.
- **Skipping the plan for medium tasks**: Writing a 20-line analysis file takes 5 minutes and saves 30 minutes of rework.
- **Over-planning simple tasks**: A typo fix doesn't need a phase spec. Use judgment.

# Kickoff Prompt Template

Use this template to create a kickoff prompt at the end of each phase plan. The prompt should be copy-pasteable into a fresh agent session.

## Template

```
Execute Phase {X} from docs/_ai_context/prompts/phases/PHASE_{X}_{NAME}.md

Instructions:
1. Read the complete plan file before starting
2. Verify all prerequisites from prior phases exist
3. Execute each step sequentially, validating after each
4. On validation failure, STOP and report — do not proceed
5. On completion, run the full validation gate
6. Prepare handoff notes for Phase {X+1}
```

## With Prerequisites

When a phase has specific prerequisites that should be checked upfront:

```
Execute Phase {X} from docs/_ai_context/prompts/phases/PHASE_{X}_{NAME}.md

Prerequisites to verify before starting:
- {output from Phase X-1} exists at `{path}`
- {config version} is {expected value}
- {dependency} is installed

No prior context is needed — the plan file contains everything.
```

## For Parallel Phases

When two phases can run independently:

```
Execute Phase {X} from docs/_ai_context/prompts/phases/PHASE_{X}_{NAME}.md
⚡ This phase can run in parallel with Phase {Y}.

Both phases share the same prerequisites from Phase {X-1} but do not depend on each other.
```

## Guidelines

- Keep the prompt self-contained — the receiving agent has no prior context
- List specific prerequisite files, not vague references
- Include the plan file path so the agent knows exactly what to read
- State that no prior context is needed (reinforces the self-containment principle)

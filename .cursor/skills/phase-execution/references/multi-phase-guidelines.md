# Multi-Phase Execution Guidelines

## Core Principles

### Context Independence

Each phase executes in a fresh agent session with no memory of prior sessions. The plan file IS the context. Never rely on information that isn't in the plan file itself.

This means every phase file must include:
- All relevant background and history
- Exact file paths for inputs and outputs
- Current metric values (not "the current metrics")
- Environment setup instructions

### Explicit Handoffs

Output from Phase N becomes input for Phase N+1. Specify exact paths — never say "use the output from the previous phase" without stating where that output lives.

At phase completion, include:
- List of created outputs with paths
- Validation results (pass/fail per gate)
- Handoff notes for the next phase (edge cases, warnings, deviations from plan)
- Kickoff prompt for the next phase

### Validation Gates

Each phase completes with validation. Do not proceed to the next phase until the gate passes. Gates ensure that each phase builds on a verified foundation.

Common gate types:
- **Metrics gate**: No regression beyond threshold on key metrics
- **Backlog gate**: All assigned items resolved or deferred with evidence
- **Documentation gate**: WORK_LOG, BACKLOG, and completion doc updated

### Atomic Commits

Each phase = one logical commit. This enables rollback to the last known-good state if something goes wrong in a later phase.

Format: `feat(scope): Phase XX - summary`

### Kickoff Prompts

Every phase ends with a ready-to-paste prompt for the next phase. This eliminates ambiguity about how to start the next session.

### Parallel Markers

Use `⚡ with Phase X` to mark phases that can run independently. This enables concurrent execution when multiple agents are available.

## Phase File Structure

Every phase plan file includes:

```yaml
---
name: Phase X - [Descriptive Name]
depends_on:
  - List of files/outputs from previous phases
outputs_for_next_phase:
  - Explicit paths to files this phase creates
validation_gate:
  - Criteria that MUST pass before marking complete
---
```

## Phase Boundaries

- Phase N completes → Validation passes → Git commit → Phase N+1 starts fresh
- Between phases: always verify prior phase outputs exist
- On failure: fix in current phase OR rollback and re-plan
- Never carry implicit context between sessions

## Pre-Plan Workflow

When a task is complex, produce a pre-plan that:

1. Lists numbered todos with target phase numbers
2. Includes dependencies between todos
3. Lives in `docs/_ai_context/prompts/phases/PHASE_XX_NAME_PREPLAN.md`

Then expand each todo into a full execution-style phase file with code snippets, validation commands, and file paths.

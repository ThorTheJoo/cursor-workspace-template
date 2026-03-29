---
document_type: GOVERNANCE
status: APPROVED
version: "1.0.0"
---

# Multi-Phase Execution Guidelines

Reference: MDD V1.3 Section 6 / Feature Spec F4.

This document governs how complex (multi-phase) work is planned, executed, and completed across agent sessions.

## Core Principles

1. **Context Independence** — Each phase executes in a fresh session with zero memory. The phase plan file IS the complete context. Never write "as discussed previously".
2. **Explicit Handoffs** — Output from Phase N becomes input for Phase N+1. Always specify exact file paths.
3. **Validation Gates** — Named, binary (PASS/FAIL) checks. ALL must pass before a phase is marked complete.
4. **Atomic Commits** — Each phase = one logical commit. Enables rollback.
5. **Kickoff Prompts** — Every phase ends with a copy-paste prompt for the next phase.
6. **Parallel Markers** — Use `with Phase X` for phases that can run independently (no shared file modifications, no data dependency).

## Phase File Requirements

Every phase file MUST include:

### YAML Front-Matter

```yaml
---
document_type: PHASE_SPECIFICATION
name: "Phase XX - Descriptive Name"
phase: "XX of YY"
depends_on:
  - "path/to/prior/output.ext"
outputs_for_next_phase:
  - "path/to/output/this/creates.ext"
validation_gate:
  - "Criteria that MUST pass"
estimated_duration: "X-Y hours"
source_pre_plan: "path/to/pre_plan.md"
---
```

### Context Manifest (Mandatory Tables)

| Table | Required | Purpose |
|---|---|---|
| This Phase Creates | Yes | Output paths + why next phase needs them |
| This Phase Requires | Yes | Input paths + which phase created them |
| Files to Read (On-Demand) | Optional | Targeted section reads for large files |
| Files to Modify | Optional | Change type + sections affected |

## Validation Gate Design

* Each gate must be independently verifiable (a command, a test, a file existence check).
* Order: structural checks -> semantic checks -> integration checks.
* Gate failure = STOP. Fix -> re-run gate -> pass -> continue.
* All gate results recorded in the completion document.

| Category | Example | Verification Method |
|---|---|---|
| File existence | Output file X exists | `ls path/to/file` |
| Schema compliance | Output matches schema Y | Schema validation tool |
| Test passage | All unit tests pass | Test runner |
| Quality threshold | Score >= N% | Validator script |
| Diff verification | No unintended changes | `git diff --stat` |
| Contract match | Producer/consumer fields align | Field comparison |

## Handoff Protocol

At phase completion, include verbatim:

```markdown
## Phase XX Complete

### Created Outputs (Verify Exist)
- [ ] `path/to/output1` - [description]
- [ ] `path/to/output2` - [description]

### Validation Results
- [ ] [Gate 1] - PASS / FAIL
- [ ] [Gate 2] - PASS / FAIL

### Handoff Notes for Phase XX+1
- [Context the next phase needs]
- [Edge cases encountered]
- [Deviations from plan]

### Git Commit
`feat(scope): Phase XX - [summary]`
```

## Kickoff Prompt (End of Every Phase)

```
Execute Phase XX+1 from the plan at `docs/_ai_context/prompts/phases/PHASE_XX+1_NAME.md`

Instructions:
1. Read the complete plan file before starting
2. Verify all prerequisites from prior phases exist
3. Execute each step sequentially, validating after each
4. On validation failure, STOP and report
5. On completion, run the full validation gate
6. Prepare handoff notes for Phase XX+2
```

## Phase Numbering

Check existing phase files for the highest number. New work gets the next sequential number. Each todo from a pre-plan gets its own phase number.

## Parallel Execution

Phases marked with parallel markers:
* MUST NOT modify the same files
* MUST NOT depend on each other's outputs
* A synchronization point (non-parallel phase) must follow if later work needs both outputs

## Error Recovery

| Failure Mode | Protocol |
|---|---|
| **Step failure** | Document error -> attempt fix -> if unfixable, create `analysis/YYYY-MM-DD_PHASE_XX_ERROR.md`, rollback, report BLOCKED |
| **Gate failure** | Identify failing check -> fix -> re-run specific gate -> do NOT proceed until ALL pass |
| **Abandonment** | Document progress -> commit with `WIP:` prefix -> create analysis file -> update phase index with BLOCKED |

## After-Completion Checklist

- [ ] Run all validation gates and record results
- [ ] Create `analysis/PHASE_XX_COMPLETION.md`
- [ ] Update phase index (status -> COMPLETE)
- [ ] Update `state/WORK_LOG.md` with enhanced template
- [ ] Run project test suite
- [ ] Commit with conventional prefix
- [ ] Append deferred items to `state/BACKLOG.md`
- [ ] Include kickoff prompt for next phase

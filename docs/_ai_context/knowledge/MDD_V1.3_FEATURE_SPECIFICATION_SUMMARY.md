---
document_type: SPECIFICATION
status: DRAFT
version: 1.0.0
date: 2026-03-29
reviewer:
  accountable: "User"
consulted: ["AI Agent"]
compliance_tags: ["MDD", "Generic", "Portable", "Feature-Specification"]
traceability_id: "SPEC-MDD-FEATURES-10-v1.0"
---

# MDD Feature Specification — Ultra-Dense Generic Edition

> **Purpose:** Standalone, framework-agnostic specification for 10 battle-tested Markdown-Driven Development features. Each feature is fully self-contained with rationale, contracts, implementation templates, enforcement rules, and failure modes. Copy any feature into any workspace rule file and adapt the placeholder paths.
>
> **Audience:** Any AI-assisted codebase using agentic workflows (Cursor, Windsurf, Copilot Workspace, Aider, or custom orchestrators).
>
> **Convention:** `{state_dir}` = your state directory (e.g., `docs/_ai_context/state/`). `{analysis_dir}` = your analysis directory. `{phases_dir}` = your phase plan directory. `{knowledge_dir}` = your canonical knowledge directory. `{backlog}` = your backlog file path. Replace all `{placeholders}` with your actual project paths.

---

## Table of Contents

| # | Feature | Section | Density |
|---|---------|---------|---------|
| 1 | Sniper Mode (Context Loading Protocol) | [F1](#f1-sniper-mode-context-loading-protocol) | Implementation-ready |
| 2 | Three Operational Modes (Ask / Plan / Agent) | [F2](#f2-three-operational-modes) | Contracts + templates |
| 3 | Complexity Triage System | [F3](#f3-complexity-triage-system) | Decision matrix + enforcement |
| 4 | Phase Execution System | [F4](#f4-phase-execution-system) | Full protocol + 10 elements |
| 5 | Authority Hierarchy / Constitution | [F5](#f5-authority-hierarchy--constitution) | Precedence chain + constraints |
| 6 | Governance Rules (14 Rules Distilled) | [F6](#f6-governance-rules) | Rules + violation definitions |
| 7 | Anti-Patterns & Failure Patterns Catalog | [F7](#f7-anti-patterns--failure-patterns-catalog) | Tables + prevention protocols |
| 8 | Structured Response Formats | [F8](#f8-structured-response-formats) | 3 templates + usage contracts |
| 9 | Knowledge Repository Governance Chain | [F9](#f9-knowledge-repository-governance-chain) | Full pipeline + schema enforcement |
| 10 | Backlog as First-Class Artifact | [F10](#f10-backlog-as-first-class-artifact) | Priority system + grooming rules |

---

# F1: Sniper Mode (Context Loading Protocol)

## 1.1 — Definition

A disciplined, manifest-driven context-loading protocol that executes at session start to prevent token waste, hallucinated file paths, and redundant full-file reads. The agent loads a machine-readable index first, resolves paths from the index, and reads only targeted sections of target files on-demand.

## 1.2 — Rationale

| Problem | Cost | Sniper Mode Fix |
|---------|------|-----------------|
| Agent guesses file paths | Hallucinated paths → failed reads → retry loops | Resolve all paths from manifest before reading |
| Agent reads entire large files | Context window blown on irrelevant content (500+ line files consume 2K-10K tokens) | Read only targeted sections (line ranges, specific headings) |
| Agent loads stale mental model | Outdated assumptions → incorrect modifications | Manifest is regenerated; freshness is verifiable |
| Agent reinvents existing capability | Duplicate code/scripts → maintenance burden | Manifest indexes capabilities; check before creating |
| No session-start contract | Agent behavior varies per session | Mandatory first step eliminates variance |

## 1.3 — Implementation Contract

### Priority Loading Order (MANDATORY — execute in sequence)

| Priority | Artifact | Type | Purpose | Fallback if Missing |
|----------|----------|------|---------|---------------------|
| 1 | `{state_dir}/repo-manifest.json` | Machine-readable JSON | File index, function signatures, capability registry, phase ownership | Use IDE search tools (grep/glob/semantic) as degraded alternative; flag missing manifest in response |
| 2 | `{phases_dir}/CONTEXT_MANIFEST.md` or `{state_dir}/MASTER_STATE.md` | Human-readable Markdown | Navigation map, project identity, current phase, agent contract, key metrics | Read `README.md` at repo root; flag degraded context |
| 3 | Target-specific files | Any | On-demand content needed for the current task | — |

### Manifest Schema (Minimum Viable)

```json
{
  "_meta": {
    "generated": "ISO-8601 timestamp",
    "version": "semver",
    "file_count": 0,
    "generator": "path/to/generator/script"
  },
  "files": {
    "path/to/file.ext": {
      "type": "script|config|doc|test|template|state",
      "functions": ["function_name_1", "function_name_2"],
      "classes": ["ClassName"],
      "phase_owner": "Phase XX or null",
      "last_modified": "ISO-8601",
      "loc": 0
    }
  },
  "capabilities": {
    "capability_name": {
      "command": "execution command",
      "script": "path/to/script",
      "output": "description of output",
      "dependencies": ["dep1", "dep2"]
    }
  },
  "phases": {
    "Phase XX": {
      "status": "COMPLETE|IN_PROGRESS|PLANNED",
      "plan_file": "path/to/phase/file.md",
      "outputs": ["path/to/output1", "path/to/output2"]
    }
  }
}
```

### Sniper Rules (Non-Negotiable)

| Rule ID | Rule | Violation Severity |
|---------|------|--------------------|
| SNP-01 | NEVER read a file >500 lines in full without targeting specific sections (line range, heading, function name) | HIGH — wastes context budget |
| SNP-02 | NEVER guess or fabricate file paths — resolve from manifest, or use IDE search (grep/glob) if manifest unavailable | CRITICAL — leads to hallucinated operations |
| SNP-03 | NEVER reinvent functionality — check `capabilities{}` in manifest (or search codebase) before writing new code | CRITICAL — creates duplicates |
| SNP-04 | ALWAYS prefer targeted section reads (`read lines 50-80`) over full file loads | MEDIUM — efficiency |
| SNP-05 | ALWAYS state which manifest entry resolved the target path in your response (traceability) | LOW — aids debugging |
| SNP-06 | If manifest is stale (>7 days or git diff shows drift), flag staleness and suggest regeneration | MEDIUM — prevents stale navigation |

### Targeted Reading Protocol

```
WHEN agent needs file content:
  1. RESOLVE path from manifest (or grep if manifest missing)
  2. CHECK file size:
     IF lines <= 500 → full read permitted
     IF lines > 500 → identify target section:
       a. By line range (from manifest or prior knowledge)
       b. By heading/function name (semantic search)
       c. By grep for specific pattern
  3. READ only the targeted section
  4. IF more context needed → expand range incrementally (±50 lines)
  5. NEVER pre-load "just in case" content
```

### Session Start Template (Copy-Paste for Users)

```
Load context from {state_dir}/repo-manifest.json and {state_dir}/MASTER_STATE.md.
Respond using the appropriate mode format (Ask/Plan/Agent).
Do NOT read full large files. Use manifest to resolve paths.
```

## 1.4 — Manifest Generation

Provide a script (any language) that:
1. Walks the project directory tree (respecting `.gitignore`)
2. Extracts: file paths, types, function/class signatures, line counts
3. Outputs `repo-manifest.json` to `{state_dir}/`
4. Is idempotent (re-running produces same result for same inputs)
5. Is registered in the manifest itself under `capabilities.generate_manifest`

Trigger regeneration after: new scripts created, files renamed/moved, phases completed, significant refactors.

## 1.5 — Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| Path resolution accuracy | % of file reads that hit a real file | >99% |
| Context efficiency | Avg lines loaded vs lines actually used | <3:1 ratio |
| Manifest freshness | Days since last regeneration | <7 days |

---

# F2: Three Operational Modes

## 2.1 — Definition

Three formalized agent behavioral modes — **Ask**, **Plan**, **Agent** — each with distinct triggers, workflows, and mandatory response formats. The modes map directly to common AI IDE interactions (investigation, planning, execution) and prevent mode confusion where agents plan when they should answer, or execute when they should plan.

## 2.2 — Mode Contracts

### Mode A: Ask (Investigation / Sniper)

| Property | Specification |
|----------|---------------|
| **Trigger** | User asks where/how/what/status/why questions; requests for information rather than action |
| **Entry Condition** | Manifest loaded (F1) |
| **Workflow** | 1. Parse query type (where/how/what/status) → 2. Manifest lookup for relevant files → 3. Targeted section read → 4. Synthesize structured response |
| **Response Contract** | Use FINDING/EVIDENCE/NEXT STEPS template (see F8) |
| **Max Prose** | 3 paragraphs. Use tables for comparisons, file lists, metrics. |
| **Side Effects** | NONE — Ask mode is read-only. No file modifications, no state updates. |
| **Backlog Hook** | If answer identifies out-of-scope work, suggest adding to `{backlog}`: `- [ ] Title – one line. (source: query).` |
| **Exit Condition** | Response delivered. User decides next action. |

### Mode B: Plan (Architecture / Design)

| Property | Specification |
|----------|---------------|
| **Trigger** | Complex tasks, architecture decisions, multi-step operations, user says "plan", "design", "how should we", "what's the approach" |
| **Entry Condition** | Manifest loaded (F1) + Complexity triage completed (F3) |
| **Workflow** | 1. Complexity triage (F3) → 2. Create plan artifact at appropriate location → 3. Define validation gates → 4. Present for human review |
| **Response Contract** | Use PLAN/CHANGES/VALIDATION/READY FOR REVIEW template (see F8) |
| **Artifact Creation** | Simple: inline. Medium: `{analysis_dir}/YYYY-MM-DD_NAME_PLAN.md`. Complex: `{phases_dir}/PHASE_XX_NAME.md` |
| **Human Checkpoint** | MANDATORY — plan must be approved before execution begins. Response must end with `READY FOR REVIEW: YES/NO` |
| **Backlog Hook** | When deferring work, append to `{backlog}`: `- [ ] Title – one line. (source: <plan id>).` |
| **Exit Condition** | Human approves plan. Transition to Agent mode for implementation. |

### Mode C: Agent (Execution)

| Property | Specification |
|----------|---------------|
| **Trigger** | Implementation task; plan already approved; user says "implement", "execute", "do it", "build" |
| **Entry Condition** | Plan exists (inline, analysis file, or phase file) + Human approval received |
| **Workflow** | P-R-I-L: 1. Plan (reference approved plan) → 2. Review (verify prerequisites exist) → 3. Implement (atomic changes scoped to plan) → 4. Log (WORK_LOG + commit) |
| **Response Contract** | Use CHANGE/FILES/VALIDATION template (see F8) |
| **Scope Lock** | Changes MUST be scoped strictly to the approved plan. No scope creep. |
| **Validation** | Run project tests/lint/validation after changes. Stop on failure. |
| **State Updates** | MANDATORY: Update `{state_dir}/WORK_LOG.md`, update `{state_dir}/MASTER_STATE.md` if project state changed |
| **Exit Condition** | All plan items implemented + validated + logged. |

## 2.3 — Mode Transition Rules

```
ASK → PLAN: When investigation reveals work needed (agent suggests, user confirms)
ASK → AGENT: PROHIBITED for non-trivial work (must plan first)
PLAN → AGENT: When human approves the plan
PLAN → ASK: When planning reveals need for more investigation
AGENT → ASK: When implementation reveals unexpected state (stop, investigate)
AGENT → PLAN: When implementation scope needs revision (stop, re-plan)
```

## 2.4 — Mode Selection Heuristic

```
IF query is a question (where/how/what/why/status) → ASK
ELSE IF task has >2 steps OR >30 min OR involves architecture → PLAN
ELSE IF task is simple AND plan exists or is trivial → AGENT
ELSE → ASK (default safe mode)
```

---

# F3: Complexity Triage System

## 3.1 — Definition

A mandatory pre-work assessment that classifies tasks into Simple/Medium/Complex tiers, each with distinct required artifacts. The classification determines whether a plan file is needed, what format it takes, and where it lives. Without explicit thresholds, agents over-plan simple tasks (wasting time) or under-plan complex ones (producing failures).

## 3.2 — Triage Matrix

| Complexity | Step Count | Duration | Validation Gates | Required Artifact | Artifact Location | Human Review |
|------------|-----------|----------|------------------|-------------------|-------------------|--------------|
| **Simple** | 1-2 steps | <30 min | None | No formal plan (inline in response) | — | Optional |
| **Medium** | 3-5 steps | 30 min – 2 hrs | 0-1 | Analysis/plan file | `{analysis_dir}/YYYY-MM-DD_NAME_PLAN.md` | Recommended |
| **Complex** | 6+ steps | 2+ hrs | 2+ | Multi-phase plan with individual phase files | `{phases_dir}/PHASE_XX_NAME.md` | **MANDATORY** |

## 3.3 — Quick Decision Rule

```
IF (steps > 5) OR (duration > 2 hours) OR (requires intermediate validation) → COMPLEX
ELSE IF (steps > 2) OR (duration > 30 min) → MEDIUM
ELSE → SIMPLE
```

## 3.4 — Escalation Triggers (Simple → Medium → Complex)

| Trigger | Escalation |
|---------|------------|
| More files affected than initially estimated | Simple → Medium |
| Intermediate validation needed | Medium → Complex |
| Cross-cutting concern discovered (touches >3 modules) | Any → Complex |
| Schema/contract changes involved | Medium → Complex |
| Multiple humans need to review different parts | Medium → Complex |
| Rollback plan needed | Medium → Complex |

## 3.5 — Enforcement

**Jumping to code for a Complex task without a plan file is a governance violation.**

The agent MUST:
1. State the complexity assessment explicitly in the response
2. Justify the tier chosen (cite step count, estimated duration, or gate count)
3. Create the appropriate artifact before writing implementation code
4. If uncertain between tiers, choose the higher tier (conservative)

## 3.6 — Artifact Templates

### Medium Plan (Analysis File)

```markdown
---
document_type: PLAN
status: DRAFT
date: YYYY-MM-DD
traceability_id: "[ticket or description]"
---

# [Plan Title]

## Context
[1-2 paragraphs: What problem are we solving? Why now?]

## Proposed Changes
| # | Step | File(s) | Change Description | LOC Est. |
|---|------|---------|--------------------|----------|
| 1 | ... | ... | ... | ... |

## Alternatives Considered
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| ... | ... | ... | ... |

## Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ... | ... | ... | ... |

## Validation
- [ ] Gate 1: [description]
- [ ] Gate 2: [description]

## READY FOR REVIEW: YES/NO
```

### Complex Plan (Pre-Plan Decomposition)

```markdown
---
document_type: PRE_PLAN
status: DRAFT
date: YYYY-MM-DD
estimated_total_duration: "X-Y hours"
traceability_id: "[ticket or description]"
---

# [Pre-Plan Title]

## Problem Statement
[What we're solving and why it's complex]

## Todo Decomposition

| Todo | Phase File | Depends On | Duration | Parallel? |
|------|-----------|------------|----------|-----------|
| 1. [Description] | PHASE_XX_NAME.md | None | 1-2 hrs | — |
| 2. [Description] | PHASE_XY_NAME.md | Todo 1 | 2-3 hrs | — |
| 3. [Description] | PHASE_XZ_NAME.md | None | 1 hr | ⚡ with Todo 2 |

## Dependencies Graph
[Text or Mermaid diagram showing todo dependencies]

## Validation Strategy
[How we know the full initiative succeeded]
```

---

# F4: Phase Execution System

## 4.1 — Definition

A comprehensive protocol for executing complex (multi-phase) work across multiple agent sessions, where each phase is context-independent, explicitly handed off, and validated before proceeding. This is the highest-fidelity execution pattern — it makes 700+ line specifications executable in fresh sessions with no prior memory.

## 4.2 — The 10 Elements

### Element 1: Context Independence

Each phase executes in a **fresh agent session** with zero memory of prior sessions. The phase plan file IS the complete context. The agent must be able to execute the phase with only:
- The phase file itself
- Files listed in the `depends_on` field
- Files listed in the "This Phase Requires" table

**Implication:** Never write "as discussed previously" or "continue from where we left off" in a phase file. Every piece of information needed must be explicit.

### Element 2: YAML Front-Matter Contract

Every phase file MUST include machine-readable metadata:

```yaml
---
document_type: PHASE_SPECIFICATION
name: "Phase XX - Descriptive Name"
phase: "XX of YY"
depends_on:
  - "path/to/prior/phase/output1.ext"
  - "path/to/prior/phase/output2.ext"
  - "none (if first phase)"
outputs_for_next_phase:
  - "path/to/output/this/phase/creates1.ext"
  - "path/to/output/this/phase/creates2.ext"
validation_gate:
  - "Criteria 1 that MUST pass"
  - "Criteria 2 that MUST pass"
estimated_duration: "X-Y hours"
source_pre_plan: "path/to/pre_plan.md (if applicable)"
---
```

**Contract:** `depends_on` lists EXACT file paths the agent must verify exist before starting. `outputs_for_next_phase` lists EXACT file paths the agent must create. `validation_gate` lists EXACT criteria that must pass before the phase is considered complete.

### Element 3: Context Manifest per Phase

Every phase includes two mandatory tables and two optional tables:

```markdown
## Context Manifest

### This Phase Creates
| Output | Path | Purpose |
|--------|------|---------|
| [artifact name] | `exact/path/to/file.ext` | [why the next phase needs it] |

### This Phase Requires (From Prior Phases)
| Input | Path | Created By |
|-------|------|------------|
| [artifact name] | `exact/path/to/file.ext` | Phase NN |

### Files to Read (On-Demand)
- `path/to/large/file.ext` — Read only sections X-Y (lines NN-MM) when needed for [purpose]
- Do NOT pre-load entire file into context

### Files to Modify
| File | Change Type | Sections Affected |
|------|-------------|-------------------|
| `path/to/file.ext` | ADDITIVE / UPDATE / DELETE | `section.key` or line range |
```

### Element 4: Validation Gates

Named, binary (PASS/FAIL) checks that must ALL pass before a phase is marked complete.

**Gate Design Rules:**
- Each gate must be independently verifiable (a command, a test, a file existence check)
- Gates must be ordered: structural checks before semantic checks before integration checks
- Gate failure = STOP. Do not proceed. Fix → re-run gate → pass → continue.
- All gate results must be recorded in the completion document

**Gate Categories:**
| Category | Example | Verification Method |
|----------|---------|---------------------|
| File existence | "Output file X exists" | `ls path/to/file` |
| Schema compliance | "Output matches schema Y" | `validate_schema(file, schema)` |
| Test passage | "All unit tests pass" | `pytest tests/ -v` |
| Quality threshold | "Quality score >= N%" | `run_validator(file)` |
| Diff verification | "No unintended changes" | `git diff --stat` |
| Contract match | "Producer fields match consumer expectations" | Field-by-field comparison |

### Element 5: Handoff Protocol

At phase completion, include this block verbatim:

```markdown
## Phase XX Complete

### Created Outputs (Verify Exist)
- [ ] `path/to/output1` — [brief description]
- [ ] `path/to/output2` — [brief description]

### Validation Results
- [ ] [Gate 1 name] — PASS / FAIL
- [ ] [Gate 2 name] — PASS / FAIL

### Handoff Notes for Phase XX+1
- [Any context the next phase needs to know]
- [Warnings about edge cases encountered]
- [Deviations from original plan, if any]

### Git Commit
`feat(scope): Phase XX - [summary]`
```

### Element 6: Kickoff Prompts

Every phase file ends with a copy-paste prompt that a user can paste into a fresh agent session to start the next phase:

```markdown
## Kickoff Prompt for Phase XX+1

> Execute Phase XX+1 from the plan at `{phases_dir}/PHASE_XX+1_NAME.md`
>
> Instructions:
> 1. Read the complete plan file before starting
> 2. Verify all prerequisites from prior phases exist
> 3. Execute each step sequentially, validating after each
> 4. On validation failure, STOP and report — do not proceed
> 5. On completion, run the full validation gate
> 6. Prepare handoff notes for Phase XX+2
```

### Element 7: Pre-Plan Decomposition

Complex initiatives start with a pre-plan that decomposes into numbered todos, each becoming an individual phase file:

```
Pre-Plan (1 file) → Numbered Todos → Individual Phase Files (N files)
                                       ↓
                                    User expands each todo into full phase spec
                                       ↓
                                    Review → Implement → Log (per phase)
```

**Phase Numbering Rule:** Check existing phase files for the highest number. New work gets the next sequential number. Each todo from a pre-plan gets its own phase number.

### Element 8: Parallel Execution Markers

Phases that can run independently (no data dependency between them) are marked with:

```
⚡ with Phase XX
```

This signals to the orchestrator (human or automated) that these phases can run in parallel sessions. The pre-plan dependency graph should explicitly mark which todos are parallelizable.

**Rules:**
- Parallel phases MUST NOT modify the same files
- Parallel phases MUST NOT depend on each other's outputs
- A synchronization point (non-parallel phase) must follow parallel phases if later work needs both outputs

### Element 9: Phase Completion Documentation

**Every phase** (not just complex ones) produces a completion document:

```markdown
---
document_type: COMPLETION
phase: XX
status: COMPLETE
date: YYYY-MM-DD
---

# Phase XX Completion Summary

## Files Created/Modified
| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file` | CREATED / MODIFIED | [what and why] |

## Validation Results
| Gate | Result | Evidence |
|------|--------|----------|
| Gate 1 | PASS / FAIL | [command output or link] |
| Gate 2 | PASS / FAIL | [command output or link] |

## Metrics (if applicable)
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| [metric name] | [value] | [value] | [+/-] |

## Lessons Learned
- [What went well]
- [What went wrong / unexpected]
- [What to do differently next time]
- [Regression risk: HIGH/MEDIUM/LOW — description]
```

**Enforcement:**
- Phase status MUST NOT be set to COMPLETE until completion doc exists
- Exception: Single-step documentation-only phases may use the WORK_LOG entry as the completion record

### Element 10: Error Recovery

Three failure modes with distinct protocols:

**Step Failure:**
1. Document the error in current phase output
2. Attempt fix within current context
3. If unfixable: create `{analysis_dir}/YYYY-MM-DD_PHASE_XX_ERROR.md`
4. Roll back partial changes (`git checkout -- .` or targeted revert)
5. Report BLOCKED status with specifics

**Gate Failure:**
1. Identify which specific check failed and why
2. Review the validation criteria for correctness
3. Fix the failing component
4. Re-run the specific gate (not all gates)
5. Do NOT proceed to next phase until ALL gates pass

**Abandonment:**
1. Document what was completed and what remains
2. Commit partial work with `WIP: Phase XX partial - [what's done]` prefix
3. Create analysis file documenting the abandonment reason
4. Tag the git rollback point
5. Update phase index with BLOCKED status

## 4.3 — Phase Execution Checklist (Agent Contract)

### Before Starting Any Phase
- [ ] Read the complete phase plan file
- [ ] Read `{state_dir}/MASTER_STATE.md` for current project state
- [ ] Check `{state_dir}/WORK_LOG.md` for recent changes
- [ ] Verify all files in `depends_on` exist
- [ ] Verify all files in "This Phase Requires" table exist

### During Execution
- [ ] Execute steps sequentially unless explicitly marked parallel
- [ ] Validate after each step — stop and report on failure
- [ ] Stay scoped to the plan — no scope creep
- [ ] Record any deviations from plan in handoff notes

### After Completion
- [ ] Run all validation gates — record results
- [ ] Create completion document (`PHASE_XX_COMPLETION.md`)
- [ ] Update phase index (status → COMPLETE)
- [ ] Update `WORK_LOG.md` with enhanced template (F6.10)
- [ ] Run project test suite
- [ ] Commit with conventional prefix
- [ ] Append deferred items to `{backlog}`
- [ ] Include kickoff prompt for next phase

---

# F5: Authority Hierarchy / Constitution

## 5.1 — Definition

A strict, ranked precedence order for sources of truth within the project. When two sources conflict, the higher-ranked source wins unconditionally. This prevents agents from overwriting canonical domain knowledge with ephemeral project state, or treating navigation indexes as authoritative sources.

## 5.2 — Precedence Chain

| Rank | Source Type | Example Path | Authority Level | Rule |
|------|-----------|--------------|-----------------|------|
| **1** | Canonical Knowledge Files (YAML/JSON) | `{knowledge_dir}/*.yaml` | **Constitutional** — defines domain truth | NEVER contradict. NEVER modify without human approval. Changes require governance chain (F9). |
| **2** | State Files | `{state_dir}/*.md`, `{state_dir}/*.json` | **Operational** — defines current execution state | Read before modifying. Update after changes. May be overwritten by agents per protocol. |
| **3** | Manifests and Indexes | `{state_dir}/repo-manifest.json`, phase indexes, prompt indexes | **Navigational** — points to truth | Do NOT define truth. Only point to it. Regeneratable from source files. |
| **4** | Rule Files and Skills | `.cursor/rules/*.mdc`, `.cursor/skills/*/SKILL.md` | **Behavioral** — guides agent actions | Overridden by ranks 1-3 when in conflict. |
| **5** | Inline Agent Reasoning | Agent's own analysis, responses, suggestions | **Ephemeral** — valid only for current session | Must be grounded in ranks 1-4. Never persists as truth without being written to appropriate tier. |

## 5.3 — Non-Negotiable Constraints

| Constraint ID | Constraint | Justification |
|---------------|-----------|---------------|
| CONST-01 | Knowledge files are **constituted authority** for domain semantics | Prevents agents from redefining terms, taxonomies, or canonical data |
| CONST-02 | MDD documentation is **ephemeral project state**, not authoritative for domain content | Project logs ≠ domain truth; logs track what happened, knowledge defines what IS |
| CONST-03 | **Config over code**: if a change can live in YAML/JSON config, propose it there first | Reduces code changes, increases auditability, enables non-developer edits |
| CONST-04 | **Deterministic first**: prefer rule-based processing over probabilistic/ML approaches | Reproducibility, debuggability, verifiability |
| CONST-05 | **Human-in-the-loop** for all knowledge file updates | Constitutional changes require human ratification |

## 5.4 — Conflict Resolution Protocol

```
WHEN agent detects conflict between two sources:
  1. IDENTIFY the rank of each source (per §5.2)
  2. HIGHER rank wins — no exceptions
  3. IF same rank → prefer more recently updated (check timestamps)
  4. IF unresolvable → STOP and ask human for resolution
  5. DOCUMENT the conflict in response:
     "CONFLICT: {source_A} (Rank {N}) says X. {source_B} (Rank {M}) says Y.
      Resolution: Using {higher_rank_source} per Authority Hierarchy."
```

## 5.5 — Knowledge File Protections

| Action | Permitted? | Condition |
|--------|-----------|-----------|
| Read knowledge files | Always | — |
| Reference knowledge files in responses | Always | Cite file path |
| Propose changes to knowledge files | Yes | Must use governance chain (F9), present as proposal |
| Directly modify knowledge files | **NO** | Requires human approval + governance chain |
| Contradict knowledge files in output | **NEVER** | Even if agent believes knowledge file is wrong, flag it rather than override |
| Create new knowledge files | Yes | Must follow schema standards (F9) and get human approval |

---

# F6: Governance Rules

## 6.1 — Definition

14 empirically-derived governance rules that prevent the most common failure modes in AI-assisted development. These rules are informed by analysis of real failures across extended agentic development (recurring violations, silent regressions, documentation drift, duplicate code).

## 6.2 — Core Rules

### Rule 1: Code Reuse Mandate

**Before writing ANY new code:**

| Step | Action | Tool |
|------|--------|------|
| 1 | Search existing codebase for similar functionality | `grep`, `glob`, semantic search |
| 2 | Check state files and registries for existing scripts/modules | Read `{state_dir}/MASTER_STATE.md` |
| 3 | Check manifest capabilities registry | Read `repo-manifest.json` → `capabilities{}` |
| 4 | Read existing implementations that might cover the need | Targeted file read |

**Violation:** Code duplication is a CRITICAL error. Duplicated functionality must be identified and consolidated. If existing code covers 70%+ of the need, extend it rather than rewrite.

### Rule 2: Automatic MDD Updates (Cascade)

MDD documentation MUST be updated automatically (without user prompting) when:

| Trigger Event | Files to Update | Update Type |
|---------------|-----------------|-------------|
| New script/module created | `MASTER_STATE.md`, relevant registries | Add entry |
| Error resolved | Create `{analysis_dir}/YYYY-MM-DD_ERROR_DEBUG.md` | New file |
| Phase completed | Phase index, `WORK_LOG.md`, completion doc | Status + new file |
| Pattern discovered | Relevant state files | Add entry |
| Metrics changed | Performance/quality reports | Update values |
| Workflow established | Prompt index, relevant docs | Add entry |

**Cascade Rule:** If updating file A affects file B (e.g., MASTER_STATE references PHASES_INDEX), update ALL dependent files in the same operation. Verify consistency after cascade.

### Rule 3: Pre-Planning Decomposition

(See F3 — Complexity Triage System for full specification)

**Core rule:** Complex tasks (6+ steps, 2+ hrs, validation gates) MUST be decomposed into a pre-plan before implementation. Jumping to code is a governance violation.

### Rule 4: Contract-First Validation

**Before any code that reads/writes structured data:**

| Step | Check | When |
|------|-------|------|
| 1 | Identify the contract (JSON schema, type definition, YAML structure, API spec) | Before coding |
| 2 | Verify field names match between producer and consumer | Before coding |
| 3 | Check for renamed/deprecated fields in recent WORK_LOG | Before coding |
| 4 | If no contract exists, CREATE one before implementing | Before coding |
| 5 | Run contract validation (schema check, type check, or manual diff) | After coding |
| 6 | Document any field changes in WORK_LOG entry | After coding |

**Common Failure Patterns:**

| Pattern | Description | Prevention |
|---------|-------------|------------|
| Field Name Drift | Producer uses `content`, consumer expects `body` | Pin names in shared schema/type |
| Version Confusion | v1 data read by v2 parser | Version field in all schemas; validate on read |
| Silent Fallback | Script degrades to lower-quality data source without warning | Fail loud; validate source field; never degrade silently |
| Baseline Mismatch | Metrics compared against stale reference | Timestamp all baselines; verify currency before comparing |

### Rule 5: Script/Module Documentation

Every new script/module MUST include:
- Header docstring: purpose (1 paragraph), features (bullet list), author, date
- Registration in relevant state/registry files
- At minimum one usage example (in docstring or README)

### Rule 6: Prohibited Actions

| # | Prohibition | Severity | Why |
|---|-------------|----------|-----|
| 1 | DO NOT create scripts/modules without searching for existing ones | CRITICAL | Prevents duplication (Rule 1) |
| 2 | DO NOT skip validation for output files | HIGH | Prevents shipping broken artifacts |
| 3 | DO NOT modify knowledge/canonical files without human approval | CRITICAL | Protects constitutional authority (F5) |
| 4 | DO NOT leave MDD documentation inconsistent after changes | HIGH | Cascade violation (Rule 2) |
| 5 | DO NOT bypass validation gates | CRITICAL | Undermines phase system (F4) |
| 6 | DO NOT guess/fabricate file paths | HIGH | Use manifest/search (F1) |
| 7 | DO NOT create duplicate functionality | CRITICAL | Rule 1 violation |
| 8 | DO NOT carry implicit context between sessions | HIGH | Violates context independence (F4 Element 1) |
| 9 | DO NOT claim checks passed without running them | CRITICAL | False confidence → silent failures |
| 10 | DO NOT allow scope creep beyond approved plan | MEDIUM | Undermines plan-review-implement cycle |

### Rule 7: Required Actions

| # | Requirement | When | Why |
|---|-------------|------|-----|
| 1 | ALWAYS search codebase before writing new code | Before any implementation | Rule 1 |
| 2 | ALWAYS validate output before declaring done | After any implementation | Quality assurance |
| 3 | ALWAYS update MDD documentation after changes | After any implementation | Rule 2 |
| 4 | ALWAYS follow P-R-I-L for non-trivial work | For Medium/Complex tasks | Process discipline |
| 5 | ALWAYS use manifest/search for file navigation | Before any file access | Rule F1 |
| 6 | ALWAYS validate contracts for structured data changes | Before/after data code | Rule 4 |
| 7 | ALWAYS log lessons learned after non-trivial work | After task completion | Rule 9 |
| 8 | ALWAYS create completion docs for multi-phase work | After phase completion | F4 Element 9 |
| 9 | ALWAYS state complexity assessment before starting work | Before any implementation | Rule 3 / F3 |
| 10 | ALWAYS verify prerequisites exist before executing a phase | Before phase execution | F4 Element 2 |

### Rule 8: Continuous Improvement

After each task: update relevant docs, log lessons, create error analysis if issues occurred, update metrics, add patterns to knowledge base, archive superseded files.

### Rule 9: Structured Lessons-Learned

Every non-trivial WORK_LOG entry MUST include:

```markdown
* **Lessons Learned:**
  - [What went well — be specific, cite files/techniques]
  - [What went wrong / unexpected — be specific, cite root cause]
  - [What to do differently next time — actionable recommendation]
  - [Regression risk: HIGH/MEDIUM/LOW — describe what could regress and why]
```

**Regression Categories (classify every regression risk):**

| Category | Description | Example | Prevention |
|----------|-------------|---------|------------|
| Field Mismatch | Producer/consumer field name drift | `content` vs `body` | Pin names in shared schema |
| Version Confusion | Stale data read by newer code | v1 golden data + v2 parser | Version fields in schemas |
| Baseline Drift | Metrics compared to wrong baseline | Pre-refactor scores used post-refactor | Timestamp + tag baselines |
| Template Divergence | Output format drifts from template | Missing required section | Template compliance checks |
| Silent Fallback | System degrades without warning | Lower quality data used silently | Fail loud, validate source |

### Rule 10: Enhanced WORK_LOG Template

ALL WORK_LOG entries MUST include these fields:

| Field | Required | Purpose | Example |
|-------|----------|---------|---------|
| **Scope** | Yes | What was done | "Phase 42 — Scoring pipeline precision" |
| **Status** | Yes | Current state | COMPLETE / IN PROGRESS / BLOCKED |
| **Duration** | Yes | Time spent | "~3 hours" |
| **Changes Made** | Yes | File-level change table | `\| file \| change \|` table |
| **Validation Results** | Yes | What was verified | "All 8 gates PASS" |
| **Regression Risk** | Yes | Impact assessment | "MEDIUM — field rename could break consumers" |
| **Lessons Learned** | Yes (non-trivial) | Per Rule 9 | Structured 4-bullet format |
| **Next Steps** | Yes | What follows | "Phase 43" or "None" |
| **Traceability** | Recommended | Link to plan/ticket | "Phase 42 plan: path/to/plan.md" |
| **Manifest Impact** | Recommended | Drift check result | "Ran manifest generator — no drift" |

### Rule 11: Backlog Grooming

(See F10 for full specification)

### Rule 12: Analysis File Archival

| Criteria | Action |
|----------|--------|
| File superseded by newer analysis | Move to `{analysis_dir}/archive/` |
| File >90 days old, no active references | Candidate for archive |
| Pre-plan expanded into phase files | Archive the pre-plan |
| Debug log for resolved issue | Archive after resolution confirmed |

**NEVER delete** — always move to archive.
**NEVER archive:** Active state files, completion docs, files referenced by current plans.

### Rule 13: Phase Completion Documentation

(See F4 Element 9 for full specification)

**Core rule:** Every multi-phase execution MUST produce a `PHASE_XX_COMPLETION.md`. Phase status MUST NOT be set to COMPLETE until the completion doc exists.

### Rule 14: Manifest Drift Enforcement

After pipeline/codebase changes that affect the manifest:

```
1. Run the manifest generator script
2. Check diff on the manifest file
3. If drift detected: update config → re-run generator → include in commit
4. In WORK_LOG entry, report ACTUAL result:
   ✅ "Ran manifest generator — no drift detected"
   ⚠️ "Ran manifest generator — drift in [section], updated manifest"
```

**Violation:** Claiming "no drift" in WORK_LOG without actually running the generator is a governance violation. If the generator cannot run (missing deps), document why and create a backlog item.

---

# F7: Anti-Patterns & Failure Patterns Catalog

## 7.1 — Definition

A curated catalog of empirically-observed anti-patterns (behaviors that consistently lead to failures in agentic development) and failure patterns (specific classes of defects with known prevention strategies). This is institutional memory that prevents regression.

## 7.2 — Session Anti-Patterns

| # | Anti-Pattern | Why It Fails | Correct Alternative | Severity |
|---|--------------|--------------|---------------------|----------|
| 1 | "Continue from where we left off" | New session has zero memory of prior sessions | Reference specific file paths and state files | CRITICAL |
| 2 | "Use the data we extracted earlier" | Agent doesn't know what data, where, or when | Provide exact path + line numbers + format | CRITICAL |
| 3 | "Same as before" / "Do it like last time" | Ambiguous — agent interprets differently each time | Repeat the full specification or reference the plan file | HIGH |
| 4 | Loading entire large files into context | Blows context window; agent forgets earlier content | Read specific sections on-demand (F1 Sniper Protocol) | HIGH |
| 5 | Implicit validation ("looks good") | Silent failures ship undetected | Explicit validation steps with verifiable output | HIGH |
| 6 | Claiming checks passed without running them | False confidence → undetected regressions | Execute command, capture output, paste evidence | CRITICAL |
| 7 | "I think the file is at..." | Path fabrication → failed reads → retry loops | Resolve from manifest or search tools | HIGH |
| 8 | Scope creep during implementation | Unreviewed changes → unintended side effects | Stay strictly within approved plan scope | MEDIUM |
| 9 | Skipping the Plan step for "quick" changes | "Quick" changes that break things take 10x longer to fix | Always triage complexity (F3); plan if >2 steps | MEDIUM |
| 10 | Modifying canonical data without approval | Domain truth corrupted → cascading downstream errors | Human-in-the-loop for knowledge files (F5) | CRITICAL |

## 7.3 — Data/Contract Failure Patterns

| # | Pattern Name | Description | Example | Detection | Prevention |
|---|-------------|-------------|---------|-----------|------------|
| 1 | **Field Name Drift** | Producer and consumer use different field names for the same concept | `content` vs `body` vs `text` | Contract validation (F6 Rule 4) | Pin field names in shared schema; never rename without updating all consumers |
| 2 | **Version Confusion** | Newer code reads stale data format | v1 golden data parsed by v2 parser | Version field check on read | Include `version` field in all structured data; validate on load |
| 3 | **Baseline Drift** | Metrics compared against outdated reference values | Pre-refactor quality scores used to measure post-refactor output | Timestamp check on baseline files | Timestamp all baselines; regenerate after structural changes |
| 4 | **Template Divergence** | Output format drifts from defined template over iterations | Missing required section in generated document | Template compliance check | Run template validator before output; diff against template |
| 5 | **Silent Fallback** | System degrades to lower-quality path without warning | Uses cached/stale data instead of fresh API call | Source field validation in output | Fail loud, not silent; validate `source` field; never degrade without explicit flag |
| 6 | **Phantom Dependency** | Code depends on file/function that was renamed or deleted | Import references deleted module | Static analysis / test run | Run tests before and after changes; check imports |
| 7 | **Cascade Failure** | Change to file A requires changes to B, C, D but only A is updated | Schema change without consumer updates | Dependency tracing | Follow cascade rule (F6 Rule 2); trace all dependents |
| 8 | **Stale Index** | Navigation index (manifest, phase index) doesn't reflect actual state | Manifest lists deleted file | Drift check (F6 Rule 14) | Run manifest generator after changes |

## 7.4 — Process Anti-Patterns

| # | Anti-Pattern | Consequence | Fix |
|---|--------------|-------------|-----|
| 1 | Writing code before planning | Rework, scope creep, unvalidated assumptions | Mandatory complexity triage (F3) |
| 2 | Skipping human review | Incorrect assumptions ship to production | Plan mode ALWAYS ends with human checkpoint |
| 3 | Not logging lessons learned | Same mistakes repeat across sessions | Mandatory structured lessons (F6 Rule 9) |
| 4 | Backlog items added but never reviewed | Silent accumulation of deferred debt | Backlog grooming protocol (F10) |
| 5 | Analysis files accumulating without archival | Context directory becomes unnavigable | Archival policy (F6 Rule 12) |
| 6 | Phase completion without completion doc | No record of what was done or learned | Mandatory completion docs (F4 Element 9) |

---

# F8: Structured Response Formats

## 8.1 — Definition

Three codified response templates — one per operational mode (F2) — that enforce consistent, scannable agent output. Templates reduce noise, ensure actionable content, and make multi-session work traceable.

## 8.2 — Template A: Investigation (Ask Mode)

```
FINDING: [1-2 sentence direct answer to the question]

EVIDENCE:
- File: [exact file path]
- Function/Class: [name, if applicable]
- Line(s): [line range, if applicable]
- Phase: [phase number, if applicable]

NEXT STEPS: [numbered actions if the finding implies work]
1. [Specific, actionable step]
2. [Specific, actionable step]
```

**Usage Contract:**
- Lead with the answer (FINDING), not the investigation process
- Evidence MUST cite exact file paths (no "somewhere in the codebase")
- Max 3 paragraphs of explanatory prose between sections
- Use tables for comparisons, metrics, file lists
- If answer identifies out-of-scope work → suggest backlog item
- If answer is "I don't know" → say so with what was searched

## 8.3 — Template B: Planning (Plan Mode)

```
PLAN: [Topic / Initiative Name]
Complexity: [Simple / Medium / Complex] (per F3 triage)

CONTEXT:
[1-2 paragraphs: What problem? Why now? What constraints?]

CHANGES:
| # | File | Change | LOC Est. |
|---|------|--------|----------|
| 1 | `path/to/file` | [Description of change] | ~NN |
| 2 | ... | ... | ... |

VALIDATION:
- [ ] Gate 1: [description — how to verify]
- [ ] Gate 2: [description — how to verify]

RISKS:
- [Risk 1 — probability, impact, mitigation]
- [Risk 2 — probability, impact, mitigation]

SELF-CRITIQUE:
- Weakest part: [honest assessment]
- How it could fail: [specific scenario]
- Alternative considered: [and why this path is better]

READY FOR REVIEW: YES / NO
```

**Usage Contract:**
- MUST include complexity assessment (F3)
- MUST include at least one validation gate
- MUST include RISKS section with at least one risk
- MUST include SELF-CRITIQUE section (honest assessment)
- MUST end with `READY FOR REVIEW: YES/NO`
- For Complex tasks: create the plan as a file, not inline
- For Medium tasks: inline is acceptable but file is preferred

## 8.4 — Template C: Execution (Agent Mode)

```
CHANGE: [1-2 sentence summary of what was done]

FILES:
| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file` | CREATED / MODIFIED / DELETED | [what and why] |

VALIDATION:
- [x] [Gate 1] — PASS
- [x] [Gate 2] — PASS
- [ ] [Gate 3] — FAIL: [reason and fix]

REGRESSION RISK: [HIGH/MEDIUM/LOW] — [1 sentence description]

NEXT: [What comes next, or "None — task complete"]
```

**Usage Contract:**
- Lead with what was done (CHANGE), not the process
- FILES table must list EVERY file touched (created, modified, or deleted)
- VALIDATION must show actual results (not planned checks)
- REGRESSION RISK must be assessed for every non-trivial change
- If validation FAILED: document failure, do not proceed, report BLOCKED

## 8.5 — Additive Elements (Use in Any Mode)

**Critique Box (use before any meaningful action):**
```
> **RISK:** [quantified blast radius — what files/services/humans affected]
> **ALTERNATIVE:** [one concrete alternative and its trade-off]
> **SELF-CRITIQUE:** [weakest part of this approach]
```

**Backlog Append (use when deferring work):**
```
BACKLOG: - [ ] [Title] – [one line description]. (source: [plan/session/query]).
```

---

# F9: Knowledge Repository Governance Chain

## 9.1 — Definition

A formal governance pipeline for managing canonical knowledge files (Rank 1 in the Authority Hierarchy, F5). The chain ensures that knowledge updates are proposed, reviewed, approved, applied, versioned, and rollback-capable — preventing accidental corruption of constitutional data.

## 9.2 — Governance Pipeline

```
Proposal → Pending Review → Validation → Human Approval → Application → Version Snapshot → History Log
                                                  ↓ (rejected)
                                            Rollback Log
```

### Pipeline Stages

| Stage | Artifact | Path | Actor | Description |
|-------|----------|------|-------|-------------|
| 1. Proposal | PENDING_UPDATES.yaml | `{knowledge_dir}/governance/PENDING_UPDATES.yaml` | Agent | Agent proposes change with rationale, evidence, and affected files |
| 2. Schema Validation | Schema files | `{knowledge_dir}/schemas/*.json` | Automated | Proposed data validated against JSON Schema before human review |
| 3. Human Review | — | — | Human | Human reviews proposed change, accepts or rejects |
| 4. Application | Knowledge files | `{knowledge_dir}/*.yaml` | Agent (after approval) | Agent applies the approved change to the canonical file |
| 5. Version Snapshot | Version directory | `{knowledge_dir}/versions/vX.Y.Z/` | Agent | Snapshot of all knowledge files at this version |
| 6. History Log | UPDATE_HISTORY.yaml | `{knowledge_dir}/governance/UPDATE_HISTORY.yaml` | Agent | Record of what changed, when, why, who approved |
| 7. Rollback (if needed) | ROLLBACK_LOG.yaml | `{knowledge_dir}/governance/ROLLBACK_LOG.yaml` | Human + Agent | Record of reverted changes with reason |

## 9.3 — Artifact Schemas

### PENDING_UPDATES.yaml

```yaml
pending_updates:
  - id: "UPDATE-YYYY-MM-DD-NNN"
    proposed_by: "agent|human"
    date: "YYYY-MM-DD"
    target_file: "path/to/knowledge/file.yaml"
    change_type: "ADD|MODIFY|DELETE"
    change_description: "What is being changed and why"
    evidence:
      - source: "path/to/evidence/file or URL"
        relevance: "Why this evidence supports the change"
    affected_consumers:
      - "path/to/file/that/reads/this/data"
    status: "PENDING|APPROVED|REJECTED"
    reviewer_notes: ""
```

### UPDATE_HISTORY.yaml

```yaml
history:
  - id: "UPDATE-YYYY-MM-DD-NNN"
    applied_date: "YYYY-MM-DD"
    approved_by: "human identifier"
    change_summary: "Brief description"
    version_before: "vX.Y.Z"
    version_after: "vX.Y.Z+1"
    files_modified:
      - "path/to/file.yaml"
    rollback_safe: true|false
```

### ROLLBACK_LOG.yaml

```yaml
rollbacks:
  - id: "ROLLBACK-YYYY-MM-DD-NNN"
    original_update: "UPDATE-YYYY-MM-DD-NNN"
    rollback_date: "YYYY-MM-DD"
    reason: "Why the change was reverted"
    rolled_back_to: "vX.Y.Z"
    executed_by: "human|agent"
```

## 9.4 — Governance Policy Document

Create `{knowledge_dir}/governance/GOVERNANCE_POLICY.md`:

```markdown
# Knowledge Repository Governance Policy

## Principles
1. Knowledge files are constitutional authority (F5 Rank 1)
2. All changes require human approval
3. All changes are versioned and rollback-capable
4. Schema validation is automated and mandatory
5. Evidence must support every proposed change

## Change Process
1. Agent or human proposes change via PENDING_UPDATES.yaml
2. Automated schema validation runs
3. Human reviews and approves/rejects
4. If approved: agent applies change, creates version snapshot, logs to history
5. If rejected: agent records rejection reason in PENDING_UPDATES

## Versioning
- Semantic versioning: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes (field renames, deletions, structure changes)
- MINOR: Additions (new entries, new fields with defaults)
- PATCH: Corrections (typos, data fixes, clarifications)

## Rollback
- Any change can be rolled back by restoring from version snapshot
- Rollback must be logged in ROLLBACK_LOG.yaml
- After rollback: verify all consumers still work
```

## 9.5 — Schema Enforcement

Every knowledge YAML/JSON file should have a corresponding JSON Schema in `{knowledge_dir}/schemas/`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Knowledge File Schema",
  "type": "object",
  "required": ["_meta", "entries"],
  "properties": {
    "_meta": {
      "type": "object",
      "required": ["version", "last_updated"],
      "properties": {
        "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
        "last_updated": { "type": "string", "format": "date" }
      }
    },
    "entries": {
      "type": "array"
    }
  }
}
```

Validation is run automatically before any proposed change is submitted for human review.

## 9.6 — Staging Area

For data imported from external sources (APIs, scrapers, parsed documents):
- Stage to `{knowledge_dir}/staging/` — NOT directly to canonical files
- Staging files are marked "DO NOT EDIT DIRECTLY — staging data for review"
- Human reviews staging data → approves → agent moves to canonical via governance chain

---

# F10: Backlog as First-Class Artifact

## 10.1 — Definition

The backlog (`{backlog}`) is an actively maintained, groomed artifact — not a passive append-only list. Both Ask and Plan modes explicitly instruct agents to append deferred work here. Without formal grooming, deferred items accumulate silently, creating invisible technical debt.

## 10.2 — Backlog Structure

```markdown
---
document_type: STATE
status: ACTIVE
last_groomed: YYYY-MM-DD
---

# Project Backlog

## Open Items

### P0 — Blocking (Must resolve before next phase)
- [ ] [Title] – [one line description]. (source: [origin]).

### P1 — Next Sprint (High priority, scheduled)
- [ ] [Title] – [one line description]. (source: [origin]).

### P2 — Backlog (Medium priority, unscheduled)
- [ ] [Title] – [one line description]. (source: [origin]).

### P3 — Wishlist (Low priority, nice-to-have)
- [ ] [Title] – [one line description]. (source: [origin]).

---

## Resolved
- [x] [Title] – [one line description]. (source: [origin]). Resolved: [date], [how].
- [x] ...

## Deprecated / Closed
- [~] [Title] – [reason for closing without resolution]. Closed: [date].
```

## 10.3 — Priority Definitions

| Priority | Label | SLA | Definition |
|----------|-------|-----|------------|
| **P0** | Blocking | Resolve before next phase | Prevents current work from proceeding; active blocker |
| **P1** | Next Sprint | Address in next 1-2 work cycles | High value/risk; scheduled for near-term |
| **P2** | Backlog | No deadline | Medium value; will be done eventually |
| **P3** | Wishlist | No commitment | Nice-to-have; may never be done |

## 10.4 — Grooming Rules

| Rule | Specification | Enforcement |
|------|---------------|-------------|
| **Source Attribution** | Every item MUST have `(source: ...)` suffix indicating where it came from (plan ID, session, query, phase) | Reject items without source |
| **No Duplicates** | Search existing items before adding; if duplicate found, add source as additional reference | Agent must search before appending |
| **Age-Out** | Items >90 days old without activity MUST be reviewed: re-prioritize (upgrade/downgrade), close with reason, or confirm still relevant | Check during periodic review |
| **Resolved Separation** | Completed items (`[x]`) MUST be moved to `## Resolved` section with resolution date and method | Never leave completed items mixed with open |
| **Periodic Review** | Full backlog review at least once per 5 phases or once per month (whichever is shorter) | Log review date in front-matter |
| **Priority Accuracy** | Items that have been P2+ for >30 days should be evaluated for promotion to P1 or closure | Part of periodic review |

## 10.5 — Agent Behavior by Mode

| Mode | Backlog Behavior |
|------|-----------------|
| **Ask** | If investigation reveals work out of scope → SUGGEST adding to backlog (do not auto-add) |
| **Plan** | When plan defers work → APPEND to backlog with plan ID as source |
| **Agent** | When implementation reveals follow-up work → APPEND to backlog with phase/task as source |

**Append Format:**
```markdown
- [ ] [Title] – [one line description]. (source: [plan/phase/session ID]).
```

## 10.6 — Backlog Metrics (Optional)

Track these metrics during periodic reviews:

| Metric | Target | Action if Exceeded |
|--------|--------|--------------------|
| Total open items | <50 | Aggressive grooming — close or archive stale items |
| P0 items open | 0 | Immediate resolution |
| Items >90 days old | <10% of total | Review and re-prioritize or close |
| Items added vs resolved (monthly) | Ratio <2:1 | Increase resolution velocity or reduce scope |

---

# Appendix A: Directory Structure Template

```
{project_root}/
├── docs/_ai_context/
│   ├── state/
│   │   ├── MASTER_STATE.md          # Project identity, constraints, current state
│   │   ├── WORK_LOG.md              # Change log with enhanced template (F6 Rule 10)
│   │   ├── BACKLOG.md               # Groomed backlog (F10)
│   │   ├── repo-manifest.json       # Machine-readable file/capability index (F1)
│   │   └── [DOMAIN]_STATE.md        # Domain-specific state files
│   ├── analysis/
│   │   ├── YYYY-MM-DD_*_PLAN.md     # Medium complexity plans (F3)
│   │   ├── YYYY-MM-DD_*_DEBUG.md    # Debug/error analysis logs
│   │   ├── PHASE_XX_COMPLETION.md   # Phase completion docs (F4 Element 9)
│   │   └── archive/                 # Superseded analysis files (F6 Rule 12)
│   ├── prompts/
│   │   ├── phases/
│   │   │   ├── PHASE_XX_NAME.md     # Complex phase plans (F3, F4)
│   │   │   ├── PHASES_INDEX.md      # Phase tracking index
│   │   │   ├── CONTEXT_MANIFEST.md  # Navigation + agent contract
│   │   │   └── MULTI_PHASE_EXECUTION_GUIDELINES.md  # Phase protocol (F4)
│   │   ├── PROMPT_INDEX.md          # Prompt discovery entry point
│   │   └── AGENT_*_MODE.md          # Mode-specific prompt files (F2)
│   ├── knowledge/
│   │   ├── *.yaml                   # Canonical domain knowledge (F5 Rank 1)
│   │   ├── governance/
│   │   │   ├── GOVERNANCE_POLICY.md # Knowledge governance policy (F9)
│   │   │   ├── PENDING_UPDATES.yaml # Proposed changes (F9)
│   │   │   ├── UPDATE_HISTORY.yaml  # Applied changes log (F9)
│   │   │   └── ROLLBACK_LOG.yaml    # Reverted changes log (F9)
│   │   ├── schemas/                 # JSON Schema validation (F9)
│   │   ├── versions/               # Version snapshots (F9)
│   │   │   ├── v1.0.0/
│   │   │   └── v1.1.0/
│   │   └── staging/                # External data staging area (F9)
│   ├── templates/                   # Output artifact templates
│   └── skills.md                    # Agent persona & behavioral contract
├── .cursor/
│   ├── rules/
│   │   └── 01-mdd.mdc              # MDD rule file (this specification)
│   └── skills/
│       └── [skill-name]/SKILL.md    # Extracted reusable skills
└── [project source code]
```

---

# Appendix B: Quick Reference Card

| Need | Feature | Section |
|------|---------|---------|
| Start a session | F1: Sniper Mode | Load manifest → targeted reads |
| Answer a question | F2: Ask Mode | FINDING → EVIDENCE → NEXT |
| Plan complex work | F2: Plan Mode + F3: Triage | Assess complexity → create artifact |
| Execute a plan | F2: Agent Mode + F4: Phases | P-R-I-L → atomic changes → log |
| Resolve conflicting info | F5: Authority Hierarchy | Higher rank wins |
| Before writing new code | F6: Rule 1 | Search first, reuse > rewrite |
| After any change | F6: Rule 2 | Cascade MDD updates |
| Before/after data code | F6: Rule 4 | Validate contracts |
| Know what NOT to do | F7: Anti-Patterns | 10 session + 8 data + 6 process |
| Format agent output | F8: Response Templates | Ask/Plan/Agent templates |
| Update domain knowledge | F9: Governance Chain | Propose → Review → Apply → Version |
| Defer work for later | F10: Backlog | P0-P3, source attribution, grooming |

---

# Appendix C: Enforcement Summary

| Feature | Violation Type | Severity | Detection Method |
|---------|---------------|----------|------------------|
| F1: Guess file path | Sniper violation | HIGH | Failed reads in output |
| F1: Read full large file | Efficiency violation | MEDIUM | Token usage analysis |
| F3: Skip triage | Governance violation | HIGH | No complexity statement in response |
| F3: Code without plan (Complex) | Governance violation | CRITICAL | Missing plan artifact |
| F4: Skip completion doc | Phase violation | HIGH | Missing PHASE_XX_COMPLETION.md |
| F4: Proceed past failed gate | Gate violation | CRITICAL | Output shows unresolved failure |
| F5: Contradict knowledge file | Constitutional violation | CRITICAL | Output contradicts Rank 1 source |
| F5: Modify knowledge without approval | Constitutional violation | CRITICAL | Git diff on knowledge files |
| F6.1: Duplicate code | Reuse violation | CRITICAL | Code similarity analysis |
| F6.2: Stale MDD docs | Cascade violation | HIGH | State inconsistency detection |
| F6.6/7: Prohibited/missed required | Rule violation | Varies | Checklist audit |
| F6.9: No lessons learned | Log violation | MEDIUM | WORK_LOG entry inspection |
| F6.14: Claim no drift without check | Integrity violation | CRITICAL | WORK_LOG claims vs evidence |
| F9: Modify knowledge without chain | Governance violation | CRITICAL | Git diff + missing PENDING_UPDATES |
| F10: Backlog item without source | Attribution violation | LOW | Backlog inspection |

---

*Specification Version: 1.0.0 | Date: 2026-03-29 | Status: DRAFT*
*Source: Forensic analysis of 66+ phase BSS pipeline codebase (13 months, 14 governance rules, 100+ analysis files)*
*Applicability: Any AI-assisted codebase using agentic workflows*

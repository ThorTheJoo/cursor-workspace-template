---
document_type: ARCHIVE
status: DEPRECATED
archived_date: "2026-03-31"
superseded_by: "User rule MDD V1.4 (slim personal rule)"
purpose: "Backup of the full MDD V1.3 Cursor personal user rule before slimming"
---

# Archived Personal User Rule — MDD V1.3 Full

This was the user's personal Cursor user rule (`Settings > Rules for AI`). It contained
the complete MDD Protocol V1.3 (~600 lines, ~8K tokens) and was injected into every agent
turn across all workspaces.

Superseded because the workspace rule `01-mdd.mdc` V1.4 now provides the behavioral floor,
making the full user rule redundant (~8K tokens of double-loading per turn).

---

## Original Content (copy of user rule as of 2026-03-31)

```
---
description: "MDD Protocol V1.3 – Agentic Critical Edition (Generic Portable). Markdown-Driven Development methodology for any workspace. Governs context loading, operational modes, phase execution, governance, and documentation authority."
globs: "**/*"
alwaysApply: true
---

# MDD Protocol V1.3 – Generic Portable Edition

**Primary constraint:** Agentic Markdown-Driven Development (MDD).
Agents own **execution**; humans own **intent** and **final sign-off**.

> **Setup:** Copy this file to `.cursor/rules/01-mdd.mdc` in your workspace.
> Search-replace `[PROJECT]` with your project name. Customize Section 14 for your domain.

---

## 1. Context Loading (Sniper Protocol) — MANDATORY FIRST STEP

**Every session MUST begin here.** Load context via manifest, not guessing.

| Priority | File | Purpose |
|----------|------|---------|
| 1 | `docs/_ai_context/state/repo-manifest.json` | Machine-readable index (files, functions, capabilities) |
| 2 | `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` | Navigation, metrics, agent contract |
| 3 | `docs/_ai_context/state/MASTER_STATE.md` | Global project state and constraints |

> **If these files don't exist yet:** Create `MASTER_STATE.md` first (project name, current status, key constraints, architecture overview). The manifest and context manifest can be built incrementally.

**Rules:**
- NEVER read full large files (>500 lines) without targeting specific sections
- NEVER guess file paths — use the manifest or search tools
- NEVER reinvent functionality — check existing capabilities first
- Prefer targeted section reads over full file loads

---

## 2. Authority Hierarchy (Constitution)

Truth has a strict precedence order. Violations are critical errors.

| Rank | Source | Authority | Rule |
|------|--------|-----------|------|
| 1 | `docs/_ai_context/knowledge/` (YAML/JSON reference files) | Canonical domain truth | NEVER contradict; human approval required for changes |
| 2 | `docs/_ai_context/state/` files | Current execution state | Read before modifying |
| 3 | Manifests and indexes | Navigation only | Do NOT define truth, only point to it |
| 4 | This rule file + `.cursor/skills/` | Behavioral guidance | Overridden by ranks 1-3 |

**Non-negotiable constraints:**
- Knowledge files are constituted authority for domain semantics
- MDD documentation is ephemeral project state (not authoritative for domain content)
- Human-in-the-loop for all knowledge file updates
- Config (YAML/JSON) over code: if a change can live in a config file, propose it there first

---

## 3. Operational Modes

Three modes, each with distinct behavior and response format.

### 3a. Ask Mode (Investigation / Sniper)

**Trigger:** Questions about where/how/what/status.

**Workflow:** Parse query → manifest lookup → targeted section read → structured response.

**Response format:**
FINDING: [1-2 sentence direct answer]
EVIDENCE:
- File: [exact path]
- Function: [name if applicable]
NEXT STEPS: [numbered actions if needed]

Max 3 paragraphs prose. Use tables for comparisons, file lists, metrics.
If the answer identifies out-of-scope work, suggest adding to `docs/_ai_context/state/BACKLOG.md`.

### 3b. Plan Mode

**Trigger:** Complex tasks, architecture decisions, multi-step operations.

**Workflow:** Complexity triage → plan file → validation gates → human review.

**Response format:**
PLAN: [Topic]
Complexity: [Simple/Medium/Complex]
CHANGES:
| File | Change | LOC |
|------|--------|-----|
VALIDATION:
- [ ] Gate 1
- [ ] Gate 2
READY FOR REVIEW: YES/NO

When deferring work, append to `BACKLOG.md`: `- [ ] Title – one line. (source: <plan id>).`

### 3c. Agent Mode (Execution)

**Trigger:** Implementation after plan approval.

**Workflow:** P-R-I-L → atomic changes → update WORK_LOG.

**Response format:**
CHANGE: [what was done]
FILES: [paths modified]
VALIDATION: [how to verify]

---

## 4. Complexity Triage

Assess complexity BEFORE starting work. This determines required artifacts.

| Complexity | Criteria | Required Artifact | Location |
|------------|----------|-------------------|----------|
| Simple | 1-2 steps, <30 min | No formal plan | — |
| Medium | 3-5 steps, <2 hrs | Analysis file | `docs/_ai_context/analysis/YYYY-MM-DD_NAME_PLAN.md` |
| Complex | 6+ steps, 2+ hrs, validation gates | Multi-phase plan | `docs/_ai_context/prompts/phases/PHASE_XX_NAME.md` |

**Quick rule:** >2 hours OR >5 steps OR intermediate validation needed → multi-phase.

**Jumping to code for complex tasks without a plan file is a governance violation.**

---

## 5. P-R-I-L Workflow

All non-trivial work follows Plan → Review → Implement → Log.

### Plan
- Simple: inline plan in response
- Medium: single analysis file in `docs/_ai_context/analysis/`
- Complex: pre-plan with numbered todos → individual `PHASE_XX_NAME.md` files
- For execution-style specs: include code snippets, validation commands, and exact file paths per step

### Review
- Human checkpoint before implementation
- Complex plans require explicit approval before any code changes

### Implement
- Atomic changes scoped strictly to the plan
- Stop on validation failure — do not proceed
- No scope creep beyond what the plan specifies

### Log
- Update `docs/_ai_context/state/WORK_LOG.md` using enhanced template (Section 8)
- Structured lessons-learned capture (Section 9)
- Conventional commit: `feat(scope): [summary]`
- Create `docs/_ai_context/analysis/PHASE_XX_COMPLETION.md` for multi-phase work

---

## 6. Phase Execution Protocol

For complex (multi-phase) work. Reference: `docs/_ai_context/prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md`.

### YAML Front-Matter Contract (every phase file)
document_type: PHASE_SPECIFICATION
name: Phase X - [Descriptive Name]
depends_on: [list of files/outputs from prior phases]
outputs_for_next_phase: [explicit paths this phase creates]
validation_gate: [criteria that MUST pass]
estimated_duration: "X-Y hours"

### Core Principles
1. **Context Independence** — Each phase in a fresh session; the plan file IS the context
2. **Explicit Handoffs** — Output from Phase N becomes input for Phase N+1; always specify paths
3. **Validation Gates** — Named gates that must pass before marking complete
4. **Atomic Commits** — Each phase = one logical commit; enables rollback
5. **Kickoff Prompts** — Every phase ends with a copy-paste prompt for the next phase
6. **Parallel Markers** — Use `⚡ with Phase X` for phases that can run independently

### Error Recovery
- **Step failure:** Document error → attempt fix → if unfixable, rollback + create analysis file
- **Gate failure:** Identify failing check → fix → re-run → do NOT proceed until pass
- **Abandonment:** Document progress → commit with `WIP:` prefix → create analysis for next attempt

---

## 7. Governance Rules

### 7a. Code Reuse Mandate
Before writing ANY new code:
1. Search existing codebase (grep, glob, semantic search)
2. Check script registries and state files
3. Read existing implementations that might cover the need

### 7b. Automatic MDD Updates
MDD documentation MUST be updated automatically when:
- New scripts or modules created → update `MASTER_STATE.md` and registries
- Errors resolved → create/update analysis in `docs/_ai_context/analysis/`
- Phase completed → update phase index, `WORK_LOG.md`, completion doc
- Patterns discovered → update relevant state files

### 7c. Contract-First Validation
Before code that reads/writes structured data:
1. Identify the contract (schema, type definition, YAML structure)
2. Verify field names match between producer and consumer
3. Check for renamed/deprecated fields in recent WORK_LOG

### 7d. Prohibited Actions
1. DO NOT create scripts/modules without searching for existing ones
2. DO NOT skip validation for output files
3. DO NOT modify knowledge/reference files without human approval
4. DO NOT leave MDD documentation inconsistent after changes
5. DO NOT bypass validation gates
6. DO NOT guess file paths — use manifest or search
7. DO NOT create duplicate functionality

### 7e. Required Actions
1. ALWAYS search codebase before writing new code
2. ALWAYS validate output before declaring done
3. ALWAYS update MDD documentation after changes
4. ALWAYS follow P-R-I-L for non-trivial work
5. ALWAYS use manifest/search for navigation
6. ALWAYS validate contracts for structured data changes
7. ALWAYS log lessons learned after non-trivial work
8. ALWAYS create completion docs for multi-phase work

---

## 8. Enhanced WORK_LOG Template

All WORK_LOG entries MUST include these fields:

| Field | Required | Purpose |
|-------|----------|---------|
| Scope | Yes | What was done |
| Status | Yes | COMPLETE / IN PROGRESS / BLOCKED |
| Duration | Yes | Approximate time spent |
| Changes Made | Yes | File-level change table |
| Validation Results | Yes | What was verified and outcome |
| Regression Risk | Yes | HIGH/MEDIUM/LOW + description |
| Lessons Learned | Yes (non-trivial) | Per Section 9 |
| Next Steps | Yes | What comes next, or "None" |

---

## 9. Lessons-Learned & Anti-Patterns

### Structured Lessons-Learned (add to every non-trivial WORK_LOG entry)
* **Lessons Learned:**
  - [What went well]
  - [What went wrong / unexpected]
  - [What to do differently next time]
  - [Regression risk: HIGH/MEDIUM/LOW — what could regress]

### Anti-Patterns (NEVER do these)
| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| "Continue from where we left off" | New session has no memory | Reference specific file paths |
| "Use the data we extracted earlier" | Agent doesn't know what/where | Provide exact path + line numbers |
| "Same as before" | Ambiguous | Repeat the specification |
| Loading entire large files | Blows context window | Read specific sections on-demand |
| Implicit validation | Silent failures | Explicit validation steps |
| Claiming checks passed without running | False confidence | Execute command, paste output |

---

## 10. Critical Feedback & Honesty

Before any meaningful action, agents MUST include:

1. **Flaws & Risks** — Quantified blast radius: what files, services, or humans are affected.
2. **Self-critique** — "What is the weakest part of this plan? How could it fail?"
3. **Self-verification** — Run tests/lint/validation if they exist. Record results.

Zero flattery. Brutal honesty. Terse and direct.

---

## 11. Learn Step (Skills Extraction)

After completing work:
- If a pattern appears >= 3 times across sessions, extract it into `.cursor/skills/[pattern-name]/SKILL.md`
- Structure: trigger conditions, context loading, key commands, response style, constraints
- Update WORK_LOG with the extracted pattern
- Update `AGENTS.md` or skill registries if they exist

---

## 12. Backlog Management

`docs/_ai_context/state/BACKLOG.md` is actively maintained:
- **Priority labels:** P0 (blocking), P1 (next sprint), P2 (backlog), P3 (wishlist)
- **Format:** `- [ ] Title – one line. (source: <origin>).`
- **Source attribution:** Every item must have source
- **Age-out:** Items >90 days without activity → re-prioritize or close with reason
- **No duplicates:** Search existing items before adding
- **Resolved items:** Move completed items to `## Resolved` section

---

## 13. Analysis Archival

Keep `docs/_ai_context/analysis/` navigable:
- Superseded files → move to `docs/_ai_context/analysis/archive/`
- Files >90 days old with no active references → candidate for archive
- Pre-plans expanded into phase files → archive the pre-plan
- NEVER delete archived files — always move

---

## 14. Domain-Specific Rules (CUSTOMIZE FOR YOUR PROJECT)

> Replace this section with rules specific to your project domain.

---

## 15. Architectural Structure

| Path | Role | Phase |
|------|------|-------|
| `docs/_ai_context/state/MASTER_STATE.md` | Agent-updated project state | All |
| `docs/_ai_context/state/WORK_LOG.md` | Change log with lessons-learned | Log |
| `docs/_ai_context/state/BACKLOG.md` | Groomed backlog | All |
| `docs/_ai_context/state/repo-manifest.json` | Machine-readable file/function index | All |
| `docs/_ai_context/analysis/` | Plans, debug logs, completion docs | Analysis/Debug |
| `docs/_ai_context/analysis/archive/` | Superseded analysis files | Archival |
| `docs/_ai_context/prompts/` | Reusable prompts and phase specs | All |
| `docs/_ai_context/knowledge/` | Canonical domain knowledge (YAML/JSON) | All |
| `docs/_ai_context/templates/` | Standardized output templates | Implementation |
| `.cursor/rules/` | Project rules | All |
| `.cursor/skills/` | Reusable agent skills | All |

---

## 16. YAML Front-Matter Standard

All MDD markdown documents should include front-matter:
document_type: [PLAN | DEBUG | COMPLETION | STATE | PROMPT | SKILL | GOVERNANCE]
status: [DRAFT | ACTIVE | APPROVED | DEPRECATED]

---

## 17. Git Conventions

Standard commits: feat(scope): [summary] / fix(scope): [summary] / docs(scope): [summary]
Phase commits: feat(pipeline): Phase XX - [summary]
Partial work: WIP: Phase XX partial - [what's done]
```

---
name: mdd-workflow
description: "Markdown-Driven Development methodology for AI-assisted codebases. Use whenever setting up a new project with AI agents, establishing documentation workflows, defining authority hierarchies for AI context, or implementing Plan-Review-Implement-Log (P-R-I-L) cycles. Triggers on: project setup, documentation architecture, agent workflow, P-R-I-L, MDD, governance, complexity triage, or context management."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# MDD Workflow

Markdown-Driven Development (MDD) treats structured documentation as a first-class engineering artifact. Instead of ad-hoc prompting or scattered notes, MDD encodes decisions, workflows, and domain knowledge into markdown files that both humans and AI agents can read, update, and execute against. This prevents context loss between sessions, enforces quality through validation gates, and creates an auditable trail of every significant decision.

MDD works because AI agents lose context between sessions. Without structured documentation, each session starts from zero. With MDD, the documentation *is* the context — an agent reads the plan file and has everything it needs.

## Authority Hierarchy

Truth has a strict precedence. When sources conflict, higher rank wins.

| Rank | Source | Example | Rule |
|------|--------|---------|------|
| 1 | Knowledge Repository (`knowledge/`) | YAML/JSON reference files, taxonomies, glossaries | Canonical domain truth — human approval required to change |
| 2 | State Files (`state/`) | MASTER_STATE.md, WORK_LOG.md, BACKLOG.md | Current execution state — read before modifying |
| 3 | Manifests & Indexes | repo-manifest.json, CONTEXT_MANIFEST.md | Navigation only — point to truth, don't define it |
| 4 | Rules & Skills | .cursor/rules/, .cursor/skills/ | Behavioral guidance — overridden by ranks 1-3 |

This hierarchy prevents a common failure mode: an agent follows a skill instruction that contradicts the actual data in a knowledge file. The knowledge file always wins.

For detailed examples and conflict resolution, see `references/authority-hierarchy.md`.

## P-R-I-L Workflow

Every non-trivial change follows four steps. This prevents scope creep because the plan constrains what gets implemented, and the log captures what actually happened.

| Step | What Happens | Why It Matters |
|------|-------------|----------------|
| **Plan** | Write a plan document appropriate to complexity | Forces thinking before doing; creates context for future agents |
| **Review** | Human checkpoint before implementation | Catches wrong assumptions before they become code |
| **Implement** | Atomic changes scoped strictly to the plan | Prevents scope creep; enables rollback |
| **Log** | Update WORK_LOG.md, commit, create completion doc | Creates institutional memory; prevents repeated mistakes |

Skip P-R-I-L only for truly trivial changes (typo fixes, single-line config updates). When in doubt, plan first.

For the full protocol with artifact requirements per step, see `references/pril-workflow.md`.

## Complexity Triage

Assess complexity *before* starting work. This determines what documentation artifacts are required.

| Complexity | Criteria | Required Artifact |
|------------|----------|-------------------|
| **Simple** | 1-2 steps, < 30 min | No formal plan — inline plan in response |
| **Medium** | 3-5 steps, < 2 hrs | Analysis file in `docs/_ai_context/analysis/` |
| **Complex** | 6+ steps, 2+ hrs, or needs validation gates | Multi-phase plan in `docs/_ai_context/prompts/phases/` |

**Quick rule:** More than 2 hours OR more than 5 steps OR intermediate validation needed → multi-phase plan.

Jumping to code for a complex task without a plan file is a governance violation — it wastes time when the agent inevitably loses context mid-task.

For the full decision matrix, see `references/complexity-triage.md`.

## Operational Modes

MDD defines three modes, each with a distinct response format.

### Ask Mode (Investigation)

Use when answering questions about where, how, what, or status.

```
FINDING: [1-2 sentence direct answer]
EVIDENCE:
- File: [exact path]
- Function: [name if applicable]
NEXT STEPS: [numbered actions if needed]
```

Keep prose to 3 paragraphs maximum. Use tables for comparisons and file lists.

### Plan Mode

Use when the task is complex, has multiple valid approaches, or requires architectural decisions.

```
PLAN: [Topic]
Complexity: [Simple/Medium/Complex]
CHANGES:
| File | Change | LOC |
|------|--------|-----|
VALIDATION:
- [ ] Gate 1
- [ ] Gate 2
READY FOR REVIEW: YES/NO
```

### Agent Mode (Execution)

Use when implementing an approved plan.

```
CHANGE: [what was done]
FILES: [paths modified]
VALIDATION: [how to verify]
```

## Critical Feedback

Before any meaningful action, include honest self-assessment:

1. **Flaws & Risks** — Quantify the blast radius: what files, services, or people are affected. Name one concrete alternative and its trade-off.
2. **Self-critique** — Identify the weakest part of the plan and how it could fail.
3. **Self-verification** — Run tests or validation if they exist. Record results. If skipping, flag why.

No flattery. Direct and terse. The goal is to catch mistakes before they happen, not to sound confident.

## Directory Structure

MDD uses a standard directory layout so agents can navigate any MDD workspace predictably.

```
docs/_ai_context/
├── state/              # Current execution state (MASTER_STATE, WORK_LOG, BACKLOG)
├── analysis/           # Plans, debug logs, completion docs, investigations
│   └── archive/        # Superseded analysis files (never delete, always move)
├── prompts/            # Reusable prompts and workflow templates
│   └── phases/         # Phase execution plans (PHASE_XX_NAME.md)
├── knowledge/          # Canonical domain knowledge (YAML/JSON) — constitutional authority
│   └── reference/      # Reference files (taxonomies, catalogs, schemas)
└── templates/          # Standardized output templates
```

For the full layout with descriptions, see `assets/directory-structure.md`.

## Governance Quick Reference

| Rule | What It Means |
|------|---------------|
| Code reuse mandate | Search codebase before writing new code — duplication is a critical error |
| Automatic MDD updates | Update docs when creating scripts, resolving errors, or completing phases |
| Contract-first validation | Verify field names match between producer and consumer before writing code |
| Config over code | If a change can live in a config file, propose it there first |

**Prohibited:**
- Creating scripts without checking if one already exists
- Modifying knowledge repository files without human approval
- Leaving MDD documentation inconsistent after changes
- Guessing file paths — use the manifest or search

**Required:**
- Search before code, validate output, update docs, follow P-R-I-L, use manifest for navigation

For the full governance rules, see `references/governance-rules.md`.

## Archival

Keep `docs/_ai_context/analysis/` navigable:
- Superseded files move to `archive/` subfolder
- Files older than 90 days without active references are candidates for archiving
- Pre-plans expanded into phase files should be archived
- Never delete archived files — always move

For details, see `references/archival-rules.md`.

## Git Conventions

Use conventional commits to make change history scannable:

```
feat(scope): summary          # New feature
fix(scope): summary           # Bug fix
docs(scope): summary          # Documentation only
refactor(scope): summary      # Code restructuring
```

For phase work: `feat(pipeline): Phase XX - summary`
For partial work: `WIP: Phase XX partial - what's done`

For the full convention, see `references/git-conventions.md`.

## References

| File | Content |
|------|---------|
| `references/authority-hierarchy.md` | Detailed hierarchy with conflict resolution examples |
| `references/pril-workflow.md` | Full P-R-I-L protocol with artifact requirements |
| `references/complexity-triage.md` | Decision matrix and complexity criteria |
| `references/governance-rules.md` | Complete governance rules with prohibited/required actions |
| `references/archival-rules.md` | File archival rules and procedures |
| `references/git-conventions.md` | Full git commit convention with examples |
| `assets/directory-structure.md` | Standard MDD directory layout diagram |

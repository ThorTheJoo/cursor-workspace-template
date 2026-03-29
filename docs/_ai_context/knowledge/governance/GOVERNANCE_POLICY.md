---
document_type: GOVERNANCE
status: APPROVED
version: "1.0.0"
---

# Governance Policy

## Purpose

Defines the mandatory metadata, compliance, and traceability standards for all Markdown-driven artifacts in this workspace. Enforces the Knowledge Governance Chain (MDD V1.3 Section 11) and Compliance by Design (MDD V1.3 Section 7).

## YAML Front-Matter Requirements

ALL Markdown documents in `docs/_ai_context/` MUST include YAML front-matter.

### Mandatory Fields

| Key | Required | Governance Purpose | Valid Values |
|-----|----------|--------------------|--------------|
| `document_type` | Always | LLM context filtering | `PLAN`, `PRE_PLAN`, `PHASE_SPECIFICATION`, `COMPLETION`, `DEBUG`, `ADR`, `STATE`, `GOVERNANCE`, `RUNBOOK`, `PROMPT`, `KNOWLEDGE` |
| `status` | Always | Workflow state management | `DRAFT`, `PENDING_REVIEW`, `APPROVED`, `ACTIVE`, `DEPRECATED`, `ARCHIVED` |
| `date` | Always | Temporal traceability | `YYYY-MM-DD` |

### Conditional Fields

| Key | When Required | Purpose |
|-----|---------------|---------|
| `reviewer.accountable` | Plans, ADRs, Governance | RACI Accountability (single person) |
| `consulted` | When expert input was sought | RACI Consulted (list of people) |
| `compliance_tags` | When regulatory/policy applies | Audit readiness (e.g., `CSG AI Policy`, `GDPR`, `PCI`, `SOC2`) |
| `traceability_id` | When mapping to business function | Business traceability (e.g., `TMF GB1033-001`) |
| `version` | Governance docs, rules, templates | Semantic versioning for controlled docs |

## Document Lifecycle

```
DRAFT -> PENDING_REVIEW -> APPROVED -> [ACTIVE | DEPRECATED | ARCHIVED]
```

* **DRAFT**: Author is still working. Not actionable.
* **PENDING_REVIEW**: Ready for the accountable reviewer.
* **APPROVED**: Reviewed and accepted. May be executed.
* **ACTIVE**: Living document in use (e.g., MASTER_STATE, PROMPT_INDEX).
* **DEPRECATED**: Superseded. Kept for history. Not to be used.
* **ARCHIVED**: Moved to `analysis/archive/`. No longer relevant.

## Naming Conventions

| Artifact Type | Pattern | Example |
|---|---|---|
| Plan | `YYYY-MM-DD_[Topic]_PLAN.md` | `2026-03-29_auth-migration_PLAN.md` |
| Pre-Plan | `YYYY-MM-DD_[Topic]_PREPLAN.md` | `2026-03-29_db-refactor_PREPLAN.md` |
| Debug Log | `YYYY-MM-DD_[Error]_DEBUG.md` | `2026-03-29_null-pointer-api_DEBUG.md` |
| ADR | `ADR-NNNN_[Title].md` | `ADR-0001_use-trpc-over-rest.md` |
| Phase | `PHASE_XX_[Name].md` | `PHASE_01_SCHEMA_SETUP.md` |
| Completion | `PHASE_XX_COMPLETION.md` | `PHASE_01_COMPLETION.md` |

## Knowledge Governance Chain

The MDD V1.3 Learn Step mandates continuous knowledge extraction:

1. **Observe**: During every task, note patterns, surprises, and failures.
2. **Extract**: After task completion, extract reusable knowledge.
3. **Classify**: Place in the correct location:
   * Reusable prompts -> `prompts/` (add to `PROMPT_INDEX.md`)
   * Domain knowledge -> `knowledge/`
   * Schemas/contracts -> `knowledge/schemas/`
   * Governance/policy -> `knowledge/governance/`
   * Patterns (>= 3 occurrences) -> `prompts/` or `templates/`
4. **Version**: Major changes to governance docs get `version` bumps.
5. **Archive**: Superseded docs move to `analysis/archive/` with `status: ARCHIVED`.

## Context Hygiene

* After completing a task, move temporary analysis files to `analysis/archive/`.
* Keep `state/` files current — stale state is worse than no state.
* `MASTER_STATE.md` is the canonical project snapshot. Update it after every significant change.
* `WORK_LOG.md` is append-only. Never delete entries.
* `BACKLOG.md` is the deferred-work queue. Review and groom periodically.

## Commit Traceability

All commits MUST use conventional prefixes and reference the driving Markdown file:

```
feat(auth): implement login endpoint per PLAN-20260329
fix(api): resolve null pointer per DEBUG-20260329
docs(mdd): update governance policy v1.1.0
chore(deps): bump trpc to v11.2
```

## Compliance Audit Trail

For regulated work, the following chain must be traceable:

```
Business Requirement (traceability_id)
  -> Plan (analysis/*.md)
    -> Implementation (source code)
      -> Validation (completion doc with gate results)
        -> Deployment (runbook with validation steps)
```

Every link in this chain must be recoverable from the Markdown artifacts.


## Conflict Resolution Protocol

Reference: MDD V1.3 Feature Spec F5.4. When two sources of truth conflict:

```
WHEN agent detects conflict between two sources:
  1. IDENTIFY the rank of each source (per Authority Hierarchy in 01-mdd.mdc Section 2)
  2. HIGHER rank wins — no exceptions
  3. IF same rank -> prefer more recently updated (check timestamps)
  4. IF unresolvable -> STOP and ask human for resolution
  5. DOCUMENT the conflict in response:
     "CONFLICT: {source_A} (Rank {N}) says X. {source_B} (Rank {M}) says Y.
      Resolution: Using {higher_rank_source} per Authority Hierarchy."
```

**Rank reminder:**

| Rank | Source | Example |
|------|--------|---------|
| 1 | Canonical Knowledge (YAML/JSON) | `knowledge/*.yaml` |
| 2 | State Files | `state/MASTER_STATE.md` |
| 3 | Manifests and Indexes | `state/repo-manifest.json` |
| 4 | Rule Files | `.cursor/rules/*.mdc` |
| 5 | Agent Reasoning | Ephemeral analysis |

## Knowledge File Protections

Reference: MDD V1.3 Feature Spec F5.5. Knowledge files (`knowledge/*.yaml`, `knowledge/*.json`) are constitutional authority.

| Action | Permitted? | Condition |
|--------|-----------|-----------|
| Read knowledge files | Always | No restrictions |
| Reference in responses | Always | Cite file path |
| Propose changes | Yes | Must use governance chain (PENDING_UPDATES.yaml), present as proposal |
| Directly modify | **NO** | Requires human approval + governance chain |
| Contradict in output | **NEVER** | Even if agent believes file is wrong, flag it rather than override |
| Create new knowledge files | Yes | Must follow schema standards and get human approval |

## Knowledge Change Process

Full governance chain for modifying canonical knowledge:

1. Agent or human proposes change via `governance/PENDING_UPDATES.yaml`
2. Automated schema validation runs (against `schemas/*.json`)
3. Human reviews and approves/rejects
4. If approved: agent applies change, creates version snapshot in `versions/`, logs to `UPDATE_HISTORY.yaml`
5. If rejected: agent records rejection reason in PENDING_UPDATES

### Versioning for Knowledge Files

* **MAJOR**: Breaking changes (field renames, deletions, structure changes)
* **MINOR**: Additions (new entries, new fields with defaults)
* **PATCH**: Corrections (typos, data fixes, clarifications)

### Rollback

* Any change can be rolled back by restoring from version snapshot in `versions/`
* Rollback must be logged in `governance/ROLLBACK_LOG.yaml`
* After rollback: verify all consumers still work

## Staging Area Protocol

For data imported from external sources (APIs, scrapers, parsed documents):

1. Stage to `knowledge/staging/` — NOT directly to canonical files
2. Staging files are marked "DO NOT EDIT DIRECTLY — staging data for review"
3. Human reviews staging data -> approves -> agent moves to canonical via governance chain
4. Never treat staging data as authoritative

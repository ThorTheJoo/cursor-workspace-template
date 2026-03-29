---
document_type: GOVERNANCE
status: ACTIVE
version: "1.0.0"
---

# Continuous Improvement Protocol

Reference: MDD V1.3 Section 11 (Learn Step), Feature Spec F9.

This protocol closes the feedback loop in the P-R-I-L workflow, making it **P-R-I-L-L** (Plan-Review-Implement-Log-**Learn**). Every non-trivial task ends with a structured learning evaluation that routes discoveries into the reference architecture.

## When This Triggers

After **every** non-trivial task completion (Medium or Complex per Complexity Triage), immediately after updating WORK_LOG.md and before the final commit.

## The Learning Checklist

Run through this checklist. If ANY item applies, execute the routing action.

### 1. Anti-Pattern Discovery

> Did a failure, bug, or inefficiency match — or NOT match — a known anti-pattern?

| Condition | Action |
|-----------|--------|
| Failure matches existing catalog entry | Note the pattern ID in WORK_LOG lessons learned |
| Failure does NOT match any existing entry | Propose new entry to `knowledge/ANTI_PATTERNS_CATALOG.md` (Name, Description, Example, Detection, Prevention) |

**Route:** `knowledge/ANTI_PATTERNS_CATALOG.md`

### 2. Reusable Pattern Extraction

> Did a coding pattern, prompt structure, or workflow appear >= 3 times across sessions?

| Condition | Action |
|-----------|--------|
| Pattern is a prompt/instruction | Extract to `prompts/[CATEGORY]_[TASK].md`, add to `prompts/PROMPT_INDEX.md` |
| Pattern is a behavioral skill | Extract to `.cursor/skills/[pattern-name]/SKILL.md` |
| Pattern is a code snippet/utility | Extract to shared library, update `state/repo-manifest.json` capabilities |

**Route:** `prompts/` or `.cursor/skills/` or source code

### 3. Process Gap

> Did the workflow miss a step, produce friction, or require improvisation?

| Condition | Action |
|-----------|--------|
| Gap is in a template | Propose template update via `knowledge/governance/PENDING_UPDATES.yaml` |
| Gap is in a rule | Document gap, propose rule refinement via `knowledge/governance/PENDING_UPDATES.yaml` |
| Gap is a missing capability | Add to `state/BACKLOG.md` with source attribution |

**Route:** `knowledge/governance/PENDING_UPDATES.yaml` or `state/BACKLOG.md`

### 4. Domain Knowledge

> Did we learn something new about the problem domain, technology, or constraints?

| Condition | Action |
|-----------|--------|
| Knowledge is from external source | Stage to `knowledge/staging/` with source citation |
| Knowledge is from internal analysis | Add to `knowledge/` directly if minor; use governance chain if major |
| Knowledge contradicts existing canonical file | STOP. Flag conflict. Do NOT modify. Propose via `PENDING_UPDATES.yaml` |

**Route:** `knowledge/staging/` or `knowledge/governance/PENDING_UPDATES.yaml`

### 5. Template/Governance Refinement

> Did an existing template or governance doc prove insufficient?

| Condition | Action |
|-----------|--------|
| Missing section in template | Propose addition via `PENDING_UPDATES.yaml` |
| Template section was confusing | Propose clarification via `PENDING_UPDATES.yaml` |
| Governance policy has a gap | Propose amendment via `PENDING_UPDATES.yaml` |

**Route:** `knowledge/governance/PENDING_UPDATES.yaml`

### 6. Architecture Observation

> Did we discover something about the project structure, performance, or scalability?

| Condition | Action |
|-----------|--------|
| Minor observation | Log in WORK_LOG lessons learned |
| Significant finding requiring action | Create analysis file: `analysis/YYYY-MM-DD_[Topic]_PLAN.md` |
| Blocking issue | Add as P0 to `state/BACKLOG.md` |

**Route:** `state/WORK_LOG.md` or `analysis/` or `state/BACKLOG.md`

## Routing Decision Tree

```
After completing work and updating WORK_LOG:
  |
  v
[Run through 6 checklist items]
  |
  +-- New anti-pattern?
  |     YES --> Propose to ANTI_PATTERNS_CATALOG.md
  |
  +-- Reusable pattern (>= 3x)?
  |     YES --> Extract to prompts/ or skills/
  |             Update PROMPT_INDEX.md
  |
  +-- Process gap?
  |     YES --> PENDING_UPDATES.yaml (template/rule change)
  |             or BACKLOG.md (missing capability)
  |
  +-- Domain knowledge?
  |     YES --> knowledge/staging/ (external)
  |             or PENDING_UPDATES.yaml (contradicts canonical)
  |
  +-- Template/governance gap?
  |     YES --> PENDING_UPDATES.yaml
  |
  +-- Architecture observation?
  |     YES --> WORK_LOG (minor) or analysis/ (major) or BACKLOG P0 (blocking)
  |
  v
[Update MASTER_STATE.md if project state changed]
  |
  v
[Commit with conventional prefix + traceability]
```

## Integration Points

This protocol is triggered by:

| Artifact | Where It Calls This Protocol |
|----------|------------------------------|
| `01-mdd.mdc` Section 11 | Learn Step: "After completing work..." |
| `templates/PHASE_COMPLETION_TEMPLATE.md` | Lessons Learned section routes here |
| `templates/DEBUG_LOG_TEMPLATE.md` | Prevention section routes here |
| `knowledge/governance/GOVERNANCE_POLICY.md` | Knowledge Governance Chain: Observe -> Extract -> Classify |
| `prompts/PROMPT_INDEX.md` | Reusable Prompts section explains extraction criteria |

## Promotion Pipeline

Learnings follow this promotion path:

```
Observation (WORK_LOG)
  -> Staging (knowledge/staging/ or PENDING_UPDATES.yaml)
    -> Human Review
      -> Canonical Knowledge (knowledge/*.yaml) -- domain truth
      -> Updated Template (templates/*.md) -- process improvement
      -> Updated Rule (01-mdd.mdc amendment) -- behavioral change
      -> New Skill (.cursor/skills/) -- reusable capability
      -> New Prompt (prompts/) -- reusable instruction
```

## Review Cadence

| Trigger | Review Scope |
|---------|-------------|
| Every 5 phases completed | Full PENDING_UPDATES.yaml review |
| Monthly | BACKLOG grooming + PENDING_UPDATES review |
| Major milestone | Full architecture review against this checklist |
| Post-incident | Targeted review of anti-patterns + governance |

## Metrics (Track in MASTER_STATE.md)

| Metric | Target | Action if Missed |
|--------|--------|-----------------|
| Learnings logged per 5 tasks | >= 3 entries | Review if tasks are truly trivial or if logging is being skipped |
| PENDING_UPDATES reviewed | Within 7 days of proposal | Escalate or auto-close stale proposals |
| Patterns extracted to skills/prompts | >= 1 per month | Review WORK_LOG for missed patterns |
| BACKLOG items resolved vs added | Ratio < 2:1 | Increase resolution velocity |

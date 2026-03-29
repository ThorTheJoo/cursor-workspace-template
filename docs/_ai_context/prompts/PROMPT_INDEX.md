---
document_type: PROMPT
status: ACTIVE
---

# Prompt Index

Single entry point for discovering all reusable prompts, phase plans, and mode-specific instructions in this workspace.

## Session Prompts

| Prompt | File | When to Use |
|---|---|---|
| Session Start | `SESSION_START.md` | Copy-paste into a new session to initialize MDD context loading |

## Phase Plans

| Phase | File | Status | Description |
|---|---|---|---|
| Guidelines | `phases/MULTI_PHASE_EXECUTION_GUIDELINES.md` | ACTIVE | How to plan, execute, and complete multi-phase work |
| Context | `phases/CONTEXT_MANIFEST.md` | ACTIVE | Navigation map and agent contract for Sniper Mode |

> Add phase files here as complex work is decomposed: `phases/PHASE_XX_NAME.md`

## Templates (for generating artifacts)

| Template | Location | When to Use |
|---|---|---|
| Medium Plan | `../templates/MEDIUM_PLAN_TEMPLATE.md` | 3-5 step tasks, 30 min - 2 hrs |
| Complex Pre-Plan | `../templates/COMPLEX_PREPLAN_TEMPLATE.md` | 6+ step tasks requiring phase decomposition |
| Phase Completion | `../templates/PHASE_COMPLETION_TEMPLATE.md` | After every phase completes |
| Debug Log | `../templates/DEBUG_LOG_TEMPLATE.md` | Bug investigation and troubleshooting |
| ADR | `../templates/ADR_TEMPLATE.md` | Architectural decisions of significance |
| Runbook | `../templates/RUNBOOK_TEMPLATE.md` | Operational procedures with validation steps |

## Response Format Templates

| Template | Location | Mode |
|---|---|---|
| Ask Mode | `../templates/RESPONSE_FORMAT_ASK.md` | Investigation / Questions |
| Plan Mode | `../templates/RESPONSE_FORMAT_PLAN.md` | Architecture / Design |
| Agent Mode | `../templates/RESPONSE_FORMAT_AGENT.md` | Implementation / Execution |

## Reference Knowledge

| Document | Location | Purpose |
|---|---|---|
| Complexity Triage | `../knowledge/COMPLEXITY_TRIAGE_MATRIX.md` | Decide Simple / Medium / Complex tier |
| Mode Transitions | `../knowledge/MODE_TRANSITION_RULES.md` | State machine for Ask / Plan / Agent |
| Anti-Patterns | `../knowledge/ANTI_PATTERNS_CATALOG.md` | Full failure pattern catalog |
| Governance Policy | `../knowledge/governance/GOVERNANCE_POLICY.md` | Metadata, compliance, knowledge protections |
| Continuous Improvement | `../knowledge/governance/CONTINUOUS_IMPROVEMENT_PROTOCOL.md` | Learning loop routing (P-R-I-L-L) |

## Reusable Prompts

> Add extracted prompt patterns here as they emerge (per MDD V1.3 Section 11 - Learn Step).
>
> Naming convention: `[CATEGORY]_[TASK].md`
> Example: `CODE_REVIEW_CHECKLIST.md`, `MIGRATION_STEPS.md`

(none yet - prompts are extracted after patterns appear >= 3 times)

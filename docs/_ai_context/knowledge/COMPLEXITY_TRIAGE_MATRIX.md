---
document_type: KNOWLEDGE
status: ACTIVE
version: "1.0.0"
---

# Complexity Triage Decision Matrix

Reference: MDD V1.3 Section 3 (Complexity Triage) / Feature Spec F2.

Use this matrix at the START of every non-trivial request to determine the correct execution path.

## Triage Criteria

| Dimension | Simple | Medium | Complex |
|-----------|--------|--------|---------|
| **Steps** | 1-2 | 3-5 | 6+ |
| **Files touched** | 1 | 2-4 | 5+ |
| **Estimated duration** | < 30 min | 30 min - 2 hrs | > 2 hrs |
| **Cross-cutting concerns** | None | Some (e.g., tests) | Multiple (auth, DB, UI, tests, config) |
| **Ambiguity** | Requirements are clear | Some open questions | Significant unknowns |
| **Risk of regression** | Negligible | Moderate | High |

## Decision Rules

### Simple -> Direct Execution (Agent Mode)

**When ALL of these are true:**
* 1-2 steps
* Single file or tightly scoped change
* Requirements are unambiguous
* No validation gates needed

**Protocol:**
1. Execute directly
2. Log in `state/WORK_LOG.md`
3. Commit

### Medium -> Plan First (Plan Mode)

**When ANY of these are true:**
* 3-5 steps
* 2-4 files touched
* Some open questions to resolve
* Validation needed

**Protocol:**
1. Create `analysis/YYYY-MM-DD_[Topic]_PLAN.md` using `templates/MEDIUM_PLAN_TEMPLATE.md`
2. Get review approval
3. Execute plan
4. Log completion in `state/WORK_LOG.md`
5. Commit

### Complex -> Pre-Plan + Phased Execution

**When ANY of these are true:**
* 6+ steps
* 5+ files touched
* > 2 hours estimated
* Multiple cross-cutting concerns
* Significant unknowns or risk

**Protocol:**
1. Create `analysis/YYYY-MM-DD_[Topic]_PREPLAN.md` using `templates/COMPLEX_PREPLAN_TEMPLATE.md`
2. Get review approval
3. Decompose into phase files: `prompts/phases/PHASE_XX_NAME.md`
4. Follow `prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md`
5. Execute phases sequentially (or parallel where marked)
6. Create completion docs per phase
7. Update `state/MASTER_STATE.md` and `state/WORK_LOG.md`
8. Final integration validation
9. Commit per phase

## Quick-Reference Flowchart

```
START: New Request
  |
  v
[Count steps, files, duration, unknowns]
  |
  +-- All criteria = Simple? ---> Execute directly
  |
  +-- Any criteria = Medium? ---> Create PLAN -> Review -> Execute
  |
  +-- Any criteria = Complex? --> Create PRE-PLAN -> Review -> Phase Files -> Execute per phase
```

## Override Rules

* **User explicitly requests a plan** -> Always produce a plan regardless of complexity.
* **User says "just do it"** -> Treat as Simple, but still log.
* **Uncertainty about complexity** -> Default to the HIGHER tier (better to over-plan than under-plan).
* **Spike/investigation needed** -> Create a time-boxed investigation phase before committing to a full plan.

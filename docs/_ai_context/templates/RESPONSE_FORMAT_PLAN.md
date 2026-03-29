---
document_type: TEMPLATE
status: ACTIVE
version: "1.0.0"
---

# Response Format: Plan Mode

Reference: MDD V1.3 Feature Spec F8, Template B.

Use this format when proposing plans for complex tasks, architecture decisions, or multi-step operations.

---

## Template

```
PLAN: [Topic / Initiative Name]
Complexity: [Simple / Medium / Complex] (per Complexity Triage)

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

---

## Usage Contract

* MUST include complexity assessment
* MUST include at least one validation gate
* MUST include RISKS section with at least one risk
* MUST include SELF-CRITIQUE section (honest assessment — not perfunctory)
* MUST end with `READY FOR REVIEW: YES/NO`
* For Complex tasks: create the plan as a file, not inline
* For Medium tasks: inline is acceptable but file is preferred

---

## Additive Element: Critique Box

Use before any meaningful action in any mode:

```
> **RISK:** [quantified blast radius — what files/services/humans affected]
> **ALTERNATIVE:** [one concrete alternative and its trade-off]
> **SELF-CRITIQUE:** [weakest part of this approach]
```

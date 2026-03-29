---
document_type: KNOWLEDGE
status: ACTIVE
version: "1.0.0"
---

# Operational Mode Transition Rules

Reference: MDD V1.3 Feature Spec F2.

## The Three Modes

| Mode | Purpose | Side Effects | Default Safety |
|------|---------|-------------|----------------|
| **Ask** | Investigation, questions, status checks | NONE (read-only) | Safe — no file modifications |
| **Plan** | Architecture, design, multi-step planning | Creates plan files only | Safe — no implementation code |
| **Agent** | Implementation, execution | Modifies source code and state | Requires approved plan |

## Mode Selection Heuristic

```
IF query is a question (where/how/what/why/status)
  -> ASK

ELSE IF task has >2 steps OR >30 min OR involves architecture
  -> PLAN

ELSE IF task is simple AND plan exists or is trivial
  -> AGENT

ELSE
  -> ASK (default safe mode)
```

## Transition State Machine

```
         +----------+
         |          |
         v          |
   +----------+     | "Need more info"
   |   ASK    |-----+
   +----------+
     |      |
     |      | "Work needed" (user confirms)
     |      v
     |  +----------+
     |  |   PLAN   |<------+
     |  +----------+       |
     |      |              | "Scope change"
     |      | "Human       |
     |      |  approves"   |
     |      v              |
     |  +----------+       |
     +->|  AGENT   |-------+
        +----------+
              |
              | "Unexpected state"
              v
         +----------+
         |   ASK    | (investigate)
         +----------+
```

## Allowed Transitions

| From | To | Trigger | Constraint |
|------|----|---------|------------|
| ASK | PLAN | Investigation reveals work needed | User confirms transition |
| ASK | AGENT | **PROHIBITED for non-trivial work** | Only for Simple tasks (1-2 steps) |
| PLAN | AGENT | Human approves the plan | Explicit approval required |
| PLAN | ASK | Planning reveals need for investigation | Agent suggests, proceeds to investigate |
| AGENT | ASK | Implementation reveals unexpected state | STOP implementation, investigate first |
| AGENT | PLAN | Implementation scope needs revision | STOP implementation, re-plan |

## Prohibited Transitions

| Transition | Why | What to Do Instead |
|-----------|-----|-------------------|
| ASK -> AGENT (non-trivial) | Skips planning, skips human review | ASK -> PLAN -> (review) -> AGENT |
| PLAN -> AGENT (no approval) | Human checkpoint bypassed | Wait for explicit approval |
| AGENT -> AGENT (scope change) | Scope creep without re-planning | AGENT -> PLAN -> (review) -> AGENT |

## Mode-Specific Backlog Behavior

| Mode | Backlog Action |
|------|---------------|
| **Ask** | If investigation reveals out-of-scope work -> SUGGEST adding to backlog (do not auto-add) |
| **Plan** | When plan defers work -> APPEND to backlog with plan ID as source |
| **Agent** | When implementation reveals follow-up work -> APPEND to backlog with phase/task as source |

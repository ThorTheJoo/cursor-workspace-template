# YAML Front-Matter Standard

Every MDD markdown document should include front-matter for agent filtering, dependency tracking, and status management.

## Required Fields (Plans)

```yaml
---
document_type: PLAN           # PLAN | DEBUG | COMPLETION | STATE | PROMPT | SKILL | GOVERNANCE
status: DRAFT                 # DRAFT | ACTIVE | APPROVED | COMPLETE | DEPRECATED
depends_on:
  - "path/to/predecessor/output"
  - "path/to/required/input"
outputs_for_next_phase:
  - "path/to/output/file1"
  - "path/to/output/file2"
validation_gate:
  - "description of gate 1"
  - "description of gate 2"
---
```

## Optional Fields

```yaml
estimated_duration: "2-3 hours"
traceability_id: "PHASE-XX-NAME-YYYYMMDD"    # Links git commits to plans
reviewer:
  accountable: "person or role"
compliance_tags: ["tag1", "tag2"]
generated: "YYYY-MM-DD"
phase: "XX"                                    # Phase number for multi-phase work
```

## Field Descriptions

| Field | Purpose | When Required |
|-------|---------|---------------|
| `document_type` | Enables filtering by document kind | Always |
| `status` | Tracks lifecycle state | Always |
| `depends_on` | Lists inputs from prior phases — used to verify prerequisites | Plans |
| `outputs_for_next_phase` | Lists outputs — used by next phase's `depends_on` | Plans |
| `validation_gate` | Criteria that must pass before marking complete | Plans |
| `estimated_duration` | Helps with scheduling and complexity assessment | Recommended for plans |
| `traceability_id` | Connects documentation to git commits and backlog items | Recommended |

## Status Lifecycle

```
DRAFT → ACTIVE → APPROVED → COMPLETE
                          → DEPRECATED (if superseded)
```

- **DRAFT**: Work in progress, not yet reviewed
- **ACTIVE**: Currently being worked on
- **APPROVED**: Reviewed and approved for execution
- **COMPLETE**: All validation gates passed
- **DEPRECATED**: Superseded by a newer version (keep for history)

## Agents and Front-Matter

Agents should respect `document_type` and `status` when selecting context:
- Only reference `COMPLETE` or `ACTIVE` plans for historical context
- Skip `DEPRECATED` documents unless specifically investigating history
- Use `depends_on` to verify prerequisites before executing

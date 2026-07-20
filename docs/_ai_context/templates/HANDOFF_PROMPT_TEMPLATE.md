---
document_type: TEMPLATE
status: ACTIVE
purpose: Ultra-dense portable handoff prompt skeleton (Gate 0 + triple-index)
---

# Handoff Prompt Template

Copy into `docs/_ai_context/prompts/<NAME>_HANDOFF_PROMPT.md`. Fill every `{{PLACEHOLDER}}`.

After authoring, register the prompt in **three** places (triple-index):

1. `docs/_ai_context/prompts/PROMPT_INDEX.md` (workflow letter + sniper block)
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` (capability / navigation row)
3. `docs/_ai_context/state/repo-manifest.json` (`sub_projects` or workflow key)

---

```markdown
---
document_type: PROMPT
status: ACTIVE
traceability_id: "{{TRACE-ID}}"
prompt_index_workflow: "{{LETTER}}"
predecessor_workflows: []
compliance_tags: ["Handoff", "MDD"]
---

# {{TITLE}}

## WHERE THIS FILE LIVES
`docs/_ai_context/prompts/{{FILENAME}}`

## PROMPT START (copy below into a new agent chat)

You are executing workflow **{{LETTER}}**: {{ONE_LINE_PURPOSE}}.

### HARD GATE 0 — Prerequisites (must pass before analysis)
| Prerequisite | Status |
|--------------|--------|
| {{INPUT_A}} | REQUIRED — locate or ask user |
| {{INPUT_B}} | REQUIRED |

If Gate 0 fails: stop, list missing paths, do not invent data.

### MDD session load (order)
1. `docs/_ai_context/state/repo-manifest.json`
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md`
3. `docs/_ai_context/prompts/PROMPT_INDEX.md`
4. `docs/_ai_context/state/MASTER_STATE.md`
5. `docs/_ai_context/state/WORK_LOG.md`

### Security
- Read-only by default.
- External writes require chat consent + `EXTERNAL_WRITE_CONSENT=1`.

### Steps
1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

### Outputs
| Artifact | Path |
|----------|------|
| Analysis | `docs/_ai_context/analysis/YYYY-MM-DD_{{SLUG}}.md` |
| Data | `{{DATA_PATH}}` |

### MDD cascade on completion
- Update WORK_LOG (Duration, Validation, Regression Risk, Lessons)
- Bump repo-manifest + CONTEXT_MANIFEST `manifest_lockstep`
- Refresh MASTER_STATE note if deliverable changed
```

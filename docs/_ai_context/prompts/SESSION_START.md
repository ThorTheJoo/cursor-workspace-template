---
document_type: PROMPT
status: ACTIVE
---

# Session Start Prompt

Copy-paste this into a new Cursor session to initialize MDD context loading properly.

Prefer the denser preloader: `AGENT_INITIAL_PRELOADER.md`.

## Standard Session Start

```
Load context in order:
1. docs/_ai_context/state/repo-manifest.json (follow sniper_context_loading if present)
2. docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md
3. docs/_ai_context/prompts/PROMPT_INDEX.md
4. docs/_ai_context/state/MASTER_STATE.md
5. docs/_ai_context/state/WORK_LOG.md (recent handoff)

Respond using the appropriate mode format (Ask/Plan/Agent) per the MDD protocol.
Do NOT read full large files. Use manifest to resolve paths.
Do NOT assume legacy keys files[] / capabilities{} exist on repo-manifest.json.
Check docs/_ai_context/analysis/ for recent decisions or active plans before starting.
External writes require chat consent + EXTERNAL_WRITE_CONSENT=1.
```

## Resuming Multi-Phase Work

```
Load the 5-file sniper stack (repo-manifest → CONTEXT_MANIFEST → PROMPT_INDEX → MASTER_STATE → WORK_LOG).
Check the phase index at docs/_ai_context/prompts/phases/ for current phase status.
Execute the next incomplete phase. Follow the kickoff prompt in the prior phase's completion doc.
Do NOT assume context from prior sessions - the phase file IS the complete context.
```

## Investigation / Question Session

```
Load the 5-file sniper stack. Use Ask mode. Answer using FINDING/EVIDENCE/NEXT STEPS.
If the answer identifies work needed, suggest adding to docs/_ai_context/state/BACKLOG.md.
```

## Quick Fix Session

```
Load docs/_ai_context/state/MASTER_STATE.md and WORK_LOG.md for current project state.
This is a simple (1-2 step) task. Execute directly in Agent mode.
Log non-trivial outcomes in WORK_LOG.md.
```

## Handoff / Cross-Machine Resume

```
Open the relevant *_HANDOFF_PROMPT.md from PROMPT_INDEX (or create from docs/_ai_context/templates/HANDOFF_PROMPT_TEMPLATE.md).
Pass HARD GATE 0 before analysis. Cascade MDD indexes on completion.
```

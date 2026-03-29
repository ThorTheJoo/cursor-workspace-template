---
document_type: PROMPT
status: ACTIVE
---

# Session Start Prompt

Copy-paste this into a new Cursor session to initialize MDD context loading properly.

## Standard Session Start

```
Load context from docs/_ai_context/state/repo-manifest.json and docs/_ai_context/state/MASTER_STATE.md.
Respond using the appropriate mode format (Ask/Plan/Agent) per the MDD protocol.
Do NOT read full large files. Use manifest to resolve paths.
Check docs/_ai_context/analysis/ for recent decisions or active plans before starting.
```

## Resuming Multi-Phase Work

```
Load context from docs/_ai_context/state/repo-manifest.json and docs/_ai_context/state/MASTER_STATE.md.
Check the phase index at docs/_ai_context/prompts/phases/ for current phase status.
Execute the next incomplete phase. Follow the kickoff prompt in the prior phase's completion doc.
Do NOT assume context from prior sessions — the phase file IS the complete context.
```

## Investigation / Question Session

```
Load context from docs/_ai_context/state/repo-manifest.json and docs/_ai_context/state/MASTER_STATE.md.
Use Ask mode. Answer using the FINDING/EVIDENCE/NEXT STEPS format.
If the answer identifies work needed, suggest adding to docs/_ai_context/state/BACKLOG.md.
```

## Quick Fix Session

```
Load docs/_ai_context/state/MASTER_STATE.md for current project state.
This is a simple (1-2 step) task. Execute directly in Agent mode.
Update docs/_ai_context/state/WORK_LOG.md when complete.
```

---

## Tips

* Always start with context loading — even for "quick" tasks, reading MASTER_STATE prevents redundant work.
* For large projects, the `repo-manifest.json` saves significant time vs. searching.
* If the manifest is missing or stale, use IDE search tools (grep/glob) as a fallback and flag the missing manifest.

---
document_type: PROMPT
status: ACTIVE
purpose: Initial instruction preloader for Ask/Agent sessions (portable)
compliance_tags: ["MDD", "Agent-Workflow"]
---

# Agent Initial Preloader

**Use this as your first message in a new chat to prime the agent.**

---

## Copy-paste block (sniper preloader)

```
You are working in this MDD workspace. Before answering or acting:

**Authority (read first, in order):**
1. `docs/_ai_context/state/repo-manifest.json` — prefer `sniper_context_loading.priority_files` when present
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md`
3. `docs/_ai_context/prompts/PROMPT_INDEX.md`
4. `docs/_ai_context/state/MASTER_STATE.md`
5. `docs/_ai_context/state/WORK_LOG.md` (handoff / recent changes)
- Semantic truth: `docs/_ai_context/knowledge/` (never contradict without human approval)

**Manifest contract:** Do NOT assume legacy root keys `files[]`, `state_files[]`, or `capabilities{}` exist — modern manifests use `sniper_context_loading` + `sub_projects` (see `docs/_ai_context/templates/REPO_MANIFEST_V2.template.json`).

**Mode:**
- **Ask:** FINDING → EVIDENCE → NEXT STEPS. Max 3 paragraphs prose. Defer out-of-scope to BACKLOG.md.
- **Agent:** P-R-I-L. Plan → human Review → Implement → Log WORK_LOG + conventional commit.

**Capabilities:** Prefer Script Registry in MASTER_STATE and CONTEXT_MANIFEST capability tables. Run `node scripts/verify_script_registry.js` after registry edits.

**Security:** No external-system writes without explicit chat consent + `EXTERNAL_WRITE_CONSENT=1`.

Execute my following instruction in the appropriate mode (Ask or Agent).
```

---

## Related

- Shorter variants: `SESSION_START.md`
- Workflow discovery: `PROMPT_INDEX.md`

---
document_type: STATE
status: ACTIVE
last_groomed: 2026-03-29
---

# Project Backlog

## Open Items

### P0 - Blocking
(none)

### P1 - Next Sprint
- [ ] Create repo-manifest.json generator script per V1.3 Sniper Mode. (source: MDD V1.3 Section 1.4).

### P2 - Backlog
- [ ] Add pre-commit hook (husky/lint-staged) for manifest validation. (source: worktree forensic analysis).
- [ ] Create .cursor/settings.json with recommended Cursor preferences. (source: improvement plan WS-002).
- [ ] Add V1.3 migration guide for V1.2 workspaces. (source: WORK_LOG v2.0.0 lessons).

### P3 - Wishlist
- [ ] Auto-generate AGENTS.md from repo-manifest.json. (source: V1.3 Sniper Mode).
- [ ] Add GitHub Actions CI for manifest validation. (source: enterprise polish).
- [ ] Create example .cursor/skills/ seed showing skill file structure. (source: cohesion audit v2.1.0).

---

## Resolved
- [x] Create PROMPT_INDEX.md entry point for prompt discovery. (source: MDD V1.3 Section 15). Resolved: 2026-03-29, created as prompts/PROMPT_INDEX.md.
- [x] Create MULTI_PHASE_EXECUTION_GUIDELINES.md in prompts/phases/. (source: MDD V1.3 Section 6). Resolved: 2026-03-29, created as prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md.
- [x] Add knowledge governance files (GOVERNANCE_POLICY.md, PENDING_UPDATES.yaml). (source: MDD V1.3 Section 9). Resolved: 2026-03-29, created full governance pipeline.
- [x] Wire continuous improvement / feedback loop into reference architecture. (source: cohesion audit v2.1.0). Resolved: 2026-03-29, CONTINUOUS_IMPROVEMENT_PROTOCOL.md + rule Section 11 wiring.
- [x] Create CONTEXT_MANIFEST.md referenced by rule Section 1. (source: cohesion audit v2.1.0). Resolved: 2026-03-29, created as prompts/phases/CONTEXT_MANIFEST.md.
- [x] Fix bootstrappers to create all 11 MDD subdirs (not just 5). (source: cohesion audit v2.1.0). Resolved: 2026-03-29, both scripts updated.

## Deprecated / Closed
(none yet)

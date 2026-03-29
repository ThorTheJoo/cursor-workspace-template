# AGENTS.md - Cursor Workspace Starter

A portable, zero-global-pollution workspace template for Cursor IDE. Every new workspace inherits foundational AI rules (MDD V1.3 + King Mode + Full-Stack) and on-demand GitHub tool management.

## Repo Map

```
.
+-- docs/_ai_context/              # MDD V1.3 SSOT
|   +-- state/                     # MASTER_STATE.md, WORK_LOG.md, BACKLOG.md, repo-manifest.json
|   +-- analysis/                  # Plans (*_PLAN.md), debug logs, completion docs
|   |   +-- archive/              # Superseded analysis files
|   +-- templates/                 # ADR_TEMPLATE.md, artifact formats
|   +-- prompts/                   # Reusable prompt library
|   |   +-- phases/               # Phase execution plans for complex work
|   +-- knowledge/                 # Canonical domain knowledge (Rank 1)
|       +-- governance/           # PENDING_UPDATES, UPDATE_HISTORY, ROLLBACK_LOG
|       +-- schemas/              # JSON Schema validation
|       +-- versions/             # Version snapshots
|       +-- staging/              # External data staging
+-- .cursor/rules/                 # Foundational AI rules (always committed)
|   +-- 00-starter-rules.mdc      # Meta-rules: loading order + priority hierarchy
|   +-- 01-mdd.mdc                # MDD V1.3 Agentic Critical Edition
|   +-- 02-kingmode.mdc           # King Mode (ULTRATHINK, intentional minimalism)
|   +-- 03-frontend-fullstack.mdc # Next.js/tRPC/Shadcn/Tailwind/Zod conventions
+-- .cursor/bin/                   # Tool binaries (populated by bootstrapper)
+-- .cursor/skills/                # Agent skills (populated by bootstrapper)
+-- .cursor/mcp/                   # MCP server configs (future use)
+-- tools/manifest.json            # SSOT: all GitHub tools available for install
+-- .tools-cache/                  # Cloned tool repos (gitignored)
+-- setup-tools.ps1                # Windows/PowerShell bootstrapper
+-- setup-tools.sh                 # Bash/WSL/DevContainer bootstrapper
+-- .devcontainer/devcontainer.json
+-- CHANGELOG.md
+-- AGENTS.md
+-- README.md
```

## Rule Hierarchy

1. **00-starter-rules.mdc** - Always loaded. Orchestrator: loading order, priority resolution, workspace paths. Zero behavioral content.
2. **01-mdd.mdc** - Always loaded. MDD V1.3: Sniper Mode context loading, Ask/Plan/Agent modes, P-R-I-L, complexity triage, 14 governance rules, phase execution, authority hierarchy.
3. **02-kingmode.mdc** - Always loaded. King Mode: ULTRATHINK, intentional minimalism, library discipline, response format.
4. **03-frontend-fullstack.mdc** - Glob-scoped to code files. Stack conventions only (no duplication from 02).

**Priority:** MDD (01) wins on process. King Mode (02) wins on design. Full-Stack (03) wins on implementation.

## MDD V1.3 Context Paths

| Path | Content | V1.3 Role |
|---|---|---|
| `docs/_ai_context/state/MASTER_STATE.md` | Current workspace snapshot | Read first every session (Sniper Mode) |
| `docs/_ai_context/state/WORK_LOG.md` | Chronological change log | Enhanced template (Section 8) |
| `docs/_ai_context/state/BACKLOG.md` | Prioritized backlog (P0-P3) | First-class artifact (Feature 10) |
| `docs/_ai_context/state/repo-manifest.json` | Machine-readable file index | Sniper Mode navigation (Feature 1) |
| `docs/_ai_context/analysis/` | Plans and debug logs | Medium complexity artifacts |
| `docs/_ai_context/prompts/phases/` | Phase execution plans | Complex work (Feature 4) |
| `docs/_ai_context/knowledge/` | Canonical domain data | Rank 1 authority (Feature 5) |
| `docs/_ai_context/templates/ADR_TEMPLATE.md` | Decision record scaffold | MADR format |

## Tool Management

* `tools/manifest.json` is the single source of truth for installable tools.
* Both bootstrappers validate manifest JSON before proceeding.
* Run `setup-tools.ps1` (Windows) or `./setup-tools.sh` (Bash) to interactively select and install.
* Cloned repos go into `.tools-cache/` (gitignored, never committed).

## Conventions

* MDD V1.3 Sniper Mode: load context from manifest, not guessing.
* Three operational modes: Ask (investigation), Plan (architecture), Agent (execution).
* P-R-I-L workflow: Plan -> Review -> Implement -> Log.
* Flaws & Risks before any meaningful action.
* ULTRATHINK triggers exhaustive multi-dimensional analysis.
* Code follows Intentional Minimalism + Full-Stack conventions.

# Cursor Workspace Starter

A portable, zero-global-pollution workspace template for Cursor IDE. Every new workspace built from this template inherits foundational AI rules (MDD V1.3 + King Mode + Full-Stack) and on-demand access to your collected GitHub tools.

## Quick Start

```powershell
# Windows (PowerShell)
.\setup-tools.ps1

# Bash / WSL / Dev Container
chmod +x setup-tools.sh && ./setup-tools.sh
```

The bootstrapper validates `tools/manifest.json`, creates the MDD documentation structure, presents an interactive checklist, and installs only what you select. Restart Cursor after setup.

## What's Included

| Component | Purpose |
|---|---|
| `.cursor/rules/00-starter-rules.mdc` | Meta-rules: loading order, priority hierarchy, workspace paths |
| `.cursor/rules/01-mdd.mdc` | MDD V1.3 Agentic Critical Edition - Sniper Mode, 3 modes, 14 governance rules |
| `.cursor/rules/02-kingmode.mdc` | King Mode - Intentional minimalism, ULTRATHINK, library discipline |
| `.cursor/rules/03-frontend-fullstack.mdc` | Full-Stack conventions - Next.js 14+, tRPC, Shadcn, Tailwind, Zod |
| `docs/_ai_context/` | MDD V1.3 SSOT - state, analysis, templates, prompts, knowledge (11 subdirs) |
| `tools/manifest.json` | Single source of truth for all GitHub tools you collect |
| `setup-tools.ps1` / `setup-tools.sh` | Cross-platform interactive bootstrapper with manifest validation |
| `.devcontainer/devcontainer.json` | Ubuntu Dev Container with git, jq, fzf, Node LTS |
| `AGENTS.md` | Repo map for Cursor Composer 2 agentic context discovery |
| `CHANGELOG.md` | Version history |

## Pre-Configured Tools

| Tool | Type | Install Method |
|---|---|---|
| [Kilo CLI](https://github.com/Kilo-Org/kilocode) | CLI | `npm install -g @kilocode/cli` |
| [GSD](https://github.com/gsd-build/get-shit-done) | Plugin | `npx get-shit-done-cursor --cursor --local` |
| [Anthropic Skills](https://github.com/anthropics/skills) | Skills | Clone + copy into `.cursor/skills/` |
| [Autoresearch](https://github.com/karpathy/autoresearch) | Research | `uv sync` (requires NVIDIA GPU) |
| [King Mode](https://github.com/aicodeking/yt-tutorial) | Rules | Already embedded as `02-kingmode.mdc` |

## How Rules Work

Cursor 2.6+ loads `.mdc` files from `.cursor/rules/` based on frontmatter:

* `alwaysApply: true` - Active in every chat session (rules 00, 01, and 02).
* `globs: [...]` - Active only when matching files are open (rule 03 activates on code files).

The starter enforces this hierarchy with zero duplication:

1. **00** orchestrates loading order and priority resolution.
2. **01** (MDD V1.3) owns all process: Sniper Mode, Ask/Plan/Agent modes, P-R-I-L, governance, state logging.
3. **02** (King Mode) owns all design: intentional minimalism, ULTRATHINK, library discipline, response format.
4. **03** (Full-Stack) owns all implementation: Next.js, tRPC, Shadcn, Tailwind, Zod, testing, deployment.

## Directory Structure

```
.
+-- .cursor/
|   +-- rules/               # AI rules (4 foundational .mdc files)
|   +-- bin/                  # Tool binaries (populated by bootstrapper)
|   +-- skills/              # 8 curated agent skills (committed, available on clone)
|   +-- mcp/                 # MCP server configs
+-- docs/
|   +-- _ai_context/         # MDD V1.3 SSOT
|       +-- state/           # MASTER_STATE.md, WORK_LOG.md, BACKLOG.md, repo-manifest.json
|       +-- analysis/        # Plans, debug logs, completion docs
|       |   +-- archive/    # Superseded files
|       +-- templates/       # ADR_TEMPLATE.md, artifact formats
|       +-- prompts/         # Reusable prompt library
|       |   +-- phases/     # Phase execution plans
|       +-- knowledge/       # Canonical domain knowledge
|           +-- governance/ # Knowledge governance chain
|           +-- schemas/    # JSON Schema validation
|           +-- versions/   # Version snapshots
|           +-- staging/    # External data staging
+-- tools/
|   +-- manifest.json        # Tool registry (SSOT)
+-- .tools-cache/            # Cloned repos (gitignored)
+-- setup-tools.ps1          # Windows bootstrapper
+-- setup-tools.sh           # Bash bootstrapper
+-- .devcontainer/
|   +-- devcontainer.json
+-- AGENTS.md                # Repo map
+-- CHANGELOG.md             # Version history
+-- README.md                # This file
+-- .gitignore
```

## Adding a New Tool

1. Open `tools/manifest.json`.
2. Copy the `_template` object into the `tools` array.
3. Fill in `name`, `repo`, `description`, `installCmd`, `platform`, and `type`.
4. Run the bootstrapper again - it validates the JSON and skips already-installed tools.

Example entry:

```json
{
  "name": "my-tool",
  "repo": "https://github.com/org/my-tool",
  "description": "What it does inside Cursor.",
  "installCmd": "npm install -g my-tool-cli",
  "platform": "both",
  "type": "cli"
}
```

## Making This a GitHub Template

1. Push this folder to a new GitHub repository.
2. Go to **Settings** > **General**.
3. Check **Template repository**.
4. Every new repo created from this template starts with your rules, manifest, and MDD structure.

## Updating Existing Workspaces

```bash
git remote add template https://github.com/YOUR-USER/cursor-workspace-starter.git
git fetch template
git merge template/main --allow-unrelated-histories
```

## License

MIT - use however you want.

# Cursor Workspace Starter

A portable, zero-global-pollution workspace template for Cursor IDE. Every new workspace built from this template inherits your foundational AI rules and gives you on-demand access to your collected GitHub tools.

## Quick Start

```powershell
# Windows (PowerShell)
.\setup-tools.ps1

# Bash / WSL / Dev Container
chmod +x setup-tools.sh && ./setup-tools.sh
```

The bootstrapper reads `tools/manifest.json`, presents an interactive checklist, and installs only what you select. Restart Cursor after setup.

## What's Included

| Component | Purpose |
|---|---|
| `.cursor/rules/01-mdd.mdc` | MDD Protocol V1.2 — P-R-I-L workflow, brutal honesty, Markdown as SSOT |
| `.cursor/rules/02-frontend-fullstack.mdc` | Full-Stack conventions — Next.js 14+, tRPC, Shadcn, Tailwind, Zod, RSC-first |
| `.cursor/rules/00-starter-rules.mdc` | Meta-rules enforcing the above two as non-optional baselines |
| `tools/manifest.json` | Single source of truth for all GitHub tools you collect |
| `setup-tools.ps1` / `setup-tools.sh` | Cross-platform interactive bootstrapper |
| `.devcontainer/devcontainer.json` | Ubuntu Dev Container with git, jq, fzf, Node LTS pre-installed |
| `AGENTS.md` | Repo map for Cursor Composer 2 agentic context discovery |

## Pre-Configured Tools

The manifest ships with four tools ready to install:

| Tool | Type | Install Method |
|---|---|---|
| [Kilo CLI](https://github.com/Kilo-Org/kilocode) | CLI | `npm install -g @kilocode/cli` |
| [GSD](https://github.com/gsd-build/get-shit-done) | Plugin | `npx get-shit-done-cursor --cursor --local` |
| [Anthropic Skills](https://github.com/anthropics/skills) | Skills | Clone + copy into `.cursor/skills/` |
| [Autoresearch](https://github.com/karpathy/autoresearch) | Research | `uv sync` (requires NVIDIA GPU) |

## Adding a New Tool

1. Open `tools/manifest.json`.
2. Copy the `_template` object into the `tools` array.
3. Fill in `name`, `repo`, `description`, `installCmd`, `platform`, and `type`.
4. Run the bootstrapper again — it skips already-installed tools.

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
4. Every new repo created from this template starts with your rules and manifest.

## Updating Existing Workspaces

If you update the template (new rules, new tools in manifest):

```bash
# Add the template repo as a remote
git remote add template https://github.com/YOUR-USER/cursor-workspace-starter.git

# Pull changes (merge or cherry-pick as needed)
git fetch template
git merge template/main --allow-unrelated-histories
```

## How Rules Work

Cursor 2.6+ loads `.mdc` files from `.cursor/rules/` based on frontmatter:

- `alwaysApply: true` — Active in every chat session (rules 00 and 01).
- `globs: [...]` — Active only when matching files are open (rule 02 activates on `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.html`).

The starter enforces this hierarchy:
1. MDD V1.2 thinking first (Flaws & Risks, P-R-I-L workflow).
2. Full-Stack conventions second (RSC, Shadcn, Tailwind, Zod, tRPC).
3. Tool-specific rules third (from anything installed via the bootstrapper).

## Pro Tips for Cursor 2.6+

- **Composer 2 agents** read `AGENTS.md` for repo-level context discovery. Keep it updated as your project grows.
- **Skills** in `.cursor/skills/` are dynamically loaded. Install Anthropic's skills collection for document creation, data analysis, and more.
- **MCP servers** can be configured in `.cursor/mcp/`. Add server configs as JSON files for external tool integrations.
- **The bootstrapper is idempotent** — run it again any time to add new tools without affecting existing installs.
- **`.tools-cache/` is gitignored** — cloned repos never pollute your commit history.

## Directory Structure

```
.
├── .cursor/
│   ├── rules/               # AI rules (always committed)
│   ├── bin/                  # Tool binaries (populated by bootstrapper)
│   ├── skills/              # Agent skills (populated by bootstrapper)
│   └── mcp/                 # MCP server configs
├── tools/
│   └── manifest.json        # Tool registry (SSOT)
├── .tools-cache/            # Cloned repos (gitignored)
├── setup-tools.ps1          # Windows bootstrapper
├── setup-tools.sh           # Bash bootstrapper
├── .devcontainer/
│   └── devcontainer.json    # Dev Container config
├── AGENTS.md                # Repo map
├── README.md                # This file
└── .gitignore
```

## License

MIT — use however you want.

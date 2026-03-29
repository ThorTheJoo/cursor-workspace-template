# AGENTS.md — Cursor Workspace Starter

This is a **cursor-workspace-starter** template repository. It provides a portable,
zero-global-pollution foundation for every new Cursor workspace.

## Repo Map

```
.
├── .cursor/rules/                 # Foundational AI rules (always active)
│   ├── 00-starter-rules.mdc      # Meta-rules: enforces MDD + Full-Stack baselines
│   ├── 01-mdd.mdc                # MDD Protocol V1.2 (P-R-I-L, brutal honesty, SSOT)
│   └── 02-frontend-fullstack.mdc  # Full-Stack: Next.js, tRPC, Shadcn, Tailwind, Zod
├── .cursor/bin/                   # Tool binaries (populated by bootstrapper)
├── .cursor/skills/                # Agent skills (populated by bootstrapper)
├── .cursor/mcp/                   # MCP server configs (future use)
├── tools/manifest.json            # SSOT: all GitHub tools available for install
├── .tools-cache/                  # Cloned tool repos (gitignored)
├── setup-tools.ps1                # Windows/PowerShell bootstrapper
├── setup-tools.sh                 # Bash/WSL/DevContainer bootstrapper
├── .devcontainer/devcontainer.json
└── README.md
```

## Rule Hierarchy

1. `00-starter-rules.mdc` — Always loaded. Enforces that rules 01 and 02 are active.
2. `01-mdd.mdc` — MDD V1.2. Always loaded. Governs all planning, analysis, and documentation.
3. `02-frontend-fullstack.mdc` — Activates on code files (`.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.html`).

Rules 01 and 02 take precedence over tool-specific rules unless explicitly overridden.

## Tool Management

- `tools/manifest.json` is the single source of truth for installable tools.
- Run `setup-tools.ps1` (Windows) or `./setup-tools.sh` (Bash) to interactively select and install.
- Cloned repos go into `.tools-cache/` (gitignored, never committed).
- Skills are copied into `.cursor/skills/`; CLIs go into `.cursor/bin/`.

## Conventions

- Every response starts with **Flaws & Risks** (MDD directive).
- Code generation follows Full-Stack conventions: RSC-first, Shadcn/Tailwind, Zod validation, kebab-case files.
- P-R-I-L workflow: Plan → Review → Implement → Log.
- Markdown files in `docs/_ai_context/` are SSOT for all project state and decisions.

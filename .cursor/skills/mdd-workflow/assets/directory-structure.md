# Standard MDD Directory Layout

```
project-root/
├── .cursor/
│   ├── rules/                    # IDE-level behavioral rules (.mdc files)
│   └── skills/                   # Agent skills (SKILL.md + references/ + assets/)
│       ├── SKILLS_INDEX.md       # Machine-readable skill registry
│       └── [skill-name]/
│           ├── SKILL.md          # Skill entry point (< 500 lines)
│           ├── references/       # Detailed reference docs (loaded on demand)
│           └── assets/           # Templates, examples, static content
│
├── docs/_ai_context/
│   ├── state/                    # Current execution state
│   │   ├── MASTER_STATE.md       # Global project state and capability map
│   │   ├── WORK_LOG.md           # Change log with lessons learned
│   │   ├── BACKLOG.md            # Prioritized pending work items
│   │   └── repo-manifest.json    # Machine-readable file/function index
│   │
│   ├── analysis/                 # Plans, debug logs, investigations
│   │   ├── YYYY-MM-DD_NAME.md   # Dated analysis/plan files
│   │   └── archive/             # Superseded files (never delete, always move)
│   │
│   ├── prompts/                  # Reusable prompts and workflow templates
│   │   ├── PROMPT_INDEX.md       # Entry point for prompt discovery
│   │   └── phases/              # Phase execution plans
│   │       ├── PHASES_INDEX.md   # Phase status tracker
│   │       ├── CONTEXT_MANIFEST.md  # Navigation, metrics, agent contract
│   │       └── PHASE_XX_NAME.md # Individual phase specs
│   │
│   ├── knowledge/                # Canonical domain knowledge (constitutional authority)
│   │   ├── reference/           # YAML/JSON reference files
│   │   ├── governance/          # Update policies and pending changes
│   │   └── staging/             # Proposed changes awaiting approval
│   │
│   └── templates/                # Standardized output templates
│
├── scripts/                      # Project scripts organized by domain
└── docs/
    ├── inputs/                   # Static source documents
    └── outputs/                  # Generated reports and artifacts
```

## What Goes Where

| Content Type | Location | Example |
|-------------|----------|---------|
| Project state and metrics | `state/` | MASTER_STATE.md |
| Work history | `state/WORK_LOG.md` | Phase completion entries |
| Pending tasks | `state/BACKLOG.md` | Prioritized items with source attribution |
| Investigation results | `analysis/` | `2026-03-15_AUTH_MIGRATION_PLAN.md` |
| Phase plans | `prompts/phases/` | `PHASE_12_API_REFACTOR.md` |
| Domain truth (YAML/JSON) | `knowledge/reference/` | API catalogs, taxonomies |
| Output format specs | `templates/` | Document templates, report formats |
| Reusable workflows | `prompts/` | Generation prompts, batch processing workflows |

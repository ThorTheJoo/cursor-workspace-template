# Manifest Schema Reference

## repo-manifest.json

Machine-readable index of your project's files, functions, and capabilities. Agents use this to navigate the codebase without guessing paths.

### Schema

```json
{
  "generated_at": "ISO8601 timestamp",
  "repo_root": "absolute path to repository root",
  "version": "semver string",

  "files": [
    {
      "path": "relative/path/to/file.py",
      "type": "script | model | config | test | template | state | analysis",
      "purpose": "One-line description of what this file does",
      "functions": ["function_name_1", "function_name_2"]
    }
  ],

  "knowledge_repo": {
    "root": "docs/_ai_context/knowledge",
    "file_count": 12,
    "files": ["reference/TAXONOMY.yaml", "reference/GLOSSARY.yaml"]
  },

  "phases": {
    "current": "Phase 5 - Integration",
    "completed": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
    "planned": ["Phase 6", "Phase 7"]
  },

  "capabilities": {
    "tests": {
      "script": "tests/",
      "command": "python -m pytest tests/ -v",
      "description": "Run full test suite"
    },
    "lint": {
      "command": "ruff check src/",
      "description": "Lint source code"
    }
  },

  "state_files": [
    {"path": "docs/_ai_context/state/MASTER_STATE.md", "name": "MASTER_STATE"},
    {"path": "docs/_ai_context/state/BACKLOG.md", "name": "BACKLOG"},
    {"path": "docs/_ai_context/state/WORK_LOG.md", "name": "WORK_LOG"}
  ],

  "prompts": {
    "root": "docs/_ai_context/prompts",
    "phases_directory": "docs/_ai_context/prompts/phases",
    "phases_index": "docs/_ai_context/prompts/phases/PHASES_INDEX.md",
    "context_manifest": "docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md"
  },

  "analysis": {
    "root": "docs/_ai_context/analysis",
    "plan_pattern": "*_PLAN.md",
    "debug_pattern": "*_DEBUG.md"
  },

  "templates": {
    "root": "docs/_ai_context/templates",
    "auto_discover": true
  },

  "extension_points": {
    "hooks": [],
    "plugins": []
  }
}
```

### Required Fields

- `generated_at` — when this manifest was last updated
- `repo_root` — absolute path for unambiguous file resolution
- `version` — manifest schema version (for forward compatibility)
- `files` — at minimum, all scripts and config files
- `state_files` — at minimum, MASTER_STATE and BACKLOG

### Optional Fields

Everything else is optional and should be added as the project grows.

### When to Regenerate

- After creating or deleting scripts/modules
- After a major phase completion
- After directory restructuring
- Monthly, even if no major changes (to catch drift)

## CONTEXT_MANIFEST.md

Human-readable navigation document for AI agents. Provides project identity, authority hierarchy, current metrics, and file index.

### Sections

1. **PROJECT IDENTITY** — repo path, purpose, current phase, core objective
2. **CONSTITUTION** — authority hierarchy (knowledge repo > state files > manifests > rules)
3. **AGENT PROMPT CONTRACT** — before/during/after checklists for agent sessions
4. **CURRENT STATE** — metrics table (baseline, target, achieved, status)
5. **CAPABILITY INDEX** — commands agents can run (tests, lint, build)
6. **PHASE COMPLETION STATUS** — table of phases with status and key deliverables
7. **FILE INDEX** — quick reference tables for core scripts, knowledge files, state files
8. **QUICK COMMANDS REFERENCE** — copy-paste bash/shell commands
9. **TROUBLESHOOTING POINTERS** — common issues and where to look
10. **META** — document version, generation date, link to machine-readable manifest

### Required Sections

Sections 1-4 are required for any MDD project. Sections 5-10 are recommended and should be added as the project grows.

### Style

- Use tables for structured data (metrics, file lists, phases)
- Keep prose to 1-2 sentences per section introduction
- Use `[placeholder]` syntax for values that vary per project
- Include exact file paths — never say "check the config" without specifying which

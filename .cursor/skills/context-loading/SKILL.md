---
name: context-loading
description: "Efficient AI context loading via manifests and targeted reads for any codebase. Use whenever starting a session in an unfamiliar codebase, loading project context, establishing file/capability inventory, or optimizing context window usage. Triggers on: session start, 'what does this project do', codebase exploration, manifest loading, repo-manifest.json, CONTEXT_MANIFEST.md, or context window optimization."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Context Loading

AI agent context windows are finite and expensive. Every line of a file you load displaces information you might need later. The difference between an effective agent session and a wasted one often comes down to loading the *right* 2,000 lines instead of the wrong 10,000.

This skill codifies the "sniper protocol" for context loading: use manifests to navigate, load targeted sections instead of full files, and never guess file paths.

## Core Principle

**Manifest-first, targeted reads, never full-file loads.**

A manifest is a machine-readable index of your project's files, capabilities, and current state. Instead of guessing where things are, you read the manifest, find the exact file and section you need, and load only that. This reduces context waste by 60-80% compared to exploratory full-file reads.

## Priority Loading Protocol

Load context in this order. Stop as soon as you have what you need.

| Priority | File | What You Get | When to Read |
|----------|------|-------------|--------------|
| 1 | `repo-manifest.json` | File paths, function locations, capability index | Every session start |
| 2 | `CONTEXT_MANIFEST.md` | Project identity, metrics, agent contract, phase status | Every session start |
| 3 | `MASTER_STATE.md` | Current phase, recent decisions, architecture overview | When implementing or investigating |
| 4 | Target-specific files | Only the relevant sections of files your task needs | On-demand during task execution |

### Priority 1: repo-manifest.json

A JSON file listing every significant file in the project with its purpose, key functions, and type. Use this as your file system index.

```json
{
  "files": [
    {"path": "src/auth/login.py", "type": "script", "purpose": "User authentication"},
    {"path": "src/models/user.py", "type": "model", "purpose": "User data model"}
  ],
  "capabilities": {
    "tests": {"command": "python -m pytest tests/ -v"},
    "lint": {"command": "ruff check src/"}
  }
}
```

### Priority 2: CONTEXT_MANIFEST.md

A human-readable manifest with project identity, authority hierarchy, agent contract (what to do before/during/after work), current metrics, and phase status. Read sections 1-4 for investigation, full file for implementation.

### Priority 3: MASTER_STATE.md

The global state document. Contains current phase, architecture overview, recent changes, and cross-cutting concerns. For large state files (1000+ lines), read only the section relevant to your task — do not load the full file.

### Priority 4: Target Files

Once you know which file you need (from the manifest), read only the relevant section. If a function is at line 450, read lines 440-480, not the entire 2000-line file.

## Rules

1. **Never read files over 500 lines without targeting a specific section.** If MASTER_STATE.md is 1,700 lines, read the section heading you need, not the whole file.

2. **Never guess file paths.** Use the manifest or search tools. Wrong file reads waste context and create confusion.

3. **Never reinvent functionality.** Before writing new code, check the manifest's `capabilities` section and search the codebase. If a function already exists, use it.

4. **Prefer section reads over full file loads.** Read line ranges: `lines 100-150` of a file is more efficient than the full file when you only need one function.

## Loading by Mode

### Investigation (Ask Mode)

You need just enough context to answer a question accurately.

1. Read `repo-manifest.json` — find relevant files
2. Read `CONTEXT_MANIFEST.md` sections 1-4 — get project identity and metrics
3. Read `MASTER_STATE.md` — check recent decisions (targeted section only)
4. Read the specific file/section that answers the question

### Planning (Plan Mode)

You need broader context to design an approach.

1. Full Priority 1-3 load
2. Read `BACKLOG.md` — check if the task relates to tracked items
3. Read `WORK_LOG.md` (last 3 entries) — understand recent changes
4. Read any predecessor plan files referenced in the task
5. If touching data structures: read the schema registry

### Execution (Agent Mode with Plan)

The plan file IS your context. Trust it.

1. Read the plan file — follow its "Before Starting Work" section
2. Read files listed in the plan's "Files to Read" table
3. Run pre-flight validators if the plan specifies them
4. Load additional context only when the plan directs you to

### Execution (Agent Mode without Plan)

1. Full Priority 1-3 load
2. Read `BACKLOG.md` — check for related items
3. Read `WORK_LOG.md` (last 3 entries)
4. If touching data files: read schema registry
5. If touching scoring/processing logic: read relevant config files

## Creating Manifests for a New Project

If your project does not have manifests yet, create them:

### repo-manifest.json

1. List all significant files (scripts, configs, models, tests)
2. For each file: path, type, purpose, key functions
3. Add `capabilities` section (test commands, lint commands, build commands)
4. Add `state_files` section (paths to key state documents)

Use the template at `assets/repo-manifest-template.json` as a starting point.

### CONTEXT_MANIFEST.md

1. Project identity (name, purpose, current phase)
2. Authority hierarchy (which files are authoritative for what)
3. Agent contract (what to do before/during/after work)
4. Current metrics
5. Capability index
6. Phase status table
7. File index (quick reference)
8. Common commands

Use the template at `assets/CONTEXT_MANIFEST_TEMPLATE.md` as a starting point.

### When to Refresh Manifests

- After creating new scripts or modules
- After completing a major phase
- After significant directory restructuring
- When a new contributor (human or AI) will start working on the project

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|-------------|-------------|---------|
| Reading entire large files (1000+ lines) | Fills context window with irrelevant content | Read targeted sections using line ranges |
| Guessing file paths from memory | Wrong paths waste reads and create confusion | Use manifest or search tools |
| Loading files "just in case" | Context waste — most won't be needed | Load on-demand when task requires it |
| "Continue from where we left off" | New sessions have no memory | Reference specific file paths and sections |
| "Same as before" | Ambiguous across sessions | Repeat the specification explicitly |
| Loading full test suites to understand a feature | Tests are verbose; feature code is more informative | Read the feature code, then specific test if needed |

## References

| File | Content |
|------|---------|
| `references/manifest-schema.md` | Full schema for repo-manifest.json and CONTEXT_MANIFEST.md |
| `assets/CONTEXT_MANIFEST_TEMPLATE.md` | Copy-paste template for a new project's context manifest |
| `assets/repo-manifest-template.json` | Copy-paste template for a new project's repo manifest |

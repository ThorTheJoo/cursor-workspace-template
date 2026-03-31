# Authority Hierarchy

## The Four Ranks

MDD defines a strict precedence for truth. When sources conflict, higher rank wins — no exceptions.

### Rank 1: Knowledge Repository

**Location:** `docs/_ai_context/knowledge/` (YAML/JSON reference files)

These files represent canonical domain truth: taxonomies, glossaries, API catalogs, relationship rules, and configuration schemas. They are the constitution of the project.

- Human approval is required for any modification
- AI agents may *propose* changes via staging files, but never modify directly
- If a skill instruction contradicts a knowledge file, the knowledge file wins

**Example conflict:** A skill says "API names use camelCase" but the API catalog YAML uses kebab-case. Follow the catalog.

### Rank 2: State Files

**Location:** `docs/_ai_context/state/` (MASTER_STATE.md, WORK_LOG.md, BACKLOG.md, indexes)

State files capture current execution state — what phase we're in, what was recently changed, what's pending. They are mutable but should be read before modifying to avoid clobbering concurrent changes.

- Read before modifying (especially BACKLOG.md and WORK_LOG.md)
- These files are ephemeral project state, not authoritative for domain content
- If a state file says a field exists but the knowledge file says it doesn't, trust the knowledge file

### Rank 3: Manifests & Indexes

**Location:** `repo-manifest.json`, `CONTEXT_MANIFEST.md`, `PHASES_INDEX.md`

Manifests are navigation tools. They point to where truth lives but don't define truth themselves.

- Use manifests to find file paths and capabilities
- Never treat manifest metadata (e.g., line counts, function lists) as authoritative — verify by reading the actual file
- If a manifest says a file exists at a path and it doesn't, the file system is truth

### Rank 4: Rules & Skills

**Location:** `.cursor/rules/`, `.cursor/skills/`

Rules and skills provide behavioral guidance — how to approach tasks, what patterns to follow, what to avoid. They are overridden by all higher ranks.

- If a rule says "always use encoding X" but a knowledge file documents that a specific file uses encoding Y, use Y
- Skills encode best practices, not absolute truth

## Conflict Resolution

When you encounter a conflict between sources:

1. Identify the rank of each source
2. Follow the higher-ranked source
3. Log the conflict in WORK_LOG.md so it can be resolved
4. If both sources are the same rank, flag for human review

**Example:** MASTER_STATE.md says the pipeline uses config v5.8.0, but the actual config file header says v5.10.0. The file system (rank 2 equivalent — actual state) wins. Update MASTER_STATE.md to match.

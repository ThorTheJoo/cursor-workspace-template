---
name: knowledge-repo
description: "Manage canonical domain knowledge with versioned YAML files, governance workflows, staging-to-production promotion, and rollback. Use when creating a knowledge repository, defining domain truth, versioning reference data, or managing glossaries/taxonomies. Triggers on: knowledge management, canonical data, taxonomy, ontology, glossary, single source of truth, domain reference files, or YAML knowledge governance."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Knowledge Repository Management

A knowledge repository is the single source of truth for domain-specific data that AI agents and code rely on: taxonomies, glossaries, canonical names, API catalogs, synonym mappings, and any reference data that multiple systems consume. Without governance, these files drift — agents hallucinate field names, invent synonyms, and corrupt reference data that downstream systems trust.

This skill establishes the framework for creating, governing, versioning, and maintaining knowledge repositories in any project.

## What Is a Knowledge Repository?

A knowledge repository is a set of version-controlled YAML/JSON files containing canonical domain truth. Unlike code (which implements logic) or state files (which track current progress), knowledge files define *what things are called* and *how they relate*.

**Key properties:**
- **AI can READ freely** but can only WRITE through a governed promotion workflow
- **Human approval required** for all changes to production knowledge files
- **Version-controlled** with explicit snapshots and rollback capability
- **Schema-validated** to prevent structural drift

**Examples of knowledge content:**
- Glossary of domain terms with canonical definitions
- Taxonomy of categories and subcategories
- API catalog mapping identifiers to official names
- Synonym mappings (which terms mean the same thing)
- Configuration canonicals (official system names and their aliases)

## Directory Structure

A well-organized knowledge repository follows this layout:

```
docs/_ai_context/knowledge/
├── domain/              # Domain frameworks and conceptual models
│   ├── TAXONOMY.yaml    # Category hierarchy
│   └── ONTOLOGY.yaml    # Entity relationships
├── reference/           # Operational reference data
│   ├── GLOSSARY.yaml    # Canonical term definitions
│   ├── API_CATALOG.yaml # API identifiers and names
│   └── SYNONYMS.yaml    # Term equivalence mappings
├── glossary/            # Extended terminology (optional)
├── registry/            # Evidence and citation tracking
│   └── EVIDENCE_SOURCES.yaml
├── governance/          # Policies, queues, and audit trails
│   ├── GOVERNANCE_POLICY.md
│   ├── PENDING_UPDATES.yaml
│   ├── UPDATE_HISTORY.yaml
│   └── ROLLBACK_LOG.yaml
├── staging/             # Pre-promotion holding area
├── schemas/             # JSON Schema files for validation
│   └── taxonomy_schema.json
├── versions/            # Frozen version snapshots
│   ├── v1.0.0/
│   └── v1.1.0/
├── CURRENT_VERSION      # Single file: current version string
├── CHANGELOG.md         # Keep a Changelog format
└── MASTER_KNOWLEDGE_REPOSITORY.yaml  # Root index (optional)
```

Not every project needs every directory. Start with `reference/`, `governance/`, and `schemas/`, then add others as complexity grows.

## Authority Hierarchy

Knowledge files sit at the top of the authority hierarchy. When sources conflict, higher rank wins.

| Rank | Source | Example | Rule |
|------|--------|---------|------|
| 1 | **Knowledge Repository** | YAML/JSON in `knowledge/` | Canonical domain truth — human approval to change |
| 2 | **State Files** | MASTER_STATE.md, WORK_LOG.md | Current execution state — read before modifying |
| 3 | **Manifests and Indexes** | repo-manifest.json | Navigation only — points to truth, doesn't define it |
| 4 | **Rules and Skills** | .cursor/rules/, .cursor/skills/ | Behavioral guidance — overridden by ranks 1-3 |

This means: if a skill instruction says "term X means Y" but the glossary says "term X means Z", the glossary wins.

## Governance Workflow

All changes to production knowledge files follow a staged workflow. This prevents accidental corruption of authoritative data.

### Stage 1: Detection

A learning candidate is identified — from pipeline output, manual discovery, or agent suggestion. The candidate is NOT yet trusted.

### Stage 2: Staging

The candidate enters `staging/` as a YAML file with metadata:
- Source (where was this discovered?)
- Frequency (how many times has it appeared?)
- Confidence level (how sure are we it's correct?)
- Proposed change (what would change in the knowledge repo?)

### Stage 3: Validation

Automated checks run against the staged candidate:
- Does it conform to the relevant JSON Schema?
- Does it conflict with existing entries?
- Is the proposed format correct?

### Stage 4: Approval

A human reviews the candidate and decides:
- **Approve** — promote to production
- **Reject** — document reason, remove from staging
- **Needs Info** — request additional evidence before deciding

### Stage 5: Promotion

Approved candidates are merged into the production knowledge files (in `reference/` or `domain/`). The staging file is removed.

### Stage 6: Versioning

After a batch of promotions, create a version snapshot and update CHANGELOG.md.

### Stage 7: Rollback (if needed)

If a promoted change causes issues downstream, rollback to the previous version snapshot.

For the full governance policy template, see `references/governance-policy.md`.

## Promotion Criteria

Content moves from staging to production when it meets these criteria:

| Criterion | What It Means |
|-----------|--------------|
| **Evidence** | Appeared in 3+ independent sources or 5+ occurrences |
| **Accuracy** | Verified against authoritative documentation |
| **Non-duplicate** | Does not overlap with existing entries |
| **Correct classification** | Domain, category, and type are accurate |
| **Schema compliance** | Conforms to the relevant JSON Schema |
| **Human sign-off** | A designated reviewer has approved |

Rejection criteria:
- Fewer than required evidence threshold
- Duplicate of existing entry
- Incorrect classification
- Unverifiable claim
- Generic terms that add noise

For details on the staging workflow, see `references/staging-workflow.md`.

## Versioning Protocol

Knowledge repositories use explicit versioning to enable rollback and audit.

### CURRENT_VERSION File

A single file at the repository root containing the current version string:

```
1.2.0
```

### versions/ Directory

Contains frozen snapshots of the knowledge repository at each version:

```
versions/
├── v1.0.0/    # Initial release
│   ├── GLOSSARY.yaml
│   └── TAXONOMY.yaml
├── v1.1.0/    # Added API catalog
│   ├── GLOSSARY.yaml
│   ├── TAXONOMY.yaml
│   └── API_CATALOG.yaml
└── v1.2.0/    # Current
```

### CHANGELOG.md

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.2.0] - 2026-03-30
### Added
- 15 new glossary terms from Q1 review
### Changed
- Updated API catalog with v2 endpoint names
### Fixed
- Corrected synonym mapping for "account" terms
```

### When to Bump Versions

- **Patch** (1.2.x): Typo fixes, minor corrections
- **Minor** (1.x.0): New entries, expanded coverage
- **Major** (x.0.0): Schema changes, structural reorganization

For the full versioning protocol, see `references/versioning-protocol.md`.

## Rollback Protocol

When a knowledge update causes downstream issues:

1. **Identify** the bad update in UPDATE_HISTORY.yaml
2. **Copy** the previous version snapshot from `versions/` back to `reference/` (or `domain/`)
3. **Update** CURRENT_VERSION to the rolled-back version
4. **Log** the rollback in ROLLBACK_LOG.yaml with reason and affected files
5. **Re-run** validation to confirm the rollback restored correct state
6. **Mark** the original candidate as rejected with the rollback reason

Rollback should be fast (under 5 minutes) because version snapshots are pre-frozen copies.

## Schema Validation

Use JSON Schema (draft-07 or later) to validate knowledge files before promotion.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["terms"],
  "properties": {
    "terms": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "definition", "domain"],
        "properties": {
          "name": {"type": "string", "minLength": 1},
          "definition": {"type": "string", "minLength": 10},
          "domain": {"type": "string", "enum": ["finance", "engineering", "operations"]}
        }
      }
    }
  }
}
```

For patterns and examples, see `references/schema-validation.md`.

## Creating a Knowledge Repository

For a new project:

1. Create the directory structure (start minimal: `reference/`, `governance/`, `schemas/`)
2. Create `CURRENT_VERSION` with `1.0.0`
3. Create `CHANGELOG.md` with initial entry
4. Create `governance/GOVERNANCE_POLICY.md` from the template
5. Add your first knowledge file (e.g., a glossary) to `reference/`
6. Create a JSON Schema for it in `schemas/`
7. Run the validation script to confirm everything parses correctly

Use the templates in `assets/` as starting points:
- `assets/MASTER_KNOWLEDGE_REPO_TEMPLATE.yaml`
- `assets/TERMINOLOGY_INDEX_TEMPLATE.yaml`
- `assets/EVIDENCE_REGISTRY_TEMPLATE.yaml`

## References

| File | Content |
|------|---------|
| `references/governance-policy.md` | Full governance policy template |
| `references/versioning-protocol.md` | Versioning rules, snapshot procedures, CHANGELOG format |
| `references/staging-workflow.md` | Staging → validation → promotion → cleanup workflow |
| `references/schema-validation.md` | JSON Schema patterns for knowledge files |
| `assets/MASTER_KNOWLEDGE_REPO_TEMPLATE.yaml` | Root index template |
| `assets/TERMINOLOGY_INDEX_TEMPLATE.yaml` | Glossary template |
| `assets/EVIDENCE_REGISTRY_TEMPLATE.yaml` | Evidence source registry template |
| `scripts/validate_knowledge_repo.py` | Validation script for knowledge repository health |

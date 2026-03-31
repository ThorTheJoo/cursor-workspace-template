# Knowledge Repository Versioning Protocol

## Overview

Knowledge repositories use explicit semantic versioning to enable rollback, audit trails, and reproducibility. Every set of promoted changes results in a new version snapshot.

## CURRENT_VERSION File

A single plain-text file at the knowledge repository root containing only the current version string:

```
1.2.0
```

No YAML, no JSON — just the version string. This makes it trivially parseable by any tool.

## versions/ Directory

Contains frozen copies of all production knowledge files at each version:

```
versions/
├── v1.0.0/
│   ├── GLOSSARY.yaml
│   └── TAXONOMY.yaml
├── v1.1.0/
│   ├── GLOSSARY.yaml
│   ├── TAXONOMY.yaml
│   └── API_CATALOG.yaml      # New file added in v1.1.0
└── v1.2.0/
    ├── GLOSSARY.yaml          # Updated with 15 new terms
    ├── TAXONOMY.yaml
    └── API_CATALOG.yaml
```

Each version directory is a complete snapshot — not a diff. This enables instant rollback by copying the directory contents back to production.

## Creating a Version Snapshot

After promoting a batch of changes:

1. Update `CURRENT_VERSION` with the new version string
2. Create `versions/vX.Y.Z/` directory
3. Copy all production knowledge files into the new version directory
4. Update `CHANGELOG.md` with the new version entry
5. Commit with message: `docs(knowledge): bump to vX.Y.Z — [summary]`

## CHANGELOG.md Format

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to the knowledge repository.

## [1.2.0] - 2026-03-30

### Added
- 15 new glossary terms from Q1 review
- API catalog entries for v2 endpoints

### Changed
- Updated taxonomy: moved "billing" under "revenue management"

### Fixed
- Corrected synonym: "acct" now maps to "account" (was "action")

### Removed
- Deprecated legacy category "misc" from taxonomy

## [1.1.0] - 2026-02-15

### Added
- API_CATALOG.yaml with 45 endpoint definitions
- 8 new synonym mappings

## [1.0.0] - 2026-01-01

### Added
- Initial GLOSSARY.yaml with 120 terms
- Initial TAXONOMY.yaml with 3-level hierarchy
```

## Versioning Rules

| Change Type | Version Bump | Examples |
|-------------|-------------|---------|
| **Patch** (x.x.Z) | Typo fixes, minor corrections, no new entries | Fix definition wording, correct a misspelling |
| **Minor** (x.Y.0) | New entries, expanded coverage, non-breaking changes | Add glossary terms, new taxonomy categories, new synonym groups |
| **Major** (X.0.0) | Schema changes, structural reorganization, breaking changes | Change YAML structure, rename required fields, merge/split files |

## When to Create a Version

- After promoting a batch of approved candidates (batch all promotions from one review session)
- Before making structural changes to knowledge file schemas
- Before starting a new project phase that depends on knowledge data
- Monthly, even if changes are minor (for audit trail consistency)

## Rollback Procedure

1. Identify the last-known-good version in `versions/`
2. Copy all files from `versions/vX.Y.Z/` to the production location (`reference/`, `domain/`, etc.)
3. Update `CURRENT_VERSION` to the rolled-back version
4. Add a rollback entry to `governance/ROLLBACK_LOG.yaml`
5. Update CHANGELOG.md with a rollback note
6. Re-run validation to confirm correct state

### ROLLBACK_LOG.yaml Format

```yaml
rollbacks:
  - version_from: "1.2.0"
    version_to: "1.1.0"
    date: "2026-03-30T14:00:00Z"
    reason: "Synonym mapping for 'acct' caused false matches in pipeline"
    affected_files: ["reference/SYNONYMS.yaml"]
    rolled_back_by: "architect-name"
```

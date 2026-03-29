# Changelog

All notable changes to the Cursor Workspace Starter template.

## [2.0.0] - 2026-03-29

### Added
* MDD V1.3 Agentic Critical Edition as `.cursor/rules/01-mdd.mdc` (Sniper Mode, 3 operational modes, complexity triage, 14 governance rules, phase execution, authority hierarchy, anti-pattern catalog, backlog management).
* Full `docs/_ai_context/` V1.3 structure: 11 subdirectories including `knowledge/governance/`, `knowledge/schemas/`, `knowledge/versions/`, `knowledge/staging/`, `prompts/phases/`, `analysis/archive/`.
* `MASTER_STATE.md`, `WORK_LOG.md`, `BACKLOG.md`, seed `repo-manifest.json` in state/.
* `ADR_TEMPLATE.md` (MADR format) in templates/.
* V1.3 feature specification and rule source archived in `knowledge/`.
* Manifest JSON validation in both bootstrapper scripts.
* MDD directory creation in bootstrapper scripts.
* Detailed install reporting (installed/failed counts) in final summary.
* `CHANGELOG.md` (this file).
* `version` field in all `.mdc` rule frontmatter.

### Changed
* **00-starter-rules.mdc**: Thinned to pure orchestrator. References V1.3. Zero duplicated content.
* **02-kingmode.mdc**: Added version field. No content changes (authoritative for design).
* **03-frontend-fullstack.mdc**: Removed duplicated Design Philosophy, Frontend Coding Standards, and duplicate System Role sections (governed by 02-kingmode.mdc). Added version field.
* Both bootstrapper scripts now create V1.3 MDD directories alongside `.cursor/` dirs.
* `README.md` and `AGENTS.md` updated for V1.3 structure and hierarchy.

### Removed
* MDD V1.2 rule (replaced by V1.3).
* All rule duplication across 00/02/03 files.

### Fixed
* Missing comma in `tools/manifest.json` between `autoresearch` and `kingmode` entries.

## [1.0.0] - 2026-03-29

### Added
* Initial template: 4 foundational `.mdc` rules (MDD V1.2), cross-platform bootstrappers, `tools/manifest.json`, `.devcontainer`, `AGENTS.md`, `README.md`, `.gitignore`.

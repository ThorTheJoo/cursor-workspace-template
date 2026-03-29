# Changelog

All notable changes to the Cursor Workspace Starter template.

## [2.1.0] - 2026-03-29

### Added
* **Continuous Improvement Protocol** (`knowledge/governance/CONTINUOUS_IMPROVEMENT_PROTOCOL.md`): 6-item learning checklist with routing decision tree. Turns P-R-I-L into P-R-I-L-L.
* **Context Manifest** (`prompts/phases/CONTEXT_MANIFEST.md`): Navigation map and agent contract for Sniper Mode.
* 9 templates: Medium Plan, Complex Pre-Plan, Phase Completion, Debug Log, Runbook, 3 Response Formats (Ask/Plan/Agent).
* 5 knowledge docs: Complexity Triage Matrix, Mode Transition Rules, Anti-Patterns Catalog (24 patterns), Governance Policy, Session Start prompts.
* 3 governance pipeline seeds: `PENDING_UPDATES.yaml`, `UPDATE_HISTORY.yaml`, `ROLLBACK_LOG.yaml`.
* `repo-manifest.schema.json` for Sniper Mode manifest validation.
* `.gitkeep` files for empty directories that need to survive `git clone`.

### Changed
* **01-mdd.mdc**: Sections 3, 4, 5, 9, 11, 15 now cross-reference their full knowledge/template docs. Section 11 expanded from "Skills Extraction" to "Continuous Improvement" with 6-item checklist. P-R-I-L Log step now includes Learn sub-step.
* **setup-tools.sh / setup-tools.ps1**: Now create all 11 MDD subdirs (was 5). Removed orphan `.cursor/automations`.
* **AGENTS.md**: Complete artifact inventory (30+ entries across 5 categories).
* **BACKLOG.md**: Groomed — 6 items resolved, moved to Resolved section.
* **MASTER_STATE.md**: Updated to v2.1.0 with wiring summary table.
* **PROMPT_INDEX.md**: Updated as full discovery hub for all artifacts.
* **DEBUG_LOG_TEMPLATE.md**: Wired to Anti-Patterns Catalog (pre-investigation check) and improvement loop.
* **PHASE_COMPLETION_TEMPLATE.md**: Added continuous improvement checklist.

### Fixed
* Ghost reference: Rule Section 1 referenced `CONTEXT_MANIFEST.md` but file didn't exist.
* Bootstrappers created only 5/11 MDD directories — fresh clones would miss nested structure.
* Orphan `.cursor/automations` created by bootstrappers but undocumented.
* Stale backlog items listed as open but already completed.

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

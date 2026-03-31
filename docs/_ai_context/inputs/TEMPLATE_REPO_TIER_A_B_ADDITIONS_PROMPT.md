---
document_type: PROMPT
status: ACTIVE
purpose: "Add Tier A generic files and Tier B genericized scripts to the cursor-workspace-template"
target_repo: "cursor-workspace-template"
estimated_duration: "1.5-2 hours"
depends_on:
  - "TEMPLATE_REPO_SKILLS_INTEGRATION_PROMPT.md (9 skills already installed)"
  - "TEMPLATE_REPO_FAT_ROUTER_PROMPT.md (fat router already installed)"
---

# Tier A + Tier B Additions to Template Repository

## Background

The template repository already has:
- 9 portable MDD skills in `.cursor/skills/` (from TEMPLATE_REPO_SKILLS_INTEGRATION_PROMPT)
- A fat `01-mdd.mdc` router (~180 lines) with behavioral guardrails (from TEMPLATE_REPO_FAT_ROUTER_PROMPT)
- A bootstrapper (`setup-tools.sh`) with `seed_mdd_from_skills()` that seeds basic state files

**What's missing:** The skills provide templates for the most basic state files (BACKLOG, WORK_LOG,
repo-manifest, CONTEXT_MANIFEST, PHASES_INDEX). But a real MDD workspace also needs:
- Governance rules document
- System-level markdown rules
- Multi-phase execution guidelines
- Knowledge repo governance policy and audit trail files
- Decision log for architectural decisions
- Templates README with AI instructions
- Validation scripts that automate what the skills describe in prose

This prompt adds those files in two tiers:
- **Tier A:** 8 generic files that are ready to use with minimal changes
- **Tier B:** 2 genericized Python validation scripts + 3 supporting files

---

## Task List

1. Create Tier A files (8 files, all generic MDD infrastructure)
2. Create Tier B scripts (2 genericized Python scripts)
3. Create Tier B supporting files (3 files)
4. Extend the bootstrapper to seed Tier A files
5. Update AGENTS.md with validation script references
6. Verify everything works

---

## Step 1: Create Tier A Files

### 1.1 `docs/_ai_context/prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md`

This is the detailed manual for running multi-phase work. The `phase-execution` skill
summarizes it; this document is the comprehensive reference.

Create this file with the following content (337 lines). This is **already generic** — no
domain-specific content to strip.

```markdown
# Multi-Phase Plan Execution Guidelines

## Core Principles

1. **Context Independence**: Each phase executes in a fresh agent session with no memory of prior sessions. The plan file IS the context.

2. **Explicit Handoffs**: Output from Phase N becomes input for Phase N+1. Never assume — always specify paths.

3. **Validation Gates**: Each phase completes with validation. Do not proceed to next phase until gate passes.

4. **Atomic Commits**: Each phase = one logical commit. Enables rollback to last known-good state.

---

## Phase Numbering and Pre-Plan Workflow

### Phase Numbering Rule

Any new plan initiative gets the **next free phase number** (e.g. 29, 30, …), whether it is a pre-plan or a full execution-style plan:

- Check existing `docs/_ai_context/prompts/phases/PHASE_XX_*.md` files to find the highest phase number.
- Assign the next sequential number to the new plan.
- Each todo from a pre-plan gets its own phase number: Todo 1 → PHASE_29, Todo 2 → PHASE_30, etc.

### Pre-Plan as Decomposition

When a task is complex (6+ steps, 2+ hrs, validation gates), produce a **pre-plan** that:

1. Lives in `docs/_ai_context/analysis/YYYY-MM-DD_NAME_PRE_PLAN.md` or `docs/_ai_context/prompts/phases/PHASE_XX_NAME_PRE_PLAN.md`.
2. Lists **numbered todos** with their target phase numbers.
3. Includes dependencies between todos (e.g. "Todo 2 depends on Todo 1 outputs").

### Expanding Todos into Phase Files

After the pre-plan is generated, prompt the agent to generate the full phase file for each todo:

    Generate a full execution-style phase spec for Todo [X] as PHASE_XX_NAME.md
    with code snippets, validation commands, and file paths.
    Reference the pre-plan: [path to pre-plan].

### Referencing the Pre-Plan

Each phase file generated from a pre-plan should:
- Include the pre-plan in `depends_on`.
- Or add a `source_pre_plan` field in the YAML front matter.

---

## Phase File Structure

Every phase plan file MUST include:

    ---
    name: Phase X - [Descriptive Name]
    phase: X of Y
    depends_on:
      - List of files/outputs from previous phases
      - "none" if first phase
    outputs_for_next_phase:
      - Explicit paths to files this phase creates
    validation_gate:
      - Criteria that MUST pass before marking complete
    ---

---

## Context Manifest Template

Include this at the start of each phase to orient the agent:

    ## Context Manifest

    ### This Phase Creates
    | Output | Path | Purpose |
    |--------|------|---------|
    | [artifact] | `path/to/file` | [why next phase needs it] |

    ### This Phase Requires (From Prior Phases)
    | Input | Path | Created By |
    |-------|------|------------|
    | [artifact] | `path/to/file` | Phase N |

    ### Files to Read (On-Demand)
    - `path/to/large/file.yaml` — Read only sections X-Y when needed

    ### Files to Modify
    | File | Change Type | Sections |
    |------|-------------|----------|
    | `path/file.yaml` | ADDITIVE | `section.key` |

---

## Before Starting Work (Agent Contract)

Before executing any phase, agents MUST:

- [ ] Read the complete plan file
- [ ] Read `docs/_ai_context/state/BACKLOG.md` for items tagged `assigned: {this_phase}`
- [ ] Address P1 items FIRST
- [ ] Read `docs/_ai_context/state/MASTER_STATE.md` for current state
- [ ] Check `docs/_ai_context/state/WORK_LOG.md` for recent changes
- [ ] Verify prerequisites from `depends_on` exist
- [ ] Run pre-flight validator if available:
      python3 scripts/mdd/phase_preflight_validator.py --phase {PHASE_ID}

---

## Execution Rules

### For the Executing Agent

1. Read the plan file completely before starting any work
2. Verify prerequisites exist before executing steps
3. Execute steps sequentially unless explicitly marked parallel
4. Validate after each step — stop and report if validation fails
5. Log progress to WORK_LOG.md
6. Do NOT read files summarized in plan unless you need content not provided

### For Phase Boundaries

- Phase N completes → Validation passes → Git commit → Phase N+1 starts fresh
- Between phases: Always verify prior phase outputs exist
- On failure: Fix in current phase OR rollback and re-plan
- Never: Carry implicit context between sessions

---

## Handoff Protocol

At phase completion, include:

    ## Phase X Complete

    ### Created Outputs (Verify Exist)
    - [ ] `path/to/output1.yaml` — [brief description]

    ### Validation Results
    - [ ] [Check 1] — PASS/FAIL

    ### Handoff Notes for Phase X+1
    - [Context the next phase needs]
    - [Warnings about edge cases]
    - [Deviations from original plan]

    ### Git Commit
    `feat(scope): Phase X - [summary]`

---

## After Completion (Agent Contract)

Every phase MUST perform these steps before marking complete:

- [ ] Update `docs/_ai_context/prompts/phases/PHASES_INDEX.md` (status → COMPLETE)
- [ ] Update `docs/_ai_context/state/WORK_LOG.md` with changes
- [ ] Create `docs/_ai_context/analysis/PHASE_XX_COMPLETION.md` with execution summary
- [ ] Run project tests if they exist
- [ ] Commit with: `feat(scope): Phase XX - [summary]`
- [ ] If deferring work, append to `docs/_ai_context/state/BACKLOG.md`

---

## Phase Completion Documentation Policy

Every multi-phase execution MUST produce a completion document.

### MANDATORY Content

Create `docs/_ai_context/analysis/PHASE_XX_COMPLETION.md` containing:

| Section | Required | Description |
|---------|----------|-------------|
| Files Created/Modified | Yes | Table of paths and change descriptions |
| Validation Results | Yes | Pass/fail for each validation gate |
| Metrics (if applicable) | Yes | Before/after comparison table |
| Lessons Learned | Yes | Key takeaways |

### Template

    ---
    document_type: COMPLETION
    phase: XX
    status: COMPLETE
    date: YYYY-MM-DD
    ---

    ## Phase XX Completion Summary

    ### Files Created/Modified
    | File | Change |
    |------|--------|
    | `path/to/file` | Description |

    ### Validation Results
    - [ ] Gate 1 — PASS/FAIL

    ### Metrics (if applicable)
    | Metric | Before | After |
    |--------|--------|-------|

    ### Lessons Learned
    - [Key takeaway]

### Enforcement

- Phases without a completion doc are considered **incomplete**
- PHASES_INDEX status should not be set to COMPLETE until the completion doc exists

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| "Continue from where we left off" | New session has no memory | Reference specific file paths |
| "Use the data we extracted earlier" | Agent doesn't know what/where | Provide exact path + line numbers |
| "Same as before" | Ambiguous | Repeat the specification |
| Loading entire large files | Blows context window | Read specific sections on-demand |
| Implicit validation | Silent failures | Explicit validation steps |

---

## Quick Reference: Phase Prompt Template

When starting a new agent session for Phase N:

    Execute Phase N from the plan at `docs/_ai_context/prompts/phases/PHASE_0X_NAME.md`

    Instructions:
    1. Read the complete plan file before starting
    2. Verify all prerequisites from prior phases exist
    3. Execute each step sequentially, validating after each
    4. On validation failure, STOP and report — do not proceed
    5. On completion, run the full validation gate
    6. Prepare handoff notes for Phase N+1

---

## Error Recovery Protocol

### If a Step Fails

1. Document the error in the current phase
2. Attempt to fix within current context
3. If unfixable, create analysis file documenting the issue
4. Roll back any partial changes
5. Report blocked status with specifics

### If Validation Gate Fails

1. Identify which specific check failed
2. Fix the failing component
3. Re-run the full validation gate
4. Do NOT proceed to next phase until gate passes

### If Phase Must Be Abandoned

1. Document what was completed and what failed
2. Commit partial work with `WIP:` prefix
3. Create analysis file for next attempt
4. Tag rollback point in git

---

## Git Commit Convention

    feat(scope): Phase X - [Summary]
    - [Key deliverable 1]
    - [Validation results]

For partial work:

    WIP: Phase X partial - [What's done]
    - [Completed items]
    - [Blocked on: specific issue]
```

---

### 1.2 `docs/_ai_context/state/MDD_GOVERNANCE_RULES.md`

This is the comprehensive governance rules document. Create it as a **genericized** version
with domain-specific rules removed. Write approximately 350-400 lines covering these 14 rules:

1. **Code Reuse Mandate** — Search before writing. Duplication is a critical error. Include a checklist: search codebase, check script registry, check state files, check repo-manifest.json.
2. **Automatic MDD Updates** — Update MDD docs when: new script created, error resolved, phase completed, pattern discovered, workflow established. Include cascade update rule.
3. **Pre-Planning Decomposition** — Complex tasks (6+ steps) must have a plan file before implementation. Reference the complexity triage matrix.
4. **Contract-First Validation** — Verify field contracts between producer and consumer before/after code changes. Include common failure patterns: field name drift, version confusion, baseline mismatch, silent fallback.
5. **Script Documentation** — Every new script needs a docstring with name, purpose, features, author, date. Registration in MDD docs after creation.
6. **Prohibited Actions** — 10 items: don't create without searching, don't skip validation, don't bypass templates, don't modify knowledge files without approval, etc.
7. **Required Actions** — 10 items: always search, always validate, always update MDD docs, always follow P-R-I-L, always log lessons learned.
8. **Continuous Improvement** — After each task: update docs, log lessons, create error analysis if needed, update metrics.
9. **Structured Lessons-Learned** — 4 questions: what went well, what went wrong, what to do differently, regression risk (HIGH/MEDIUM/LOW). Regression categories table.
10. **Enhanced WORK_LOG Template** — Required fields table: scope, status, duration, changes, validation, regression risk, lessons, next steps.
11. **Backlog Grooming** — Priority labels, age-out rules, resolved separation, source attribution, periodic review.
12. **Analysis Archival** — Move superseded files to archive/. Never delete. When to archive and when NOT to.
13. **Phase Completion Documentation** — Every phase needs a completion doc. Mandatory and optional sections.
14. **Manifest Drift Enforcement** — Run the manifest generator after changes. Report actual results in WORK_LOG.

**IMPORTANT:** The Domain-Specific Rules section from the source should be REMOVED entirely.
Replace it with a placeholder section:

```markdown
## Domain-Specific Rules

Add project-specific rules below. Examples:
- Quality thresholds for generated outputs
- API integration policies
- Template compliance requirements
- Naming conventions for generated files
```

The YAML frontmatter should be:
```yaml
---
document_type: GOVERNANCE
status: APPROVED
version: 2.0
compliance_tags: ["Markdown-Driven Development", "P-R-I-L"]
---
```

Remove all references to: BSS, TMF, Mobily, Confluence, ArchiMate, AMEFF, E2E use cases,
Encompass, GB1033, MOBNS, CQL, correlation scoring, ground truth. Replace script paths
like `scripts/e2e/` with generic `scripts/` paths. Replace domain-specific examples with
generic ones (e.g., field name drift example: `content` vs `body` vs `text`).

---

### 1.3 `docs/_ai_context/state/MASTER_MARKDOWN_SYSTEM_RULES.md`

Create a **genericized** version (~150 lines). This defines how markdown is used as a
first-class artifact. Keep:
- Section 1: Core Principles (markdown as system of record, never delete history, minimal invasiveness)
- Section 2: Directory Layout (the `docs/_ai_context/` tree with descriptions)
- Section 3: Standard Workflow (locate state → create analysis → implement → capture outcome)
- Section 4: Debugging Conventions (error analysis file pattern)
- Section 5: Template Usage Rules (read templates before generating)
- Section 6: Prompt Extraction (extract stable workflows to `prompts/`)
- Section 7: Incremental Learnings (empty section with instructions to add dated bullets)
- Section 8: Onboarding (how to port this pattern to other projects)

**Strip all domain references.** Remove:
- `MASTER_CUMULATIVE_STATE.md`, `ARCHIMATE_*`, `E2E_*` references
- All dated bullets in Section 7 (they're BSS-specific). Keep the section header with
  instructions to add project-specific learnings.
- References to `docs/inputs/`, `docs/outputs/` (project-specific)
- Confluence, Encompass, TMF references

Replace domain examples with generic placeholders like `[YOUR_DOMAIN_MASTER_STATE.md]`.

---

### 1.4 `docs/_ai_context/knowledge/governance/GOVERNANCE_POLICY.md`

Create a **genericized** version (~100 lines). Keep the structure:
- Promotion Workflow (7 steps: detection → frequency gate → review → approval → promotion → validation → rollback)
- Approval Criteria sections — replace BSS-specific types (NEW_SYNONYM, NEW_API, NEW_TMF_MAPPING)
  with generic types: NEW_TERM, NEW_COMPONENT, NEW_RELATIONSHIP, NEW_PATTERN, NEW_RULE
- Rejection Criteria — keep as-is (generic)
- Priority Scoring formula — keep as-is but replace domain weights with generic domains:
  `core_domain: 1.0, secondary_domain: 0.85, supporting_domain: 0.70`
- Rollback Procedure — keep as-is (generic)
- Review Cadence — keep as-is
- Audit Trail — keep as-is
- Escalation — keep, replace "ADO work item" with "issue tracker work item"

---

### 1.5 `docs/_ai_context/knowledge/governance/UPDATE_HISTORY.yaml`

Create as an **empty template** (no actual entries):

```yaml
# Knowledge Repository Update History
# Records all approved/rejected/rollback changes

metadata:
  created_at: "YYYY-MM-DDTHH:MM:SSZ"
  last_updated: null
  total_approved: 0
  total_rejected: 0
  total_rollbacks: 0

approved: []
  # Example:
  # - id: new_term_20260130_0
  #   learning_type: new_term
  #   data:
  #     term: "example term"
  #     canonical: "ExampleCanonical"
  #   approved_by: reviewer
  #   approved_at: "YYYY-MM-DDTHH:MM:SSZ"
  #   promoted_to:
  #     file: "reference/GLOSSARY.yaml"
  #     section: "terms.example"

rejected: []
  # Example:
  # - id: new_component_20260130_1
  #   learning_type: new_component
  #   rejected_by: "reviewer"
  #   rejected_at: "YYYY-MM-DDTHH:MM:SSZ"
  #   reason: "Generic term, not a real component"

rollbacks: []
  # Example:
  # - original_id: new_component_20260130_2
  #   rolled_back_at: "YYYY-MM-DDTHH:MM:SSZ"
  #   reason: "Caused downstream issues"
  #   restored_version: "v1.0.0"
```

---

### 1.6 `docs/_ai_context/knowledge/governance/ROLLBACK_LOG.yaml`

Create as an **empty template**:

```yaml
# Knowledge Repository Rollback Log
# Records rollback events for audit and recovery

metadata:
  created_at: "YYYY-MM-DDTHH:MM:SSZ"
  last_rollback: null
  total_rollbacks: 0

# Rollback procedure:
# 1. Document the bad update in this file
# 2. Restore previous version snapshot from versions/
# 3. Verify restoration success
# 4. Update UPDATE_HISTORY.yaml with rollback record

rollbacks: []
  # Example:
  # - id: "rollback_20260130160000"
  #   triggered_by: "reviewer"
  #   triggered_at: "YYYY-MM-DDTHH:MM:SSZ"
  #   cause:
  #     candidate_id: "new_component_20260130_2"
  #     learning_type: "new_component"
  #     symptom: "Caused downstream validation failures"
  #     discovery_method: "Automated validation suite"
  #   restoration:
  #     from_version: "v1.1.0"
  #     to_version: "v1.0.0"
  #     files_affected:
  #       - "reference/COMPONENTS.yaml"
  #   verification:
  #     ran_at: "YYYY-MM-DDTHH:MM:SSZ"
  #     status: "passed"
  #     notes: "Downstream validation clean after rollback"
```

---

### 1.7 `docs/_ai_context/state/DECISION_LOG.yaml`

Create as an **empty template** with structure and examples:

```yaml
# Decision Log — Machine-Readable Audit Trail
# Purpose: Track config/code/architecture decisions with structured evidence
# Format: Each entry has id, date, change, rationale, evidence, impact, reversibility

# Example entry:
# - id: "DEC-YYYYMMDD-001"
#   date: "YYYY-MM-DD"
#   phase: "XX"
#   change: "Description of what changed"
#   rationale: "Why this change was made"
#   evidence: "docs/_ai_context/analysis/YYYY-MM-DD_ANALYSIS.md"
#   impact: "What this affects and expected outcome"
#   approved_by: "Role or person"
#   reversible: true
#   rollback: "How to undo this change"
```

---

### 1.8 `docs/_ai_context/templates/README.md`

Create a **genericized** templates index (~80 lines):

```markdown
## Templates Index

This folder contains standardized output templates.

### Available Templates

| Template | Purpose | Status |
|----------|---------|--------|
| `PHASE_PLAN_TEMPLATE.md` | Phase plan with enforcement hooks | Production |

Add project-specific templates as they're created.

---

## AI-Assisted Template Enhancement

> **AI AGENT: READ THIS SECTION BEFORE MODIFYING ANY TEMPLATE**

### Template Structure Constraints

**Protected Elements:**
- YAML front-matter schema
- Required sections (varies per template)
- Version tracking in metadata

### What CAN Be Extended

- Add new columns to tables
- Add new sections
- Add project-specific examples
- Create variants for specific use cases
- Enhance descriptions with more detail

### How to Make Changes

1. **Preserve existing structure** — Add, don't replace core sections
2. **Follow MDD conventions** — Use YAML front-matter, proper markdown
3. **Update Change History** — Add a new row documenting the change
4. **Increment version** — Update version in metadata
5. **Validate against MDD rules**

### Change Documentation

Always update the Change History table:

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [Author] | Initial version |

### After Making Changes

1. Review for accuracy
2. Test with a real project if possible
3. Update any downstream documentation that references this template

---

## Contribution Guidelines

- **Minor changes** (typos): Increment patch version (1.0 → 1.0.1)
- **New sections/columns**: Increment minor version (1.0 → 1.1)
- **Structural changes**: Increment major version (1.0 → 2.0)

### Quality Checklist

- [ ] All required sections preserved
- [ ] YAML front-matter valid
- [ ] Change History updated
- [ ] Version incremented
- [ ] Markdown renders correctly
```

---

## Step 2: Create Tier B Scripts

### 2.1 `scripts/mdd/phase_preflight_validator.py`

Create a **genericized** phase pre-flight validator. This script automates backlog checking,
aging enforcement, plan anti-pattern scanning, and optional config-to-code wiring checks.

The script should be placed at `scripts/mdd/phase_preflight_validator.py` (not in `scripts/e2e/`
which was the BSS-specific location).

**Key genericizations from the source script:**
- Remove all hardcoded BSS paths (CONFIG_PATH, SCORING_PATH, CORRELATION_PATH, INDEX_BUILDER_PATH, PREPLAN_PATH)
- Make paths configurable via CLI arguments with sensible defaults
- Remove `check_index_field_usage()` (BSS-specific field list)
- Remove `check_gap_items()` (BSS pre-plan specific)
- Keep and generalize: `check_backlog()`, `check_backlog_completion()`, `check_backlog_aging()`, `check_data_schemas()`, `check_config_wiring()`, `check_reference_files()`
- `check_config_wiring()` should accept `--config` and `--code-files` arguments instead of hardcoded paths
- `check_reference_files()` should accept `--config` argument

Write the full script (~300 lines). Here is the structure:

```python
#!/usr/bin/env python3
"""
Phase Pre-Flight Validator (Generic MDD)
=========================================
Mechanically enforces backlog-first rule, aging checks, and plan anti-pattern
scanning BEFORE any phase execution begins.

Usage:
    python3 scripts/mdd/phase_preflight_validator.py --phase 5
    python3 scripts/mdd/phase_preflight_validator.py --phase 5 --strict
    python3 scripts/mdd/phase_preflight_validator.py --phase 5 --check-aging
    python3 scripts/mdd/phase_preflight_validator.py --completion 5
    python3 scripts/mdd/phase_preflight_validator.py --phase 5 --check-wiring \\
        --config config/app.yaml --code-files src/scoring.py src/pipeline.py
    python3 scripts/mdd/phase_preflight_validator.py --phase 5 --all

Exit codes:
    0 = All checks pass
    1 = Warnings (non-blocking)
    2 = Failures (blocking in --strict mode)
"""

import argparse
import re
import sys
import os
from pathlib import Path

# Default paths (MDD convention — override with --backlog, --config, etc.)
DEFAULT_BACKLOG = "docs/_ai_context/state/BACKLOG.md"


class ValidationResult:
    """Collects pass/warning/failure results and produces a formatted report."""
    # ... (same as source — this class is already generic)


def parse_backlog_items(backlog_path, phase_id):
    """Extract backlog items assigned to a specific phase."""
    # ... (same logic as source, but use backlog_path parameter)


def check_backlog(backlog_path, phase_id, result):
    """Check that P1 items assigned to this phase are addressed."""
    # ... (same logic, parameterized)


def check_backlog_completion(backlog_path, phase_id, result):
    """For --completion mode: verify all items DONE or DEFERRED with reason."""
    # ...


def check_backlog_aging(backlog_path, current_phase, result):
    """Check for P1 items that have survived > 2 phases."""
    # ...


def check_config_wiring(config_path, code_files, result):
    """Verify config keys (weights, feature flags) are referenced in code.

    Scans a YAML config for keys matching patterns like:
    - weight keys: `key: 0.5  # weight`
    - flag keys: `use_something: true` or `enable_something: false`

    Then checks if those keys appear in the provided code files.
    """
    # ... (generalized from source — accept config_path and list of code_files)


def check_reference_files(config_path, result):
    """Verify that file paths referenced in config actually exist."""
    # ... (generalized — accepts config_path parameter)


def scan_plan_antipatterns(plan_file, result):
    """Scan a plan file for common anti-patterns."""
    # Check for: encoding='utf-8' (without -sig), except:pass,
    # except ImportError:pass, "as discussed", references without paths
    # ... (same as source check_data_schemas but renamed and slightly expanded)


def main():
    parser = argparse.ArgumentParser(description="Phase Pre-Flight Validator (MDD)")
    parser.add_argument("--phase", required=True, help="Phase ID (e.g., 5, 12.A)")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--backlog", default=DEFAULT_BACKLOG, help="Path to BACKLOG.md")
    parser.add_argument("--check-wiring", action="store_true", help="Check config-to-code wiring")
    parser.add_argument("--config", type=str, help="YAML config file for wiring checks")
    parser.add_argument("--code-files", nargs="+", help="Code files to check for config references")
    parser.add_argument("--check-aging", action="store_true", help="Check P1 backlog aging")
    parser.add_argument("--check-plan", type=str, help="Plan file to scan for anti-patterns")
    parser.add_argument("--completion", action="store_true", help="Run completion gate checks")
    parser.add_argument("--all", action="store_true", help="Run all applicable checks")
    args = parser.parse_args()

    result = ValidationResult()
    # ... (dispatch to check functions based on args)

    exit_code = result.report()
    if args.strict and exit_code == 1:
        exit_code = 2
    sys.exit(exit_code)
```

**Dependencies:** Only Python stdlib (`argparse`, `re`, `sys`, `os`, `pathlib`). No `yaml`
import needed (config wiring uses regex, not YAML parsing, to avoid requiring PyYAML in
projects that don't use it). If the project has PyYAML available, the agent may optionally
use `yaml.safe_load` for better config parsing.

---

### 2.2 `scripts/mdd/data_schema_validator.py`

Create a **genericized** data schema validator. This automates CSV header verification,
BOM detection, and plan file anti-pattern scanning.

Place at `scripts/mdd/data_schema_validator.py`.

**Key genericizations from the source:**
- Remove correlation matrix validation (BSS-specific)
- Remove INDEX_DATA_MODEL references (BSS-specific)
- Make SCHEMAS_FILE path configurable via `--schemas` argument
- Default schemas path: `docs/_ai_context/knowledge/reference/DATA_FILE_SCHEMAS.yaml`
- Keep: `validate_csv_schemas()`, `check_bom()`, `scan_plan_field_references()`
- Simplify `scan_plan_field_references()` to only check for generic anti-patterns
  (not BSS-specific field names)

Write the full script (~200 lines). Structure:

```python
#!/usr/bin/env python3
"""
Data Schema Validator (Generic MDD)
====================================
Validates CSV headers, BOM encoding, and plan files against a schema registry.

Usage:
    python3 scripts/mdd/data_schema_validator.py --csv-schemas
    python3 scripts/mdd/data_schema_validator.py --check-bom
    python3 scripts/mdd/data_schema_validator.py --plan docs/_ai_context/prompts/phases/PHASE_5.md
    python3 scripts/mdd/data_schema_validator.py --all
    python3 scripts/mdd/data_schema_validator.py --schemas path/to/schemas.yaml --all

Exit codes: 0 = pass, 1 = warnings, 2 = failures

Requires: PyYAML (pip install pyyaml)
"""

import argparse
import csv
import re
import sys
import yaml
from pathlib import Path

DEFAULT_SCHEMAS = "docs/_ai_context/knowledge/reference/DATA_FILE_SCHEMAS.yaml"


class ValidationResult:
    # ... (same as source)


def load_schemas(schemas_path):
    # ... (parameterized path)


def validate_csv_schemas(schemas, repo_root, result):
    """Validate CSV files against declared schemas."""
    # ... (same logic, uses repo_root parameter)


def check_bom(schemas, repo_root, result):
    """Check BOM encoding on CSV files."""
    # ...


def scan_plan_antipatterns(plan_file, result):
    """Scan a plan file for common data-related anti-patterns."""
    # Checks: encoding='utf-8' without -sig, except:pass,
    # except ImportError:pass, row.get() without None check patterns
    # ... (generic version — no BSS field names)


def main():
    parser = argparse.ArgumentParser(description="Data Schema Validator (MDD)")
    parser.add_argument("--schemas", default=DEFAULT_SCHEMAS, help="Path to schemas YAML")
    parser.add_argument("--csv-schemas", action="store_true")
    parser.add_argument("--check-bom", action="store_true")
    parser.add_argument("--plan", type=str, help="Scan plan file for anti-patterns")
    parser.add_argument("--all", action="store_true")
    # ...
```

**Dependencies:** Python stdlib + `pyyaml`. Add `pyyaml` to a `requirements.txt` or note it
in the script docstring.

---

### 2.3 Supporting Files for Tier B

#### `scripts/mdd/README.md`

```markdown
# MDD Validation Scripts

Generic validation scripts for Markdown-Driven Development workflows.

## Scripts

| Script | Purpose | Dependencies |
|--------|---------|-------------|
| `phase_preflight_validator.py` | Pre-flight and completion gate checks | Python stdlib only |
| `data_schema_validator.py` | CSV/JSON schema validation | PyYAML |

## Usage

### Before Starting a Phase

    python3 scripts/mdd/phase_preflight_validator.py --phase 5 --all

### Before Closing a Phase

    python3 scripts/mdd/phase_preflight_validator.py --phase 5 --completion

### Validating Data Schemas

    python3 scripts/mdd/data_schema_validator.py --all

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks pass |
| 1 | Warnings (non-blocking) |
| 2 | Failures (blocking in --strict mode) |
```

#### `scripts/mdd/__init__.py`

Create as an empty file (makes `scripts/mdd/` importable).

#### `docs/_ai_context/knowledge/reference/DATA_FILE_SCHEMAS.yaml`

Create as an empty template that projects can populate:

```yaml
# Data File Schemas Registry
# Maps data files to their expected schemas for automated validation.
# Used by: scripts/mdd/data_schema_validator.py
#
# Add entries as your project creates/consumes CSV, JSON, or YAML data files.

metadata:
  version: "1.0.0"
  description: "Schema registry for data file validation"
  last_updated: null

# CSV file schemas
# Each entry: path, headers (list), delimiter, has_bom
csv_files: {}
  # Example:
  # users_export:
  #   path: "data/users.csv"
  #   headers: ["id", "name", "email", "created_at"]
  #   delimiter: ","
  #   has_bom: false

# JSON structure schemas
# Each entry: file path, expected top-level fields, nested field paths
json_structures: {}
  # Example:
  # config:
  #   path: "config/app.json"
  #   required_fields: ["version", "settings", "features"]
  #   nested_paths:
  #     - "settings.database.host"
  #     - "settings.database.port"
```

---

## Step 3: Extend the Bootstrapper

Add these seeds to the `seed_mdd_from_skills()` function in `setup-tools.sh`.
Append these lines after the existing seeds:

```bash
# === Tier A: Governance and Guidelines ===

# Multi-phase execution guidelines
[ -f "$mdd_root/prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md" ] || {
    echo "  Creating MULTI_PHASE_EXECUTION_GUIDELINES.md (from template file)"
    # This file is pre-created in the template at its destination path
}

# Governance rules
[ -f "$mdd_root/state/MDD_GOVERNANCE_RULES.md" ] || {
    echo "  MDD_GOVERNANCE_RULES.md will be created on first use"
}

# Knowledge governance files
mkdir -p "$mdd_root/knowledge/governance"
[ -f "$mdd_root/knowledge/governance/GOVERNANCE_POLICY.md" ] || {
    echo "  Creating GOVERNANCE_POLICY.md"
}
[ -f "$mdd_root/knowledge/governance/UPDATE_HISTORY.yaml" ] || {
    echo "  Creating UPDATE_HISTORY.yaml"
}
[ -f "$mdd_root/knowledge/governance/ROLLBACK_LOG.yaml" ] || {
    echo "  Creating ROLLBACK_LOG.yaml"
}

# Decision log
[ -f "$mdd_root/state/DECISION_LOG.yaml" ] || {
    echo "  Creating DECISION_LOG.yaml"
}

# Templates README
[ -f "$mdd_root/templates/README.md" ] || {
    echo "  Creating templates/README.md"
}

# Data schemas registry
mkdir -p "$mdd_root/knowledge/reference"
[ -f "$mdd_root/knowledge/reference/DATA_FILE_SCHEMAS.yaml" ] || {
    echo "  Creating DATA_FILE_SCHEMAS.yaml"
}

# Validation scripts
mkdir -p scripts/mdd
[ -f "scripts/mdd/phase_preflight_validator.py" ] || {
    echo "  Validation scripts at scripts/mdd/ ready to use"
}
```

Since these Tier A files live at their final destination paths in the template (not as
skill assets), the bootstrapper just needs to create the directory structure and log
that the files exist. The actual files are committed directly to the template repo.

---

## Step 4: Update AGENTS.md

Add a validation scripts section to AGENTS.md:

```markdown
## Validation Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/mdd/phase_preflight_validator.py` | Pre-flight checks before phase execution | `python3 scripts/mdd/phase_preflight_validator.py --phase 5 --all` |
| `scripts/mdd/data_schema_validator.py` | CSV/JSON schema validation | `python3 scripts/mdd/data_schema_validator.py --all` |
| `.cursor/skills/knowledge-repo/scripts/validate_knowledge_repo.py` | Knowledge repo health check | `python3 .cursor/skills/knowledge-repo/scripts/validate_knowledge_repo.py` |
```

---

## Step 5: Verify

```bash
# Tier A files exist
for f in \
  "docs/_ai_context/prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md" \
  "docs/_ai_context/state/MDD_GOVERNANCE_RULES.md" \
  "docs/_ai_context/state/MASTER_MARKDOWN_SYSTEM_RULES.md" \
  "docs/_ai_context/knowledge/governance/GOVERNANCE_POLICY.md" \
  "docs/_ai_context/knowledge/governance/UPDATE_HISTORY.yaml" \
  "docs/_ai_context/knowledge/governance/ROLLBACK_LOG.yaml" \
  "docs/_ai_context/state/DECISION_LOG.yaml" \
  "docs/_ai_context/templates/README.md"; do
  [ -f "$f" ] && echo "PASS: $f" || echo "FAIL: $f"
done

# Tier B scripts exist and are syntactically valid
for f in \
  "scripts/mdd/phase_preflight_validator.py" \
  "scripts/mdd/data_schema_validator.py"; do
  [ -f "$f" ] && python3 -c "import py_compile; py_compile.compile('$f', doraise=True)" \
    && echo "PASS: $f (syntax OK)" \
    || echo "FAIL: $f"
done

# Preflight validator help works (stdlib only, no external deps)
python3 scripts/mdd/phase_preflight_validator.py --phase test --help 2>/dev/null \
  && echo "PASS: preflight validator runs" || echo "FAIL: preflight validator"

# No BSS contamination in Tier A/B files
for keyword in "Mobily" "BSS" "TMF" "ArchiMate" "AMEFF" "Confluence" "Encompass" "MOBNS" "GB1033" "correlation_scoring" "ground_truth"; do
  hits=$(grep -ril "$keyword" docs/_ai_context/state/MDD_GOVERNANCE_RULES.md \
    docs/_ai_context/state/MASTER_MARKDOWN_SYSTEM_RULES.md \
    docs/_ai_context/knowledge/governance/ \
    scripts/mdd/ 2>/dev/null | wc -l)
  [ "$hits" -eq 0 ] && echo "PASS: no '$keyword' contamination" || echo "FAIL: '$keyword' found in $hits files"
done
```

---

## Step 6: Commit

```bash
git add docs/_ai_context/ scripts/mdd/ AGENTS.md setup-tools.sh
git commit -m "$(cat <<'EOF'
feat(mdd): Add Tier A governance files and Tier B validation scripts

Tier A (8 generic files):
- MULTI_PHASE_EXECUTION_GUIDELINES.md (337 lines)
- MDD_GOVERNANCE_RULES.md (14 core rules, genericized)
- MASTER_MARKDOWN_SYSTEM_RULES.md (markdown-as-artifact rules)
- Knowledge governance: GOVERNANCE_POLICY.md, UPDATE_HISTORY.yaml, ROLLBACK_LOG.yaml
- DECISION_LOG.yaml (ADR-style decision tracking)
- Templates README with AI enhancement instructions

Tier B (2 scripts + 3 supporting files):
- scripts/mdd/phase_preflight_validator.py (backlog, aging, wiring checks)
- scripts/mdd/data_schema_validator.py (CSV headers, BOM, plan anti-patterns)
- DATA_FILE_SCHEMAS.yaml empty registry template
- Bootstrapper extended to seed governance files

All files genericized: zero BSS/domain contamination.
EOF
)"
```

---

## Summary

| Category | Files | Purpose |
|----------|-------|---------|
| Tier A: Guidelines | `MULTI_PHASE_EXECUTION_GUIDELINES.md` | Comprehensive multi-phase manual |
| Tier A: Governance | `MDD_GOVERNANCE_RULES.md` | 14 core rules |
| Tier A: System Rules | `MASTER_MARKDOWN_SYSTEM_RULES.md` | Markdown-as-artifact conventions |
| Tier A: Knowledge Gov | `GOVERNANCE_POLICY.md`, `UPDATE_HISTORY.yaml`, `ROLLBACK_LOG.yaml` | Knowledge repo audit trail |
| Tier A: Decision Log | `DECISION_LOG.yaml` | ADR-style decisions |
| Tier A: Templates | `templates/README.md` | Template index + AI instructions |
| Tier B: Preflight | `scripts/mdd/phase_preflight_validator.py` | Backlog, aging, wiring checks |
| Tier B: Schema | `scripts/mdd/data_schema_validator.py` | CSV/JSON validation |
| Tier B: Support | `README.md`, `__init__.py`, `DATA_FILE_SCHEMAS.yaml` | Script docs + schema registry |

**Total new files:** 13
**BSS contamination:** 0 (verified by keyword scan)
**External dependencies:** PyYAML (for data_schema_validator.py only)

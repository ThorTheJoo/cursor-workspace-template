---
document_type: PROMPT
status: ACTIVE
purpose: "Self-contained agent prompt for integrating 9 MDD skills into the cursor-workspace-template GitHub repo"
target_repo: "https://github.com/ThorTheJoo/cursor-workspace-template"
estimated_duration: "2-3 hours"
---

# MDD Skills Integration — Template Repo Prompt

## What This Prompt Does

This prompt instructs you to integrate 9 portable MDD (Markdown-Driven Development) skills
into this workspace template. The skills follow the [Anthropic Agent Skills specification](https://agentskills.io/specification)
and were extracted from a production BSS document pipeline that ran 72+ phases over 4 months.

The skills encode a battle-tested AI-assisted development methodology:
- **P-R-I-L workflow** (Plan → Review → Implement → Log)
- **Authority hierarchy** (Knowledge > State > Manifests > Rules/Skills)
- **Sniper context loading** (manifest-first, targeted reads, never full-file loads)
- **Self-contained plans** (every plan executable in an independent agent window with zero prior context)
- **Data verification** (verify actual file schemas before writing parsing code)
- **Backlog aging** (P0 blocks current phase, P1 escalates after 2 phases)

## Task List

1. **Create the MDD_ROOT config system** — A single variable controlling where MDD files live
2. **Create all 9 skill folders** with SKILL.md + references/ + assets/ files
3. **Create skills README.md and SKILLS_INDEX.md**
4. **Slim down `01-mdd.mdc`** to a router that delegates to skills
5. **Enhance the bootstrapper** to seed MDD state files from skill assets
6. **Update AGENTS.md** to reference the skills framework
7. **Verify** everything works

---

## CRITICAL: The MDD_ROOT Variable System

### Problem

The skills reference `docs/_ai_context/` paths ~88 times across 48 files. These paths are
MDD conventions (not hardcoded dependencies), but a team that wants to use a different
directory structure (e.g., `.ai/` or `_context/`) would need painful search-replace.

### Solution: Define MDD_ROOT Once, Reference Everywhere

Every skill file that mentions a directory path uses the **convention name** `{MDD_ROOT}/`.
At the top of the skills README.md, we define:

```
MDD_ROOT = docs/_ai_context
```

This means:
- `{MDD_ROOT}/state/BACKLOG.md` → `docs/_ai_context/state/BACKLOG.md`
- `{MDD_ROOT}/analysis/` → `docs/_ai_context/analysis/`
- `{MDD_ROOT}/knowledge/` → `docs/_ai_context/knowledge/`

To change the root for a project, update the README definition and run:
```bash
find .cursor/skills -type f -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.py" | \
  xargs sed -i 's|docs/_ai_context/|your/custom/path/|g'
```

### Implementation

When writing every file below, use the literal string `docs/_ai_context/` (the default).
But add the `MDD_ROOT` declaration to README.md and a "Customization" section explaining
how to change it. The convention-based approach means paths work out-of-the-box for the
default layout while being trivially changeable.

Additionally, create a helper script at `.cursor/skills/scripts/set-mdd-root.sh` that
automates the path replacement:

```bash
#!/usr/bin/env bash
# set-mdd-root.sh — Change MDD_ROOT across all skill files
# Usage: ./set-mdd-root.sh "your/custom/path/"
set -euo pipefail

OLD_ROOT="docs/_ai_context/"
NEW_ROOT="${1:?Usage: $0 <new-root-path>}"

# Ensure new root ends with /
[[ "$NEW_ROOT" == */ ]] || NEW_ROOT="${NEW_ROOT}/"

echo "Replacing MDD_ROOT: $OLD_ROOT → $NEW_ROOT"

find .cursor/skills -type f \( -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.py" \) \
  -exec sed -i "s|${OLD_ROOT}|${NEW_ROOT}|g" {} +

# Update README declaration
sed -i "s|MDD_ROOT = .*|MDD_ROOT = ${NEW_ROOT%/}|" .cursor/skills/README.md

echo "Done. Updated $(grep -rl "${NEW_ROOT}" .cursor/skills/ | wc -l) files."
```

---

## Step 1: Create Directory Structure

Create all directories first:

```bash
# Skills directories
mkdir -p .cursor/skills/mdd-workflow/{references,assets}
mkdir -p .cursor/skills/plan-generation/{references,assets}
mkdir -p .cursor/skills/phase-execution/{references,assets}
mkdir -p .cursor/skills/data-verification/references
mkdir -p .cursor/skills/context-loading/{references,assets}
mkdir -p .cursor/skills/knowledge-repo/{references,assets,scripts}
mkdir -p .cursor/skills/backlog-management/assets
mkdir -p .cursor/skills/work-logging/{references,assets}
mkdir -p .cursor/skills/prompt-optimization/references
mkdir -p .cursor/skills/scripts
```

---

## Step 2: Create the Skills Source Archive

The 9 skills exist in a source repository at `/root/projects/general-use-case/.cursor/skills/`.
An archive has been pre-built at `/tmp/mdd-skills-tier1.tar.gz` (48 files, 64KB).

**If the archive is available**, extract it:
```bash
tar xzf /tmp/mdd-skills-tier1.tar.gz
cp -r skills-payload/* .cursor/skills/
rm -rf skills-payload
```

**If the archive is NOT available**, you must create each file from the specifications below.
The rest of this prompt contains the COMPLETE content for every file that needs to exist.

---

## Step 3: Skills to Create (Complete Specifications)

### 3.0 Root Files

#### `.cursor/skills/README.md`

Create this file. It is the master index for the skills framework. Key requirements:
- YAML frontmatter with name: `mdd-skills-framework`
- MDD_ROOT declaration: `MDD_ROOT = docs/_ai_context`
- Tier 1 table listing all 9 portable skills with purpose and key innovation
- Installation section (Cursor, Claude Code, Claude.ai, Claude API)
- Customization section explaining how to change MDD_ROOT
- Spec compliance section referencing agentskills.io

The content should closely follow this structure:

```
---
name: mdd-skills-framework
description: "9 portable MDD methodology skills following the Anthropic Agent Skills spec."
metadata:
  author: mdd-framework
  version: "1.0.0"
  spec: "agentskills.io v1.0"
---

# MDD Skills Framework

> **MDD_ROOT = docs/_ai_context**
>
> All path references in these skills use `docs/_ai_context/` as the default root.
> To change it, run: `.cursor/skills/scripts/set-mdd-root.sh "your/path/"`

## Skills

| Skill | Purpose | Key Innovation |
|-------|---------|---------------|
| mdd-workflow | Core MDD: P-R-I-L, authority hierarchy, governance | Constitutional truth precedence |
| plan-generation | Self-contained plan writing with quality gates | "Zero prior context" principle |
| phase-execution | Multi-phase execution with validation gates | Context-independent handoffs |
| data-verification | Verify data schemas before writing parsing code | Silent failure prevention |
| context-loading | Efficient AI context loading via manifests | Sniper mode: manifest-first |
| knowledge-repo | Canonical knowledge management with governance | Staging → promotion → versioning |
| backlog-management | Prioritized backlog with aging enforcement | P0 can't defer; P1 escalates after 2 phases |
| work-logging | Structured work logging with lessons learned | Regression risk classification |
| prompt-optimization | Prompt, plan, and workflow optimization | Progressive disclosure budgeting |

## Customization

### Changing MDD_ROOT

The default directory for all MDD files is `docs/_ai_context/`. To use a different path:

    .cursor/skills/scripts/set-mdd-root.sh "your/custom/path/"

This updates all 88 path references across 48 files in one command.

## Installation

- **Cursor**: Skills in `.cursor/skills/` are auto-discovered
- **Claude Code**: Copy to `.claude/skills/` for Claude Code compatibility
- **Claude.ai**: Upload individual SKILL.md files as custom skills

## Spec

All skills follow the Agent Skills Specification (agentskills.io):
- YAML frontmatter with name and description
- Directory name matches name field
- SKILL.md < 500 lines; detailed content in references/
- Progressive disclosure: Discovery → Activation → Execution
```

#### `.cursor/skills/SKILLS_INDEX.md`

Create a machine-readable index with:
- Registry table: all 9 skills with tier=portable, status=COMPLETE, line counts
- Validation section
- Discovery budget section (~830 tokens for 9 skills)
- Note: "Portable skills have NO inter-skill dependencies"

#### `.cursor/skills/scripts/set-mdd-root.sh`

Create the script from the specification above. Make it executable (`chmod +x`).

---

### 3.1 Skill: `mdd-workflow`

**What it encodes:** The core MDD methodology — authority hierarchy, P-R-I-L workflow,
complexity triage, operational modes (Ask/Plan/Agent), critical feedback requirements,
directory structure convention, governance rules, archival rules, git conventions.

**Source:** This was extracted from a 600-line user rule (MDD Protocol V1.3) and 4 Cursor
rules (.mdc files). The skill distills the essentials into <200 lines with detailed
references for deep dives.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~190 | Authority hierarchy table, P-R-I-L quick reference, complexity triage matrix, 3 operational modes with response templates, critical feedback section, directory structure, governance quick reference, archival rules, git conventions, references table |
| `references/authority-hierarchy.md` | ~80 | Detailed 4-rank hierarchy (Knowledge > State > Manifest > Rules/Skills) with conflict resolution examples |
| `references/pril-workflow.md` | ~70 | Full P-R-I-L with artifact requirements per complexity tier, plan locations, review requirements, logging protocol |
| `references/complexity-triage.md` | ~60 | Decision matrix, complexity criteria, required artifacts per tier, examples |
| `references/governance-rules.md` | ~60 | Code reuse mandate, auto MDD updates, contract-first validation, prohibited/required actions table |
| `references/archival-rules.md` | ~40 | When to archive, how to archive, never-delete rule |
| `references/git-conventions.md` | ~40 | Conventional commits, phase commits, WIP prefix |
| `assets/directory-structure.md` | ~50 | Full MDD directory tree with descriptions of each folder |

**Frontmatter for SKILL.md:**
```yaml
---
name: mdd-workflow
description: "Markdown-Driven Development methodology for AI-assisted codebases. Use whenever setting up a new project with AI agents, establishing documentation workflows, defining authority hierarchies for AI context, or implementing Plan-Review-Implement-Log (P-R-I-L) cycles. Triggers on: project setup, documentation architecture, agent workflow, P-R-I-L, MDD, governance, complexity triage, or context management."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

**Key content for SKILL.md body** (write the full content, do not truncate):

- **Authority Hierarchy** section with 4-rank table: Knowledge (`knowledge/`) > State (`state/`) > Manifests (repo-manifest.json, CONTEXT_MANIFEST.md) > Rules/Skills (.cursor/rules/, .cursor/skills/)
- **P-R-I-L** section with 4-step table: Plan (write document) → Review (human checkpoint) → Implement (atomic changes) → Log (WORK_LOG, commit, completion doc)
- **Complexity Triage** section with 3-tier table: Simple (<30 min, no plan) / Medium (3-5 steps, analysis file in `docs/_ai_context/analysis/`) / Complex (6+ steps, phase plan in `docs/_ai_context/prompts/phases/`)
- **Operational Modes** section: Ask (FINDING/EVIDENCE/NEXT STEPS format), Plan (PLAN/CHANGES/VALIDATION format), Agent (CHANGE/FILES/VALIDATION format)
- **Critical Feedback** section: flaws/risks, self-critique, self-verification. No flattery.
- **Directory Structure** section showing `docs/_ai_context/` tree
- **Governance Quick Reference** table: code reuse, auto MDD updates, contract-first, config over code
- **References** table pointing to all reference files

---

### 3.2 Skill: `plan-generation`

**What it encodes:** How to write self-contained plans that can execute in independent
agent windows with zero prior context. Quality gates and checklists.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~137 | Core principle ("zero prior context"), self-containment rule with failure examples, mandatory checklist (structure/traceability/executability/validation), plan types table, plan location rules, references |
| `references/self-containment-checklist.md` | ~70 | Full checklist from plan-generation-quality.mdc: data verification, producer→consumer audit, silent failure check, context sources, what makes a plan FAIL |
| `references/frontmatter-standard.md` | ~50 | YAML front-matter fields (document_type, status, depends_on, outputs_for_next_phase, validation_gate, etc.) |
| `references/plan-quality-gates.md` | ~50 | What makes a plan fail review, selective signal check, silent failure check |
| `assets/PHASE_PLAN_TEMPLATE.md` | ~150 | Complete generic phase plan template with all mandatory sections |

**Frontmatter for SKILL.md:**
```yaml
---
name: plan-generation
description: "Generate self-contained, executable plans that can run in independent agent sessions with zero prior context. Use whenever creating phase plans, analysis plans, execution specs, or breaking complex work into documented steps. Triggers on: 'create a plan', 'write a phase', 'break this down', multi-step tasks, plan files, validation gates, or structured execution specs."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.3 Skill: `phase-execution`

**What it encodes:** How to execute multi-phase plans with pre-flight validation, backlog
enforcement, completion gates, and structured handoffs.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~153 | Before writing code (pre-flight: read backlog, check P1 items), before any config change (wiring verification), completion protocol, anti-patterns table, backlog aging quick reference, error recovery summary, references |
| `references/multi-phase-guidelines.md` | ~100 | Context independence, explicit handoffs, validation gates, atomic commits, kickoff prompts, parallel markers |
| `references/preflight-checklist.md` | ~60 | Read backlog, check aging, verify wiring, announce P1 items |
| `references/completion-protocol.md` | ~60 | Run validator, re-read backlog, update statuses, create completion doc, run tests, commit |
| `references/anti-patterns.md` | ~50 | "Why It Fails" / "Instead" table for common execution mistakes |
| `references/error-recovery.md` | ~40 | Step failure, gate failure, abandonment protocols |
| `assets/CONTEXT_MANIFEST_TEMPLATE.md` | ~120 | Template with project identity, authority hierarchy, agent contract, metrics, capabilities |
| `assets/PHASES_INDEX_TEMPLATE.md` | ~40 | Phase registry template |
| `assets/KICKOFF_PROMPT_TEMPLATE.md` | ~20 | Copy-paste kickoff prompt template |

**Frontmatter for SKILL.md:**
```yaml
---
name: phase-execution
description: "Execute multi-phase plans with pre-flight validation, backlog enforcement, completion gates, and structured handoffs. Use whenever implementing work from a plan file, running a phase spec, or executing documented steps that reference PHASE_*.md files. Triggers on: 'execute', 'run phase', 'implement the plan', kickoff prompts, plan references, or PHASE_*.md files."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.4 Skill: `data-verification`

**What it encodes:** Verify data file schemas before writing parsing code. The #1 cause
of data pipeline bugs is field name mismatches.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~136 | Core principle ("never trust documentation"), CSV verification (utf-8-sig, headers, delimiter), JSON/YAML verification (sample entry, trace lineage), dataclass extension (Producer→Container→Consumer), silent failure prevention, quick checklist table |
| `references/csv-verification.md` | ~60 | Encoding patterns, BOM detection, delimiter detection, header validation, common gotchas |
| `references/json-verification.md` | ~50 | Sample entry reading, nested field access, schema registry lookup, common gotchas |
| `references/producer-consumer-audit.md` | ~60 | Full Producer→Container→Consumer tracing methodology with generic examples |
| `references/silent-failure-prevention.md` | ~50 | Anti-patterns (except:pass, silent None), required patterns (log WARNING, raise on unexpected) |

**Frontmatter for SKILL.md:**
```yaml
---
name: data-verification
description: "Verify data file schemas, column headers, and field existence before writing any parsing code. Use whenever code reads CSV files, accesses JSON fields, consumes dataclass/dict structures, or a plan references fields on any data structure. Triggers on: CSV parsing, pandas read_csv, JSON field access, dataclass extension, DataFrame operations, schema validation, or any code that opens a data file."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.5 Skill: `context-loading`

**What it encodes:** Efficient AI context loading via manifests and targeted reads.
The "sniper protocol" that prevents context window waste.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~160 | Core principle ("manifest-first, targeted reads"), priority loading table (4 levels), rules (never >500 lines, never guess paths, never reinvent), loading by mode (Ask/Plan/Agent), creating manifests for new projects, anti-patterns table |
| `references/manifest-schema.md` | ~80 | repo-manifest.json schema, CONTEXT_MANIFEST.md schema, when to refresh |
| `assets/CONTEXT_MANIFEST_TEMPLATE.md` | ~120 | Generic template with project identity, authority hierarchy, agent contract, metrics, capabilities |
| `assets/repo-manifest-template.json` | ~50 | Clean JSON template with empty arrays and placeholder values |

**Frontmatter for SKILL.md:**
```yaml
---
name: context-loading
description: "Efficient AI context loading via manifests and targeted reads for any codebase. Use whenever starting a session in an unfamiliar codebase, loading project context, establishing file/capability inventory, or optimizing context window usage. Triggers on: session start, 'what does this project do', codebase exploration, manifest loading, repo-manifest.json, CONTEXT_MANIFEST.md, or context window optimization."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.6 Skill: `knowledge-repo`

**What it encodes:** Canonical knowledge management with governance, versioning,
staging-to-production promotion, and rollback. This is the most file-heavy skill.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~265 | What a knowledge repo is, directory structure, authority hierarchy, governance workflow, promotion criteria, versioning protocol, rollback protocol, validation, bootstrapping instructions |
| `references/governance-policy.md` | ~80 | Full governance: learning candidate queue, approval workflow, priority formula, rollback triggers |
| `references/versioning-protocol.md` | ~50 | CURRENT_VERSION, versions/ snapshots, CHANGELOG.md, when to bump |
| `references/staging-workflow.md` | ~50 | Staging → validation → review → promotion → clear staging |
| `references/schema-validation.md` | ~60 | JSON Schema patterns, how to create schemas, common patterns |
| `assets/MASTER_KNOWLEDGE_REPO_TEMPLATE.yaml` | ~30 | Minimal template with metadata and placeholder domains |
| `assets/TERMINOLOGY_INDEX_TEMPLATE.yaml` | ~20 | Empty glossary template |
| `assets/EVIDENCE_REGISTRY_TEMPLATE.yaml` | ~25 | Empty evidence registry with authority levels |
| `scripts/validate_knowledge_repo.py` | ~170 | Python script that validates knowledge repo health (CURRENT_VERSION, YAML parsing, schema validation, CHANGELOG) — accepts `--knowledge-root` argument with default `docs/_ai_context/knowledge` |

**Frontmatter for SKILL.md:**
```yaml
---
name: knowledge-repo
description: "Manage canonical domain knowledge with versioned YAML files, governance workflows, staging-to-production promotion, and rollback capabilities. Use whenever creating a knowledge repository, defining domain truth, versioning reference data, managing glossaries or taxonomies, or establishing governance for AI knowledge files. Triggers on: knowledge management, canonical data, taxonomy, ontology, glossary, 'single source of truth', domain reference files, or YAML knowledge governance."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.7 Skill: `backlog-management`

**What it encodes:** Prioritized backlog tracking with aging enforcement.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~128 | Purpose, format (checkbox + source attribution), priority labels (P0-P3), aging enforcement rules (P0 blocks, P1 escalates after 2 phases, P2 review every 5), grooming rules, when to add/close items |
| `assets/BACKLOG_TEMPLATE.md` | ~40 | Template with grooming rules, active items sections, resolved section |

**Frontmatter for SKILL.md:**
```yaml
---
name: backlog-management
description: "Maintain prioritized backlogs with aging enforcement, source attribution, and phase assignment. Use when tracking deferred work, managing task priorities, grooming backlogs, or enforcing that old items do not languish indefinitely. Triggers on: backlog, deferred items, task tracking, P0/P1/P2 priorities, 'what is pending', aging enforcement, or work item triage."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.8 Skill: `work-logging`

**What it encodes:** Structured work logging with lessons learned and regression risk.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~128 | Purpose, when to log, mandatory fields table (scope, status, duration, changes, validation, regression risk, lessons, next steps), lessons learned structure, regression risk categories, conventional commits |
| `references/lessons-learned-patterns.md` | ~70 | 4 mandatory questions, regression categories with prevention, anti-patterns table, pattern extraction trigger |
| `assets/WORK_LOG_TEMPLATE.md` | ~50 | Template with entry structure and all mandatory fields |

**Frontmatter for SKILL.md:**
```yaml
---
name: work-logging
description: "Structured work logging with lessons learned, regression risk assessment, and change tracking. Use after completing any non-trivial work to create audit trails and capture institutional knowledge. Triggers on: 'log this work', 'update work log', post-implementation documentation, lessons learned, change tracking, WORK_LOG.md, or regression risk assessment."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

### 3.9 Skill: `prompt-optimization`

**What it encodes:** Systematic optimization of prompts, plans, skills, and AI workflows.

**Files to create:**

| File | Lines | Content |
|------|-------|---------|
| `SKILL.md` | ~180 | Purpose, progressive disclosure budgeting (3 levels), skill description optimization (how to write trigger descriptions), prompt quality checklist, context window optimization, pattern extraction rules, skill structure guide |
| `references/prompt-patterns.md` | ~80 | Session initializer pattern, kickoff prompt pattern, investigation prompt pattern, plan prompt pattern, anti-patterns |
| `references/skill-extraction.md` | ~60 | When to extract (≥3 occurrences), how to structure, validation checklist, description optimization loop |

**Frontmatter for SKILL.md:**
```yaml
---
name: prompt-optimization
description: "Optimize agent prompts, plan structures, skill descriptions, and AI workflow efficiency. Use when improving prompt quality, reducing context waste, designing session initializers, refining skill trigger accuracy, or extracting reusable patterns from agent sessions. Triggers on: prompt improvement, workflow optimization, 'make this more efficient', context window management, skill description tuning, or prompt engineering."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---
```

---

## Step 4: Slim Down `01-mdd.mdc` to a Router

The existing `01-mdd.mdc` is a ~600-line always-loaded rule containing the full MDD methodology.
Now that methodology lives in skills (loaded on-demand), the rule should become a slim router
that keeps MDD awareness always-on but delegates details to skills.

**Replace** the content of `.cursor/rules/01-mdd.mdc` with approximately this structure:

```yaml
---
description: "MDD Protocol — slim router delegating to .cursor/skills/ for detailed methodology"
alwaysApply: true
---
```

Followed by a markdown body (~50-80 lines) containing:

1. **One-paragraph MDD summary** — "This workspace uses Markdown-Driven Development. All non-trivial work follows Plan → Review → Implement → Log."
2. **Authority hierarchy** (4-line table) — Knowledge > State > Manifests > Rules/Skills
3. **Skill activation table** — When to use each skill:
   - Setting up project → `mdd-workflow`
   - Creating plans → `plan-generation`
   - Executing phases → `phase-execution`
   - Parsing data files → `data-verification`
   - Loading context → `context-loading`
   - Managing knowledge → `knowledge-repo`
   - Tracking backlog → `backlog-management`
   - Logging work → `work-logging`
   - Optimizing prompts → `prompt-optimization`
4. **Directory convention** — `MDD_ROOT = docs/_ai_context` with brief structure
5. **Quick prohibitions** — Don't guess paths, don't skip validation, don't duplicate code

This reduces always-loaded tokens from ~8K to ~800 while maintaining always-on MDD awareness.

**Important:** Do NOT delete the old `01-mdd.mdc` without backing it up first. Archive it
to `docs/_ai_context/analysis/archive/01-mdd-v1.3-full.mdc` for reference.

---

## Step 5: Enhance the Bootstrapper

The bootstrapper (`setup-tools.sh` / `setup-tools.ps1`) should seed MDD state files
from skill assets when setting up a new workspace.

Add a function `seed_mdd_from_skills` to `setup-tools.sh`:

```bash
seed_mdd_from_skills() {
    local skills_dir=".cursor/skills"
    local mdd_root="docs/_ai_context"

    echo "Seeding MDD state files from skill assets..."

    # Create directory structure
    mkdir -p "$mdd_root"/{state,analysis/archive,prompts/phases,knowledge/{governance,reference,schemas,staging,versions},templates}

    # Seed from backlog-management
    [ -f "$mdd_root/state/BACKLOG.md" ] || {
        cp "$skills_dir/backlog-management/assets/BACKLOG_TEMPLATE.md" "$mdd_root/state/BACKLOG.md"
        echo "  Created BACKLOG.md"
    }

    # Seed from work-logging
    [ -f "$mdd_root/state/WORK_LOG.md" ] || {
        cp "$skills_dir/work-logging/assets/WORK_LOG_TEMPLATE.md" "$mdd_root/state/WORK_LOG.md"
        echo "  Created WORK_LOG.md"
    }

    # Seed from context-loading
    [ -f "$mdd_root/state/repo-manifest.json" ] || {
        cp "$skills_dir/context-loading/assets/repo-manifest-template.json" "$mdd_root/state/repo-manifest.json"
        echo "  Created repo-manifest.json"
    }
    [ -f "$mdd_root/prompts/phases/CONTEXT_MANIFEST.md" ] || {
        cp "$skills_dir/context-loading/assets/CONTEXT_MANIFEST_TEMPLATE.md" "$mdd_root/prompts/phases/CONTEXT_MANIFEST.md"
        echo "  Created CONTEXT_MANIFEST.md"
    }

    # Seed from phase-execution
    [ -f "$mdd_root/prompts/phases/PHASES_INDEX.md" ] || {
        cp "$skills_dir/phase-execution/assets/PHASES_INDEX_TEMPLATE.md" "$mdd_root/prompts/phases/PHASES_INDEX.md"
        echo "  Created PHASES_INDEX.md"
    }

    # Seed from knowledge-repo
    [ -f "$mdd_root/knowledge/MASTER_KNOWLEDGE_REPOSITORY.yaml" ] || {
        cp "$skills_dir/knowledge-repo/assets/MASTER_KNOWLEDGE_REPO_TEMPLATE.yaml" \
           "$mdd_root/knowledge/MASTER_KNOWLEDGE_REPOSITORY.yaml"
        echo "  Created MASTER_KNOWLEDGE_REPOSITORY.yaml"
    }
    [ -f "$mdd_root/knowledge/glossary/TERMINOLOGY_INDEX.yaml" ] || {
        cp "$skills_dir/knowledge-repo/assets/TERMINOLOGY_INDEX_TEMPLATE.yaml" \
           "$mdd_root/knowledge/glossary/TERMINOLOGY_INDEX.yaml"
        echo "  Created TERMINOLOGY_INDEX.yaml"
    }

    # Seed MASTER_STATE.md if it doesn't exist
    [ -f "$mdd_root/state/MASTER_STATE.md" ] || {
        cat > "$mdd_root/state/MASTER_STATE.md" << 'MASTER_EOF'
---
document_type: STATE
status: ACTIVE
---

# Project State

Read order for any non-trivial task:
1. `docs/_ai_context/state/repo-manifest.json` — file/function lookup
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` — project identity
3. This file — current state
4. `docs/_ai_context/state/BACKLOG.md` — pending work

---

## Skills Framework

This workspace uses 9 MDD skills at `.cursor/skills/`. See `.cursor/skills/README.md`.

---

## Recent Changes

(Add entries as work progresses)
MASTER_EOF
        echo "  Created MASTER_STATE.md"
    }

    echo "MDD seeding complete."
}
```

Call this function from the main bootstrapper flow after the MDD directory structure is created.

Also add the equivalent logic to `setup-tools.ps1` for Windows users.

---

## Step 6: Update AGENTS.md

Add a skills section to `AGENTS.md`. This file is used by Cursor Composer 2 for agentic
context discovery. Add the following section:

```markdown
## Skills Framework

9 portable MDD methodology skills at `.cursor/skills/`:

| Skill | Trigger Keywords |
|-------|-----------------|
| mdd-workflow | project setup, MDD, P-R-I-L, governance |
| plan-generation | create plan, write phase, break down task |
| phase-execution | execute plan, run phase, implement spec |
| data-verification | CSV parsing, JSON access, schema validation |
| context-loading | session start, codebase exploration, manifest |
| knowledge-repo | knowledge management, taxonomy, glossary |
| backlog-management | backlog, deferred items, priorities |
| work-logging | work log, lessons learned, change tracking |
| prompt-optimization | prompt improvement, workflow optimization |

Skills follow the [Anthropic Agent Skills spec](https://agentskills.io/specification).
Each skill is a self-contained folder with SKILL.md + references/ + assets/.

MDD_ROOT: `docs/_ai_context/` — changeable via `.cursor/skills/scripts/set-mdd-root.sh`
```

---

## Step 7: Verify

After all files are created, run these verification commands:

```bash
# 1. Count skill directories (should be 9)
ls -d .cursor/skills/*/  | wc -l

# 2. Count SKILL.md files (should be 9)
find .cursor/skills -name "SKILL.md" | wc -l

# 3. Verify all names match directories
for d in .cursor/skills/*/; do
  name=$(basename "$d")
  grep -q "^name: $name$" "$d/SKILL.md" && echo "PASS: $name" || echo "FAIL: $name"
done

# 4. Verify no SKILL.md exceeds 500 lines
for f in .cursor/skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  skill=$(basename $(dirname "$f"))
  [ "$lines" -lt 500 ] && echo "PASS: $skill ($lines lines)" || echo "FAIL: $skill ($lines lines)"
done

# 5. Verify set-mdd-root.sh is executable
[ -x .cursor/skills/scripts/set-mdd-root.sh ] && echo "PASS: set-mdd-root.sh executable" || echo "FAIL: not executable"

# 6. Verify bootstrapper seeds correctly
mkdir -p /tmp/test-mdd && cd /tmp/test-mdd
# (run seed_mdd_from_skills function)
# Check all seeded files exist:
for f in docs/_ai_context/state/BACKLOG.md \
         docs/_ai_context/state/WORK_LOG.md \
         docs/_ai_context/state/MASTER_STATE.md \
         docs/_ai_context/state/repo-manifest.json \
         docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md \
         docs/_ai_context/prompts/phases/PHASES_INDEX.md \
         docs/_ai_context/knowledge/MASTER_KNOWLEDGE_REPOSITORY.yaml; do
  [ -f "$f" ] && echo "PASS: $f" || echo "FAIL: $f missing"
done
cd -
rm -rf /tmp/test-mdd

# 7. Verify 01-mdd.mdc is slim (< 100 lines)
wc -l .cursor/rules/01-mdd.mdc
```

---

## Step 8: Commit

```bash
git add .cursor/skills/ .cursor/rules/01-mdd.mdc AGENTS.md setup-tools.sh setup-tools.ps1
git add docs/_ai_context/analysis/archive/

git commit -m "$(cat <<'EOF'
feat(skills): Add 9 portable MDD skills (Anthropic Agent Skills format)

- 9 methodology skills: mdd-workflow, plan-generation, phase-execution,
  data-verification, context-loading, knowledge-repo, backlog-management,
  work-logging, prompt-optimization
- MDD_ROOT variable system with set-mdd-root.sh for path customization
- 01-mdd.mdc slimmed to router (~80 lines, was ~600)
- Bootstrapper seeds MDD files from skill assets
- AGENTS.md updated with skills reference
- Follows Anthropic Agent Skills spec (agentskills.io)
EOF
)"
```

---

## Content Source Reference

The actual file contents for each skill were extracted from a production BSS document
pipeline workspace. If the tar archive (`/tmp/mdd-skills-tier1.tar.gz`) is not available,
the agent should write each file from scratch following the specifications above.

The specifications include:
- Exact frontmatter for every SKILL.md (name, description, metadata)
- File list with approximate line counts for every skill
- Content requirements for every file
- The full content of `mdd-workflow/SKILL.md` is available as a reference pattern
  (190 lines covering authority hierarchy, P-R-I-L, complexity triage, modes, feedback,
  directory structure, governance, archival, git conventions)

When writing files from scratch, follow the Anthropic `skill-creator` style:
- Imperative form ("Read the backlog" not "You should read the backlog")
- Explain WHY over rigid ALWAYS/NEVER
- Generic examples (no domain-specific content)
- Theory of mind — write for a smart agent
- Progressive disclosure — essentials in SKILL.md, details in references/

---

## Summary of Changes

| Area | Before | After |
|------|--------|-------|
| `.cursor/skills/` | 8 curated skills (existing) | 8 existing + 9 MDD skills |
| `.cursor/rules/01-mdd.mdc` | ~600 lines, always loaded (~8K tokens) | ~80 lines router (~800 tokens) |
| `setup-tools.sh` | Creates MDD directories | Also seeds state files from skill assets |
| `AGENTS.md` | No skills reference | Skills framework section with trigger table |
| MDD_ROOT customization | Not possible | `set-mdd-root.sh` changes all 88 refs in one command |
| Total always-loaded tokens | ~12K+ (rules) | ~1.6K (slim rules) + ~830 on-demand (skill discovery) |

# AGENTS.md - Cursor Workspace Starter

A portable, zero-global-pollution workspace template for Cursor IDE. Every new workspace inherits foundational AI rules (MDD V1.3 + King Mode + Full-Stack) and on-demand GitHub tool management.

## Repo Map

```
.
+-- docs/_ai_context/              # MDD V1.3 SSOT
|   +-- state/                     # MASTER_STATE.md, WORK_LOG.md, BACKLOG.md, repo-manifest.json
|   +-- analysis/                  # Plans (*_PLAN.md), debug logs, completion docs
|   |   +-- archive/              # Superseded analysis files
|   +-- templates/                 # ADR_TEMPLATE.md, artifact formats
|   +-- prompts/                   # Reusable prompt library
|   |   +-- phases/               # Phase execution plans for complex work
|   +-- knowledge/                 # Canonical domain knowledge (Rank 1)
|       +-- governance/           # PENDING_UPDATES, UPDATE_HISTORY, ROLLBACK_LOG
|       +-- schemas/              # JSON Schema validation
|       +-- versions/             # Version snapshots
|       +-- staging/              # External data staging
+-- .cursor/rules/                 # Foundational AI rules (always committed)
|   +-- 00-starter-rules.mdc      # Meta-rules: loading order + priority hierarchy
|   +-- 01-mdd.mdc                # MDD V1.4 Agentic Critical Edition
|   +-- 02-kingmode.mdc           # King Mode (ULTRATHINK, intentional minimalism)
|   +-- 03-frontend-fullstack.mdc # Next.js/tRPC/Shadcn/Tailwind/Zod conventions
|   +-- 04-security-policy.mdc    # Zero-trust: prompt injection, supply chain, MCP gating
+-- .cursor/bin/                   # Tool binaries (populated by bootstrapper)
+-- .cursor/skills/                # Curated agent skills (committed, available on clone)
|   +-- skill-creator/SKILL.md    # Create and iterate on new skills
|   +-- doc-coauthoring/SKILL.md  # Structured doc co-authoring workflow
|   +-- frontend-design/SKILL.md  # Distinctive, production-grade UI design
|   +-- webapp-testing/SKILL.md   # Playwright-based web app testing
|   +-- mcp-builder/SKILL.md      # MCP server development guide
|   +-- docx/SKILL.md             # Word document creation/editing
|   +-- pdf/SKILL.md              # PDF processing and manipulation
|   +-- xlsx/SKILL.md             # Excel/spreadsheet operations
+-- .cursor/mcp/                   # MCP server configs (see docs/MCP.md)
+-- bin/                           # Security scripts
|   +-- skill-scan.sh             # Static pattern scanner for tools/skills
|   +-- scan-secrets.sh           # Secret detection (gitleaks/trufflehog/grep)
+-- tools/manifest.json            # SSOT: all GitHub tools available for install
+-- .tools-cache/                  # Cloned tool repos (gitignored)
+-- setup-tools.ps1                # Windows/PowerShell bootstrapper
+-- setup-tools.sh                 # Bash/WSL/DevContainer bootstrapper
+-- .devcontainer/devcontainer.json        # Default dev container
+-- .devcontainer/devcontainer.no-net.json # Air-gapped dev container (--network=none)
+-- docs/MCP.md                    # MCP server conventions and capability gating
+-- .env.example                   # Env var template (no secrets)
+-- sample.envrc                   # direnv template for secret manager integration
+-- SECURITY.md                    # Security policy + disclosure
+-- SECURITY-LOCK.json             # Generated: SHA256 hashes of installed tools
+-- CONTRIBUTING.md                # How to add tools and security checks
+-- CHANGELOG.md
+-- AGENTS.md
+-- README.md
```

## Rule Hierarchy

1. **00-starter-rules.mdc** - Always loaded. Orchestrator: loading order, priority resolution, workspace paths. Zero behavioral content.
2. **01-mdd.mdc** - Always loaded. MDD V1.4: fat router with always-on behavioral floor (authority hierarchy, context loading, P-R-I-L, complexity triage, security constraints, prohibitions/requirements, critical feedback) + skill routing for procedural details.
3. **02-kingmode.mdc** - Always loaded. King Mode: ULTRATHINK, intentional minimalism, library discipline, response format.
4. **03-frontend-fullstack.mdc** - Glob-scoped to code files. Stack conventions only (no duplication from 02).
5. **04-security-policy.mdc** - Always loaded. Zero-trust security: prompt injection defense, supply chain pinning, MCP capability gating, skill scanning gate.

**Priority:** MDD (01) wins on process. King Mode (02) wins on design. Full-Stack (03) wins on implementation. Security (04) wins on trust decisions and cannot be overridden by 01-03.

## MDD V1.4 Context Paths

### State (read-write)

| Path | Content | V1.3 Role |
|---|---|---|
| `docs/_ai_context/state/MASTER_STATE.md` | Current workspace snapshot | Read first every session (Sniper Mode) |
| `docs/_ai_context/state/WORK_LOG.md` | Chronological change log | Enhanced template (Section 8) |
| `docs/_ai_context/state/BACKLOG.md` | Prioritized backlog (P0-P3) | First-class artifact (Feature 10) |
| `docs/_ai_context/state/repo-manifest.json` | Machine-readable file index | Sniper Mode navigation (Feature 1) |

### Decision Support (read-only reference)

| Path | Content | V1.3 Role |
|---|---|---|
| `docs/_ai_context/knowledge/COMPLEXITY_TRIAGE_MATRIX.md` | Simple/Medium/Complex decision rules | Section 4 |
| `docs/_ai_context/knowledge/MODE_TRANSITION_RULES.md` | Ask/Plan/Agent state machine | Section 3 |
| `docs/_ai_context/knowledge/ANTI_PATTERNS_CATALOG.md` | 34 failure patterns incl. 10 security (institutional memory) | Section 9 |
| `docs/_ai_context/knowledge/governance/GOVERNANCE_POLICY.md` | Metadata, compliance, knowledge protections | Features 5/9 |
| `docs/_ai_context/knowledge/governance/CONTINUOUS_IMPROVEMENT_PROTOCOL.md` | Learning loop routing checklist (7 items incl. security) | Section 11 |
| `docs/_ai_context/knowledge/governance/SECURITY_CONTROLS.md` | Security policy: secrets, supply chain, OWASP, agent controls | Section 7d |

### Templates (artifact generation)

| Path | When to Use |
|---|---|
| `docs/_ai_context/templates/MEDIUM_PLAN_TEMPLATE.md` | Medium complexity tasks (3-5 steps) |
| `docs/_ai_context/templates/COMPLEX_PREPLAN_TEMPLATE.md` | Complex tasks (6+ steps) |
| `docs/_ai_context/templates/PHASE_COMPLETION_TEMPLATE.md` | After completing any phase |
| `docs/_ai_context/templates/DEBUG_LOG_TEMPLATE.md` | Bug investigation |
| `docs/_ai_context/templates/RUNBOOK_TEMPLATE.md` | Operational procedures |
| `docs/_ai_context/templates/ADR_TEMPLATE.md` | Architectural decisions (MADR) |
| `docs/_ai_context/templates/RESPONSE_FORMAT_ASK.md` | Ask mode output format |
| `docs/_ai_context/templates/RESPONSE_FORMAT_PLAN.md` | Plan mode output format |
| `docs/_ai_context/templates/RESPONSE_FORMAT_AGENT.md` | Agent mode output format |

### Prompts and Navigation

| Path | Content | V1.3 Role |
|---|---|---|
| `docs/_ai_context/prompts/PROMPT_INDEX.md` | Discovery entry point for all prompts | All modes |
| `docs/_ai_context/prompts/SESSION_START.md` | Copy-paste session initialization | Feature 1 |
| `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` | Navigation map + agent contract | Sniper Mode |
| `docs/_ai_context/prompts/phases/MULTI_PHASE_EXECUTION_GUIDELINES.md` | Phase execution protocol | Feature 4 |

### Security

| Path | Content | V1.3 Role |
|---|---|---|
| `.cursor/rules/04-security-policy.mdc` | Agent zero-trust policy (prompt injection, supply chain, MCP, scanning) | Always-on security rule |
| `docs/_ai_context/knowledge/governance/SECURITY_CONTROLS.md` | Full security policy (secrets, supply chain, OWASP) | Section 7d detailed reference |
| `SECURITY.md` | Public security policy and disclosure | Root-level security contact |
| `SECURITY-LOCK.json` | Generated SHA256 hashes of installed tools | Auditability artifact |
| `bin/skill-scan.sh` | Static pattern scanner for dangerous code in tools/skills | Supply chain defense |
| `bin/scan-secrets.sh` | Secret detection (gitleaks/trufflehog or grep fallback) | Secret hygiene |
| `docs/MCP.md` | MCP server conventions and capability gating | MCP security guidance |
| `.env.example` | Environment variable template (no secrets) | Section 7d.6 convention |
| `sample.envrc` | direnv template for secret manager integration | Secret management |
| `.devcontainer/devcontainer.no-net.json` | Air-gapped dev container (--network=none) | Network isolation |
| `.gitignore` | 40+ sensitive file patterns blocked | Section 7d L1 defense |

### Governance Pipeline

| Path | Content |
|---|---|
| `docs/_ai_context/knowledge/governance/PENDING_UPDATES.yaml` | Proposed knowledge changes |
| `docs/_ai_context/knowledge/governance/UPDATE_HISTORY.yaml` | Applied changes log |
| `docs/_ai_context/knowledge/governance/ROLLBACK_LOG.yaml` | Reverted changes log |
| `docs/_ai_context/knowledge/schemas/repo-manifest.schema.json` | JSON Schema for repo manifest |

## Tool Management

* `tools/manifest.json` is the single source of truth for installable tools.
* Both bootstrappers validate manifest JSON before proceeding.
* Run `setup-tools.ps1` (Windows) or `./setup-tools.sh` (Bash) to interactively select and install.
* Cloned repos go into `.tools-cache/` (gitignored, never committed).

## Curated Skills

8 agent skills sourced from [anthropics/skills](https://github.com/anthropics/skills), committed directly into the template. Available immediately on every fresh clone — no bootstrapper required.

| Skill | Trigger | License | Architecture Role |
|---|---|---|---|
| `skill-creator` | "create a skill", "improve this skill" | Apache 2.0 | Closes Gap 13 (skill seed); makes Learn Step actionable |
| `doc-coauthoring` | "write a doc", "draft a spec", "PRD" | Apache 2.0 | Operationalizes Plan mode for structured documents |
| `frontend-design` | "build a page", "style this UI", "landing page" | Apache 2.0 | Complements King Mode (02-kingmode.mdc) design execution |
| `webapp-testing` | "test this app", "verify the UI", Playwright | Apache 2.0 | Closes self-verification gap (MDD Section 10) |
| `mcp-builder` | "build an MCP server", "integrate API" | Apache 2.0 | Makes `.cursor/mcp/` actionable |
| `docx` | "Word doc", ".docx", "report as Word" | Proprietary | Enterprise document generation |
| `pdf` | ".pdf", "merge PDFs", "extract text from PDF" | Proprietary | PDF processing and manipulation |
| `xlsx` | ".xlsx", "spreadsheet", "Excel file" | Proprietary | Spreadsheet creation and analysis |

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
Each skill is a self-contained folder with `SKILL.md` + `references/` + `assets/`.

MDD_ROOT: `docs/_ai_context/` — changeable via `.cursor/skills/scripts/set-mdd-root.sh`

## Conventions

* MDD V1.3 Sniper Mode: load context from manifest, not guessing.
* Three operational modes: Ask (investigation), Plan (architecture), Agent (execution).
* P-R-I-L workflow: Plan -> Review -> Implement -> Log.
* Flaws & Risks before any meaningful action.
* ULTRATHINK triggers exhaustive multi-dimensional analysis.
* Code follows Intentional Minimalism + Full-Stack conventions.
* Security baked in: 14 agent security rules (7d), 10 security anti-patterns, 5-layer defense-in-depth for secrets.
* Bootstrappers hardened: install command allowlist + commit pinning for supply chain security.

## Experiment JP Agent OS Entry Point

For Hermes Desktop, Open Claw, or another local agent OS, read `docs/_ai_context/prompts/AGENT_OS_HANDOFF.md` after the standard MDD context load.

Primary refresh command:

```powershell
python scripts/management/refresh_all.py --own-account 62848015857
```

The command writes machine-readable status to `reports/data/agent-refresh-status.json` and refreshes `reports/management-dashboard.html`. Agent inbox drops should land under `docs/_ai_context/inputs/inbox/email/`, `docs/_ai_context/inputs/inbox/onedrive/`, or `docs/_ai_context/inputs/inbox/manual/`.

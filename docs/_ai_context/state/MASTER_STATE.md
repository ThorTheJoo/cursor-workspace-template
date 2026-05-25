---
document_type: STATE
status: APPROVED
reviewer:
  accountable: "thagra01"
compliance_tags: ["CSG-AI-Policy", "MDD-V1.4", "King-Mode"]
traceability_id: "WS-001-cursor-workspace-starter"
---

# MASTER_STATE.md

**Last Updated:** 2026-05-25  
**Version:** 1.5.1

## Current Workspace State

**Experiment JP** — ENGEN Jet Park fuel & convenience operations. Management reporting pipeline active with source-classified inputs (POS, payroll, bank, manual recon).

### Input Source Layers

| Layer | Type | Files | Purpose |
|-------|------|-------|---------|
| POS System | auto-generated | `Starter Docs/`, `Refresh/`, `Additional/*.TXT` | Daily/monthly sales, wet stock, EFT |
| Inventory | auto-generated | `Additional/*Stock*`, shrinkage, purchases | Stock take, shrink, COGS |
| Accounting | auto-generated | `Additional/*Debtors*`, creditors, levy | AR/AP, franchise reporting |
| Payroll System | auto-generated | `Nett Pay List*.xls*` | Weekly net pay → FNB CSV |
| Bank Feed | auto-generated | `62848015857.ofx`, `*.ofx` | FNB account 62848015857 — Apr 2026: 327 trx |
| Manual Recon | human-maintained | `CASH UP APRIL 26.xlsx`, `Schedule of Accounts*.xlsx` | Petty cash, supplier invoices |
| OCR / WhatsApp | photo → OCR synthesis | `deepseek_text_*.txt` | ATG dips, CIT, EOD screenshots — confirm vs POS |

Registry: `docs/_ai_context/knowledge/reference/input-source-registry.yaml`  
File catalog: `docs/_ai_context/knowledge/reference/file-type-catalog.yaml`  
Architecture: `docs/_ai_context/knowledge/FILE_INGESTION_ARCHITECTURE.md`  
Guides: `docs/_ai_context/guides/DATA_INTERPRETATION_GUIDE.md` · `MANAGEMENT_DASHBOARD_SPECIFICATION.md`  
Analysis: `2026-05-24_ADDITIONAL_FOLDER_AND_FILE_REPO.md` · `2026-05-24_OCR_WHATSAPP_DISCOVERY.md` · `2026-05-24_REFRESH_POS_DROP.md` · `2026-05-24_BANK_OFX_REFRESH.md` · `2026-05-25_OPTIMIZATION_SESSION.md`

### Reporting Pipeline

| Output | Script |
|--------|--------|
| `reports/management-dashboard.html` | `scripts/management/generate_dashboard.py` |
| `reports/file-views/index.html` | `scripts/management/generate_file_views.py` |
| `reports/file-views/{report_type}.html` | `scripts/management/generate_file_views.py` |
| `reports/help/*.html` | `scripts/management/generate_file_views.py` |
| `reports/data/canonical-latest.json` | `scripts/management/parse_reports.py` |
| `reports/data/ingest-ledger.json` | `scripts/management/build_file_repo.py` |
| `reports/data/series/*.json` | `scripts/management/build_file_repo.py` |
| `reports/data/file-repo-index.json` | `scripts/management/build_file_repo.py` |
| `reports/payroll/Payment_*.csv` | `scripts/payroll/netpay_to_payment_csv.py --all` |
| `docs/_ai_context/prompts/HANDOFF_OPTIMIZATION_REFACTOR.md` | Optimization handoff for external models |

Latest optimization: `cash_variance_by_cashier` now parses cashier/shift variance summaries and uses batch/date content keys; the rank-1 catalog metadata update is tracked in `BACKLOG.md` pending human approval.

### Domain Skills (2026-05-24)

| Category | Count | Index |
|----------|-------|-------|
| Custom fuel/C-store | 3 | `fuel-station-operations`, `convenience-store-operations`, `fuel-petrochemical-inventory` |
| Retail inventory | 10 | See `.cursor/skills/DOMAIN_SKILLS_INDEX.md` |
| Finance & P&L | 6 | Same |
| Ops capabilities | 3 | inventory-demand-planning, energy-procurement, returns-reverse-logistics |
| E-commerce retail | 1 suite | `ecommerce-retail` (10 commands) |
| MDD portable | 9+ | Built-in template skills |

**Total skills with SKILL.md:** 40

### Core Components

| Component | Status | Version | Notes |
|---|---|---|---|
| `.cursor/rules/00-starter-rules.mdc` | Active | 2.2.0 | Thin orchestrator: loading order + priority resolution |
| `.cursor/rules/01-mdd.mdc` | Active | 1.4.0 | Fat router: always-on behavioral floor + security constraints + skill routing |
| `.cursor/rules/02-kingmode.mdc` | Active | 1.1.0 | King Mode: ULTRATHINK, intentional minimalism |
| `.cursor/rules/03-frontend-fullstack.mdc` | Active | 1.1.0 | Stack conventions only (no duplication) |
| `.cursor/rules/04-security-policy.mdc` | Active | 1.0.0 | Zero-trust: prompt injection, supply chain, MCP gating, skill scanning |
| `tools/manifest.json` | Valid | - | 5 tools + pinnedRef/requiresApproval/skillScan fields |
| `setup-tools.sh` / `setup-tools.ps1` | Enhanced | - | --help, --dry-run, --preset, --all, --none flags + SECURITY-LOCK.json |
| `bin/skill-scan.sh` | Active | 1.0.0 | Static pattern scanner for dangerous code in tools/skills |
| `bin/scan-secrets.sh` | Active | 1.0.0 | Secret detection (gitleaks/trufflehog/grep fallback) |
| `.cursor/skills/` | Complete | - | 8 curated skills + 9 portable MDD skills (committed) |
| `docs/_ai_context/` | Complete | - | Full V1.4 structure (11 subdirs, 35+ artifacts) |
| `CONTRIBUTING.md` | Active | - | How to add tools and security checks |
| `docs/MCP.md` | Active | - | MCP server conventions and capability gating |
| `.devcontainer/devcontainer.no-net.json` | Active | - | Air-gapped dev container (--network=none) |

### Rule Hierarchy (Zero Duplication)

```
00-starter-rules.mdc  (orchestrator: loading order + paths)
  +-- 01-mdd.mdc       (process: V1.4 fat router — behavioral floor + security + skill routing)
  +-- 02-kingmode.mdc   (design: minimalism, ULTRATHINK, library discipline)
  +-- 03-frontend-fullstack.mdc  (implementation: Next.js, tRPC, Shadcn, Zod)
  +-- 04-security-policy.mdc     (trust: zero-trust, supply chain, MCP gating)
```

Priority: MDD (01) wins on process. King Mode (02) wins on design. Full-Stack (03) wins on implementation. Security (04) wins on trust decisions.

### Wiring Summary

| Layer | Artifacts | Wired To |
|---|---|---|
| Rules (behavioral) | 5 .mdc files | Cross-reference knowledge/templates via inline refs |
| Knowledge (reference) | 7 docs (triage, modes, anti-patterns, governance, improvement, manifest spec, feature spec) | Referenced by rules + templates |
| Templates (artifact generation) | 9 templates (plan, pre-plan, completion, debug, runbook, ADR, 3 response formats) | Used by P-R-I-L-L workflow |
| Prompts (reusable) | SESSION_START, PROMPT_INDEX, CONTEXT_MANIFEST, MULTI_PHASE_GUIDELINES | Referenced by rules + knowledge |
| State (SSOT) | MASTER_STATE, WORK_LOG, BACKLOG, repo-manifest.json | Updated by every non-trivial task |
| Security (defense-in-depth) | 04-security-policy.mdc, SECURITY_CONTROLS.md, 10 security anti-patterns, .gitignore (40+ patterns), .env.example, SECURITY.md, SECURITY-LOCK.json, bin/skill-scan.sh, bin/scan-secrets.sh, devcontainer.no-net.json, bootstrapper hardening | Enforced by 01-mdd.mdc Section 6 + 04-security-policy.mdc (always-on) + wired into all templates |
| Governance (feedback loop) | CONTINUOUS_IMPROVEMENT_PROTOCOL, PENDING_UPDATES, UPDATE_HISTORY, ROLLBACK_LOG, GOVERNANCE_POLICY | Triggered after every task (Learn step) |
| Skills (agent capabilities) | 17 SKILL.md files (8 curated + 9 portable MDD methodology skills) | Triggered by description match; portable MDD skills provide on-demand workflow depth |
| Bootstrappers | setup-tools.sh/ps1 | Create MDD directory structure + seed state files from skill assets + validate manifest + install tools |

### Architecture Decisions

* ADR template: `docs/_ai_context/templates/ADR_TEMPLATE.md`
* V1.3 feature specification: `docs/_ai_context/knowledge/MDD_V1.3_FEATURE_SPECIFICATION_SUMMARY.md`
* V1.3 rule source (archived): `docs/_ai_context/analysis/archive/01-mdd-v1.3-full.mdc`
* V1.3 slim router (archived): `docs/_ai_context/analysis/archive/01-mdd-v1.3-slim-router.mdc`

### Constraints

* Rules 01-03 are non-optional and take priority over tool-specific rules.
* `.tools-cache/` is gitignored.
* All workspace configuration stays local.
* Knowledge files (Rank 1 per V1.4 Authority Hierarchy) require human approval to modify.
* Continuous Improvement Protocol runs after every non-trivial task (P-R-I-L).

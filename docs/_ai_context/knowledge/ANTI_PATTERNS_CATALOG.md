---
document_type: KNOWLEDGE
status: ACTIVE
version: "1.0.0"
---

# Anti-Patterns and Failure Patterns Catalog

Reference: MDD V1.3 Feature Spec F7. This is the full institutional memory — the condensed version lives in the `.cursor/rules/01-mdd.mdc` rule (Section 9).

Consult this catalog when debugging failures, reviewing plans, or onboarding new team members.

---

## Session Anti-Patterns

| # | Anti-Pattern | Why It Fails | Correct Alternative | Severity |
|---|--------------|--------------|---------------------|----------|
| 1 | "Continue from where we left off" | New session has zero memory of prior sessions | Reference specific file paths and state files | CRITICAL |
| 2 | "Use the data we extracted earlier" | Agent does not know what data, where, or when | Provide exact path + line numbers + format | CRITICAL |
| 3 | "Same as before" / "Do it like last time" | Ambiguous — agent interprets differently each time | Repeat the full specification or reference the plan file | HIGH |
| 4 | Loading entire large files into context | Blows context window; agent forgets earlier content | Read specific sections on-demand (Sniper Protocol) | HIGH |
| 5 | Implicit validation ("looks good") | Silent failures ship undetected | Explicit validation steps with verifiable output | HIGH |
| 6 | Claiming checks passed without running them | False confidence -> undetected regressions | Execute command, capture output, paste evidence | CRITICAL |
| 7 | "I think the file is at..." | Path fabrication -> failed reads -> retry loops | Resolve from manifest or search tools | HIGH |
| 8 | Scope creep during implementation | Unreviewed changes -> unintended side effects | Stay strictly within approved plan scope | MEDIUM |
| 9 | Skipping the Plan step for "quick" changes | "Quick" changes that break things take 10x longer to fix | Always triage complexity; plan if >2 steps | MEDIUM |
| 10 | Modifying canonical data without approval | Domain truth corrupted -> cascading downstream errors | Human-in-the-loop for knowledge files | CRITICAL |

---

## Data and Contract Failure Patterns

| # | Pattern Name | Description | Example | Detection | Prevention |
|---|-------------|-------------|---------|-----------|------------|
| 1 | **Field Name Drift** | Producer and consumer use different field names for the same concept | `content` vs `body` vs `text` | Contract validation | Pin field names in shared schema; never rename without updating all consumers |
| 2 | **Version Confusion** | Newer code reads stale data format | v1 golden data parsed by v2 parser | Version field check on read | Include `version` field in all structured data; validate on load |
| 3 | **Baseline Drift** | Metrics compared against outdated reference values | Pre-refactor quality scores used to measure post-refactor output | Timestamp check on baseline files | Timestamp all baselines; regenerate after structural changes |
| 4 | **Template Divergence** | Output format drifts from defined template over iterations | Missing required section in generated document | Template compliance check | Run template validator before output; diff against template |
| 5 | **Silent Fallback** | System degrades to lower-quality path without warning | Uses cached/stale data instead of fresh API call | Source field validation in output | Fail loud, not silent; validate `source` field; never degrade without explicit flag |
| 6 | **Phantom Dependency** | Code depends on file/function that was renamed or deleted | Import references deleted module | Static analysis / test run | Run tests before and after changes; check imports |
| 7 | **Cascade Failure** | Change to file A requires changes to B, C, D but only A is updated | Schema change without consumer updates | Dependency tracing | Follow cascade rule; trace all dependents |
| 8 | **Stale Index** | Navigation index (manifest, phase index) does not reflect actual state | Manifest lists deleted file | Drift check | Run manifest generator after changes; check imports |
| 9 | **Manifest Lockstep Drift** | `CONTEXT_MANIFEST` version / `manifest_lockstep` ≠ `repo-manifest.json` version | Agents load stale contract; sniper stack diverges | Diff version fields at session start | Bump both in the same MDD cascade; fail review if mismatch |
| 10 | **Invented Handoff Counts** | Agent invents workflow metrics or Gate 0 inputs when files missing | False confidence, wrong decisions | Gate 0 hard stop | Handoff template: stop and list missing paths |
| 11 | **Legacy Manifest Assumptions** | Agent requires root `files[]` / `capabilities{}` on modern manifests | Failed lookups, reinvented indexes | Schema check | Use `sniper_context_loading` + `sub_projects`; see REPO_MANIFEST_V2.template.json |

---

## Process Anti-Patterns

| # | Anti-Pattern | Consequence | Fix |
|---|--------------|-------------|-----|
| 1 | Writing code before planning | Rework, scope creep, unvalidated assumptions | Mandatory complexity triage |
| 2 | Skipping human review | Incorrect assumptions ship to production | Plan mode ALWAYS ends with human checkpoint |
| 3 | Not logging lessons learned | Same mistakes repeat across sessions | Mandatory structured lessons |
| 4 | Backlog items added but never reviewed | Silent accumulation of deferred debt | Backlog grooming protocol |
| 5 | Analysis files accumulating without archival | Context directory becomes unnavigable | Archival policy |
| 6 | Phase completion without completion doc | No record of what was done or learned | Mandatory completion docs |
| 7 | External write without chat consent | Irreversible remote mutations | `external-write-guard` + dry-run + env flag |
| 8 | Seeding new repos from polluted template `state/` | Domain project bleeds into fresh workspaces | Seed from `templates/REPO_MANIFEST_V2.template.json`, not live state |

---

## Security Anti-Patterns

Reference: MDD V1.3 Section 7d, `SECURITY_CONTROLS.md`. These patterns are the most dangerous because they often cause **irrecoverable** damage (secrets in git history cannot be fully purged from shared repos).

| # | Anti-Pattern | Why It Fails | Correct Alternative | Severity |
|---|--------------|--------------|---------------------|----------|
| 1 | **Hardcoded secrets in source** | Secrets persist in git history permanently; rotation requires code change + deploy | Use `process.env.VAR_NAME`; store in `.env` (gitignored); reference `.env.example` for names | CRITICAL |
| 2 | **Committing .env files** | Entire credential set exposed in one file; often contains production secrets | Add to `.gitignore`; use `.env.example` with empty values; use vault for production | CRITICAL |
| 3 | **Placeholder secrets that look real** (`sk-xxxx`, `ghp_abc123`) | Developers and scanners learn to ignore patterns that resemble real tokens; real leaks go unnoticed | Use descriptive placeholders: `YOUR_STRIPE_KEY_HERE`, `REPLACE_WITH_JWT_SECRET` | HIGH |
| 4 | **Disabling TLS verification** (`NODE_TLS_REJECT_UNAUTHORIZED=0`) | Opens man-in-the-middle attack surface; often left in production code | Fix the certificate chain; use proper CA bundles; never disable in production | CRITICAL |
| 5 | **CORS wildcard** (`Access-Control-Allow-Origin: *`) | Any website can make authenticated requests to your API | Allowlist specific origins; use environment-based CORS config | HIGH |
| 6 | **Logging sensitive data** (tokens, passwords, PII in WORK_LOG/console) | Logs are often stored with less protection than source code; PII logging may violate GDPR | Sanitize log output; use structured logging with redaction; never log auth tokens | HIGH |
| 7 | **Unpinned dependencies** (`"dep": "latest"` or `"dep": "*"`) | Supply chain attack via version hijacking; malicious code injected in patch release | Pin exact versions; commit lock files; audit before upgrading | HIGH |
| 8 | **eval/Invoke-Expression on external input** | Remote code execution if input is compromised | Allowlist commands; validate input; use structured execution (spawn, not eval) | CRITICAL |
| 9 | **Skipping pre-commit hooks** (`--no-verify`) | Bypasses all local security gates (secret scanning, linting) | Never use `--no-verify` in normal workflow; if needed, document why in commit message | HIGH |
| 10 | **Security by obscurity** (hiding API endpoints instead of auth) | Endpoints are discoverable via browser tools, logs, or enumeration | Always enforce authentication + authorization; never rely on URL secrecy | HIGH |

---
## How to Use This Catalog

1. **During plan review:** Scan the relevant anti-pattern tables. If the plan has characteristics matching any pattern, flag it.
2. **During debugging:** Check Data/Contract Failure Patterns first — most production bugs match one of the 8 patterns.
3. **During retrospectives:** Reference specific pattern IDs (e.g., "We hit Pattern #5 - Silent Fallback") for precision.
4. **Onboarding:** New contributors should read this before their first multi-phase execution.

---

## Contributing

When a new anti-pattern is observed (a failure that does not match existing patterns):
1. Document in the relevant DEBUG log
2. After the fix is confirmed, propose adding to this catalog
3. Include: Name, Description, Real Example, Detection, Prevention

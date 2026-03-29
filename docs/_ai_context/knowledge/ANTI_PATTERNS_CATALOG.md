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
| 8 | **Stale Index** | Navigation index (manifest, phase index) does not reflect actual state | Manifest lists deleted file | Drift check | Run manifest generator after changes |

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

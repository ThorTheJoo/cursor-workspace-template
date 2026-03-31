# Lessons Learned Patterns

Reference material for capturing structured lessons after non-trivial work.

## The Four Mandatory Questions

Every lessons-learned section must answer these questions:

### 1. What went well?
Document techniques, tools, or approaches that succeeded. Future agents should replicate these.

**Examples:**
- "Pre-reading the schema file before writing parsing code caught 3 field name mismatches"
- "Running the validation suite after each atomic change caught a regression immediately"
- "Using a feature flag let us test the new scoring path without risking the production flow"

### 2. What went wrong / was unexpected?
Document surprises, wrong assumptions, and bugs encountered. Be specific — name files, line numbers, and exact error messages when possible.

**Examples:**
- "Assumed the CSV used UTF-8 encoding, but corporate Excel exports include a BOM — needed UTF-8-SIG"
- "The `except ImportError: pass` silently skipped all enrichment for 276 pages — took 2 hours to diagnose"
- "Config key `max_boost: 5.0` was defined but the code used a hardcoded `3.0` — config was dead"

### 3. What to do differently next time?
Concrete, actionable changes — not vague aspirations. "Be more careful" is not actionable. "Add a schema validation step before any CSV parsing code" is.

**Examples:**
- "Always read the first 3 rows of a CSV before writing parsing code — never trust documentation"
- "Replace all `except: pass` with `except X as e: logger.warning(...)` — silent failures are the worst bugs"
- "After adding a config key, grep the codebase to verify something actually reads it"

### 4. Regression risk assessment
Rate as HIGH, MEDIUM, or LOW. Describe what could break and how to detect it.

**Examples:**
- "HIGH — Changed the tokenizer used by 4 scoring functions. If any function still uses the old tokenizer, scores will be inconsistent. Detection: run the full regression suite."
- "MEDIUM — Added a new field to the dataclass. If a downstream consumer doesn't handle the new field, it will get a default None. Detection: grep for all consumers of this dataclass."
- "LOW — Documentation-only change. No runtime impact."

## Regression Risk Categories

| Category | What Happens | How to Prevent |
|----------|-------------|----------------|
| **Field Mismatch** | Code writes `score_total` but consumer reads `total_score` | Pin field names in a shared schema or type definition |
| **Version Confusion** | New code reads old cached data that lacks required fields | Add version stamps to data files; validate version on load |
| **Baseline Drift** | "Improvement" is measured against an outdated baseline | Always timestamp baselines; re-run baseline before comparing |
| **Template Divergence** | Generated output drifts from the expected format | Run template compliance checks after generation |
| **Silent Fallback** | Script falls back to degraded behavior without logging | Replace all fallbacks with logged warnings; fail loud in audit mode |

## Anti-Patterns in Lessons Learned

These phrases indicate a lessons-learned section that will not help future agents:

| Anti-Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| "Continue from where we left off" | New session has no memory | Reference specific file paths and state files |
| "Use the data we extracted earlier" | Agent doesn't know what or where | Provide exact file path and line numbers |
| "Same as before" | Ambiguous — "before" doesn't exist | Repeat the specification explicitly |
| "Be more careful" | Not actionable | "Add validation step X before step Y" |
| "It should work now" | No verification | "Verified by running command X, output was Y" |
| Implicit validation | Silent failures | "Ran `pytest tests/`, all 42 tests passed" |
| Claiming checks passed without running them | False confidence | Execute the command, paste the output |

## Pattern Extraction Rule

When a lesson appears **3 or more times** across work log entries:

1. **Identify** — Search WORK_LOG.md for recurring themes
2. **Extract** — Create a rule (`.cursor/rules/`) or skill (`.cursor/skills/`)
3. **Codify** — Write the pattern with trigger conditions, examples, and enforcement
4. **Reference** — Link the new rule/skill in the work log entry
5. **Validate** — Confirm the pattern fires correctly on realistic scenarios

**Example extraction flow:**
- Work log mentions "CSV encoding issue" 3 times across different phases
- Extract into a data-verification rule: "All CSV reads must use `encoding='utf-8-sig'`"
- Future agents get this knowledge automatically via rule loading

## Example Lessons (Generic)

### Good: Specific and Actionable
```
**Lessons Learned:**
- What went well: Using the schema validator before writing any parsing code
  caught that the `user_email` column was actually named `email_address` in the CSV.
- What went wrong: The migration script ran successfully but didn't update the
  cache, so the old data was served for 1 hour until the TTL expired.
- Do differently: Add cache invalidation to the migration checklist. Specifically,
  after any schema change, run `scripts/invalidate_cache.py --scope affected_tables`.
- Regression risk: MEDIUM — Cache invalidation is manual. If forgotten after future
  migrations, stale data will be served until TTL expires (1 hour).
```

### Bad: Vague and Unhelpful
```
**Lessons Learned:**
- What went well: Everything went smoothly.
- What went wrong: Some minor issues.
- Do differently: Be more careful next time.
- Regression risk: LOW.
```

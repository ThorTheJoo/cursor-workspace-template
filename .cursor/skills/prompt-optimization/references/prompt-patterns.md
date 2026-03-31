# Effective Prompt Patterns

Common patterns for structuring prompts, plans, and agent interactions in AI-assisted development.

## Session Initializer Pattern

A copy-paste block that loads project context at the start of a new session.

```markdown
Load context:
1. Read `docs/_ai_context/state/repo-manifest.json` for file/capability inventory
2. Read `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` sections 1-4 for project identity
3. Read `docs/_ai_context/state/MASTER_STATE.md` for current phase and constraints
4. Check `docs/_ai_context/state/BACKLOG.md` for pending items related to my task
```

**When to use:** At the start of any non-trivial session where the agent needs project awareness.

**Key principle:** Manifest-first loading — navigate via index, not by guessing file paths.

## Kickoff Prompt Pattern

Starts a phase execution in a fresh agent session with zero prior context.

```markdown
Execute Phase [X] from [exact file path].

Context files to read first:
- [path 1] — [what to look for]
- [path 2] — [what to look for]

Expected outputs:
- [output 1]
- [output 2]

Validation: run [command] and verify [expected result].
```

**Key principle:** Self-containment. The agent reading this prompt has never seen your conversation. Include everything it needs.

**Common failures:**
- "Continue from where we left off" — the agent has no "before"
- "Use the same config" — which config? Exact path needed
- Missing validation commands — agent can't verify its own work

## Investigation Prompt Pattern

Structured format for Ask-mode queries.

```markdown
FINDING: [1-2 sentence direct answer]
EVIDENCE:
- File: [exact path]
- Function: [name, line number if applicable]
- Data: [relevant metrics or values]
NEXT STEPS: [numbered actions if needed]
```

**When to use:** When answering "where/how/what/why" questions about the codebase.

**Key principle:** Evidence-based. Every claim is backed by a specific file and location.

## Plan Prompt Pattern

Structured format for multi-step execution plans.

```markdown
PLAN: [Topic]
Complexity: [Simple / Medium / Complex]

CHANGES:
| File | Change | LOC |
|------|--------|-----|

VALIDATION:
- [ ] Gate 1: [command] → [expected result]
- [ ] Gate 2: [command] → [expected result]

RISKS:
| Risk | Impact | Mitigation |
|------|--------|------------|

READY FOR REVIEW: YES/NO
```

**Key principle:** Validation gates before code. Every step has a verifiable success criterion.

## Execution Prompt Pattern

Structured format for reporting completed work.

```markdown
CHANGE: [what was done]
FILES: [paths modified]
VALIDATION: [how to verify — paste actual command output]
REGRESSION RISK: [HIGH/MEDIUM/LOW — what to watch]
```

**Key principle:** Prove it works. Paste actual output, not claims.

## Anti-Patterns

Prompt patterns that consistently fail in AI-assisted development:

| Anti-Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| "Continue from where we left off" | New session has no memory of prior work | Reference specific file paths and state files |
| "Use the data we extracted earlier" | Agent doesn't know what data or where it is | Provide exact file path, line numbers, and field names |
| "Same as before" | "Before" doesn't exist in a stateless session | Repeat the full specification |
| "Check the config" | Which config? Which keys? | "Read `path/to/config.yaml`, key `section.field`, current value is X" |
| "Fix the scoring" | Which file? Which function? What's broken? | "In `scoring.py` line 45, function `score_match`, the weight is 3.0 but config says 5.0" |
| Loading entire large files | Wastes context window | "Read `file.py` lines 40-80 (the `score_match` function)" |
| Implicit validation | "It should work now" | "Run `pytest tests/test_scoring.py -v`, expect 12/12 pass" |
| Vague error description | "It's not working" | "Running `python main.py --input test.csv` produces `KeyError: 'user_id'` at line 23" |

## Compound Prompt Patterns

For complex tasks, combine patterns:

### Plan + Execute
1. Start with the Plan pattern to get approval
2. Switch to Execution pattern for each step
3. End with a summary using the Execution pattern

### Investigate + Plan
1. Start with the Investigation pattern to understand current state
2. Use findings to populate the Plan pattern
3. Get approval before executing

### Kickoff + Session Initializer
1. Session initializer loads general context
2. Kickoff prompt focuses on the specific phase
3. Agent has both broad context and specific instructions

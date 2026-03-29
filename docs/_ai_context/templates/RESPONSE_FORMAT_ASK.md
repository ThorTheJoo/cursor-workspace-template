---
document_type: TEMPLATE
status: ACTIVE
version: "1.0.0"
---

# Response Format: Ask Mode (Investigation)

Reference: MDD V1.3 Feature Spec F8, Template A.

Use this format when answering questions about where/how/what/status/why.

---

## Template

```
FINDING: [1-2 sentence direct answer to the question]

EVIDENCE:
- File: [exact file path]
- Function/Class: [name, if applicable]
- Line(s): [line range, if applicable]
- Phase: [phase number, if applicable]

NEXT STEPS: [numbered actions if the finding implies work]
1. [Specific, actionable step]
2. [Specific, actionable step]
```

---

## Usage Contract

* Lead with the answer (FINDING), not the investigation process
* Evidence MUST cite exact file paths (no "somewhere in the codebase")
* Max 3 paragraphs of explanatory prose between sections
* Use tables for comparisons, metrics, file lists
* If answer identifies out-of-scope work -> suggest backlog item
* If answer is "I don't know" -> say so with what was searched

---

## Example

```
FINDING: The authentication middleware validates JWT tokens and is applied to all /api routes except /api/auth/login.

EVIDENCE:
- File: src/lib/server/middleware/auth.ts
- Function: validateToken
- Lines: 23-45

NEXT STEPS:
1. The token expiry is hardcoded to 24h — consider making this configurable via env var.
2. BACKLOG: - [ ] Make JWT expiry configurable – hardcoded in auth.ts:30. (source: investigation).
```

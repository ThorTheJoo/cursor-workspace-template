# Knowledge Repository Staging Workflow

## Overview

New knowledge enters through a staging area before being promoted to production. This prevents untested or incorrect data from corrupting authoritative reference files.

## Workflow Diagram

```
Discovery → staging/ → Schema Validation → Human Review → reference/ (production)
                                              ↓ (reject)
                                         REJECTED with reason
```

## Step 1: Submit to Staging

When a candidate is identified (from pipeline output, manual discovery, or agent suggestion), create a YAML file in `staging/`:

```yaml
# staging/candidate_001.yaml
candidate_id: "CAND-001"
type: "NEW_TERM"
submitted: "2026-03-30T10:00:00Z"
submitted_by: "pipeline-run-42"
source: "Discovered in user feedback analysis"

proposed:
  term: "churn prediction"
  definition: "Statistical model estimating probability of customer leaving"
  domain: "analytics"
  synonyms: ["attrition forecast", "retention risk score"]

evidence:
  frequency: 12
  sources:
    - "docs/analysis/q1_report.md (lines 45-48)"
    - "src/models/churn.py (class name)"
    - "data/glossary_draft.csv (row 89)"
  confidence: 0.90

status: "pending_validation"
```

## Step 2: Automated Validation

Run schema validation against the candidate:

1. **Format check** — YAML parses without errors
2. **Schema compliance** — Candidate matches the relevant JSON Schema
3. **Duplicate check** — Term/entry does not already exist in production
4. **Conflict check** — No contradictions with existing entries

```bash
python scripts/validate_knowledge_repo.py --check-staging
```

If validation fails, update the candidate status to `validation_failed` with the error details.

## Step 3: Human Review

A designated reviewer evaluates the candidate:

- Is the term/entry genuinely useful and accurate?
- Is the classification correct?
- Does the evidence support the proposed addition?
- Would this change break any downstream consumers?

Decision options:
- **approve** — promote to production
- **reject** — document reason, archive the candidate
- **needs_info** — request additional evidence or clarification

Update the candidate file with the decision:

```yaml
review:
  decision: "approve"
  reviewer: "domain-expert-name"
  reviewed_at: "2026-03-30T14:00:00Z"
  notes: "Verified against Q1 analytics report. Term is widely used."
```

## Step 4: Promotion

For approved candidates:

1. Add the entry to the appropriate production file (e.g., `reference/GLOSSARY.yaml`)
2. Log the promotion in `governance/UPDATE_HISTORY.yaml`
3. Remove the candidate file from `staging/`
4. If this is part of a batch, collect all promotions before versioning

```yaml
# governance/UPDATE_HISTORY.yaml (append)
updates:
  - candidate_id: "CAND-001"
    type: "NEW_TERM"
    promoted_to: "reference/GLOSSARY.yaml"
    promoted_at: "2026-03-30T15:00:00Z"
    version: "1.3.0"
```

## Step 5: Cleanup

After a batch of promotions:

1. Create a version snapshot (see versioning protocol)
2. Clear the `staging/` directory of processed candidates
3. Archive rejected candidates to `staging/archive/` (do not delete)
4. Update `CHANGELOG.md`

## Staging Directory Lifecycle

| State | Location | Action |
|-------|----------|--------|
| New candidate | `staging/candidate_NNN.yaml` | Awaiting validation |
| Validated | `staging/candidate_NNN.yaml` (status: validated) | Awaiting review |
| Approved | Promoted to `reference/` | Candidate file removed |
| Rejected | `staging/archive/candidate_NNN.yaml` | Kept for audit trail |

## Batch Processing

For efficiency, batch multiple candidates:

1. Accumulate candidates in `staging/` over a review period (e.g., one week)
2. Run validation on all candidates at once
3. Present the batch to the reviewer
4. Promote all approved candidates in a single version bump
5. Clean staging after the batch is complete

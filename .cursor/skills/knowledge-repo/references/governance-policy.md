# Knowledge Repository Governance Policy Template

## Purpose

This policy governs all updates to the authoritative knowledge repository. All changes must follow this workflow to maintain data quality and prevent corruption of canonical reference data.

## Promotion Workflow

1. **Detection** — Pipeline, agent, or human identifies a learning candidate
2. **Frequency Gate** — Candidate must meet minimum evidence threshold (default: 3+ independent sources or 5+ occurrences)
3. **Review Queue** — Candidate enters `governance/PENDING_UPDATES.yaml` with metadata
4. **Human Review** — Designated reviewer approves, rejects, or requests more information
5. **Promotion** — Approved candidates update production knowledge files
6. **Validation** — Post-promotion validation confirms schema compliance and no regressions
7. **Rollback** — If validation fails, revert to previous version and reject the candidate

## Candidate Types and Approval Criteria

### NEW_TERM (Glossary Addition)
- Term must be domain-relevant, not a generic word
- Definition must be verifiable against authoritative documentation
- Not a duplicate or variant of an existing term

### NEW_SYNONYM
- Canonical term must already exist in the knowledge repository
- Synonym must be a genuine alternative name (not a typo or abbreviation-only)
- Must not create ambiguity with other terms

### NEW_CATEGORY (Taxonomy Addition)
- Category must represent a real grouping used in the domain
- Parent category must exist
- Not a duplicate of an existing category

### CORRECTION
- Error must be documented with evidence
- Original source of the incorrect entry should be noted
- Correction must not break downstream consumers

## Rejection Criteria

- Fewer than minimum evidence threshold
- Duplicate of existing entry
- Incorrect classification or domain assignment
- Unverifiable claim (no documentation source)
- Generic terms that would add noise (e.g., "system", "service", "data")
- Would create transitive ambiguity (A = B and B = C, so A = C unintentionally)

## Priority Scoring

Candidates are prioritized using:

```
Priority = (frequency × 0.4) + (inverse_confidence × 0.3) + (domain_weight × 0.3)
```

Higher priority candidates are reviewed first. Domain weights should be customized per project based on business criticality.

## Review Cadence

| Frequency | Activity |
|-----------|----------|
| Weekly | Review top 20 pending candidates |
| Monthly | Full queue cleanup and archival of stale candidates |
| Quarterly | Policy review and threshold adjustment |

## Audit Trail

All changes are logged in `governance/UPDATE_HISTORY.yaml`:
- Candidate creation timestamp and source
- Review decision, reviewer, and rationale
- Promotion or rejection timestamp
- Rollback events with reason

## Escalation

If a candidate requires specialized domain expert review:
1. Tag with `needs_info` status in PENDING_UPDATES.yaml
2. Create a work item in your project tracker
3. Assign to the appropriate domain owner
4. Update the candidate when resolved

## PENDING_UPDATES.yaml Structure

```yaml
pending_updates:
  - id: "PU-001"
    type: "NEW_TERM"
    term: "example term"
    proposed_definition: "A term meaning..."
    source: "discovered in pipeline run 2026-03-15"
    frequency: 7
    confidence: 0.85
    domain: "operations"
    status: "pending_review"
    created: "2026-03-15T10:00:00Z"
    reviewer: null
    decision: null
```

# Archival Rules

Keep `docs/_ai_context/analysis/` navigable by archiving superseded content.

## When to Archive

| Condition | Action |
|-----------|--------|
| Analysis file superseded by a newer version | Move to `docs/_ai_context/analysis/archive/` |
| File older than 90 days with no active references | Candidate for archiving — review first |
| Pre-plan expanded into full phase files | Archive the pre-plan |
| Completion doc for a phase that's been superseded | Archive when no longer referenced |

## Rules

- **Never delete** archived files — always move them to `archive/`
- **Never archive** active state files (MASTER_STATE.md, WORK_LOG.md, BACKLOG.md)
- **Never archive** completion docs that are still referenced by open backlog items
- **Never archive** files that are currently referenced by active phase plans

## Process

1. Identify the candidate file
2. Check for active references (grep for the filename across `docs/_ai_context/`)
3. If no active references, move to `docs/_ai_context/analysis/archive/`
4. If referenced, update the reference to point to the new location, or keep the file in place

## Why This Matters

A flat `analysis/` directory with 200+ files becomes impossible to navigate. Archiving keeps the active workspace clean while preserving history for rollback and auditing.

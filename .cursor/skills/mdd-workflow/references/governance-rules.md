# Governance Rules

## Code Reuse Mandate

Before writing any new code:

1. Search the existing codebase (grep, glob, semantic search)
2. Check script registries and state files
3. Read existing implementations that might cover the need

Code duplication is a critical error. If functionality exists, reuse it. If it almost exists, extend it. Only create new code when no existing solution is viable.

This matters because duplicate implementations drift over time — one gets fixed while the other doesn't, causing subtle bugs that are hard to trace.

## Automatic MDD Updates

Documentation must be updated automatically (without user prompting) when:

| Event | Update Required |
|-------|----------------|
| New script or module created | Script registry, MASTER_STATE.md |
| Error resolved | Analysis file in `docs/_ai_context/analysis/` |
| Phase completed | Phase index, WORK_LOG.md, completion doc |
| Pattern discovered | Relevant state files |
| Performance metrics change | Performance reports |

**Cascade rule:** If updating one file affects another, update all dependents. An inconsistent documentation set is worse than no documentation.

## Contract-First Validation

Before writing code that reads or writes structured data:

1. Identify the contract (schema, type definition, YAML structure)
2. Verify field names match between producer and consumer
3. Check for recently renamed or deprecated fields

After implementation: run validation, document any field changes.

This prevents the most common class of bugs in data pipelines — a producer changes a field name and the consumer silently gets null values.

## Config Over Code

If a change can live in a configuration file, propose it there first. Configuration changes are:
- Easier to review (no code logic to trace)
- Easier to revert (change one value)
- More visible (config files are typically small and readable)

Only put logic in code when the behavior genuinely requires programmatic control.

## Prohibited Actions

| Action | Why It's Prohibited |
|--------|-------------------|
| Creating scripts without searching for existing ones | Causes duplication that drifts |
| Modifying knowledge repo files without human approval | Knowledge files are constitutional authority |
| Leaving MDD docs inconsistent after changes | Stale docs cause wrong decisions in future sessions |
| Guessing file paths | Wastes time on FileNotFoundError; use manifest or search |
| Skipping validation gates | Undetected failures cascade into bigger problems |
| Bypassing template compliance | Downstream tools depend on exact formats |

## Required Actions

| Action | Why It's Required |
|--------|-----------------|
| Search codebase before writing new code | Prevents duplication |
| Validate output before declaring done | Catches silent failures |
| Update MDD docs after changes | Keeps context accurate for next session |
| Follow P-R-I-L for non-trivial work | Prevents scope creep and context loss |
| Use manifest or search for navigation | Ensures correct file paths |
| Log lessons learned after non-trivial work | Prevents repeated mistakes |

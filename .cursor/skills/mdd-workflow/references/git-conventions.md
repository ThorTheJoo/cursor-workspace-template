# Git Conventions

## Conventional Commits

Use conventional commit prefixes to make change history scannable:

```
feat(scope): summary      # New feature or capability
fix(scope): summary       # Bug fix
docs(scope): summary      # Documentation only changes
refactor(scope): summary  # Code restructuring without behavior change
test(scope): summary      # Adding or updating tests
chore(scope): summary     # Maintenance tasks (deps, tooling)
```

The `scope` identifies the subsystem (e.g., `pipeline`, `scoring`, `config`, `docs`).

## Phase Commits

For multi-phase work, use a structured commit message:

```
feat(pipeline): Phase XX - [Summary]

- [Key deliverable 1]
- [Key deliverable 2]
- [Validation results]
```

## Partial / Blocked Work

If a phase must be committed incomplete:

```
WIP: Phase XX partial - [what's done]

- [Completed items]
- [Blocked on: specific issue]
```

The `WIP:` prefix signals that this commit is not production-ready and may need to be amended or followed up.

## Traceability

When a JIRA ticket, GitHub issue, or traceability ID exists, include it:

```
feat(pipeline): Phase 68 - Enhanced scoring [PHASE68-SCORING-20260220]
```

This connects the git log to the MDD documentation trail.

## Rules

- Each phase = one logical commit (enables clean rollback)
- Atomic commits: don't mix unrelated changes
- Never force-push to shared branches without explicit team approval
- Tag rollback points before risky changes

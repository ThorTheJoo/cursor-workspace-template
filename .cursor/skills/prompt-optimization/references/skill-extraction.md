# Skill Extraction Process

How to identify, extract, and validate reusable patterns as Cursor Agent Skills.

## When to Extract

Extract a pattern into a skill when ALL of these criteria are met:

| Criterion | Threshold |
|-----------|-----------|
| Frequency | Pattern appeared in 3+ sessions or work log entries |
| Complexity | Pattern involves > 50 tokens of instructions |
| Repeatability | Pattern applies to future work (not a one-off fix) |
| Trigger clarity | You can define clear conditions for when it applies |

Do NOT extract:
- One-off investigations (document as analysis files instead)
- Trivial patterns (< 50 tokens — just put in a rule)
- Highly volatile patterns that change every phase

## Extraction Steps

### 1. Identify the Pattern

Search for recurring themes in:
- `WORK_LOG.md` lessons-learned sections
- `.cursor/rules/` for rules that started as repeated advice
- Agent chat transcripts (if accessible)
- Plan files that repeat the same setup instructions

### 2. Define the Scope

Answer these questions:
- **What** does the skill teach the agent to do?
- **When** should it trigger? (List 5-10 realistic user queries)
- **What files** does it need to read?
- **What actions** does it produce?
- **What mistakes** does it prevent?

### 3. Write the SKILL.md

Follow this structure:

```markdown
---
name: [kebab-case-name]
description: "[< 1024 chars: WHAT + WHEN + trigger keywords]"
metadata:
  author: [team-or-framework]
  version: "1.0.0"
  tier: [portable | domain]
---

# [Skill Title]

## Purpose
[Why this skill exists — what problem it solves]

## [Core Instruction Sections]
[The actual skill content — procedures, rules, tables, examples]

## References
[Links to references/ and assets/ files]
```

### 4. Create Supporting Files

- **`references/`** — Background material, detailed examples, pattern catalogs (50-150 lines each)
- **`assets/`** — Templates, starter configs, sample files
- **`scripts/`** — Automation scripts (optional, only if the skill has executable components)

### 5. Register the Skill

Add an entry to `SKILLS_INDEX.md`:

```markdown
| # | skill-name | tier | COMPLETE | SK-X | [line count] |
```

## Validation Checklist

Before considering a skill complete:

- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] `name` field matches the directory name
- [ ] `description` is < 1024 characters
- [ ] `description` includes WHAT, WHEN, and trigger keywords
- [ ] SKILL.md body is < 500 lines
- [ ] All referenced files in `references/` and `assets/` exist
- [ ] No hardcoded project-specific paths in portable-tier skills
- [ ] Tested with 5+ realistic queries — skill triggers correctly

## Description Optimization Loop

The description determines trigger accuracy. Iterate until satisfied:

1. **Draft** — Write initial description covering what, when, and keywords
2. **Test** — Try 10 queries: 5 that should trigger, 5 that should not
3. **Measure** — Count true positives, false positives, false negatives
4. **Refine** — Add missed trigger phrases; remove terms causing false triggers
5. **Repeat** — Until ≥ 80% of target queries trigger correctly

### Common Refinements

| Issue | Fix |
|-------|-----|
| Doesn't trigger on "update the backlog" | Add "update" and "backlog" as trigger phrases |
| Triggers on "update the README" | Make trigger more specific: "update backlog" not just "update" |
| Doesn't trigger on questions | Add question forms: "what is pending", "what's deferred" |
| Triggers too broadly | Replace abstract nouns with concrete terms |

## Tier Classification

| Tier | Criteria | Reference Scope |
|------|----------|-----------------|
| **Portable** | Works in any workspace. No domain-specific terms. | Generic software development examples |
| **Domain** | References project-specific knowledge files, indexes, or tools | Can reference `docs/_ai_context/knowledge/` etc. |

Portable skills must never mention project-specific entities, tools, or file paths. Use generic examples (user auth, product catalog, payment processing).

---
name: prompt-optimization
description: "Optimize agent prompts, plan structures, skill descriptions, and AI workflow efficiency. Use when improving prompt quality, reducing context waste, designing session initializers, refining skill trigger accuracy, or extracting reusable patterns from agent sessions. Triggers on: prompt improvement, workflow optimization, 'make this more efficient', context window management, skill description tuning, or prompt engineering."
metadata:
  author: mdd-framework
  version: "1.0.0"
  tier: portable
---

# Prompt & Plan Optimization

## Purpose

Prompts, plans, and skills degrade over time. Descriptions become too narrow (skills don't trigger when they should) or too broad (irrelevant context loaded every turn). Plans accumulate assumptions from prior sessions that no longer hold. Rules grow until they consume the context window.

This skill provides systematic techniques for keeping AI-assisted workflows efficient, accurate, and maintainable.

## Progressive Disclosure Budgeting

AI context windows are finite. Every token loaded is a token unavailable for reasoning. Structure content in three tiers:

### Tier 1: Discovery (~100 tokens per skill)
- **What:** Skill name + description field
- **When loaded:** Every turn, automatically
- **Budget discipline:** Description must be < 1024 characters. Include WHAT it does AND WHEN to use it.

### Tier 2: Activation (< 5,000 tokens per skill)
- **What:** Full SKILL.md body
- **When loaded:** Only when the skill is triggered by a matching user query
- **Budget discipline:** SKILL.md must be < 500 lines. Move reference material to `references/`.

### Tier 3: Execution (on-demand)
- **What:** `references/`, `assets/`, `scripts/` directories
- **When loaded:** Only when the skill body explicitly instructs the agent to read them
- **Budget discipline:** No limit, but each file should be self-contained.

### Token Budget Audit

Periodically audit your context spend:

1. Count always-on rules (`.cursor/rules/*.mdc` with `alwaysApply: true`)
2. Estimate tokens: ~4 chars per token for English prose
3. If always-on rules exceed 10,000 tokens, convert lower-priority rules to on-demand skills
4. If a skill's SKILL.md exceeds 300 lines, split reference material into `references/`

## Skill Description Optimization

The description field is the most important 1024 characters in a skill. It determines whether the skill triggers.

### Writing Effective Descriptions

**Include:**
- WHAT the skill does (concrete capabilities)
- WHEN to use it (specific scenarios and trigger conditions)
- Trigger keywords (exact phrases users might say)

**Be "pushy"** — list specific scenarios rather than abstract categories:

| Bad | Good |
|-----|------|
| "Helps with data files" | "Verify CSV column headers, JSON field existence, and dataclass schemas before writing parsing code. Use when code reads CSV files, accesses JSON fields, or extends data structures." |
| "Project management" | "Maintain prioritized backlogs with aging enforcement. Use when tracking deferred work, managing P0/P1/P2 priorities, or grooming task lists." |
| "Code quality" | "Run linting, type checking, and test suites. Use when verifying code changes, checking for regressions, or validating before commit." |

### Description Optimization Loop

1. **Write** an initial description
2. **Test** with 5-10 realistic user queries that should trigger it
3. **Measure** — did the skill activate for all relevant queries?
4. **Refine** — add missed trigger phrases, remove overly broad terms
5. **Repeat** until trigger accuracy is satisfactory

### Common Description Failures

| Problem | Symptom | Fix |
|---------|---------|-----|
| Too narrow | Skill never triggers | Add more trigger phrases and scenarios |
| Too broad | Skill triggers on unrelated queries | Replace abstract terms with specific ones |
| Missing verbs | Misses action-oriented queries | Add "Use when [verb]ing..." phrases |
| Missing nouns | Misses topic-oriented queries | Add key entity names and file types |

## Prompt Quality Checklist

Apply this checklist to any prompt, plan, or phase spec:

### Self-Containment
- [ ] Can be executed in a fresh session with zero prior context?
- [ ] All file paths are explicit (no "the config file" — say which one)?
- [ ] All metrics include current baseline values?
- [ ] No references to "as discussed" or "from our conversation"?

### Specificity
- [ ] Code changes include before/after snippets with file paths and line numbers?
- [ ] Validation commands are copy-pasteable (not pseudocode)?
- [ ] Environment setup (env vars, dependencies, paths) is documented?

### Completeness
- [ ] Every step has a verification command or expected output?
- [ ] Error handling: what to do if a step fails?
- [ ] Completion criteria: how does the agent know it's done?

### Efficiency
- [ ] Only loads context that's actually needed for the task?
- [ ] Large files are read by section, not loaded entirely?
- [ ] Reuses existing capabilities instead of re-implementing?

## Context Window Optimization

### Measuring Current Spend

Estimate your always-on context:
1. Sum the line counts of all `alwaysApply: true` rules
2. Add the user rules section
3. Add all skill descriptions (discovery tier)
4. Multiply total lines by ~10 tokens/line for a rough estimate

### Reducing Waste

| Strategy | When to Use | Savings |
|----------|------------|---------|
| Convert always-on rule to skill | Rule applies to < 30% of sessions | 100% of rule tokens when not triggered |
| Split large rule into core + reference | Rule > 100 lines | 50-70% moved to on-demand |
| Merge redundant rules | Two rules cover overlapping concerns | Eliminate duplication |
| Move examples to references | Skill body has > 5 examples | 30-50% of body moved to Tier 3 |
| Shorten description | Description > 800 chars with filler | Faster parsing, same trigger accuracy |

### Identifying Waste

Signs that context is being wasted:
- Always-on rules that only apply during specific phases
- Skill descriptions longer than 1024 characters
- Rules that repeat information available in skills
- Large file reads when only a few lines are needed
- Loading manifests/indexes that aren't used in the current task

## Pattern Extraction into Skills

When a pattern appears **3 or more times** across sessions, extract it into a reusable skill.

### Extraction Criteria

Extract when ALL of these are true:
- Pattern has appeared in 3+ sessions
- Pattern involves significant context (> 50 tokens of instructions)
- Pattern is repeatable (not a one-off investigation)
- Pattern has clear trigger conditions

### Extraction Process

See `references/skill-extraction.md` for the detailed process.

### Skill Structure Quick Reference

```
.cursor/skills/[skill-name]/
├── SKILL.md              # < 500 lines, instructions only
├── references/            # Supporting docs (50-150 lines each)
│   ├── pattern-catalog.md
│   └── examples.md
├── assets/                # Templates, configs
│   └── template.md
└── scripts/               # Automation scripts (optional)
```

**SKILL.md requirements:**
- YAML frontmatter with `name`, `description`, `metadata`
- `description` < 1024 characters
- Body < 500 lines
- Imperative tone ("Do X", not "You should do X")
- Explain why, not just what
- Generic examples (no project-specific references in portable skills)

## Prompt Patterns

Common effective prompt patterns for AI-assisted development are documented in `references/prompt-patterns.md`.

## References

- Skill extraction process: `references/skill-extraction.md`
- Effective prompt patterns: `references/prompt-patterns.md`

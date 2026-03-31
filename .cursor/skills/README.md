---
name: mdd-skills-framework
description: "9 portable MDD methodology skills following the Anthropic Agent Skills spec."
metadata:
  author: mdd-framework
  version: "1.0.0"
  spec: "agentskills.io v1.0"
---

# MDD Skills Framework

> **MDD_ROOT = docs/_ai_context**
>
> All path references in these skills use `docs/_ai_context/` as the default root.
> To change it, run: `.cursor/skills/scripts/set-mdd-root.sh "your/path/"`

A collection of 9 portable skills packaged to the [Anthropic Agent Skills specification](https://agentskills.io/specification).
Each skill is self-contained in its own folder with a `SKILL.md` file plus optional `references/` and `assets/`.

## Tier 1: Portable Skills (Generic MDD Methodology)

These skills work in **any** workspace. They encode the Markdown-Driven Development methodology.

| Skill | Purpose | Key Innovation |
|-------|---------|---------------|
| mdd-workflow | Core MDD: P-R-I-L, authority hierarchy, governance | Constitutional truth precedence |
| plan-generation | Self-contained plan writing with quality gates | "Zero prior context" principle |
| phase-execution | Multi-phase execution with validation gates | Context-independent handoffs |
| data-verification | Verify data schemas before writing parsing code | Silent failure prevention |
| context-loading | Efficient AI context loading via manifests | Sniper mode: manifest-first |
| knowledge-repo | Canonical knowledge management with governance | Staging → promotion → versioning |
| backlog-management | Prioritized backlog with aging enforcement | P0 can't defer; P1 escalates after 2 phases |
| work-logging | Structured work logging with lessons learned | Regression risk classification |
| prompt-optimization | Prompt, plan, and workflow optimization | Progressive disclosure budgeting |

## Customization

### Changing MDD_ROOT

The default directory for all MDD files is `docs/_ai_context/`. To use a different path:

```bash
.cursor/skills/scripts/set-mdd-root.sh "your/custom/path/"
```

This updates all `docs/_ai_context/` path references across skill files in one command.

## Installation

- **Cursor**: Skills in `.cursor/skills/` are auto-discovered
- **Claude Code**: Copy to `.claude/skills/` for Claude Code compatibility
- **Claude.ai**: Upload individual SKILL.md files as custom skills
- **Claude API**: Provide skill folder paths to your agent runtime

## Spec Compliance

All skills follow the [Agent Skills Specification](https://agentskills.io/specification):
- YAML frontmatter with `name` and `description`
- Directory name matches `name` field
- SKILL.md < 500 lines; detailed content in `references/`
- Progressive disclosure: Discovery → Activation → Execution

---
document_type: PROMPT
status: ACTIVE
purpose: "Replace the slim 01-mdd.mdc router with a fat router that preserves behavioral guardrails while delegating procedural details to skills"
target_repo: "cursor-workspace-template"
estimated_duration: "30 minutes"
supersedes: "The slim router created by TEMPLATE_REPO_SKILLS_INTEGRATION_PROMPT.md"
---

# Fat Router: Replace Slim `01-mdd.mdc` With Behavioral-Floor Version

## Background — What Happened and Why This Change Is Needed

### The Original State

The template repo had a `01-mdd.mdc` file (~600 lines) as an always-applied Cursor rule
(`alwaysApply: true`). This file contained the entire MDD Protocol V1.3 — authority hierarchy,
P-R-I-L workflow, complexity triage, operational modes, governance rules, archival rules,
git conventions, directory structure, critical feedback requirements, and more.

**Cost:** ~8,000 tokens injected into every single agent turn, regardless of task.
**Benefit:** Every behavioral constraint was always visible to the agent. No methodology
rule could be accidentally skipped.

### What Was Changed

As part of a skills integration effort, 9 portable MDD skills were created in
`.cursor/skills/`. These skills encode the same methodology in Anthropic Agent Skills format
with progressive disclosure (loaded on-demand, not always-on).

The `01-mdd.mdc` was slimmed down to a ~80-line "router" that just said:
"For X, use skill Y." The original was archived to
`docs/_ai_context/analysis/archive/01-mdd-v1.3-full.mdc`.

### The Problem With the Slim Router

The slim router is **too aggressive**. It traded behavioral safety for token savings.

**Cursor skills are NOT always-loaded.** They activate only when the agent recognizes a
match between the user's request and the skill description. This is a judgment call — and
when it fails, the methodology is invisible. Specifically:

1. **Skills don't activate for implicit methodology.** If the user says "fix this bug," no
   skill triggers. The agent won't know to follow P-R-I-L, won't load context via manifests,
   and won't check the backlog — because nothing in "fix this bug" matches a skill trigger.

2. **Behavioral constraints become optional.** The full MDD rule had hard prohibitions
   ("never guess file paths," "never skip validation"). With the slim router, these only
   apply if the agent happens to load the `mdd-workflow` skill — which it won't for most
   routine tasks.

3. **Cold start fails.** A new agent session in a new workspace: the agent has no context.
   With the full rule, it immediately knows "load repo-manifest.json first." With the slim
   router, it might just dive into code, skipping the context loading protocol entirely.

4. **Cascading ignorance.** If `context-loading` doesn't trigger → agent doesn't find
   `MASTER_STATE.md` → doesn't learn about authority hierarchy → makes decisions that
   contradict the knowledge repo. Each missed activation compounds.

### The Solution: Fat Router

Keep the behavioral floor in the always-applied rule. Delegate procedural details to skills.

**Key insight:** Rules enforce behavior. Skills provide procedures. The slim router tried
to push behavior into skills, and behavior doesn't belong there because skill activation
is voluntary.

The fat router is ~180 lines (~2,000 tokens). This is a 75% reduction from the original
(~8,000 tokens) while preserving 95% of the behavioral safety.

### What Goes in the Fat Router (always enforced)

| Content | Why It Must Be Always-On |
|---------|-------------------------|
| Authority hierarchy | Prevents agents from contradicting canonical knowledge |
| Context loading protocol | Prevents cold-start failures — must happen every session |
| P-R-I-L requirement | Core workflow — must apply to all non-trivial work |
| Complexity triage | Determines whether a plan is needed — must be evaluated early |
| Hard prohibitions | "Never guess paths," "never skip validation" — must always apply |
| Required actions | "Search before code," "validate output" — behavioral floor |
| Critical feedback | Honest self-assessment — must apply to every meaningful action |
| Directory convention | MDD_ROOT definition — agents must know the layout always |
| Skill activation table | Routing to on-demand details — the router's primary job |

### What Stays in Skills Only (loaded on-demand)

| Content | Why It's OK as On-Demand |
|---------|------------------------|
| Detailed plan templates | Only needed when actually writing plans |
| Full governance rules with examples | Only needed during governance discussions |
| Archival procedures | Only needed when archiving files |
| Git convention details | Only needed at commit time |
| Work log templates | Only needed when logging work |
| Data verification procedures | Only needed when writing data parsing code |
| Knowledge repo governance | Only needed when managing knowledge files |
| Lessons-learned structure | Only needed when documenting lessons |
| Backlog grooming details | Only needed when managing the backlog |

---

## Task: Replace the Slim Router

### Step 1: Verify Current State

First, confirm the current state of `01-mdd.mdc`:

```bash
wc -l .cursor/rules/01-mdd.mdc
head -5 .cursor/rules/01-mdd.mdc
```

If it's ~80 lines (the slim router), proceed. If it's already ~600 lines (the original),
skip this entire prompt — the revert already happened.

Also verify the archive exists:

```bash
ls -la docs/_ai_context/analysis/archive/01-mdd-v1.3-full.mdc
```

If the archive does NOT exist, check if the original content is still in `01-mdd.mdc`
(i.e., the slim router was never applied). Adapt accordingly.

### Step 2: Replace `01-mdd.mdc` With the Fat Router

Replace the entire contents of `.cursor/rules/01-mdd.mdc` with the following.
This is the complete, final content — write it exactly as specified.

---

**BEGIN FILE: `.cursor/rules/01-mdd.mdc`**

```
---
description: "MDD Protocol — Always-on behavioral floor with skill routing for detailed procedures. Enforces authority hierarchy, P-R-I-L workflow, context loading, and governance constraints. Delegates procedural details to .cursor/skills/."
globs: "**/*"
alwaysApply: true
---

# MDD Protocol (Behavioral Floor + Skill Router)

This workspace uses **Markdown-Driven Development (MDD)**: structured documentation as a
first-class engineering artifact. AI agents lose context between sessions — MDD documentation
IS the context. Plans, state files, and knowledge repos persist what agents need across sessions.

> **MDD_ROOT = `docs/_ai_context`** — All MDD files live under this path.
> Change it with: `.cursor/skills/scripts/set-mdd-root.sh "your/path/"`

---

## 1. Authority Hierarchy (Non-Negotiable)

When sources conflict, higher rank wins. This is constitutional — no exception.

| Rank | Source | Location | Rule |
|------|--------|----------|------|
| 1 | Knowledge Repository | `docs/_ai_context/knowledge/` | Canonical domain truth — human approval to change |
| 2 | State Files | `docs/_ai_context/state/` | Current execution state — read before modifying |
| 3 | Manifests & Indexes | `repo-manifest.json`, `CONTEXT_MANIFEST.md` | Navigation only — points to truth, doesn't define it |
| 4 | Rules & Skills | `.cursor/rules/`, `.cursor/skills/` | Behavioral guidance — overridden by ranks 1-3 |

If a skill says "term X means Y" but a knowledge file says "term X means Z," the knowledge file wins.

---

## 2. Context Loading (Mandatory First Step)

**Every session MUST begin with context loading.** Do not answer questions or write code
until you have loaded the minimum context for the task.

| Priority | File | When to Read |
|----------|------|-------------|
| 1 | `docs/_ai_context/state/repo-manifest.json` | Every session — file/function lookup |
| 2 | `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` | Every session — project identity |
| 3 | `docs/_ai_context/state/MASTER_STATE.md` | When implementing or investigating |
| 4 | Target-specific files (on-demand) | Only what the current task needs |

**Rules:**
- NEVER read files over 500 lines without targeting a specific section
- NEVER guess file paths — use the manifest or search tools
- NEVER reinvent functionality — check existing capabilities first

For the full context loading protocol: read `.cursor/skills/context-loading/SKILL.md`

---

## 3. P-R-I-L Workflow (Required for Non-Trivial Work)

Every non-trivial change follows **Plan → Review → Implement → Log**.

| Step | What Happens | Artifact |
|------|-------------|----------|
| **Plan** | Write a plan document appropriate to complexity | See triage below |
| **Review** | Human checkpoint before implementation | Explicit approval for complex work |
| **Implement** | Atomic changes scoped strictly to the plan | No scope creep |
| **Log** | Update WORK_LOG.md, commit, create completion doc | Institutional memory |

Skip P-R-I-L only for truly trivial changes (typo fixes, single-line config updates).

---

## 4. Complexity Triage (Assess Before Starting)

| Complexity | Criteria | Required Artifact |
|------------|----------|-------------------|
| **Simple** | 1-2 steps, < 30 min | No formal plan |
| **Medium** | 3-5 steps, < 2 hrs | Analysis file in `docs/_ai_context/analysis/` |
| **Complex** | 6+ steps, 2+ hrs, validation gates | Phase plan in `docs/_ai_context/prompts/phases/` |

**Quick rule:** > 2 hours OR > 5 steps OR intermediate validation needed → multi-phase plan.
Jumping to code for a complex task without a plan is a governance violation.

For plan writing: read `.cursor/skills/plan-generation/SKILL.md`
For phase execution: read `.cursor/skills/phase-execution/SKILL.md`

---

## 5. Behavioral Constraints (Always Enforced)

### Prohibited

- Do NOT guess file paths — use the manifest or search tools
- Do NOT skip validation gates — run every validation command before declaring done
- Do NOT create scripts/modules without searching for existing ones (code reuse mandate)
- Do NOT modify knowledge repository files without human approval (Rank 1 authority)
- Do NOT leave MDD documentation inconsistent after changes
- Do NOT bypass completion gates on phase work
- Do NOT use `except: pass` or silent fallbacks on critical paths
- Do NOT claim checks passed without actually running them

### Required

- ALWAYS search the codebase before writing new code
- ALWAYS validate output before declaring done
- ALWAYS update MDD docs (WORK_LOG, BACKLOG, state) after non-trivial changes
- ALWAYS follow P-R-I-L for non-trivial work
- ALWAYS use manifest or search for file navigation
- ALWAYS verify data schemas before writing parsing code (CSV: use `utf-8-sig` encoding)
- ALWAYS log lessons learned after non-trivial work

---

## 6. Critical Feedback (Before Any Meaningful Action)

Before any meaningful action, include honest self-assessment:

1. **Flaws & Risks** — Quantify blast radius. Name one alternative and its trade-off.
2. **Self-critique** — What is the weakest part of this approach? How could it fail?
3. **Self-verification** — Run tests/validation if they exist. Record results.

No flattery. Direct and terse. If skipping verification, flag explicitly and explain why.

---

## 7. MDD Directory Structure

```
docs/_ai_context/
├── state/              # MASTER_STATE, WORK_LOG, BACKLOG, indexes
├── analysis/           # Plans, debug logs, completion docs
│   └── archive/        # Superseded files (never delete, always move)
├── prompts/            # Reusable prompts, workflow templates
│   └── phases/         # Phase plans (PHASE_XX_NAME.md)
├── knowledge/          # Canonical domain knowledge (Rank 1 authority)
│   └── reference/      # Taxonomies, catalogs, schemas
└── templates/          # Standardized output templates
```

---

## 8. Skill Activation (On-Demand Deep Dives)

For detailed procedures, templates, and scripts, activate the relevant skill:

| When you need to... | Read this skill |
|---------------------|----------------|
| Set up a project with MDD, understand governance details | `mdd-workflow` |
| Write a self-contained plan or phase spec | `plan-generation` |
| Execute a plan file with pre-flight checks | `phase-execution` |
| Write code that parses CSV, JSON, or extends data structures | `data-verification` |
| Optimize context loading or create manifests | `context-loading` |
| Create or govern a knowledge repository | `knowledge-repo` |
| Track deferred work, groom priorities | `backlog-management` |
| Log completed work with lessons learned | `work-logging` |
| Improve prompts, plans, or skill descriptions | `prompt-optimization` |

Skills live in `.cursor/skills/[name]/SKILL.md`. Read the SKILL.md file to activate.

---

## 9. Deferred Work

Any discovered work that is out of current scope must go to `docs/_ai_context/state/BACKLOG.md`:
- Format: `- [ ] [P1] Title – description. (source: <origin>).`
- Priorities: P0 (blocking), P1 (next sprint), P2 (backlog), P3 (wishlist)
- P0 items block the current phase. P1 items escalate to P0 after 2 phases.

For backlog grooming and aging rules: read `.cursor/skills/backlog-management/SKILL.md`
```

**END FILE**

---

### Step 3: Verify the Fat Router

Run these checks:

```bash
# Line count should be ~180 (between 160 and 200)
wc -l .cursor/rules/01-mdd.mdc

# Should have alwaysApply: true in frontmatter
head -5 .cursor/rules/01-mdd.mdc

# Should reference all 9 skills
grep -c "\.cursor/skills/" .cursor/rules/01-mdd.mdc
# Expected: 11-13 references (9 skill names + a few path references)

# Should contain all behavioral keywords
for keyword in "Authority Hierarchy" "P-R-I-L" "Complexity Triage" "Prohibited" "Required" \
               "Critical Feedback" "Context Loading" "MDD_ROOT" "BACKLOG"; do
  grep -q "$keyword" .cursor/rules/01-mdd.mdc && echo "PASS: $keyword" || echo "FAIL: $keyword"
done

# Token estimate (rough: lines × 10 tokens/line)
lines=$(wc -l < .cursor/rules/01-mdd.mdc)
echo "Estimated tokens: $((lines * 10)) (target: ~1800, max: 2500)"
```

### Step 4: Verify the Archive Still Exists

```bash
# The original full MDD should still be in the archive
wc -l docs/_ai_context/analysis/archive/01-mdd-v1.3-full.mdc
# Expected: ~600 lines

# If it doesn't exist, no action needed — the full original was never archived
# (meaning the slim router prompt may not have been fully executed)
```

### Step 5: Commit

```bash
git add .cursor/rules/01-mdd.mdc
git commit -m "$(cat <<'EOF'
fix(rules): Replace slim 01-mdd.mdc router with fat router

The slim router (~80 lines) delegated all MDD methodology to on-demand
skills, but Cursor skills only activate when the agent recognizes a match.
This left behavioral constraints (authority hierarchy, P-R-I-L, context
loading, prohibitions) unenforceable for routine tasks.

The fat router (~180 lines, ~2K tokens) keeps the behavioral floor
always-on while still delegating procedural details to skills. This is
75% fewer tokens than the original (~8K) with 95% behavioral safety.

What's always enforced: authority hierarchy, context loading protocol,
P-R-I-L workflow, complexity triage, prohibitions, required actions,
critical feedback, directory convention, skill routing.

What's on-demand (via skills): plan templates, governance details,
archival procedures, git conventions, data verification procedures,
work log templates, backlog grooming, knowledge repo governance.
EOF
)"
```

---

## Summary of the Change

| Metric | Original (V1.3) | Slim Router | Fat Router (this change) |
|--------|-----------------|-------------|--------------------------|
| Lines | ~600 | ~80 | ~180 |
| Tokens (est.) | ~8,000 | ~800 | ~2,000 |
| Authority hierarchy | Always on | On-demand (via skill) | Always on |
| Context loading | Always on | On-demand (via skill) | Always on |
| P-R-I-L enforcement | Always on | On-demand (via skill) | Always on |
| Prohibitions | Always on | On-demand (via skill) | Always on |
| Critical feedback | Always on | On-demand (via skill) | Always on |
| Plan templates | Always on | On-demand (via skill) | On-demand (via skill) |
| Governance details | Always on | On-demand (via skill) | On-demand (via skill) |
| Git conventions | Always on | On-demand (via skill) | On-demand (via skill) |
| Data verification | Always on | On-demand (via skill) | On-demand (via skill) |
| Token reduction vs original | — | 90% | 75% |
| Behavioral safety vs original | — | ~40% | ~95% |

The fat router is the pragmatic middle ground: cheap enough to be always-on,
comprehensive enough that no behavioral constraint is left to voluntary activation.

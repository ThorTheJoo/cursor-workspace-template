# Context Manifest — {PROJECT_NAME}

## 1. Project Identity

| Field | Value |
|-------|-------|
| Project | {project name} |
| Purpose | {one-sentence description} |
| Current Phase | {phase number and name} |
| Config Version | {current config version} |

## 2. Authority Hierarchy

| Rank | Source | Location |
|------|--------|----------|
| 1 | Knowledge Repository | `docs/_ai_context/knowledge/` |
| 2 | State Files | `docs/_ai_context/state/` |
| 3 | Manifests | `repo-manifest.json`, this file |
| 4 | Rules & Skills | `.cursor/rules/`, `.cursor/skills/` |

## 3. Agent Prompt Contract

Before executing any phase:
- [ ] Read MASTER_STATE.md for current project state
- [ ] Check WORK_LOG.md for recent changes
- [ ] Verify prerequisites from `depends_on` exist
- [ ] Load any required configuration or dependencies

After completing any phase:
- [ ] Update PHASES_INDEX.md (status → COMPLETE)
- [ ] Update WORK_LOG.md with changes
- [ ] Create completion doc
- [ ] Run project tests
- [ ] Commit with conventional prefix
- [ ] Append deferred items to BACKLOG.md

## 4. Key Metrics

| Metric | Current Value | Target | Status |
|--------|:------------:|:------:|:------:|
| {metric 1} | {value} | {target} | {status} |
| {metric 2} | {value} | {target} | {status} |

## 5. Capability Index

| Capability | Command | Status |
|-----------|---------|--------|
| {capability 1} | `{command}` | {status} |
| {capability 2} | `{command}` | {status} |

## 6. Phase Table

| Phase | Name | Status | Key Output |
|-------|------|--------|-----------|
| {N} | {name} | {status} | {output path} |

## 7. Quick Commands

```bash
# {Common command 1}
{command}

# {Common command 2}
{command}
```

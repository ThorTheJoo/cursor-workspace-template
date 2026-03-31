---
document_type: MANIFEST
status: ACTIVE
version: 1.0.0
generated: "[YYYY-MM-DD]"
reviewer:
  accountable: "[Your Team or Role]"
compliance_tags: ["MDD", "Agent-Workflow", "Navigation"]
---

# CONTEXT MANIFEST
## [PROJECT_NAME]

---

## 1. PROJECT IDENTITY

**Repository:** `[path/to/your/repo]`
**Git Status:** [e.g., main branch, tracking origin/main]
**Purpose:** [One-line project purpose]

**Current Phase:** [e.g., Phase 3 - Integration Testing]

**Core Objective:**
[2-3 sentences describing the main deliverables and outcomes.]

---

## 2. CONSTITUTION (Authority Hierarchy)

### Authoritative Sources (Read Order)
1. **Knowledge Repository** = Single Source of Truth
   - Path: `docs/_ai_context/knowledge/`
   - Contains: Taxonomies, glossaries, canonical reference data
   - **Rule:** NEVER redefine terms that exist here

2. **State Files** = Current Execution State
   - Path: `docs/_ai_context/state/`
   - Contains: MASTER_STATE, WORK_LOG, BACKLOG, indexes
   - **Rule:** Read before modifying

3. **This Manifest** = Navigation Index
   - **Rule:** Points to truth, does NOT define truth

### Non-Negotiable Constraints
- Knowledge repository is constituted authority (domain truth)
- MDD documentation is ephemeral project state
- Human-in-the-loop for knowledge repository updates
- Config files over hardcoded values

---

## 3. AGENT PROMPT CONTRACT

### Before Starting Work
- [ ] Read `docs/_ai_context/state/MASTER_STATE.md`
- [ ] Check `docs/_ai_context/state/WORK_LOG.md` for recent changes
- [ ] Verify prerequisites for current phase exist

### During Execution
- [ ] Use project-specific validators as documented
- [ ] Never hardcode what should come from config/YAML
- [ ] Follow P-R-I-L workflow for non-trivial changes

### After Completion
- [ ] Update PHASES_INDEX.md (set phase status to COMPLETE)
- [ ] Update WORK_LOG.md with changes
- [ ] Create completion doc in `docs/_ai_context/analysis/`
- [ ] Run validation: `[YOUR_TEST_COMMAND]`
- [ ] Commit with conventional prefix: `feat(scope): summary`
- [ ] Append deferred work to `docs/_ai_context/state/BACKLOG.md`

---

## 4. CURRENT STATE (Achieved Metrics)

| Metric | Baseline | Target | Achieved | Status |
|--------|----------|--------|----------|--------|
| [YOUR_METRIC_1] | [value] | [value] | [value] | [status] |
| [YOUR_METRIC_2] | [value] | [value] | [value] | [status] |

---

## 5. CAPABILITY INDEX

| Capability | Command | Output |
|------------|---------|--------|
| Run tests | `[YOUR_TEST_COMMAND]` | Test results |
| Lint code | `[YOUR_LINT_COMMAND]` | Lint report |
| Build | `[YOUR_BUILD_COMMAND]` | Build artifacts |

---

## 6. PHASE COMPLETION STATUS

| Phase | Name | Status | Key Deliverable | Validation |
|-------|------|--------|-----------------|------------|
| 1 | [Phase name] | [status] | [deliverable] | [criteria] |
| 2 | [Phase name] | [status] | [deliverable] | [criteria] |

---

## 7. FILE INDEX (Quick Reference)

### Core Scripts
| Concern | File | Purpose |
|---------|------|---------|
| [concern] | `path/to/script` | [purpose] |

### Knowledge Repository
| File | Path | Purpose |
|------|------|---------|
| [name] | `docs/_ai_context/knowledge/[file]` | [purpose] |

### State Files
| File | Path | Purpose |
|------|------|---------|
| Repo Manifest | `docs/_ai_context/state/repo-manifest.json` | Machine-readable index |
| Backlog | `docs/_ai_context/state/BACKLOG.md` | Deferred work items |
| Work Log | `docs/_ai_context/state/WORK_LOG.md` | Change history |

---

## 8. QUICK COMMANDS REFERENCE

```bash
# Run tests
[YOUR_TEST_COMMAND]

# Check status
[YOUR_STATUS_COMMAND]
```

---

## 9. TROUBLESHOOTING POINTERS

| Issue | Where to Look |
|-------|---------------|
| [common issue] | [file or command] |

---

## 10. META

- **Document Version:** 1.0.0
- **Generated:** [YYYY-MM-DD]
- **Machine-Readable Index:** `docs/_ai_context/state/repo-manifest.json`

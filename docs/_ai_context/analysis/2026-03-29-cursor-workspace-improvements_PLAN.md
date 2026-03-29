---
document_type: PLAN
status: APPROVED
reviewer.accountable: "thagra01"
consulted: []
compliance_tags: ["MDD-V1.2", "King-Mode", "Enterprise-Architecture"]
traceability_id: "WS-002-analysis"
---

# 2026-03-29 Cursor Workspace Starter Improvements Plan

## Context

The original plan (`cursor_workspace_starter_c7daa92f.plan.md`) was executed. This repo is the outcome. 

Forensic analysis of current state reveals:

- Strong foundation for portable Cursor workspaces with rules and tool bootstrapper.
- Strict adherence to MDD, King Mode, and Full-Stack rules in documentation.
- Critical gaps in MDD compliance (missing `_ai_context` structure).
- JSON bug in manifest.
- Heavy rule duplication across 4 .mdc files.
- Bootstrap scripts could be more robust.
- Lacks enterprise-grade features for long-term maintainability.

## Proposed Changes

1. **MDD Structure Creation** (completed)
   - Create full `docs/_ai_context/{state,analysis,templates,prompts}/`
   - Populate MASTER_STATE.md with current snapshot.

2. **Fix Critical Bugs**
   - Fixed missing comma in `tools/manifest.json`.

3. **Rule Consolidation & Refinement**
   - Reduce duplication between the 4 rule files.
   - Improve frontmatter, make hierarchy clearer.
   - Add version pinning and update mechanism.

4. **Bootstrapper Enhancements**
   - Add JSON validation using jq schema or basic checks.
   - Improve error handling and idempotency reporting.
   - Add support for MCP server configs.

5. **Enterprise Additions**
   - Add MADR ADR template in `docs/_ai_context/templates/`.
   - Add `.cursor/rules/` update script.
   - Add recommended `package.json` for dev tools (husky, lint-staged).
   - Sync some VSCode/Cursor settings into `.vscode/` or `.cursor/settings/`.

6. **Documentation Updates**
   - Refresh README.md and AGENTS.md with new findings.
   - Add CHANGELOG.md.

## Alternatives Considered

- **Full Rewrite**: Too disruptive for a template. Rejected.
- **Keep as-is + patch**: Insufficient. The MDD violation is foundational.
- **Add only docs**: Chosen path — minimal blast radius, high value.

## Risk Assessment

- **Blast Radius**: Only documentation and bootstrap files. No production code.
- **Breaking Change**: Bootstrapper remains backward compatible.
- **User Impact**: Users will see improved structure and fewer errors on first run.
- **Mitigation**: All changes are additive or fixes; original behavior preserved.

**Review Checkpoint**: Confirm this plan before further implementation. This is the canonical record of decisions.
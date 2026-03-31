# Contributing

## How to Add a New Tool (30 Seconds)

1. Open `tools/manifest.json`.
2. Copy the `_template` object into the `tools` array.
3. Fill in the fields:

```json
{
  "name": "my-tool",
  "repo": "https://github.com/org/my-tool",
  "pinnedRef": "v2.1.0",
  "description": "What this tool does inside Cursor.",
  "installCmd": "npm install -g my-tool-cli",
  "platform": "both",
  "type": "cli",
  "requiresApproval": ["network"],
  "skillScan": false
}
```

4. Run `./setup-tools.sh` (Bash) or `setup-tools.ps1` (Windows).

### Manifest Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique kebab-case identifier |
| `repo` | Yes | Full GitHub HTTPS URL |
| `pinnedRef` | Strongly recommended | Tag (`v1.2.3`) or commit SHA. Unpinned tools trigger a security warning |
| `description` | Yes | What the tool provides |
| `installCmd` | Yes | Shell command run after clone (cwd = cloned repo) |
| `platform` | Yes | `win`, `unix`, or `both` |
| `type` | Yes | `cli`, `skills`, `plugin`, `research`, or `rules` |
| `requiresGpu` | No | `true` if GPU hardware is needed |
| `requiresApproval` | No | Array of capabilities: `shell`, `file:write`, `network`, `secrets` |
| `skillScan` | No | `true` to run `bin/skill-scan.sh` before installation |

### Install Command Allowlist

The bootstrapper validates `installCmd` against a prefix allowlist:
`npm install`, `npm ci`, `pip install`, `uv pip install`, `npx`, `cargo install`, `go install`, `uv sync`, `echo`.

Commands not matching the allowlist will prompt for manual confirmation.

## How to Add a Security Check

1. For **pattern-based scanning**: add patterns to `bin/skill-scan.sh` in the `DANGEROUS_PATTERNS` array.
2. For **secret detection**: add regex patterns to `bin/scan-secrets.sh` in the `SECRET_PATTERNS` array.
3. For **agent behavioral rules**: add directives to `.cursor/rules/04-security-policy.mdc`.
4. Update `SECURITY.md` Quick Reference table with the new control and its status.

## Verified Forks Pattern

For maximum supply chain security, maintain audited forks of critical tools:

1. Fork the upstream repo into your org.
2. Review all code, then tag a release (e.g., `v1.2.3-audited`).
3. In `manifest.json`, point `repo` to your fork and `pinnedRef` to your audited tag.
4. Periodically sync with upstream, review diffs, and cut new audited tags.

This is a **documented pattern**, not enforced infrastructure. Use it when the threat model warrants it.

## Commit Conventions

```
feat(scope): summary of feature
fix(scope): summary of bug fix
docs(scope): documentation update
refactor(scope): code restructuring
```

## Code of Conduct

Be respectful and constructive. Security-related contributions are especially welcome.

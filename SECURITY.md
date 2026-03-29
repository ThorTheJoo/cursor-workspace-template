# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT** open a public GitHub issue for security vulnerabilities.
2. Email: [SECURITY_CONTACT_EMAIL] with details.
3. Include: description, reproduction steps, impact assessment.
4. Expected response time: 48 hours for acknowledgment, 7 days for initial assessment.

## Security Controls

This project implements defense-in-depth security controls documented in:

- **`.gitignore`** -- Blocks 40+ sensitive file patterns from git
- **`.cursor/rules/01-mdd.mdc` Section 7d** -- Agent behavioral security rules (14 controls)
- **`docs/_ai_context/knowledge/governance/SECURITY_CONTROLS.md`** -- Full security policy
- **`docs/_ai_context/knowledge/ANTI_PATTERNS_CATALOG.md`** -- Security anti-patterns (10 patterns)
- **Bootstrapper hardening** -- Install command allowlist + commit pinning

## Quick Reference

| Control | Status |
|---------|--------|
| Secret file patterns in .gitignore | Active |
| Agent secret prevention rules | Active (01-mdd.mdc 7d.1-6) |
| Pre-commit secret scanning | Template provided (see SECURITY_CONTROLS.md 1.4) |
| Supply chain pinning | Supported via manifest `commit` field |
| Install command allowlist | Active in both bootstrappers |
| Security review gates | In all plan/phase/completion templates |
| Continuous improvement security routing | Active (checklist item #7) |
| OWASP Top 10 alignment | Documented in SECURITY_CONTROLS.md Section 4 |

## Dependencies

When adding dependencies:
- Pin exact versions (no `^`, `~`, `*`, or `latest`)
- Run `npm audit` / `pip-audit` before merging
- Commit lock files (`package-lock.json`, `yarn.lock`, etc.)

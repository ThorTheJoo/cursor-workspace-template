---
document_type: GOVERNANCE
status: APPROVED
version: "1.0.0"
date: 2026-03-29
reviewer:
  accountable: "thagra01"
compliance_tags: ["security", "secrets-management", "supply-chain", "OWASP"]
traceability_id: "WS-003-security-hardening"
---

# Security Controls Policy

Reference: MDD V1.3 Section 7d (Security Rules). This document is the detailed security policy for the workspace template. The condensed behavioral rules live in `.cursor/rules/01-mdd.mdc`.

---

## 1. Secret & Credential Management

### 1.1 Prevention Layers (Defense in Depth)

| Layer | Control | Enforcement |
|-------|---------|-------------|
| **L1: .gitignore** | Block known secret file patterns from staging | Automatic (git) |
| **L2: Agent behavioral rules** | AI prohibited from writing secrets into any file | Rule 01-mdd.mdc Section 7d |
| **L3: Pre-commit hook** | Scan staged files for secret patterns before commit | `gitleaks` or `detect-secrets` via husky |
| **L4: CI pipeline** | Server-side secret scanning on push | GitHub Secret Scanning / GitGuardian / TruffleHog |
| **L5: Code review** | Human reviewer checks for hardcoded secrets | PR review checklist |

### 1.2 .gitignore Coverage

The `.gitignore` MUST block at minimum:

| Category | Patterns |
|----------|----------|
| Environment files | `.env`, `.env.local`, `.env.*.local`, `.env.production`, `.env.staging` |
| Private keys | `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `*.cert`, `*.crt` |
| SSH keys | `id_rsa`, `id_rsa.*`, `id_ed25519`, `id_ed25519.*`, `*.gpg` |
| Credential files | `credentials.json`, `serviceAccountKey.json`, `service-account*.json`, `*-credentials.json`, `*.credential` |
| Auth configs | `.htpasswd`, `.netrc`, `.npmrc`, `.pypirc`, `.docker/config.json` |
| Cloud providers | `.aws/credentials`, `.azure/accessTokens.json`, `kubeconfig`, `terraform.tfstate`, `*.tfvars` |

### 1.3 Environment Variable Convention

```
.env.example    <-- Committed. Variable names + descriptions. NO values.
.env            <-- NOT committed. Local overrides with real values.
.env.local      <-- NOT committed. Machine-specific overrides.
.env.production <-- NOT committed. Production values (use vault/CI secrets instead).
```

Template `.env.example` format:
```bash
# Database
DATABASE_URL=                    # PostgreSQL connection string (e.g., postgresql://user:pass@host:5432/db)
DATABASE_POOL_SIZE=10            # Non-sensitive defaults are OK

# Auth
JWT_SECRET=                      # Generate: openssl rand -base64 32
NEXTAUTH_SECRET=                 # Generate: openssl rand -base64 32
NEXTAUTH_URL=http://localhost:3000

# External APIs
STRIPE_SECRET_KEY=               # From https://dashboard.stripe.com/apikeys
STRIPE_PUBLISHABLE_KEY=          # Public key (safe to expose client-side)

# Monitoring (non-sensitive)
SENTRY_DSN=                      # From Sentry project settings
```

### 1.4 Pre-Commit Hook Setup

Recommended tool: `gitleaks` (language-agnostic, fast, low false-positive rate).

```bash
# Install (add to bootstrapper)
npm install --save-dev husky
npx husky init

# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Secret scanning
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks protect --staged --verbose
else
  echo "WARNING: gitleaks not installed. Skipping secret scan."
  echo "Install: https://github.com/gitleaks/gitleaks#installing"
fi
```

Alternative: `.gitleaksrc.toml` for custom rules:
```toml
[allowlist]
description = "Project-specific allowlist"
paths = [
  '''.env\.example''',
  '''docs/_ai_context/templates/.*''',
]
```

### 1.5 Secret Rotation Protocol

When a secret is accidentally committed:

1. **Immediately** rotate the compromised credential at the source (API dashboard, vault, etc.)
2. Do NOT try to rewrite git history in shared repos -- the secret is already exposed
3. Add the secret pattern to `.gitleaksrc.toml` allowlist if it was a false positive
4. Document the incident in `docs/_ai_context/analysis/YYYY-MM-DD_secret-leak_DEBUG.md`
5. Review and tighten `.gitignore` patterns

---

## 2. Agent Security Controls

### 2.1 What Agents Must Never Do

| Control | Rule ID | Rationale |
|---------|---------|-----------|
| Write secrets into source files | 7d.1 | Secrets in code persist in git history permanently |
| Hardcode connection strings | 7d.2 | Credential rotation becomes impossible |
| Generate fake secrets as placeholders | 7d.8 | `sk-xxxx` patterns train developers to ignore real leaks |
| Disable TLS verification | 7d.10 | Opens MITM attack surface |
| Set CORS to wildcard `*` | 7d.10 | Allows any origin to call APIs |
| Skip `--no-verify` on commits | 7d.10 | Bypasses pre-commit secret scanning |
| Log PII or tokens | 7d.4 | Logs are often less protected than source code |

### 2.2 What Agents Must Always Do

| Control | Rule ID | Rationale |
|---------|---------|-----------|
| Use `process.env.VAR` for secrets | 7d.5 | Secrets come from environment, not code |
| Sanitize user input (Zod/DOMPurify) | 7d.9 | Prevents XSS, injection attacks |
| State threat model for auth code | 7d.7 | Forces security thinking before implementation |
| Check CVEs for new dependencies | 7d.11 | Prevents shipping known vulnerabilities |
| Pin dependency versions | 7d.13 | Prevents supply chain attacks via version hijacking |

### 2.3 Security Review Gate

Any plan or phase that touches the following domains MUST include a security checklist:

| Domain | Trigger |
|--------|---------|
| Authentication / Authorization | Login, signup, role checks, session management |
| Cryptography | Encryption, hashing, token generation, key management |
| User Data / PII | Forms, profiles, data export, analytics |
| External APIs | Third-party integrations, webhook receivers |
| File Upload / Download | User-submitted content, document processing |
| Database Queries | Raw SQL, ORM queries with user input |
| Infrastructure | Docker, CI/CD, deployment configs, env vars |

**Security Checklist (embed in plan/phase):**
```markdown
## Security Review
- [ ] No secrets hardcoded in source
- [ ] User input validated and sanitized
- [ ] Auth checks on all protected routes/procedures
- [ ] Error messages don't leak internal details
- [ ] Dependencies checked for known CVEs
- [ ] HTTPS enforced for all external calls
- [ ] Rate limiting on public endpoints
- [ ] Logging excludes sensitive values
```

---

## 3. Supply Chain Security

### 3.1 Dependency Management

| Control | Implementation |
|---------|---------------|
| Pin versions | Use exact versions in `package.json` (not `^` or `~` for production deps) |
| Audit regularly | `npm audit` / `pip-audit` / `cargo audit` in CI |
| Lock files | Always commit `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` |
| Review new deps | Before adding: check npm/PyPI page, GitHub stars, last publish date, maintainer count |
| Minimal deps | Prefer built-in APIs over micro-packages (e.g., `crypto` over `uuid` for random IDs) |

### 3.2 Tool Manifest Security

The `tools/manifest.json` bootstrapper executes install commands. Controls:

| Control | Status |
|---------|--------|
| Only GitHub URLs allowed | Enforced by bootstrapper validation |
| `installCmd` must be from committed manifest | Enforced by git history |
| Manifest changes require review | Enforced by PR process |
| Pin to specific commit/tag | Supported via `commit` field in manifest schema |
| Warn before executing `installCmd` | Implemented in bootstrapper |

Recommended manifest entry with pinning:
```json
{
  "name": "tool-name",
  "repo": "https://github.com/org/repo",
  "commit": "abc123def456",
  "installCmd": "npm install",
  "checksumSha256": "optional-but-recommended"
}
```

### 3.3 Docker / DevContainer Security

- Use specific image tags, never `latest`
- Run as non-root user
- Don't mount host secrets into containers
- Use multi-stage builds to minimize attack surface

---

## 4. Application Security (OWASP Top 10 Alignment)

| OWASP Category | Control in This Template |
|----------------|------------------------|
| A01: Broken Access Control | Protected procedures in tRPC; auth middleware pattern in 03-fullstack.mdc |
| A02: Cryptographic Failures | Env vars for secrets (7d.1-6); no hardcoded keys |
| A03: Injection | Zod input validation; parameterized queries via Prisma/Supabase (03-fullstack.mdc) |
| A04: Insecure Design | Threat model requirement for auth code (7d.7); security review gate |
| A05: Security Misconfiguration | CSP headers guidance (03-fullstack.mdc); `.env.example` convention |
| A06: Vulnerable Components | Dependency audit (7d.11, 7d.14); version pinning (7d.13) |
| A07: Auth Failures | Rate limiting middleware pattern; JWT/Supabase auth in context |
| A08: Software/Data Integrity | Supply chain controls (Section 3); manifest validation |
| A09: Logging Failures | Structured logging guidance (03-fullstack.mdc); PII exclusion (7d.4) |
| A10: SSRF | Input validation; URL allowlisting for external calls |

---

## 5. Compliance Mapping

For regulated environments, map controls to your compliance framework:

| Control Domain | Relevant Standards | Template Artifacts |
|---------------|-------------------|-------------------|
| Access Control | SOC2 CC6.1, PCI DSS 7.x | Auth middleware, protected procedures |
| Data Protection | GDPR Art.32, SOC2 CC6.7 | Encryption guidance, PII handling rules |
| Audit Trail | SOC2 CC7.2, PCI DSS 10.x | WORK_LOG, commit traceability, governance chain |
| Change Management | SOC2 CC8.1, PCI DSS 6.x | P-R-I-L workflow, human review gates |
| Vulnerability Management | SOC2 CC7.1, PCI DSS 6.x | Dependency audit, CVE checks |
| Incident Response | SOC2 CC7.3 | Secret rotation protocol (Section 1.5), debug templates |

---

## 6. Integration Points

This policy is referenced by and wired to:

| Artifact | How It References This Policy |
|----------|------------------------------|
| `01-mdd.mdc` Section 7d | Condensed security rules with link to this doc |
| `ANTI_PATTERNS_CATALOG.md` | Security anti-patterns section |
| `CONTINUOUS_IMPROVEMENT_PROTOCOL.md` | Security routing in learning checklist |
| `MEDIUM_PLAN_TEMPLATE.md` | Security review checkbox |
| `COMPLEX_PREPLAN_TEMPLATE.md` | Security review section |
| `PHASE_COMPLETION_TEMPLATE.md` | Security validation in completion checklist |
| `DEBUG_LOG_TEMPLATE.md` | Security incident classification |
| `.gitignore` | Secret file pattern blocking |
| `setup-tools.sh` / `setup-tools.ps1` | Manifest validation, install command safety |

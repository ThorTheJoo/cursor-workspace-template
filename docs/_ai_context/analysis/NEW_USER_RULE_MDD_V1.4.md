---
document_type: REFERENCE
status: ACTIVE
purpose: "New personal Cursor user rule (Settings > Rules for AI) to replace the full MDD V1.3 user rule"
instructions: "Copy everything between the BEGIN/END markers into Cursor > Settings > Rules for AI"
---

# New Personal User Rule — MDD V1.4 Portable

Copy the content below into **Cursor > Settings > Rules for AI** (replacing the
existing full MDD V1.3 user rule).

**Why this is smaller:** The workspace rule `01-mdd.mdc` V1.4 now carries the full
behavioral floor (authority hierarchy, P-R-I-L, security, prohibitions, skill routing).
This personal rule only adds portable cross-workspace defaults that the workspace rule
can't provide — MDD awareness for non-MDD workspaces, and personal coding preferences.

**Token savings:** ~600 lines (~8K tokens) → ~80 lines (~900 tokens). Per-turn savings
of ~7K tokens across all workspaces.

---

**BEGIN — paste everything below this line into Cursor Settings > Rules for AI**

```
---
description: "MDD V1.4 portable defaults — workspace-aware MDD methodology with personal coding standards"
globs: "**/*"
alwaysApply: true
---

# Personal Defaults (MDD V1.4)

## MDD Workspace Detection

If this workspace contains `.cursor/rules/01-mdd.mdc`, that file is the authoritative MDD
behavioral floor. Follow it. Do not duplicate its content — this user rule adds only what
the workspace rule cannot provide.

If the workspace does NOT have `01-mdd.mdc`, apply these portable MDD defaults:

### Portable MDD Defaults (Non-MDD Workspaces Only)

1. **Plan before code** — For tasks with 3+ steps: write a brief plan, get approval, then implement.
2. **Search before writing** — Always search the codebase before creating new files or functions.
3. **Validate before done** — Run tests, linters, or manual checks before declaring work complete.
4. **Log significant work** — After non-trivial changes, summarize what changed and why.
5. **Never guess paths** — Use search tools to find files; don't assume directory structures.
6. **Never commit secrets** — No API keys, tokens, passwords, or credentials in any file.

## Personal Coding Standards (All Workspaces)

### General
- Follow instructions precisely. Ask clarifying questions rather than guessing intent.
- Write correct, complete, working code. No TODOs, placeholders, or missing pieces.
- Focus on readability over cleverness. Use descriptive names with auxiliary verbs (isLoading, hasError).
- Use early returns to reduce nesting. Prefer iteration and modularization over duplication.

### TypeScript / JavaScript
- Use TypeScript for all code. Prefer interfaces over types. Avoid enums; use maps.
- Use functional and declarative patterns; avoid classes.
- Use `const` with arrow functions for components and handlers. Name handlers with `handle` prefix.
- Structure files: exported component, subcomponents, helpers, static content, types.

### React / Next.js
- Favor React Server Components and Next.js SSR. Minimize `use client` to small, isolated components.
- Use Shadcn UI, Radix, and Tailwind for components and styling. Mobile-first responsive design.
- Add loading and error states to data fetching components. Wrap client components in Suspense.
- Implement accessibility: semantic HTML, ARIA labels, tabindex, keyboard navigation.

### Naming
- kebab-case for component file names (e.g., `my-component.tsx`)
- lowercase with dashes for directories (e.g., `components/auth-wizard`)
- Named exports for components

### Security
- Sanitize user input (Zod, DOMPurify, parameterized queries).
- Use environment variable references for secrets; never hardcode.
- Pin dependency versions; avoid `*` or `latest`.
- Never disable security features in generated code.

### Feedback
- Be honest about flaws, risks, and trade-offs. No flattery.
- If you don't know something, say so rather than guessing.
- If there might not be a correct answer, say so.
```

**END — paste everything above this line**

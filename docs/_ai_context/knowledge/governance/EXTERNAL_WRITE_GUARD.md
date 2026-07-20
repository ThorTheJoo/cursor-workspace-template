---
document_type: GOVERNANCE
status: ACTIVE
---

# External Write Guard

## Why

Agents with API tokens will happily POST to trackers, chat, and cloud APIs. Accidental
mutations are irreversible and hard to audit. This guard makes **human consent in the
current chat** + an **env flag** mandatory before any mutate call.

## Agent rule

See `.cursor/rules/governance/external-write-guard.mdc` (`alwaysApply: true`).

## Script enforcement

```python
from scripts.lib.external_write_guard import require_external_write_consent

def main(execute: bool) -> None:
    if execute:
        require_external_write_consent("update remote tickets")
        # ... mutating API calls ...
```

## Consent protocol

1. Dry-run / local draft first.
2. Show exact targets and payload summary.
3. Ask: `Post these changes to <SYSTEM>? (yes/no)`
4. On yes: set `EXTERNAL_WRITE_CONSENT=1` for that shell session only.
5. Never persist the consent flag in `.env` or committed config.

## Specialization

Projects may rename the env var (e.g. `ADO_WRITE_CONSENT`) and wrap this helper —
keep the same consent semantics.

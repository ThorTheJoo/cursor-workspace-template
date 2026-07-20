"""Guard for mutating external-system API calls — requires explicit human consent.

Set in the shell ONLY after the user approves writes in chat:

    $env:EXTERNAL_WRITE_CONSENT = '1'   # PowerShell
    export EXTERNAL_WRITE_CONSENT=1     # bash

Scripts that create/update remote data MUST call require_external_write_consent()
before any POST/PATCH/DELETE to mutating endpoints.
"""
from __future__ import annotations

import os
import sys

CONSENT_ENV = "EXTERNAL_WRITE_CONSENT"
CONSENT_VALUES = {"1", "true", "yes", "approved"}


def has_external_write_consent() -> bool:
    return os.environ.get(CONSENT_ENV, "").strip().lower() in CONSENT_VALUES


def require_external_write_consent(action: str = "mutate external system") -> None:
    """Exit with code 2 if external write consent was not granted."""
    if has_external_write_consent():
        return
    print(
        f"BLOCKED: Refusing to {action}.\n"
        f"External writes require explicit user consent in chat AND:\n"
        f"  $env:{CONSENT_ENV} = '1'   # PowerShell\n"
        f"  export {CONSENT_ENV}=1     # bash\n"
        "Dry-run is still allowed without this flag.",
        file=sys.stderr,
    )
    sys.exit(2)

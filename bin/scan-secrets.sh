#!/usr/bin/env bash
#
# scan-secrets.sh -- Lightweight secret scanner for the workspace
#
# Uses gitleaks or trufflehog if available, otherwise falls back to
# grep-based pattern matching for common secret formats.
#
# Usage: ./bin/scan-secrets.sh [target-dir]
# Exit:  0 = clean, 1 = secrets found, 2 = usage error
#
# CI-safe: exits non-zero on findings for use in pipelines.

set -euo pipefail

TARGET_DIR="${1:-.}"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "[!!] Directory not found: $TARGET_DIR"
    exit 2
fi

SECRET_PATTERNS=(
    'sk-[a-zA-Z0-9]{20,}'
    'sk-proj-[a-zA-Z0-9_-]{20,}'
    'ghp_[a-zA-Z0-9]{36}'
    'gho_[a-zA-Z0-9]{36}'
    'github_pat_[a-zA-Z0-9_]{20,}'
    'AKIA[0-9A-Z]{16}'
    'xoxb-[0-9]{10,}'
    'xoxp-[0-9]{10,}'
    'hooks\.slack\.com/services/'
    'AIza[a-zA-Z0-9_-]{35}'
    'ya29\.[a-zA-Z0-9_-]+'
    'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*'
    'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}'
    'sq0csp-[a-zA-Z0-9_-]{43}'
    'PRIVATE KEY-----'
    'password\s*[:=]\s*["\x27][^"\x27]{8,}'
)

EXCLUDE_DIRS=(".git" "node_modules" ".tools-cache" "__pycache__" ".venv")
EXCLUDE_FILES=("*.lock" "*.map" "package-lock.json" "yarn.lock" "pnpm-lock.yaml")

FINDING_COUNT=0

# Prefer dedicated tools if available
if command -v gitleaks &>/dev/null; then
    echo "[>>] Using gitleaks for secret scanning..."
    if gitleaks detect --source="$TARGET_DIR" --no-git --verbose 2>&1; then
        echo "[OK] No secrets found (gitleaks)."
        exit 0
    else
        echo "[!!] gitleaks found potential secrets. Review output above."
        exit 1
    fi
fi

if command -v trufflehog &>/dev/null; then
    echo "[>>] Using trufflehog for secret scanning..."
    if trufflehog filesystem "$TARGET_DIR" --no-update 2>&1; then
        echo "[OK] No secrets found (trufflehog)."
        exit 0
    else
        echo "[!!] trufflehog found potential secrets. Review output above."
        exit 1
    fi
fi

# Fallback: grep-based scanning
echo "[>>] No dedicated scanner found. Using grep-based fallback..."
echo "     (Install gitleaks or trufflehog for more thorough scanning.)"
echo ""

EXCLUDE_ARGS=""
for d in "${EXCLUDE_DIRS[@]}"; do
    EXCLUDE_ARGS+=" --exclude-dir=$d"
done
for f in "${EXCLUDE_FILES[@]}"; do
    EXCLUDE_ARGS+=" --exclude=$f"
done

for pattern in "${SECRET_PATTERNS[@]}"; do
    MATCHES=$(eval grep -rnE $EXCLUDE_ARGS "'$pattern'" "'$TARGET_DIR'" 2>/dev/null \
        | grep -v '\.git/' \
        | grep -v 'scan-secrets\.sh' \
        | grep -v '\.env\.example' \
        | grep -v 'sample\.envrc' \
        | grep -v 'SECURITY' \
        | grep -v 'CONTRIBUTING' \
        | head -20 || true)

    if [[ -n "$MATCHES" ]]; then
        COUNT=$(echo "$MATCHES" | wc -l)
        FINDING_COUNT=$((FINDING_COUNT + COUNT))
        echo "[!!] Pattern match: $pattern ($COUNT hit(s))"
        echo "$MATCHES" | while IFS= read -r line; do
            echo "     $line"
        done
        echo ""
    fi
done

if [[ "$FINDING_COUNT" -eq 0 ]]; then
    echo "[OK] No secret patterns detected (grep fallback)."
    exit 0
else
    echo "[!!] $FINDING_COUNT potential secret(s) found. Review findings above."
    echo "     False positives are possible with grep-based scanning."
    echo "     Install gitleaks (https://github.com/gitleaks/gitleaks) for better accuracy."
    exit 1
fi

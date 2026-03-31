#!/usr/bin/env bash
#
# skill-scan.sh -- Static pattern scanner for installed tools and skills
#
# Scans a target directory for dangerous code patterns commonly used in
# supply chain attacks, prompt injection, and data exfiltration.
#
# Usage: ./bin/skill-scan.sh <target-dir> [tool-name]
# Exit:  0 = clean, 1 = findings detected, 2 = usage error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="$SCRIPT_DIR/../.tools-cache"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <target-directory> [tool-name]"
    echo "Scans for dangerous patterns in tool/skill source code."
    exit 2
fi

TARGET_DIR="$1"
TOOL_NAME="${2:-$(basename "$TARGET_DIR")}"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "[!!] Directory not found: $TARGET_DIR"
    exit 2
fi

DANGEROUS_PATTERNS=(
    'eval('
    'exec('
    'os\.system('
    'subprocess\.call.*shell=True'
    'Invoke-Expression'
    'iex '
    'curl.*\|.*sh'
    'curl.*\|.*bash'
    'wget.*\|.*sh'
    'wget.*\|.*bash'
    'wget -O -'
    'fetch\(.*\).*\.then'
    'new Function('
    'child_process'
    'require\(.child_process.\)'
    'spawn\('
    'execSync\('
    '__import__'
    'importlib'
    'ctypes'
    'LD_PRELOAD'
    'DYLD_INSERT_LIBRARIES'
)

EXFIL_PATTERNS=(
    'ngrok'
    'webhook\.site'
    'requestbin'
    'burpcollaborator'
    'oastify\.com'
    'interact\.sh'
    'pipedream\.net'
    'hookbin\.com'
)

FINDING_COUNT=0
FINDINGS=""

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    MATCHES=$(grep -rn --include='*.sh' --include='*.py' --include='*.js' --include='*.ts' \
        --include='*.mjs' --include='*.cjs' --include='*.md' --include='*.mdc' \
        --include='*.yaml' --include='*.yml' --include='*.json' \
        -E "$pattern" "$TARGET_DIR" 2>/dev/null | grep -v '\.git/' || true)

    if [[ -n "$MATCHES" ]]; then
        FINDING_COUNT=$((FINDING_COUNT + $(echo "$MATCHES" | wc -l)))
        FINDINGS+="--- Pattern: $pattern ---"$'\n'"$MATCHES"$'\n'$'\n'
    fi
done

for pattern in "${EXFIL_PATTERNS[@]}"; do
    MATCHES=$(grep -rn --include='*' -i "$pattern" "$TARGET_DIR" 2>/dev/null | grep -v '\.git/' || true)

    if [[ -n "$MATCHES" ]]; then
        FINDING_COUNT=$((FINDING_COUNT + $(echo "$MATCHES" | wc -l)))
        FINDINGS+="--- Exfil domain: $pattern ---"$'\n'"$MATCHES"$'\n'$'\n'
    fi
done

REPORT_FILE="$REPORT_DIR/scan-report-${TOOL_NAME}.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")

mkdir -p "$REPORT_DIR"

if [[ "$FINDING_COUNT" -eq 0 ]]; then
    cat > "$REPORT_FILE" <<EOF
{
  "tool": "$TOOL_NAME",
  "scannedAt": "$TIMESTAMP",
  "targetDir": "$TARGET_DIR",
  "findingCount": 0,
  "status": "CLEAN",
  "findings": []
}
EOF
    echo "[OK] $TOOL_NAME: No dangerous patterns found."
    exit 0
else
    cat > "$REPORT_FILE" <<EOF
{
  "tool": "$TOOL_NAME",
  "scannedAt": "$TIMESTAMP",
  "targetDir": "$TARGET_DIR",
  "findingCount": $FINDING_COUNT,
  "status": "FINDINGS",
  "details": "See scan-report-${TOOL_NAME}.txt for full output"
}
EOF
    echo "$FINDINGS" > "$REPORT_DIR/scan-report-${TOOL_NAME}.txt"
    echo "[!!] $TOOL_NAME: $FINDING_COUNT potentially dangerous pattern(s) found."
    echo "     Report: $REPORT_FILE"
    echo "     Details: $REPORT_DIR/scan-report-${TOOL_NAME}.txt"
    exit 1
fi

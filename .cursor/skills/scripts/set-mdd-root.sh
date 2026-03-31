#!/usr/bin/env bash
# set-mdd-root.sh — Change MDD_ROOT across all skill files
# Usage: ./set-mdd-root.sh "your/custom/path/"
set -euo pipefail

OLD_ROOT="docs/_ai_context/"
NEW_ROOT="${1:?Usage: $0 <new-root-path>}"

# Ensure new root ends with /
[[ "$NEW_ROOT" == */ ]] || NEW_ROOT="${NEW_ROOT}/"

echo "Replacing MDD_ROOT: $OLD_ROOT → $NEW_ROOT"

find .cursor/skills -type f \( -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.py" \) \
  -exec sed -i "s|${OLD_ROOT}|${NEW_ROOT}|g" {} +

# Update README declaration
sed -i "s|MDD_ROOT = .*|MDD_ROOT = ${NEW_ROOT%/}|" .cursor/skills/README.md

echo "Done. Updated $(grep -rl "${NEW_ROOT}" .cursor/skills/ | wc -l) files."

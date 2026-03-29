#!/usr/bin/env bash
#
# Cursor Workspace Starter — Bash Tool Bootstrapper
#
# Parses tools/manifest.json, validates it, presents interactive selection
# (fzf if available, else yes/no prompts), clones selected repos into
# .tools-cache/, runs install commands, and ensures .cursor/ and docs/
# directories are properly structured.
#
# Idempotent: safe to run multiple times.
#
# Requirements: bash 4+, git, jq
# Optional:     fzf (multi-select UI), npm/npx (CLI tools), uv (Python tools)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MANIFEST="tools/manifest.json"
CACHE_DIR=".tools-cache"
CURSOR_DIR=".cursor"
DOCS_DIR="docs/_ai_context"

# ── Colors ──────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
RESET='\033[0m'

banner()  { echo -e "\n${CYAN}  ========================================${RESET}"; echo -e "${CYAN}   Cursor Workspace Starter — Bootstrapper${RESET}"; echo -e "${CYAN}  ========================================${RESET}\n"; }
step()    { echo -e "${YELLOW}[>>]${RESET} $1"; }
ok()      { echo -e "${GREEN}[OK]${RESET} $1"; }
skip()    { echo -e "${DIM}[--] $1${RESET}"; }
err()     { echo -e "${RED}[!!]${RESET} $1"; }

# ── Preflight ───────────────────────────────────────────────────────

banner

if ! command -v git &>/dev/null; then
    err "git is not installed. Install git and retry."
    exit 1
fi
ok "git detected: $(git --version)"

if ! command -v jq &>/dev/null; then
    err "jq is not installed. Install jq (apt install jq / brew install jq) and retry."
    exit 1
fi
ok "jq detected: $(jq --version)"

if [[ ! -f "$MANIFEST" ]]; then
    err "tools/manifest.json not found. Add your tools and retry."
    exit 1
fi

# ── Validate manifest JSON ─────────────────────────────────────────

step "Validating manifest JSON..."

if ! jq empty "$MANIFEST" 2>/dev/null; then
    err "tools/manifest.json contains invalid JSON. Fix syntax errors and retry."
    exit 1
fi

if ! jq -e '.tools | type == "array"' "$MANIFEST" >/dev/null 2>&1; then
    err "tools/manifest.json is missing a 'tools' array at the root level."
    exit 1
fi

VALIDATION_ERRORS=0
TOOL_COUNT=$(jq '.tools | length' "$MANIFEST")

for i in $(seq 0 $((TOOL_COUNT - 1))); do
    name=$(jq -r ".tools[$i].name // empty" "$MANIFEST")
    repo=$(jq -r ".tools[$i].repo // empty" "$MANIFEST")

    if [[ -z "$name" ]]; then
        err "Tool at index $i is missing required field 'name'."
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
    fi

    if [[ -z "$repo" ]]; then
        err "Tool '$name' (index $i) is missing required field 'repo'."
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
    elif [[ ! "$repo" =~ ^https://github\.com/ ]]; then
        err "Tool '$name' has non-GitHub repo URL: $repo (expected https://github.com/...)."
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
    fi
done

if [[ "$VALIDATION_ERRORS" -gt 0 ]]; then
    err "Manifest has $VALIDATION_ERRORS validation error(s). Fix them before proceeding."
    exit 1
fi

ok "Manifest validated: $TOOL_COUNT tool(s), 0 errors."

# ── Parse manifest ──────────────────────────────────────────────────

if [[ "$TOOL_COUNT" -eq 0 ]]; then
    err "No tools in manifest. Add entries to tools/manifest.json first."
    exit 1
fi

echo ""

# ── Interactive selection ───────────────────────────────────────────

SELECTED=()

has_fzf() { command -v fzf &>/dev/null; }

if has_fzf; then
    step "fzf detected — launching multi-select (TAB to toggle, ENTER to confirm)..."
    echo ""

    FZF_INPUT=""
    for i in $(seq 0 $((TOOL_COUNT - 1))); do
        name=$(jq -r ".tools[$i].name" "$MANIFEST")
        desc=$(jq -r ".tools[$i].description" "$MANIFEST")
        platform=$(jq -r ".tools[$i].platform" "$MANIFEST")
        gpu=$(jq -r ".tools[$i].requiresGpu // false" "$MANIFEST")

        if [[ "$platform" == "win" ]]; then
            continue
        fi

        label="$name — $desc"
        if [[ "$gpu" == "true" ]]; then
            label="$label [REQUIRES GPU]"
        fi

        FZF_INPUT+="$i|$label"$'\n'
    done

    if [[ -n "$FZF_INPUT" ]]; then
        CHOSEN=$(echo "$FZF_INPUT" | fzf --multi --delimiter='|' --with-nth=2 --prompt="Select tools > " --header="TAB=toggle  ENTER=confirm" || true)
        while IFS= read -r line; do
            if [[ -n "$line" ]]; then
                idx=$(echo "$line" | cut -d'|' -f1)
                SELECTED+=("$idx")
            fi
        done <<< "$CHOSEN"
    fi
else
    for i in $(seq 0 $((TOOL_COUNT - 1))); do
        name=$(jq -r ".tools[$i].name" "$MANIFEST")
        desc=$(jq -r ".tools[$i].description" "$MANIFEST")
        platform=$(jq -r ".tools[$i].platform" "$MANIFEST")
        gpu=$(jq -r ".tools[$i].requiresGpu // false" "$MANIFEST")

        if [[ "$platform" == "win" ]]; then
            skip "$name — windows-only, skipping."
            continue
        fi

        label="$name — $desc"
        if [[ "$gpu" == "true" ]]; then
            label="$label [REQUIRES GPU]"
        fi

        echo -e "  ${label}"
        read -rp "  Install? (y/N): " answer
        if [[ "$answer" =~ ^[yY] ]]; then
            SELECTED+=("$i")
            ok "Selected: $name"
        else
            skip "Skipped: $name"
        fi
        echo ""
    done
fi

if [[ ${#SELECTED[@]} -eq 0 ]]; then
    echo ""
    step "No tools selected. Ensuring directory structure only."
fi

# ── Ensure .cursor directories ──────────────────────────────────────

for dir in "$CURSOR_DIR/rules" "$CURSOR_DIR/bin" "$CURSOR_DIR/skills" "$CURSOR_DIR/mcp" "$CURSOR_DIR/automations"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        ok "Created $dir"
    fi
done

# ── Ensure MDD docs directories ────────────────────────────────────

for dir in "$DOCS_DIR/state" "$DOCS_DIR/analysis" "$DOCS_DIR/templates" "$DOCS_DIR/prompts" "$DOCS_DIR/knowledge"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        ok "Created $dir"
    fi
done

mkdir -p "$CACHE_DIR"

# ── Clone and install ───────────────────────────────────────────────

INSTALLED_COUNT=0
FAILED_COUNT=0

for idx in "${SELECTED[@]}"; do
    name=$(jq -r ".tools[$idx].name" "$MANIFEST")
    repo=$(jq -r ".tools[$idx].repo" "$MANIFEST")
    install_cmd=$(jq -r ".tools[$idx].installCmd" "$MANIFEST")
    tool_type=$(jq -r ".tools[$idx].type" "$MANIFEST")

    echo ""
    step "Installing $name..."

    clone_dir="$CACHE_DIR/$name"

    if [[ -d "$clone_dir" ]]; then
        skip "$name already cloned at $clone_dir — skipping clone."
    else
        step "Cloning $repo..."
        if git clone --depth 1 "$repo" "$clone_dir" 2>/dev/null; then
            ok "Cloned $name"
        else
            err "Failed to clone $name. Skipping install."
            FAILED_COUNT=$((FAILED_COUNT + 1))
            continue
        fi
    fi

    if [[ -n "$install_cmd" && "$install_cmd" != "null" ]]; then
        step "Running: $install_cmd"
        pushd "$clone_dir" > /dev/null
        if eval "$install_cmd"; then
            ok "Installed $name"
            INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
        else
            err "Install failed for $name. Check the tool's README for manual steps."
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi
        popd > /dev/null
    else
        INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
    fi

    if [[ "$tool_type" == "skills" ]]; then
        skills_src="$clone_dir/skills"
        skills_dest="$CURSOR_DIR/skills"
        if [[ -d "$skills_src" ]]; then
            step "Copying skills from $name into $skills_dest/..."
            cp -r "$skills_src"/* "$skills_dest/" 2>/dev/null || true
            ok "Skills copied for $name"
        fi
    fi
done

# ── Verify foundational rules ──────────────────────────────────────

echo ""
RULE_FILES=("00-starter-rules.mdc" "01-mdd.mdc" "02-kingmode.mdc" "03-frontend-fullstack.mdc")
RULES_OK=0
for rf in "${RULE_FILES[@]}"; do
    if [[ -f "$CURSOR_DIR/rules/$rf" ]]; then
        ok "Rule verified: $rf"
        RULES_OK=$((RULES_OK + 1))
    else
        err "Missing rule: $rf — workspace may be incomplete."
    fi
done

# ── Detect environment ──────────────────────────────────────────────

IS_DEVCONTAINER=false
if [[ -n "${REMOTE_CONTAINERS:-}" ]] || [[ -n "${CODESPACES:-}" ]] || [[ -f "/.dockerenv" ]]; then
    IS_DEVCONTAINER=true
fi

# ── Final banner ────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}  ========================================${RESET}"
echo -e "${GREEN}   Setup Complete${RESET}"
echo -e "${GREEN}  ========================================${RESET}"
echo ""
echo -e "  Tools selected:  ${#SELECTED[@]} / $TOOL_COUNT"
echo -e "  Installed OK:    $INSTALLED_COUNT"
if [[ "$FAILED_COUNT" -gt 0 ]]; then
    echo -e "  ${RED}Failed:        $FAILED_COUNT${RESET}"
fi
echo -e "  Rules verified:  $RULES_OK / ${#RULE_FILES[@]} foundational .mdc files"
echo -e "  MDD dirs:        5 (state, analysis, templates, prompts, knowledge)"
echo ""

if $IS_DEVCONTAINER; then
    echo -e "${CYAN}  Dev Container detected. Workspace is ready.${RESET}"
else
    echo -e "${YELLOW}  Restart Cursor to activate rules and tool integrations.${RESET}"
fi

echo ""

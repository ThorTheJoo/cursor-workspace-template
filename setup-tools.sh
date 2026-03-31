#!/usr/bin/env bash
#
# Cursor Workspace Starter â€” Bash Tool Bootstrapper
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

# â”€â”€ Colors â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
RESET='\033[0m'

banner()  { echo -e "\n${CYAN}  ========================================${RESET}"; echo -e "${CYAN}   Cursor Workspace Starter â€” Bootstrapper${RESET}"; echo -e "${CYAN}  ========================================${RESET}\n"; }
step()    { echo -e "${YELLOW}[>>]${RESET} $1"; }
ok()      { echo -e "${GREEN}[OK]${RESET} $1"; }
skip()    { echo -e "${DIM}[--] $1${RESET}"; }
err()     { echo -e "${RED}[!!]${RESET} $1"; }

seed_mdd_from_skills() {
    local skills_dir="$CURSOR_DIR/skills"
    local mdd_root="$DOCS_DIR"

    step "Seeding MDD state files from skill assets..."

    # Create directory structure
    mkdir -p "$mdd_root"/{state,analysis/archive,prompts/phases,templates}
    mkdir -p "$mdd_root"/knowledge/{governance,reference,schemas,staging,versions,glossary}

    # Seed from backlog-management
    if [[ -f "$skills_dir/backlog-management/assets/BACKLOG_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/state/BACKLOG.md" ]] || {
            cp "$skills_dir/backlog-management/assets/BACKLOG_TEMPLATE.md" "$mdd_root/state/BACKLOG.md"
            ok "Created $mdd_root/state/BACKLOG.md"
        }
    fi

    # Seed from work-logging
    if [[ -f "$skills_dir/work-logging/assets/WORK_LOG_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/state/WORK_LOG.md" ]] || {
            cp "$skills_dir/work-logging/assets/WORK_LOG_TEMPLATE.md" "$mdd_root/state/WORK_LOG.md"
            ok "Created $mdd_root/state/WORK_LOG.md"
        }
    fi

    # Seed from context-loading
    if [[ -f "$skills_dir/context-loading/assets/repo-manifest-template.json" ]]; then
        [[ -f "$mdd_root/state/repo-manifest.json" ]] || {
            cp "$skills_dir/context-loading/assets/repo-manifest-template.json" "$mdd_root/state/repo-manifest.json"
            ok "Created $mdd_root/state/repo-manifest.json"
        }
    fi

    if [[ -f "$skills_dir/context-loading/assets/CONTEXT_MANIFEST_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/prompts/phases/CONTEXT_MANIFEST.md" ]] || {
            cp "$skills_dir/context-loading/assets/CONTEXT_MANIFEST_TEMPLATE.md" "$mdd_root/prompts/phases/CONTEXT_MANIFEST.md"
            ok "Created $mdd_root/prompts/phases/CONTEXT_MANIFEST.md"
        }
    fi

    # Seed from phase-execution
    if [[ -f "$skills_dir/phase-execution/assets/PHASES_INDEX_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/prompts/phases/PHASES_INDEX.md" ]] || {
            cp "$skills_dir/phase-execution/assets/PHASES_INDEX_TEMPLATE.md" "$mdd_root/prompts/phases/PHASES_INDEX.md"
            ok "Created $mdd_root/prompts/phases/PHASES_INDEX.md"
        }
    fi

    # Seed from knowledge-repo
    if [[ -f "$skills_dir/knowledge-repo/assets/MASTER_KNOWLEDGE_REPO_TEMPLATE.yaml" ]]; then
        [[ -f "$mdd_root/knowledge/MASTER_KNOWLEDGE_REPOSITORY.yaml" ]] || {
            cp "$skills_dir/knowledge-repo/assets/MASTER_KNOWLEDGE_REPO_TEMPLATE.yaml" "$mdd_root/knowledge/MASTER_KNOWLEDGE_REPOSITORY.yaml"
            ok "Created $mdd_root/knowledge/MASTER_KNOWLEDGE_REPOSITORY.yaml"
        }
    fi

    if [[ -f "$skills_dir/knowledge-repo/assets/TERMINOLOGY_INDEX_TEMPLATE.yaml" ]]; then
        [[ -f "$mdd_root/knowledge/glossary/TERMINOLOGY_INDEX.yaml" ]] || {
            mkdir -p "$mdd_root/knowledge/glossary"
            cp "$skills_dir/knowledge-repo/assets/TERMINOLOGY_INDEX_TEMPLATE.yaml" "$mdd_root/knowledge/glossary/TERMINOLOGY_INDEX.yaml"
            ok "Created $mdd_root/knowledge/glossary/TERMINOLOGY_INDEX.yaml"
        }
    fi

    # Seed MASTER_STATE.md if it doesn't exist
    [[ -f "$mdd_root/state/MASTER_STATE.md" ]] || {
        cat > "$mdd_root/state/MASTER_STATE.md" << 'MASTER_EOF'
---
document_type: STATE
status: ACTIVE
---

# Project State

Read order for any non-trivial task:
1. `docs/_ai_context/state/repo-manifest.json` — file/function lookup
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` — project identity
3. This file — current state
4. `docs/_ai_context/state/BACKLOG.md` — pending work

---

## Skills Framework

This workspace uses MDD skills at `.cursor/skills/`. See `.cursor/skills/README.md`.

---

## Recent Changes

(Add entries as work progresses)
MASTER_EOF
        ok "Created $mdd_root/state/MASTER_STATE.md"
    }

    ok "MDD seeding complete."
}

# â”€â”€ Preflight â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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

# â”€â”€ Validate manifest JSON â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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

# â”€â”€ Parse manifest â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

if [[ "$TOOL_COUNT" -eq 0 ]]; then
    err "No tools in manifest. Add entries to tools/manifest.json first."
    exit 1
fi

echo ""

# â”€â”€ Interactive selection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

SELECTED=()

has_fzf() { command -v fzf &>/dev/null; }

if has_fzf; then
    step "fzf detected â€” launching multi-select (TAB to toggle, ENTER to confirm)..."
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

        label="$name â€” $desc"
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
            skip "$name â€” windows-only, skipping."
            continue
        fi

        label="$name â€” $desc"
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

# â”€â”€ Ensure .cursor directories â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

for dir in "$CURSOR_DIR/rules" "$CURSOR_DIR/bin" "$CURSOR_DIR/skills" "$CURSOR_DIR/mcp"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        ok "Created $dir"
    fi
done

# â”€â”€ Ensure MDD docs directories â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

for dir in "$DOCS_DIR/state" "$DOCS_DIR/analysis" "$DOCS_DIR/templates" "$DOCS_DIR/prompts" "$DOCS_DIR/knowledge"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        ok "Created $dir"
    fi
done

seed_mdd_from_skills

mkdir -p "$CACHE_DIR"

# â”€â”€ Clone and install â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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
        skip "$name already cloned at $clone_dir -- skipping clone."
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

    # Pin to specific commit if specified in manifest (supply chain security)
    pinned_commit=$(jq -r ".tools[$idx].commit // empty" "$MANIFEST")
    if [[ -n "$pinned_commit" ]]; then
        step "Pinning $name to commit $pinned_commit..."
        pushd "$clone_dir" > /dev/null
        if git fetch origin "$pinned_commit" 2>/dev/null && git checkout "$pinned_commit" 2>/dev/null; then
            ok "Pinned to $pinned_commit"
        else
            err "Failed to pin $name to $pinned_commit. Using HEAD."
        fi
        popd > /dev/null
    fi

    if [[ -n "$install_cmd" && "$install_cmd" != "null" ]]; then
        # Security: validate install command against allowlist
        ALLOWED_PREFIXES=("npm install" "npm ci" "pip install" "uv pip install" "npx" "cargo install" "go install")
        CMD_ALLOWED=false
        for prefix in "${ALLOWED_PREFIXES[@]}"; do
            if [[ "$install_cmd" == "$prefix"* ]]; then
                CMD_ALLOWED=true
                break
            fi
        done

        if ! $CMD_ALLOWED; then
            err "SECURITY WARNING: '$install_cmd' is not a recognized install command."
            read -rp "  Execute anyway? (y/N): " answer
            if [[ ! "$answer" =~ ^[yY] ]]; then
                skip "Skipped install for $name (user declined)."
                FAILED_COUNT=$((FAILED_COUNT + 1))
                continue
            fi
        fi

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

# â”€â”€ Verify foundational rules â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

echo ""
RULE_FILES=("00-starter-rules.mdc" "01-mdd.mdc" "02-kingmode.mdc" "03-frontend-fullstack.mdc")
RULES_OK=0
for rf in "${RULE_FILES[@]}"; do
    if [[ -f "$CURSOR_DIR/rules/$rf" ]]; then
        ok "Rule verified: $rf"
        RULES_OK=$((RULES_OK + 1))
    else
        err "Missing rule: $rf â€” workspace may be incomplete."
    fi
done

# â”€â”€ Detect environment â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

IS_DEVCONTAINER=false
if [[ -n "${REMOTE_CONTAINERS:-}" ]] || [[ -n "${CODESPACES:-}" ]] || [[ -f "/.dockerenv" ]]; then
    IS_DEVCONTAINER=true
fi

# â”€â”€ Final banner â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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
echo -e "  MDD dirs:        11 (full V1.3 structure)"
echo ""

if $IS_DEVCONTAINER; then
    echo -e "${CYAN}  Dev Container detected. Workspace is ready.${RESET}"
else
    echo -e "${YELLOW}  Restart Cursor to activate rules and tool integrations.${RESET}"
fi

echo ""

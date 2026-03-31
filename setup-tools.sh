#!/usr/bin/env bash
#
# Cursor Workspace Starter -- Bash Tool Bootstrapper
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
LOCK_FILE="SECURITY-LOCK.json"

# -- Defaults ----------------------------------------------------------------

DRY_RUN=false
SELECT_ALL=false
SELECT_NONE=false
PRESET=""

# -- Colors ------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
RESET='\033[0m'

banner()  { echo -e "\n${CYAN}  ========================================${RESET}"; echo -e "${CYAN}   Cursor Workspace Starter -- Bootstrapper${RESET}"; echo -e "${CYAN}  ========================================${RESET}\n"; }
step()    { echo -e "${YELLOW}[>>]${RESET} $1"; }
ok()      { echo -e "${GREEN}[OK]${RESET} $1"; }
skip()    { echo -e "${DIM}[--] $1${RESET}"; }
err()     { echo -e "${RED}[!!]${RESET} $1"; }

# -- Help --------------------------------------------------------------------

show_help() {
    cat <<'HELPEOF'
Usage: ./setup-tools.sh [OPTIONS]

Options:
  --help          Show this help message and exit
  --dry-run       Show what would be installed without making changes
  --all           Select all compatible tools (skip interactive prompt)
  --none          Select no tools (only create directory structure + seed MDD)
  --preset=NAME   Select tools by preset profile:
                    minimal    - only type:rules and type:skills
                    fullstack  - everything except requiresGpu:true
                    airgapped  - no tools (MDD structure only, zero network)

Examples:
  ./setup-tools.sh                  # Interactive selection (fzf or y/N)
  ./setup-tools.sh --dry-run        # Preview without changes
  ./setup-tools.sh --preset=minimal # Install only rules and skills
  ./setup-tools.sh --all            # Install everything compatible
HELPEOF
    exit 0
}

# -- Argument parsing --------------------------------------------------------

for arg in "$@"; do
    case "$arg" in
        --help)       show_help ;;
        --dry-run)    DRY_RUN=true ;;
        --all)        SELECT_ALL=true ;;
        --none)       SELECT_NONE=true ;;
        --preset=*)   PRESET="${arg#--preset=}" ;;
        *)
            err "Unknown option: $arg"
            echo "Run ./setup-tools.sh --help for usage."
            exit 1
            ;;
    esac
done

# -- Root guard --------------------------------------------------------------

if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then
    err "Do not run this script as root. It does not require elevated privileges."
    exit 1
fi

# -- MDD seeding -------------------------------------------------------------

seed_mdd_from_skills() {
    local skills_dir="$CURSOR_DIR/skills"
    local mdd_root="$DOCS_DIR"

    step "Seeding MDD state files from skill assets..."

    mkdir -p "$mdd_root"/{state,analysis/archive,prompts/phases,templates}
    mkdir -p "$mdd_root"/knowledge/{governance,reference,schemas,staging,versions,glossary}

    if [[ -f "$skills_dir/backlog-management/assets/BACKLOG_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/state/BACKLOG.md" ]] || {
            cp "$skills_dir/backlog-management/assets/BACKLOG_TEMPLATE.md" "$mdd_root/state/BACKLOG.md"
            ok "Created $mdd_root/state/BACKLOG.md"
        }
    fi

    if [[ -f "$skills_dir/work-logging/assets/WORK_LOG_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/state/WORK_LOG.md" ]] || {
            cp "$skills_dir/work-logging/assets/WORK_LOG_TEMPLATE.md" "$mdd_root/state/WORK_LOG.md"
            ok "Created $mdd_root/state/WORK_LOG.md"
        }
    fi

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

    if [[ -f "$skills_dir/phase-execution/assets/PHASES_INDEX_TEMPLATE.md" ]]; then
        [[ -f "$mdd_root/prompts/phases/PHASES_INDEX.md" ]] || {
            cp "$skills_dir/phase-execution/assets/PHASES_INDEX_TEMPLATE.md" "$mdd_root/prompts/phases/PHASES_INDEX.md"
            ok "Created $mdd_root/prompts/phases/PHASES_INDEX.md"
        }
    fi

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

    [[ -f "$mdd_root/state/MASTER_STATE.md" ]] || {
        cat > "$mdd_root/state/MASTER_STATE.md" << 'MASTER_EOF'
---
document_type: STATE
status: ACTIVE
---

# Project State

Read order for any non-trivial task:
1. `docs/_ai_context/state/repo-manifest.json` -- file/function lookup
2. `docs/_ai_context/prompts/phases/CONTEXT_MANIFEST.md` -- project identity
3. This file -- current state
4. `docs/_ai_context/state/BACKLOG.md` -- pending work

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

# -- Preflight ---------------------------------------------------------------

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

if $DRY_RUN; then
    echo -e "${CYAN}  [DRY RUN] No files will be created or modified.${RESET}"
    echo ""
fi

# -- Validate manifest JSON --------------------------------------------------

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

# -- Parse manifest ----------------------------------------------------------

if [[ "$TOOL_COUNT" -eq 0 ]]; then
    err "No tools in manifest. Add entries to tools/manifest.json first."
    exit 1
fi

echo ""

# -- Tool selection (preset / flag / interactive) ----------------------------

matches_preset() {
    local idx=$1
    local tool_type tool_gpu
    tool_type=$(jq -r ".tools[$idx].type" "$MANIFEST")
    tool_gpu=$(jq -r ".tools[$idx].requiresGpu // false" "$MANIFEST")

    case "$PRESET" in
        minimal)
            [[ "$tool_type" == "rules" || "$tool_type" == "skills" ]]
            ;;
        fullstack)
            [[ "$tool_gpu" != "true" ]]
            ;;
        airgapped)
            return 1
            ;;
        *)
            err "Unknown preset: $PRESET. Valid presets: minimal, fullstack, airgapped."
            exit 1
            ;;
    esac
}

SELECTED=()

if $SELECT_NONE || [[ "$PRESET" == "airgapped" ]]; then
    step "No tools selected (--none / --preset=airgapped). Directory structure only."

elif $SELECT_ALL || [[ -n "$PRESET" ]]; then
    for i in $(seq 0 $((TOOL_COUNT - 1))); do
        platform=$(jq -r ".tools[$i].platform" "$MANIFEST")
        if [[ "$platform" == "win" ]]; then
            continue
        fi

        if $SELECT_ALL || matches_preset "$i"; then
            name=$(jq -r ".tools[$i].name" "$MANIFEST")
            SELECTED+=("$i")
            ok "Auto-selected: $name"
        fi
    done

else
    # Interactive selection
    has_fzf() { command -v fzf &>/dev/null; }

    if has_fzf; then
        step "fzf detected -- launching multi-select (TAB to toggle, ENTER to confirm)..."
        echo ""

        FZF_INPUT=""
        for i in $(seq 0 $((TOOL_COUNT - 1))); do
            name=$(jq -r ".tools[$i].name" "$MANIFEST")
            desc=$(jq -r ".tools[$i].description" "$MANIFEST")
            platform=$(jq -r ".tools[$i].platform" "$MANIFEST")
            gpu=$(jq -r ".tools[$i].requiresGpu // false" "$MANIFEST")
            pinned=$(jq -r ".tools[$i].pinnedRef // empty" "$MANIFEST")

            if [[ "$platform" == "win" ]]; then
                continue
            fi

            label="$name -- $desc"
            if [[ "$gpu" == "true" ]]; then
                label="$label [REQUIRES GPU]"
            fi
            if [[ -z "$pinned" ]]; then
                label="$label [UNPINNED]"
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
            pinned=$(jq -r ".tools[$i].pinnedRef // empty" "$MANIFEST")

            if [[ "$platform" == "win" ]]; then
                skip "$name -- windows-only, skipping."
                continue
            fi

            label="$name -- $desc"
            if [[ "$gpu" == "true" ]]; then
                label="$label [REQUIRES GPU]"
            fi
            if [[ -z "$pinned" ]]; then
                label="$label [UNPINNED]"
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
fi

if [[ ${#SELECTED[@]} -eq 0 ]]; then
    echo ""
    step "No tools selected. Ensuring directory structure only."
fi

# -- Dry run summary ---------------------------------------------------------

if $DRY_RUN; then
    echo ""
    echo -e "${CYAN}  [DRY RUN] Would install:${RESET}"
    for idx in "${SELECTED[@]}"; do
        name=$(jq -r ".tools[$idx].name" "$MANIFEST")
        pinned=$(jq -r ".tools[$idx].pinnedRef // \"HEAD (unpinned)\"" "$MANIFEST")
        echo -e "    - $name @ $pinned"
    done
    echo ""
    echo -e "${CYAN}  [DRY RUN] Would create directory structure + seed MDD files.${RESET}"
    echo -e "${CYAN}  [DRY RUN] No changes made. Exiting.${RESET}"
    exit 0
fi

# -- Ensure .cursor directories ----------------------------------------------

for dir in "$CURSOR_DIR/rules" "$CURSOR_DIR/bin" "$CURSOR_DIR/skills" "$CURSOR_DIR/mcp"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        ok "Created $dir"
    fi
done

# -- Ensure MDD docs directories ---------------------------------------------

for dir in "$DOCS_DIR/state" "$DOCS_DIR/analysis" "$DOCS_DIR/templates" "$DOCS_DIR/prompts" "$DOCS_DIR/knowledge"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        ok "Created $dir"
    fi
done

seed_mdd_from_skills

mkdir -p "$CACHE_DIR"
mkdir -p "bin"

# -- Clone and install -------------------------------------------------------

INSTALLED_COUNT=0
FAILED_COUNT=0
LOCK_ENTRIES=""

for idx in "${SELECTED[@]}"; do
    name=$(jq -r ".tools[$idx].name" "$MANIFEST")
    repo=$(jq -r ".tools[$idx].repo" "$MANIFEST")
    install_cmd=$(jq -r ".tools[$idx].installCmd" "$MANIFEST")
    tool_type=$(jq -r ".tools[$idx].type" "$MANIFEST")
    pinned_ref=$(jq -r ".tools[$idx].pinnedRef // empty" "$MANIFEST")
    do_scan=$(jq -r ".tools[$idx].skillScan // false" "$MANIFEST")

    echo ""
    step "Installing $name..."

    if [[ -z "$pinned_ref" ]]; then
        err "WARNING: $name has no pinnedRef -- installing from HEAD is a supply chain risk."
        read -rp "  Continue anyway? (y/N): " answer
        if [[ ! "$answer" =~ ^[yY] ]]; then
            skip "Skipped $name (unpinned, user declined)."
            FAILED_COUNT=$((FAILED_COUNT + 1))
            continue
        fi
    fi

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

    # Pin to specific ref (tag or SHA) if specified in manifest
    if [[ -n "$pinned_ref" ]]; then
        step "Pinning $name to ref $pinned_ref..."
        pushd "$clone_dir" > /dev/null
        if git fetch --depth 1 origin "$pinned_ref" 2>/dev/null && git checkout FETCH_HEAD 2>/dev/null; then
            ok "Pinned to $pinned_ref"
        elif git checkout "$pinned_ref" 2>/dev/null; then
            ok "Checked out $pinned_ref"
        else
            err "Failed to pin $name to $pinned_ref. Using HEAD."
        fi
        popd > /dev/null
    fi

    # Run skill scan if requested
    if [[ "$do_scan" == "true" && -x "bin/skill-scan.sh" ]]; then
        step "Running skill scan on $name..."
        if ! "bin/skill-scan.sh" "$clone_dir" "$name"; then
            err "Skill scan found dangerous patterns in $name."
            read -rp "  Install anyway? (y/N): " answer
            if [[ ! "$answer" =~ ^[yY] ]]; then
                skip "Skipped $name (scan findings, user declined)."
                FAILED_COUNT=$((FAILED_COUNT + 1))
                continue
            fi
        fi
    fi

    # Run install command
    SCAN_CLEAN=true
    if [[ -n "$install_cmd" && "$install_cmd" != "null" ]]; then
        ALLOWED_PREFIXES=("npm install" "npm ci" "pip install" "uv pip install" "uv sync" "npx" "cargo install" "go install" "echo")
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
            SCAN_CLEAN=false
        fi
        popd > /dev/null
    else
        INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
    fi

    # Mark as installed
    touch "$clone_dir/.installed"

    # Compute directory hash for SECURITY-LOCK.json
    DIR_HASH=""
    if command -v sha256sum &>/dev/null; then
        DIR_HASH=$(find "$clone_dir" -type f -not -path '*/.git/*' -print0 | sort -z | xargs -0 sha256sum 2>/dev/null | sha256sum | cut -d' ' -f1)
    elif command -v shasum &>/dev/null; then
        DIR_HASH=$(find "$clone_dir" -type f -not -path '*/.git/*' -print0 | sort -z | xargs -0 shasum -a 256 2>/dev/null | shasum -a 256 | cut -d' ' -f1)
    fi

    LOCK_ENTRIES="${LOCK_ENTRIES}    { \"name\": \"$name\", \"pinnedRef\": \"${pinned_ref:-HEAD}\", \"dirHash\": \"sha256:${DIR_HASH:-unknown}\", \"scanClean\": $SCAN_CLEAN },\n"

    # Copy skills if applicable
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

# -- Generate SECURITY-LOCK.json --------------------------------------------

if [[ -n "$LOCK_ENTRIES" ]]; then
    LOCK_ENTRIES="${LOCK_ENTRIES%,\\n}"
    GENERATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")
    cat > "$LOCK_FILE" <<LOCKEOF
{
  "generated": "$GENERATED_AT",
  "tools": [
$(echo -e "$LOCK_ENTRIES")
  ]
}
LOCKEOF
    ok "Generated $LOCK_FILE"
fi

# -- Verify foundational rules -----------------------------------------------

echo ""
RULE_FILES=("00-starter-rules.mdc" "01-mdd.mdc" "02-kingmode.mdc" "03-frontend-fullstack.mdc" "04-security-policy.mdc")
RULES_OK=0
for rf in "${RULE_FILES[@]}"; do
    if [[ -f "$CURSOR_DIR/rules/$rf" ]]; then
        ok "Rule verified: $rf"
        RULES_OK=$((RULES_OK + 1))
    else
        err "Missing rule: $rf -- workspace may be incomplete."
    fi
done

# -- Detect environment -------------------------------------------------------

IS_DEVCONTAINER=false
if [[ -n "${REMOTE_CONTAINERS:-}" ]] || [[ -n "${CODESPACES:-}" ]] || [[ -f "/.dockerenv" ]]; then
    IS_DEVCONTAINER=true
fi

# -- Final banner -------------------------------------------------------------

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
echo -e "  MDD dirs:        11 (full V1.4 structure)"
if [[ -f "$LOCK_FILE" ]]; then
    echo -e "  Security lock:   $LOCK_FILE (generated)"
fi
echo ""

if $IS_DEVCONTAINER; then
    echo -e "${CYAN}  Dev Container detected. Workspace is ready.${RESET}"
else
    echo -e "${YELLOW}  Restart Cursor to activate rules and tool integrations.${RESET}"
fi

echo ""

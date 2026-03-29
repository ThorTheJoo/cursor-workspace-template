<#
.SYNOPSIS
    Cursor Workspace Starter — PowerShell Tool Bootstrapper
.DESCRIPTION
    Parses tools/manifest.json, presents an interactive selection menu,
    clones selected repos into .tools-cache/, runs install commands,
    and ensures .cursor/ directories are properly structured.
    Idempotent: safe to run multiple times.
.NOTES
    Requires: git, PowerShell 5.1+
    Optional: npm/npx (for CLI tools), uv (for Python tools)
#>

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# ── Colors & helpers ────────────────────────────────────────────────

function Write-Banner {
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host "   Cursor Workspace Starter — Bootstrapper" -ForegroundColor Cyan
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step([string]$msg) {
    Write-Host "[>>] $msg" -ForegroundColor Yellow
}

function Write-Ok([string]$msg) {
    Write-Host "[OK] $msg" -ForegroundColor Green
}

function Write-Skip([string]$msg) {
    Write-Host "[--] $msg" -ForegroundColor DarkGray
}

function Write-Err([string]$msg) {
    Write-Host "[!!] $msg" -ForegroundColor Red
}

# ── Preflight checks ───────────────────────────────────────────────

Write-Banner

$gitVersion = $null
try { $gitVersion = git --version 2>&1 } catch {}
if (-not $gitVersion) {
    Write-Err "git is not installed or not on PATH. Install git and retry."
    exit 1
}
Write-Ok "git detected: $gitVersion"

$manifestPath = Join-Path $ScriptDir "tools\manifest.json"
if (-not (Test-Path $manifestPath)) {
    Write-Err "tools/manifest.json not found at $manifestPath"
    exit 1
}

# ── Parse manifest ──────────────────────────────────────────────────

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$tools = $manifest.tools

if ($tools.Count -eq 0) {
    Write-Err "No tools found in manifest. Add entries to tools/manifest.json first."
    exit 1
}

Write-Ok "Found $($tools.Count) tool(s) in manifest."
Write-Host ""

# ── Interactive selection ───────────────────────────────────────────

$selectedTools = @()

foreach ($tool in $tools) {
    $platformOk = ($tool.platform -eq "both") -or ($tool.platform -eq "win")
    if (-not $platformOk) {
        Write-Skip "$($tool.name) — unix-only, skipping on Windows."
        continue
    }

    $gpuRequired = $false
    if ($tool.PSObject.Properties.Name -contains "requiresGpu") {
        $gpuRequired = $tool.requiresGpu
    }

    $label = "$($tool.name) — $($tool.description)"
    if ($gpuRequired) { $label += " [REQUIRES GPU]" }

    Write-Host "  $label" -ForegroundColor White
    $answer = Read-Host "  Install? (y/N)"

    if ($answer -match "^[yY]") {
        $selectedTools += $tool
        Write-Ok "Selected: $($tool.name)"
    }
    else {
        Write-Skip "Skipped: $($tool.name)"
    }
    Write-Host ""
}

if ($selectedTools.Count -eq 0) {
    Write-Host ""
    Write-Step "No tools selected. Ensuring directory structure only."
}

# ── Ensure .cursor directories ──────────────────────────────────────

$dirs = @(
    ".cursor\rules",
    ".cursor\bin",
    ".cursor\skills",
    ".cursor\mcp",
    ".cursor\automations"
)

foreach ($d in $dirs) {
    $fullPath = Join-Path $ScriptDir $d
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Ok "Created $d"
    }
}

# ── Ensure .tools-cache exists ──────────────────────────────────────

$cachePath = Join-Path $ScriptDir ".tools-cache"
if (-not (Test-Path $cachePath)) {
    New-Item -ItemType Directory -Path $cachePath -Force | Out-Null
}

# ── Clone and install selected tools ────────────────────────────────

foreach ($tool in $selectedTools) {
    Write-Host ""
    Write-Step "Installing $($tool.name)..."

    $cloneDir = Join-Path $cachePath $tool.name

    # Idempotency: skip clone if dir exists
    if (Test-Path $cloneDir) {
        Write-Skip "$($tool.name) already cloned at $cloneDir — skipping clone."
    }
    else {
        Write-Step "Cloning $($tool.repo)..."
        try {
            git clone --depth 1 $tool.repo $cloneDir 2>&1 | Out-Null
            Write-Ok "Cloned $($tool.name)"
        }
        catch {
            Write-Err "Failed to clone $($tool.name): $_"
            Write-Err "Skipping install for $($tool.name)."
            continue
        }
    }

    # Run install command
    if ($tool.installCmd) {
        Write-Step "Running install: $($tool.installCmd)"
        $originalDir = Get-Location
        try {
            Set-Location $cloneDir
            Invoke-Expression $tool.installCmd
            Write-Ok "Installed $($tool.name)"
        }
        catch {
            Write-Err "Install failed for $($tool.name): $_"
            Write-Err "You may need to install manually. Check the tool's README."
        }
        finally {
            Set-Location $originalDir
        }
    }

    # Post-install: copy skills if type is "skills"
    if ($tool.type -eq "skills") {
        $skillsSource = Join-Path $cloneDir "skills"
        $skillsDest = Join-Path $ScriptDir ".cursor\skills"
        if (Test-Path $skillsSource) {
            Write-Step "Copying skills from $($tool.name) into .cursor/skills/..."
            Copy-Item -Path "$skillsSource\*" -Destination $skillsDest -Recurse -Force
            Write-Ok "Skills copied for $($tool.name)"
        }
    }
}

# ── Verify foundational rules exist ────────────────────────────────

$ruleFiles = @("00-starter-rules.mdc", "01-mdd.mdc", "02-kingmode.mdc", "03-frontend-fullstack.mdc")
$rulesDir = Join-Path $ScriptDir ".cursor\rules"

foreach ($rf in $ruleFiles) {
    $rulePath = Join-Path $rulesDir $rf
    if (Test-Path $rulePath) {
        Write-Ok "Rule file verified: $rf"
    }
    else {
        Write-Err "Missing rule file: $rf — your workspace may be incomplete."
    }
}

# ── Detect environment ──────────────────────────────────────────────

$isDevContainer = $false
if ($env:REMOTE_CONTAINERS -or $env:CODESPACES) {
    $isDevContainer = $true
}

# ── Final banner ────────────────────────────────────────────────────

Write-Host ""
Write-Host "  ========================================" -ForegroundColor Green
Write-Host "   Setup Complete" -ForegroundColor Green
Write-Host "  ========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Tools installed: $($selectedTools.Count) / $($tools.Count)" -ForegroundColor White
Write-Host "  Rules verified:  $($ruleFiles.Count) foundational .mdc files" -ForegroundColor White
Write-Host ""

if ($isDevContainer) {
    Write-Host "  Dev Container detected. Workspace is ready." -ForegroundColor Cyan
}
else {
    Write-Host "  Restart Cursor to activate rules and tool integrations." -ForegroundColor Yellow
}

Write-Host ""

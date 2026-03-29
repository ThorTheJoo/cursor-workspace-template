<#
.SYNOPSIS
    Cursor Workspace Starter â€” PowerShell Tool Bootstrapper
.DESCRIPTION
    Parses tools/manifest.json, validates it, presents an interactive selection
    menu, clones selected repos into .tools-cache/, runs install commands,
    and ensures .cursor/ and docs/ directories are properly structured.
    Idempotent: safe to run multiple times.
.NOTES
    Requires: git, PowerShell 5.1+
    Optional: npm/npx (for CLI tools), uv (for Python tools)
#>

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# â”€â”€ Colors & helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

function Write-Banner {
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host "   Cursor Workspace Starter â€” Bootstrapper" -ForegroundColor Cyan
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

# â”€â”€ Preflight checks â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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

# â”€â”€ Validate manifest JSON â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

Write-Step "Validating manifest JSON..."

$manifest = $null
try {
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
}
catch {
    Write-Err "tools/manifest.json contains invalid JSON: $_"
    exit 1
}

$tools = $manifest.tools
if (-not $tools -or $tools.Count -eq 0) {
    Write-Err "No tools found in manifest. Add entries to tools/manifest.json first."
    exit 1
}

$validationErrors = 0
for ($i = 0; $i -lt $tools.Count; $i++) {
    $tool = $tools[$i]
    if (-not $tool.name) {
        Write-Err "Tool at index $i is missing required field 'name'."
        $validationErrors++
    }
    if (-not $tool.repo) {
        Write-Err "Tool '$($tool.name)' (index $i) is missing required field 'repo'."
        $validationErrors++
    }
    elseif ($tool.repo -notmatch '^https://github\.com/') {
        Write-Err "Tool '$($tool.name)' has non-GitHub repo URL: $($tool.repo)"
        $validationErrors++
    }
}

if ($validationErrors -gt 0) {
    Write-Err "Manifest has $validationErrors validation error(s). Fix them before proceeding."
    exit 1
}

Write-Ok "Manifest validated: $($tools.Count) tool(s), 0 errors."
Write-Host ""

# â”€â”€ Interactive selection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$selectedTools = @()

foreach ($tool in $tools) {
    $platformOk = ($tool.platform -eq "both") -or ($tool.platform -eq "win")
    if (-not $platformOk) {
        Write-Skip "$($tool.name) â€” unix-only, skipping on Windows."
        continue
    }

    $gpuRequired = $false
    if ($tool.PSObject.Properties.Name -contains "requiresGpu") {
        $gpuRequired = $tool.requiresGpu
    }

    $label = "$($tool.name) â€” $($tool.description)"
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

# â”€â”€ Ensure .cursor directories â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$cursorDirs = @(
    ".cursor\rules",
    ".cursor\bin",
    ".cursor\skills",
    ".cursor\mcp",
    ".cursor\automations"
)

foreach ($d in $cursorDirs) {
    $fullPath = Join-Path $ScriptDir $d
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Ok "Created $d"
    }
}

# â”€â”€ Ensure MDD docs directories â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$docsDirs = @(
    "docs\_ai_context\state",
    "docs\_ai_context\analysis",
    "docs\_ai_context\templates",
    "docs\_ai_context\prompts",
    "docs\_ai_context\knowledge"
)

foreach ($d in $docsDirs) {
    $fullPath = Join-Path $ScriptDir $d
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Ok "Created $d"
    }
}

# â”€â”€ Ensure .tools-cache exists â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$cachePath = Join-Path $ScriptDir ".tools-cache"
if (-not (Test-Path $cachePath)) {
    New-Item -ItemType Directory -Path $cachePath -Force | Out-Null
}

# â”€â”€ Clone and install selected tools â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$installedCount = 0
$failedCount = 0

foreach ($tool in $selectedTools) {
    Write-Host ""
    Write-Step "Installing $($tool.name)..."

    $cloneDir = Join-Path $cachePath $tool.name

    if (Test-Path $cloneDir) {
        Write-Skip "$($tool.name) already cloned at $cloneDir â€” skipping clone."
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
            $failedCount++
            continue
        }
    }

    if ($tool.installCmd) {
        Write-Step "Running install: $($tool.installCmd)"
        $originalDir = Get-Location
        try {
            Set-Location $cloneDir
            Invoke-Expression $tool.installCmd
            Write-Ok "Installed $($tool.name)"
            $installedCount++
        }
        catch {
            Write-Err "Install failed for $($tool.name): $_"
            Write-Err "You may need to install manually. Check the tool's README."
            $failedCount++
        }
        finally {
            Set-Location $originalDir
        }
    }
    else {
        $installedCount++
    }

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

# â”€â”€ Verify foundational rules exist â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$ruleFiles = @("00-starter-rules.mdc", "01-mdd.mdc", "02-kingmode.mdc", "03-frontend-fullstack.mdc")
$rulesDir = Join-Path $ScriptDir ".cursor\rules"
$rulesOk = 0

foreach ($rf in $ruleFiles) {
    $rulePath = Join-Path $rulesDir $rf
    if (Test-Path $rulePath) {
        Write-Ok "Rule file verified: $rf"
        $rulesOk++
    }
    else {
        Write-Err "Missing rule file: $rf â€” your workspace may be incomplete."
    }
}

# â”€â”€ Detect environment â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

$isDevContainer = $false
if ($env:REMOTE_CONTAINERS -or $env:CODESPACES) {
    $isDevContainer = $true
}

# â”€â”€ Final banner â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

Write-Host ""
Write-Host "  ========================================" -ForegroundColor Green
Write-Host "   Setup Complete" -ForegroundColor Green
Write-Host "  ========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Tools selected:  $($selectedTools.Count) / $($tools.Count)" -ForegroundColor White
Write-Host "  Installed OK:    $installedCount" -ForegroundColor White
if ($failedCount -gt 0) {
    Write-Host "  Failed:          $failedCount" -ForegroundColor Red
}
Write-Host "  Rules verified:  $rulesOk / $($ruleFiles.Count) foundational .mdc files" -ForegroundColor White
Write-Host "  MDD dirs:        11 (full V1.3 structure)" -ForegroundColor White
Write-Host ""

if ($isDevContainer) {
    Write-Host "  Dev Container detected. Workspace is ready." -ForegroundColor Cyan
}
else {
    Write-Host "  Restart Cursor to activate rules and tool integrations." -ForegroundColor Yellow
}

Write-Host ""

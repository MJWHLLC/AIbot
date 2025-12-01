<#
PowerShell helper to create a GitHub repository using the GitHub CLI (`gh`) and push the current folder.
Usage (PowerShell):
  .\create_github_repo.ps1 -RepoName "my-repo" -Owner "MJWHLLC" -Visibility public -Description "Paralegal Agent AI bots"

Notes:
- Requires `gh` (GitHub CLI) installed and authenticated: https://cli.github.com/
- If you omit `-Owner`, `gh` will create the repo under your user account.
- This script will:
  1) Initialize git if needed
  2) Create the remote repo with `gh repo create`
  3) Add all files and create an initial commit if none exist
  4) Push to `origin` (main branch)

#>
param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName,

    [string]$Owner = "",
    [ValidateSet('public','private')]
    [string]$Visibility = 'public',
    [string]$Description = "",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$cwd = (Get-Location).Path
Write-Host "Working directory: $cwd"

# Ensure git exists
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is not installed or not in PATH. Install git first."; exit 1
}

# Ensure gh exists
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "Warning: gh (GitHub CLI) not found. The script will still create a local repo and prepare commands for manual creation." -ForegroundColor Yellow
}

# Initialize git repository if it doesn't exist
if (-not (Test-Path .git)) {
    Write-Host "Initializing new git repository..."
    git init
} else {
    Write-Host "Git repository already initialized."
}

# Set default branch name to main if not configured
try {
    $currentBranch = git symbolic-ref --short HEAD 2>$null
} catch {
    $currentBranch = $null
}
if (-not $currentBranch) {
    git checkout -b main
    $currentBranch = 'main'
}

# Stage files and create initial commit if none exists
$hasCommits = $false
try { git rev-parse --verify HEAD > $null 2>&1; $hasCommits = $true } catch { $hasCommits = $false }
if (-not $hasCommits) {
    Write-Host "Creating initial commit..."
    git add -A
    git commit -m "chore: initial commit (paralegal_agent)"
} else {
    Write-Host "Repository already has commits. Skipping initial commit."
}

# Build full repo identifier if Owner provided
$repoIdentifier = if ($Owner -and $Owner.Trim() -ne '') { "$Owner/$RepoName" } else { $RepoName }

if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "Creating GitHub repository $repoIdentifier ($Visibility)..."
    $createArgs = @($repoIdentifier, "--$Visibility")
    if ($Description) { $createArgs += "--description"; $createArgs += $Description }
    if ($Force) { $createArgs += "--confirm" }

    # Use gh to create and set remote
    gh repo create @createArgs --source . --remote origin --push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository created and pushed successfully via gh."
    } else {
        Write-Host "gh returned non-zero exit code. Please verify errors above." -ForegroundColor Yellow
    }
} else {
    Write-Host "gh CLI not found. Showing manual commands to run instead:" -ForegroundColor Yellow
    Write-Host "1) Create a repo on GitHub with name: $RepoName (owner: $Owner, visibility: $Visibility)"
    Write-Host "2) Add remote and push from this folder:" -ForegroundColor Cyan
    Write-Host "   git remote add origin https://github.com/$repoIdentifier.git"
    Write-Host "   git branch -M main"
    Write-Host "   git push -u origin main"
}

Write-Host "Done." -ForegroundColor Green

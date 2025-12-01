#!/usr/bin/env bash
# create_github_repo.sh - create GitHub repo using `gh` CLI or print manual commands
# Usage: ./create_github_repo.sh <repo-name> [owner] [public|private]

set -euo pipefail
REPO_NAME=${1:-}
OWNER=${2:-}
VISIBILITY=${3:-public}
DESCRIPTION=${4:-"Paralegal Agent AI bots"}

if [ -z "$REPO_NAME" ]; then
  echo "Usage: $0 <repo-name> [owner] [public|private] [description]"
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "git not installed; install git first" >&2
  exit 1
fi

if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
fi

# Ensure branch
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
if [ -z "$current_branch" ] || [ "$current_branch" = "HEAD" ]; then
  git checkout -b main
fi

# Create initial commit if none exists
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "Creating initial commit..."
  git add -A
  git commit -m "chore: initial commit (paralegal_agent)"
else
  echo "Repository already has commits."
fi

if command -v gh >/dev/null 2>&1; then
  FULL_NAME="$REPO_NAME"
  if [ -n "$OWNER" ]; then
    FULL_NAME="$OWNER/$REPO_NAME"
  fi
  echo "Creating repo via gh: $FULL_NAME ($VISIBILITY)"
  gh repo create "$FULL_NAME" --$VISIBILITY --description "$DESCRIPTION" --source . --remote origin --push
  echo "Repo created and pushed via gh."
else
  FULL_NAME="$REPO_NAME"
  if [ -n "$OWNER" ]; then
    FULL_NAME="$OWNER/$REPO_NAME"
  fi
  echo "gh CLI not found. Run the following commands to publish manually:" >&2
  echo "  git remote add origin https://github.com/$FULL_NAME.git"
  echo "  git branch -M main"
  echo "  git push -u origin main"
fi

echo "Done."

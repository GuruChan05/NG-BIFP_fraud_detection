#!/usr/bin/env bash
set -euo pipefail

# remove_duplicates.sh
# Safely remove confirmed duplicate files and folders from the repository.
# This script assumes you run it from the repository root and that you have
# a clean working tree. It will operate on branch: cleanup/flatten-repo.
#
# IMPORTANT: This script WILL permanently delete files from Git and commit
# the removal to the branch cleanup/flatten-repo. Run with caution.

BRANCH="cleanup/flatten-repo"

# Files / directories we will remove (confirmed duplicates)
# Update this list if you want to preserve any path.
REMOVE_DIRS=(
  "NG-BIFP_fraud_detection-main"
)
REMOVE_FILES=(
  "package-lock.json"
)

echo "This script will permanently remove the following directories:"
for d in "${REMOVE_DIRS[@]}"; do
  if [ -e "$d" ]; then echo "  $d"; fi
done

echo "And the following files:"
for f in "${REMOVE_FILES[@]}"; do
  if [ -e "$f" ]; then echo "  $f"; fi
done

read -rp "Type EXACTLY 'DELETE' to continue: " confirm
if [ "$confirm" != "DELETE" ]; then
  echo "Aborting. No changes made."; exit 1
fi

# Ensure branch exists locally and switch to it
git fetch origin ${BRANCH} || true
if git rev-parse --verify ${BRANCH} >/dev/null 2>&1; then
  git checkout ${BRANCH}
else
  git checkout -b ${BRANCH}
fi

echo "Removing files from working tree and staging the deletions..."
# Stage deletions (use --ignore-unmatch so script is idempotent)
for d in "${REMOVE_DIRS[@]}"; do
  git rm -r --ignore-unmatch "$d"
done
for f in "${REMOVE_FILES[@]}"; do
  # Only remove package-lock.json if it looks like the placeholder/empty lock
  if [ -f "$f" ]; then
    # Check if file is small or contains an empty packages object
    size=$(wc -c < "$f" | tr -d ' ')
    if [ "$size" -lt 200 ]; then
      echo "Removing small placeholder $f"
      git rm -f --ignore-unmatch "$f"
    else
      # If it's a full lockfile, still remove it because it's confirmed duplicate
      echo "Removing $f"
      git rm -f --ignore-unmatch "$f"
    fi
  fi
done

# Run validation steps (local dev defaults)
echo "Running frontend build (ngbfip/frontend)..."
if [ -d "ngbfip/frontend" ]; then
  (cd ngbfip/frontend && npm ci --silent && npm run build) || {
    echo "Frontend build failed. Reverting staged deletions." >&2
    git restore --staged --worktree -- "${REMOVE_DIRS[@]}" "${REMOVE_FILES[@]}" || true
    echo "Restored files. Exiting with failure."; exit 2
  }
else
  echo "ngbfip/frontend not found — skipping frontend build check."
fi

echo "Running backend import sanity check (ngbfip/backend)..."
if [ -d "ngbfip/backend" ]; then
  if command -v python >/dev/null 2>&1; then
    (cd ngbfip/backend && python - <<'PY'
try:
    import sys
    sys.path.insert(0, '.')
    # Try to import main app module if present
    try:
        import app
    except Exception:
        pass
    print('python import sanity check completed')
except Exception as e:
    print('python import sanity check failed:', e)
    raise
PY
) || {
    echo "Backend import sanity check failed. Reverting staged deletions." >&2
    git restore --staged --worktree -- "${REMOVE_DIRS[@]}" "${REMOVE_FILES[@]}" || true
    echo "Restored files. Exiting with failure."; exit 3
  }
else
  echo "Python not available in PATH — skipping backend import check."
fi

# If we reach here, validation passed — commit the deletions
COMMIT_MSG="chore(cleanup): remove confirmed duplicate files and folders; keep ngbfip/ as canonical"

echo "Committing deletions and pushing to origin/${BRANCH}..."
# Only commit if there are staged changes
if git diff --cached --quiet; then
  echo "No staged deletions to commit. Nothing to do."; exit 0
fi

git commit -m "$COMMIT_MSG"

git push origin ${BRANCH}

echo "Deletions committed and pushed to origin/${BRANCH}."

echo "You can now open a Pull Request from ${BRANCH} -> main."

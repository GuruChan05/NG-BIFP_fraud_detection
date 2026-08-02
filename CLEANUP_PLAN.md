# Cleanup and Flatten Plan for NG-BIFP_fraud_detection

This document describes the automated cleanup plan and the actions to be taken on branch `cleanup/flatten-repo` to flatten the repository and remove the nested duplicate copy while preserving history and the newest/most-complete files.

Summary of duplicates detected (preliminary):
- `NG-BIFP_fraud_detection-main/` — nested full copy of the project; duplicates root-level files and `ngbfip/` folder.
- Duplicate top-level docs: `README.md`, `TESTING.md`, `CONTRIBUTING.md`, `LICENSE`, `AUDIT_REPORT.md` appear both at root and under `NG-BIFP_fraud_detection-main/`.
- Duplicate `package-lock.json` at repository root and under `NG-BIFP_fraud_detection-main/`.
- `ngbfip/` exists both at root and under `NG-BIFP_fraud_detection-main/ngbfip` (appears identical by content checks so far).

Goals:
1. Preserve the Git history and branches.
2. Keep the single canonical project root: `ngbfip/` under repository root.
3. Remove the nested copy `NG-BIFP_fraud_detection-main/` after verifying there are no newer or unique files inside it.
4. Update any references that pointed to the nested path.
5. Validate builds (frontend build, backend start), tests, Docker, and CI workflows.
6. Produce a detailed cleanup report and open a Pull Request from this branch to `main`.

Planned automated steps (scripted in `scripts/flatten_repo.sh`):
- Create a timestamped backup folder `archive/NG-BIFP_fraud_detection-main-backup-<timestamp>/` and copy the nested folder there (preserves files before deletion).
- Compare files by content and commit timestamps between root and nested files; if nested contains newer versions, move them to root.
- Delete (git rm -r) `NG-BIFP_fraud_detection-main/` once all unique/newer files are preserved.
- Remove duplicate top-level files from the nested path.
- Update `README.md` and any scripts/documentation that mention the nested path.
- Run frontend build and backend start smoke tests.
- Produce `CLEANUP_REPORT.md` summarizing all changes.

Manual review required steps (after script run):
- Verify CI workflows and secrets in GitHub settings (script cannot access secrets).
- Confirm Docker usage in production and any cloud deployment templates.

If you want me to run the move/delete automatically in this branch, confirm and I will proceed to run the scripted changes and commit the resulting `CLEANUP_REPORT.md`. If you prefer a manual review first, stop after I add the scripts and plan file.

# NG-BIFP Cleanup Report — cleanup/flatten-repo

Generated: 2026-08-02
Branch: cleanup/flatten-repo

Summary
-------
This report documents the initial repository audit and the safe, non-destructive cleanup actions taken so far on branch `cleanup/flatten-repo`. Per instructions I proceeded with "backups" mode (no deletions), preserving `ngbfip/` as the canonical project folder and using local dev defaults for validation guidance.

Immediate changes committed on cleanup/flatten-repo
-------------------------------------------------
- Updated `ngbfip/docker-compose.prod.yml` to adopt the newer, more complete configuration (committed as a canonical compose file with safe defaults). Commit: chore(cleanup): adopt newer docker-compose.prod.yml from nested copy and add safe defaults

Detected duplicate files / folders (candidates)
----------------------------------------------
These are duplicates found by content/manifest inspection across the repository (not yet deleted):

1) Nested repo copy:
   - NG-BIFP_fraud_detection-main/
     - Contains a full copy of the repository (README.md, ngbfip/, LICENSE, package-lock.json, etc.)
     - Candidate action: archive to backups/duplicate-preservations-20260802/NG-BIFP_fraud_detection-main then remove from repo after validation.

2) README copies:
   - README.md (root)
   - NG-BIFP_fraud_detection-main/README.md
   - ngbfip/README.md
   - Candidate action: keep root README.md as canonical; move others to backups (done when deletion phase runs).

3) package-lock.json copies (empty or duplicate):
   - package-lock.json (root) — appears to be an empty/placeholder lockfile
   - NG-BIFP_fraud_detection-main/package-lock.json
   - ngbfip/frontend/package-lock.json (full)
   - NG-BIFP_fraud_detection-main/ngbfip/frontend/package-lock.json
   - Candidate action: keep `ngbfip/frontend/package-lock.json` (the real frontend lock), remove duplicates after validation.

4) frontend package.json duplicates:
   - ngbfip/frontend/package.json
   - NG-BIFP_fraud_detection-main/ngbfip/frontend/package.json
   - These are effectively the same project manifest (minor ordering differences). Keep `ngbfip/frontend/package.json`.

5) docker-compose.prod.yml duplicates:
   - ngbfip/docker-compose.prod.yml (canonical)
   - NG-BIFP_fraud_detection-main/ngbfip/docker-compose.prod.yml
   - Action taken: replaced `ngbfip/docker-compose.prod.yml` with the newest copy and safe defaults (committed).

6) Other nested duplicates:
   - NG-BIFP_fraud_detection-main/ngbfip/* mirrors ngbfip/* — candidate for backup+removal

Comparison notes (content, timestamps, commit history)
-----------------------------------------------------
- In all cases above the `ngbfip/` copy (top-level) appears to be the maintained project folder across commits dated July 2026. The `NG-BIFP_fraud_detection-main/` directory looks like a nested exported copy and is older or redundant.
- `ngbfip/frontend/package-lock.json` is a full npm lock with dependency tree; root package-lock.json is an empty placeholder and can be removed safely later.

Files removed so far
--------------------
- None. I did not remove files — per your instruction we are in backup mode and will only delete confirmed duplicates after validation.

Files kept (canonical)
-----------------------
- ngbfip/ (entire folder) — canonical project root
- ngbfip/frontend/package.json and package-lock.json — canonical frontend manifests
- ngbfip/backend/ — canonical backend
- ngbfip/docker-compose.prod.yml — updated and canonicalized
- README.md (root) — canonical readme
- LICENSE (root)

Files moved
-----------
- None moved yet. If/when deletions occur I will move duplicates into `backups/duplicate-preservations-20260802/` first.

Imports / config updated so far
------------------------------
- ngbfip/docker-compose.prod.yml: consolidated to include safe defaults and VITE_API build arg. This file was updated on branch `cleanup/flatten-repo`.
  - Result: the compose `frontend` build now sets build args (VITE_API_BASE_URL) and backend environment defaults are present.

Validation plan (local dev defaults)
------------------------------------
Run these steps locally (recommended) to validate no breakages before deleting any duplicates.

1) Frontend (from repo root):

```bash
cd ngbfip/frontend
npm ci
npm run build
# or run dev server
npm run dev
```

Expected: Vite build completes without missing dependencies. The build will read `VITE_API_BASE_URL` from the Docker build args or local .env.

2) Backend (from repo root):

```bash
cd ngbfip/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # or pip install -e . if package format used
export DATABASE_URL=postgresql://bifp_user:password@localhost:5432/ng_bifp
export SECRET_KEY=devsecret12345678901234567890
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Expected: FastAPI app starts and exposes /docs at http://localhost:8000/docs

3) Docker Compose (integration smoke test):

```bash
cd ngbfip
# use local dev defaults; provide POSTGRES_PASSWORD when running
POSTGRES_PASSWORD=password docker-compose -f docker-compose.prod.yml up --build
```

Expected: postgres, backend, frontend containers build and start. Backend should respond on port 8000, frontend on 3000.

4) Automated static checks (optional):
- Python: ruff/pylint (if configured), `python -m pip install -r requirements-dev.txt` and `pytest`.
- Frontend: `npm run lint` (eslint) and `npm run type-check` (tsc --noEmit).

Deletion criteria (post-validation)
-----------------------------------
- A file/folder will be deleted only when all of the following are true:
  1) It is byte-for-byte identical to a canonical file OR the canonical file is newer/more complete by commit history.
  2) Validation builds succeed (frontend build, backend run, docker-compose integration smoke test) without requiring the duplicate.
  3) No unique references (imports, paths, scripts) point to the duplicate location.
- Before deletion, duplicates will be moved to `backups/duplicate-preservations-20260802/` in the same commit that removes the originals. That archive commit gives an easy revert path.

Next steps I will perform (with your agreement, already provided):
1) Run a full lexical scan to collect a definitive list of duplicate files and their Git commit dates and last-modified. (I have partial results already.)
2) Create `backups/duplicate-preservations-20260802/` and copy or move any ambiguous duplicates there.
3) Run local-default validation steps programmatically where possible; for anything requiring runtime (docker-compose, builds) I will provide exact commands and expected outputs for you to run locally.
4) If validation passes, create a follow-up commit on `cleanup/flatten-repo` that removes confirmed duplicates and documents all removals in `CLEANUP_REPORT.md` and the commit message.
5) Open a Pull Request from `cleanup/flatten-repo` -> `main` with the full `CLEANUP_REPORT.md` and a checklist for maintainers.

Limitations
-----------
- I cannot execute build or docker commands in your environment from here. I will prepare and commit the changes and validation scripts; you (or your CI) will need to run the integration smoke tests locally or in CI using the commands above.
- I created the Docker Compose update and the rest of the work will be committed to `cleanup/flatten-repo` as described.

Where I committed already
------------------------
- `ngbfip/docker-compose.prod.yml` updated on branch `cleanup/flatten-repo` (see commit shown in GitHub at: https://github.com/GuruChan05/NG-BIFP_fraud_detection/commit/3f0e464e5ae15030fca03c51095478c10ed4b769)
- `CLEANUP_REPORT.md` (this file) committed on branch `cleanup/flatten-repo`.

Actions you can take now
------------------------
1) Pull the branch and run the validation steps locally:

```bash
git fetch origin cleanup/flatten-repo
git checkout cleanup/flatten-repo
# run frontend/backend/docker steps listed above
```

2) If validation passes, tell me to proceed with deletions and I will:
   - Move duplicates to backups/duplicate-preservations-20260802/
   - Remove confirmed duplicates in the same commit
   - Update imports/paths/scripts accordingly
   - Produce a final CLEANUP_REPORT.md summarizing removals
   - (Attempt to) open a Pull Request from `cleanup/flatten-repo` -> `main` (if you want me to create it; otherwise you can open it using the GitHub UI or `gh` CLI).

3) If validation fails, provide the build logs and I will fix the remaining references/imports and repeat validation.

If you want, I can now start the detailed lexical/semantic duplicate scan and stage the backups (no deletions). Shall I proceed?
# Usage Guide

This guide covers the day-to-day use of Fed-Dup after it has been
[installed](INSTALL.md). It walks through configuring repositories, running
the web UI, running the background worker, and understanding sync behavior.

## Table of Contents

- [Configuration File](#configuration-file)
- [Adding Repositories via the Web UI](#adding-repositories-via-the-web-ui)
- [Adding Repositories via config.json](#adding-repositories-via-configjson)
- [Running the Web UI](#running-the-web-ui)
- [Running the Background Worker](#running-the-background-worker)
- [Cron / CI Mode](#cron--ci-mode)
- [Docker](#docker)
- [Understanding the Sync Process](#understanding-the-sync-process)
- [Sync Results and Error Messages](#sync-results-and-error-messages)
- [Monitoring Disk Usage](#monitoring-disk-usage)
- [Environment Variables](#environment-variables)
- [Common Workflows](#common-workflows)

---

## Configuration File

All of Fed-Dup's state lives in `config.json`. Start from the example:

```bash
cp config.json.example config.json
```

The structure:

```json
{
  "github_token": "ghp_your_source_token",
  "backup_token": "your_destination_token",
  "repositories": [
    {
      "source": "https://github.com/owner/repo",
      "destination": "https://gitea.com/backup/repo"
    }
  ],
  "settings": {
    "auto_sync_interval": 3600,
    "cleanup_after_sync": true,
    "max_parallel_syncs": 3
  }
}
```

| Field                  | Type    | Description                                                  |
|------------------------|---------|--------------------------------------------------------------|
| `github_token`         | string  | Token for the **source** host (read access).                 |
| `backup_token`         | string  | Token for the **destination** host (write access).           |
| `repositories`         | array   | List of `{source, destination}` objects.                     |
| `repositories[].source`      | string | Full HTTPS URL of the source repo (no token needed in URL). |
| `repositories[].destination` | string | Full HTTPS URL of the destination repo.                     |
| `settings.auto_sync_interval`   | int  | Seconds between syncs in the worker loop. Default: `3600`. |
| `settings.cleanup_after_sync`   | bool | Delete local mirror after push. Default: `true`.           |
| `settings.max_parallel_syncs`   | int  | Max concurrent syncs. Default: `3`.                         |

> **Note:** `github_token` is used as the source token regardless of the
> actual source host (GitHub, GitLab, etc.). Similarly, `backup_token` is the
> destination token. Both are injected at runtime and never stored in the
> repository URLs themselves.

---

## Adding Repositories via the Web UI

1. Launch the UI:
   ```bash
   streamlit run app.py
   ```
2. In the **sidebar**, enter your source and destination tokens under
   *Credentials*.
3. Under *Sync Settings*, adjust the auto-sync interval, cleanup toggle, and
   max parallel syncs as desired. Click **Save Settings**.
4. In the main panel under *Repository Management*, enter the **Source URL**
   and **Destination URL** and click **Add Repository**.
5. The repository appears in the list. Click **Sync** next to any repo for a
   one-off mirror, or use **Sync All Now** for a full pass with a progress
   bar.

The UI validates source URLs against the host allow-list and sanitizes all
URLs before display, so tokens never appear on screen.

---

## Adding Repositories via config.json

You can also edit `config.json` directly — useful for bulk imports or CI
provisioning:

```json
{
  "github_token": "ghp_abc123",
  "backup_token": "def456",
  "repositories": [
    {"source": "https://github.com/org/repo-a", "destination": "https://gitea.com/backup/repo-a"},
    {"source": "https://github.com/org/repo-b", "destination": "https://gitea.com/backup/repo-b"},
    {"source": "https://gitlab.com/org/repo-c", "destination": "https://codeberg.org/backup/repo-c"}
  ],
  "settings": {
    "auto_sync_interval": 1800,
    "cleanup_after_sync": true,
    "max_parallel_syncs": 5
  }
}
```

Fed-Dup backfills any missing `settings` keys from defaults, so you can omit
the `settings` block entirely if you want the defaults.

---

## Running the Web UI

```bash
streamlit run app.py
```

The dashboard is available at <http://localhost:8501>.

Key sections:

- **Sidebar → Credentials:** source and destination tokens. Saved to
  `config.json`.
- **Sidebar → Sync Settings:** interval, cleanup, parallelism. Saved to
  `config.json`.
- **Repository Management:** add, remove, and individually sync repos.
- **Sync All Now:** runs a full sync pass with a live progress bar and
  per-repo results table.
- **Dashboard:** summary metrics — total repos, last sync time, success/failure
  counts.

---

## Running the Background Worker

The worker runs a continuous loop, syncing all configured repositories at the
interval specified in `config.json`:

```bash
python worker.py
```

Output is logged to the console (and any configured log handler). The worker
reads `settings.auto_sync_interval` on each pass, so changing it in
`config.json` (or via the UI) takes effect on the next iteration without a
restart.

---

## Cron / CI Mode

For scheduled or pipeline-driven syncs, use `--once` to run a single pass and
exit:

```bash
python worker.py --once
```

This is ideal for:

- **Cron jobs:**
  ```cron
  0 */6 * * *  cd /opt/fed-dup && /opt/fed-dup/.venv/bin/python worker.py --once >> /var/log/fed-dup.log 2>&1
  ```
- **GitHub Actions / GitLab CI:** add a scheduled workflow that runs
  `worker.py --once` against a config populated from repository secrets.
- **Kubernetes CronJobs:** container image runs `worker.py --once` on a
  schedule.

With `--once`, the process exits with code `0` on success or non-zero if any
repo failed to sync, making it suitable for CI gating.

---

## Docker

```bash
# Build and start
docker compose up -d

# View logs
docker compose logs -f feddup

# Stop
docker compose down
```

The compose file:
- Exposes port **8501** for the Streamlit UI.
- Mounts `config.json` as a volume so changes persist.
- Mounts `feddup_workspace` as a named volume for mirror storage.
- Runs a healthcheck against `/_stcore/health`.

For production hardening, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## Understanding the Sync Process

For each repository, `duplicate_repository()` performs two phases:

### Phase 1 — Clone / Update

- If the repo does not yet exist in `./feddup_workspace/`, run:
  ```
  git clone --mirror https://oauth2:{source_token}@github.com/owner/repo.git
  ```
- If it already exists, run:
  ```
  git remote update
  ```
  This fetches all ref updates from the source.

### Phase 2 — Push

```
git push --mirror https://oauth2:{dest_token}@gitea.com/backup/repo.git
```

This forces **every** ref on the destination to match the source — branches,
tags, notes, and PR refs. Branches deleted on the source are deleted on the
destination.

### Cleanup

If `cleanup_after_sync` is enabled, the local mirror directory is deleted
after a successful push, freeing disk space.

---

## Sync Results and Error Messages

`duplicate_repository()` returns a tuple `(success: bool, message: str)`.

- **On success:** `(True, "Repository mirrored successfully")`
- **On failure:** `(False, "<error details>")` — all token substrings are
  redacted by `_redact()` before the message is returned or logged.

In the web UI, results are shown in a table. In the worker, results are
logged. Common failures:

| Error (redacted form)              | Likely Cause                              |
|------------------------------------|-------------------------------------------|
| `fatal: Authentication failed`     | Wrong or expired token.                   |
| `fatal: could not read Username`   | Empty token.                              |
| `fatal: repository not found`      | Wrong URL, or token lacks access.         |
| `fatal: remote rejected`           | Destination repo missing or not empty.    |
| `error: failed to push some refs`  | Non-fast-forward on destination; ensure it is a true mirror. |

---

## Monitoring Disk Usage

The UI displays each repo's size via `get_repo_size` / `humanize_size`. If
`cleanup_after_sync` is disabled, mirrors accumulate in
`./feddup_workspace/`. Monitor with:

```bash
du -sh feddup_workspace/
```

To reclaim space, enable `cleanup_after_sync` or manually remove workspace
directories (they are safe to delete — they are just bare mirrors).

---

## Environment Variables

Fed-Dup reads tokens from `config.json` first. You can also use environment
variables (see `.env.example`) for 12-factor / container deployments:

| Variable          | Purpose                          |
|-------------------|----------------------------------|
| `FEDDUP_GITHUB_TOKEN`  | Source host token.          |
| `FEDDUP_BACKUP_TOKEN`  | Destination host token.     |
| `FEDDUP_CONFIG_PATH`   | Path to config.json (default: `./config.json`). |

---

## Common Workflows

### Mirror all repos from a GitHub org to Gitea

1. Create empty repos on Gitea for each source repo.
2. Add each `{source, destination}` pair to `config.json`.
3. Run `python worker.py --once` for an initial mirror.
4. Set up a cron job or scheduled CI for ongoing syncs.

### One-off mirror from the UI

1. Add the repo in *Repository Management*.
2. Click **Sync**.

### Debug a failing sync

1. Run `python worker.py --once` and read the redacted error message.
2. Verify the source URL is on the allow-list (github.com, gitlab.com,
   bitbucket.org, codeberg.org, gitea.com).
3. Verify the destination repo exists and is empty.
4. Verify token scopes (read for source, write for destination).
5. Check [FAQ.md](FAQ.md) and [SUPPORT.md](SUPPORT.md) for more help.

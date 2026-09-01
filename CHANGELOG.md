# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Parallel sync execution with configurable concurrency pool.
- Webhook-triggered sync (push to source → mirror immediately).
- per-repository sync scheduling (cron expressions).
- Mirror status history and failure retry with backoff.
- Optional S3 / object-storage destination backend.

---

## [1.0.0] — 2025-09-01

### Added
- **Core engine** (`feddup/engine.py`): `duplicate_repository()` implementing
  a two-phase mirror — `git clone --mirror` / `git remote update` followed by
  `git push --mirror` — with token injection via the
  `https://oauth2:{token}@host` URL form.
- **Configuration module** (`feddup/config.py`): JSON-based, database-free
  config with `load_config`, `save_config`, `add_repository`,
  `remove_repository`, `get_repository_count`, `get_repositories`, and
  `get_setting`. Forward-compatible: missing keys are backfilled from
  `DEFAULT_SETTINGS`.
- **Utilities** (`feddup/utils.py`): `sanitize_git_url` (strips embedded
  credentials while preserving the `https://` protocol and `.git` suffix),
  `validate_source_url` (host allow-list for GitHub, GitLab, Bitbucket,
  Codeberg, Gitea), `validate_destination_url`, `cleanup_workspace`,
  `get_repo_size`, `humanize_size`.
- **Logger** (`feddup/logger.py`): idempotent `get_logger(name)` with
  `propagate = False` to prevent duplicate log lines.
- **Streamlit web UI** (`app.py`): sidebar credentials and sync settings,
  repository add / remove / sync, "Sync All Now" with a live progress bar,
  and a dashboard with summary metrics. Loads custom `styles.css` when
  present.
- **Background worker** (`worker.py`): continuous `auto_sync_loop()` reading
  the interval from config, plus `--once` mode for cron / CI pipelines.
- **Token redaction** (`feddup/engine._redact`): all error messages and
  subprocess output are scrubbed of token substrings before logging or
  returning to the caller.
- **Test suite** (`tests/`): 46 pytest tests covering utils, config, and
  engine (with `subprocess.run` mocked via `patch`).
- **Deployment**: `Dockerfile` (python:3.11-slim, git + curl, healthcheck
  against `/_stcore/health`), `docker-compose.yml` with named volumes,
  `.dockerignore`, `.env.example`, `config.json.example`.
- **CI/CD**: 16 GitHub Actions workflows — build, test, ci, cd, deploy,
  release, publish, pr (Conventional Commits title validation), stale,
  labeler, greetings, codeql, main, pages, dependency-review, scorecards.
- **Project metadata**: `.github/labeler.yml`, `.github/dependabot.yml`,
  `.github/CODEOWNERS`, issue / PR templates, discussion welcome README.
- **Documentation**: README, CONTRIBUTING, CODE_OF_CONDUCT (Contributor
  Covenant 2.1), SECURITY, CHANGELOG, FAQ, NOTICE, SUPPORT, INSTALL, BUILD,
  DEPLOYMENT, ROADMAP, ADR, AUTHORS, MAINTAINERS, GOVERNANCE, PRICING,
  COPYING, CITATIONS, and the full `docs/` directory.
- **Landing page** (`index.html`) and **social image** (`social-image.png`).
- **Custom stylesheet** (`styles.css`) for the Streamlit UI.

### Security
- `sanitize_git_url` rewritten to preserve the `https://` protocol after
  stripping embedded credentials. The previous regex `re.sub(r'.*@', '', url)`
  inadvertently removed the protocol, causing malformed URLs downstream.
- `config.json` excluded from version control via `.gitignore`.
- All tokens redacted from error paths via `_redact()`.

### Fixed
- `test_no_cleanup_keeps_repo_dir` rewritten so the mocked `subprocess.run`
  actually creates the repo directory on the "clone" call, fixing a false
  negative in the assertion.
- `test_no_protocol_after_strip` updated to expect the protocol to be
  restored by the new `sanitize_git_url` implementation.

---

## Versioning Summary

| Version | Date       | Highlights                                   |
|---------|------------|----------------------------------------------|
| 1.0.0   | 2025-09-01 | Initial stable release — full engine, UI, worker, CI/CD, docs. |

---

[Unreleased]: https://github.com/feddup/fed-dup/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/feddup/fed-dup/releases/tag/v1.0.0

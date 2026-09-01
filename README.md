<div align="center">

# 🛡️ Fed-Dup

### Federated Repository Duplication Engine

**A database-free Git mirroring tool that duplicates repositories to a backup host — built with Python & Streamlit.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/container-Docker-2496ED.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC.svg)](tests/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Lint: flake8](https://img.shields.io/badge/lint-flake8-4B8BBE.svg)](https://flake8.pycqa.org/)

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/feddup)

</div>

---

## ✨ Features

- **Database-free** — all state lives in a single `config.json` file. No SQLite, no Postgres, no Redis.
- **Token-safe** — credentials are injected at runtime and redacted from every error message and log line.
- **Multi-host** — mirror from GitHub, GitLab, Bitbucket, Codeberg, and Gitea to any HTTPS Git destination.
- **Two-phase sync** — `git clone --mirror` / `git remote update` followed by `git push --mirror` for true, ref-for-ref fidelity (branches, tags, notes, PR refs).
- **Web UI** — a Streamlit dashboard for adding/removing repos, editing credentials, and triggering syncs with a live progress bar.
- **Background worker** — a long-running `worker.py` loop or `--once` mode for cron / CI pipelines.
- **Docker-ready** — slim image, healthcheck against `/_stcore/health`, and a `docker-compose.yml` for one-command deploys.
- **CI/CD baked in** — 16 GitHub Actions workflows covering build, test, lint, release, publish, CodeQL, Scorecards, Dependabot, stale triage, and more.
- **Forward-compatible config** — missing keys are backfilled from defaults, so old `config.json` files keep working after upgrades.

## 🚀 Quick Start

### Prerequisites

- Python **3.11+**
- **Git** installed and on `PATH`
- A source-host access token with read scope (GitHub PAT, GitLab token, etc.)
- A destination-host access token with write scope

### Install

```bash
git clone https://github.com/feddup/fed-dup.git
cd fed-dup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Configure

```bash
cp config.json.example config.json
# Edit config.json — add your tokens and repository list
```

### Run the Web UI

```bash
streamlit run app.py
```

The dashboard opens at <http://localhost:8501>.

### Run the background worker

```bash
# Continuous loop (reads interval from config.json)
python worker.py

# Single sync pass (ideal for cron / CI)
python worker.py --once
```

### Docker

```bash
docker compose up -d
# UI at http://localhost:8501
```

## 📖 How It Works

Fed-Dup performs a **true mirror** of each repository:

1. **Clone / update** — if the repo is not yet in the local workspace, it runs `git clone --mirror <source>`. On subsequent syncs it runs `git remote update` to fetch all ref updates.
2. **Push** — it then runs `git push --mirror <destination>`, which forces every ref (branches, tags, notes, pull-request refs, etc.) on the destination to match the source exactly.

Token injection uses the `https://oauth2:{token}@host/path.git` URL form, which is accepted by GitHub, GitLab, Gitea, and Codeberg. Before any URL is logged or displayed, `sanitize_git_url` strips the embedded credentials and ensures the `https://` protocol and `.git` suffix are present.

## 🗂️ Project Structure

```
fed-dup/
├── feddup/                # Core Python package
│   ├── __init__.py        #   Public API re-exports
│   ├── engine.py          #   duplicate_repository() — clone + push
│   ├── config.py          #   JSON config load/save/mutate
│   ├── utils.py           #   URL sanitization, validation, helpers
│   └── logger.py          #   Idempotent logging setup
├── app.py                 # Streamlit web UI
├── worker.py              # Background sync loop / --once mode
├── tests/                 # pytest suite (46 tests)
├── .github/workflows/     # 16 CI/CD workflows
├── docs/                  # Extended documentation
├── Dockerfile             # Slim production image
├── docker-compose.yml     # One-command deploy
└── config.json.example    # Configuration template
```

## ⚙️ Configuration

`config.json` holds everything:

```json
{
  "github_token": "",
  "backup_token": "",
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

| Setting                | Default | Description                                              |
|------------------------|---------|----------------------------------------------------------|
| `auto_sync_interval`   | `3600`  | Seconds between automatic sync passes (worker loop).     |
| `cleanup_after_sync`   | `true`  | Delete the local mirror after each push to save disk.    |
| `max_parallel_syncs`   | `3`     | Maximum concurrent repository syncs.                     |

Environment-variable overrides are documented in [`.env.example`](.env.example).

## 🧪 Testing

```bash
pip install pytest pytest-cov
pytest --cov=feddup --cov-report=term-missing
```

All 46 tests should pass. See [`tests/`](tests/) for the full suite.

## 🤝 Contributing

Contributions are welcome! Please read [**CONTRIBUTING.md**](CONTRIBUTING.md)
for the development workflow, commit-message conventions (Conventional Commits),
and pull-request checklist. By participating you agree to abide by our
[**Code of Conduct**](CODE_OF_CONDUCT.md).

## 📜 License

Fed-Dup is released under the **MIT License**. See [LICENSE](LICENSE) for the
full text.

## 💖 Support

If Fed-Dup saves you time, consider buying us a coffee:

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/feddup)

For bugs and feature requests, please [open an issue](https://github.com/feddup/fed-dup/issues).
For questions and discussion, use [GitHub Discussions](https://github.com/feddup/fed-dup/discussions).

## 🙏 Acknowledgements

Built with [Streamlit](https://streamlit.io/), powered by [Git](https://git-scm.com/),
and inspired by the need for simple, self-hosted repository backups.
See [AUTHORS.md](AUTHORS.md) for the full list of contributors.

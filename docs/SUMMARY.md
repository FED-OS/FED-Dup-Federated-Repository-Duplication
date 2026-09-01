<!-- This document is mirrored from the root [SUMMARY.md](../SUMMARY.md). -->
<!-- The canonical version lives in the repository root. -->

# Summary

## Fed-Dup — Federated Repository Duplication Engine

Fed-Dup is a **database-free Git mirroring tool** built with Python and
Streamlit. It duplicates Git repositories from a source host to a backup
destination host using true Git mirroring, providing an exact, ref-for-ref
copy of each repository.

---

## Problem

Developers and organizations rely on Git hosting platforms (GitHub, GitLab,
Bitbucket, Codeberg, Gitea) for their source code. While these platforms are
generally reliable, they are single points of failure. Account suspensions,
platform outages, accidental deletions, policy changes, and geopolitical
access restrictions can all cause loss of access to critical code. Existing
backup solutions are either commercial (expensive, opaque), database-backed
(heavy, operationally complex), or require manual scripting (fragile,
unmaintained).

## Solution

Fed-Dup provides a simple, self-hosted, database-free alternative:

- **True mirroring** — `git clone --mirror` + `git push --mirror` ensures the
  destination is an exact copy of the source, including all branches, tags,
  notes, and pull-request refs.
- **Database-free** — all state lives in a single `config.json` file. No
  database to install, manage, or back up.
- **Web UI** — a Streamlit dashboard for managing repositories, editing
  credentials, and triggering syncs with live progress feedback.
- **Background worker** — a continuous loop for always-on deployments, plus a
  `--once` mode for cron jobs and CI pipelines.
- **Token-safe** — credentials are injected at runtime and redacted from all
  error messages and logs.
- **Docker-ready** — one-command deployment with healthchecks and persistent
  volumes.

---

## Key Features

1. **Two-phase mirror sync** — clone/update then push, for exact fidelity.
2. **Multi-host support** — GitHub, GitLab, Bitbucket, Codeberg, Gitea as
   sources; any HTTPS Git host as destination.
3. **Streamlit web UI** — add/remove repos, edit settings, sync with progress
   bar, view dashboard metrics.
4. **Background worker** — `auto_sync_loop()` or `--once` for cron/CI.
5. **Token redaction** — `_redact()` scrubs tokens from all output.
6. **URL sanitization** — strips credentials, preserves `https://`, ensures
   `.git` suffix.
7. **Forward-compatible config** — missing keys backfilled from defaults.
8. **Docker + Compose** — slim image, healthcheck, named volumes.
9. **16 CI/CD workflows** — build, test, lint, release, publish, CodeQL,
   Scorecards, Dependabot, stale, labeler, greetings, dependency review.
10. **Comprehensive documentation** — 25+ docs files covering installation,
    usage, deployment, security, contributing, roadmap, and more.

---

## Technical Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Language        | Python 3.11+                        |
| UI Framework    | Streamlit                           |
| Mirroring       | Git (CLI, `--mirror` operations)    |
| Configuration   | JSON (config.json)                  |
| Containerization| Docker, Docker Compose              |
| CI/CD           | GitHub Actions (16 workflows)       |
| Testing         | pytest (46 tests)                   |
| Linting         | flake8, black, mypy, bandit         |
| License         | MIT                                 |

---

## Project Structure (Overview)

```
fed-dup/
├── feddup/              # Core package (engine, config, utils, logger)
├── app.py               # Streamlit web UI
├── worker.py            # Background sync worker
├── tests/               # 46 pytest tests
├── .github/workflows/   # 16 CI/CD workflows
├── docs/                # Extended documentation
├── Dockerfile           # Production container image
├── docker-compose.yml   # One-command deploy
├── config.json.example  # Configuration template
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
├── README.md            # Project overview & quick start
└── ...                  # 25+ additional docs & config files
```

---

## Target Audience

- **Individual developers** who want to back up their personal repos to a
  second host.
- **Small teams and startups** who need a self-hosted mirror without the cost
  and complexity of commercial backup services.
- **Open-source maintainers** who want to mirror their projects to
  decentralized hosts (Codeberg, Gitea) for resilience.
- **DevOps engineers** who need a cron/CI-driven mirroring step in their
  pipeline.
- **Organizations with compliance requirements** that mandate off-platform
  backups of source code.

---

## Getting Started

```bash
git clone https://github.com/feddup/fed-dup.git
cd fed-dup
pip install -r requirements.txt
cp config.json.example config.json  # Edit with your tokens
streamlit run app.py                # Open http://localhost:8501
```

See [INSTALL.md](INSTALL.md) for detailed setup and
[usage.md](usage.md) for daily usage.

---

## Documentation Map

| Document              | Purpose                                           |
|-----------------------|---------------------------------------------------|
| [README.md](README.md) | Project overview, quick start, badges           |
| [INSTALL.md](INSTALL.md) | Step-by-step installation guide               |
| [usage.md](usage.md) | Daily usage, configuration, workflows            |
| [BUILD.md](BUILD.md) | Building from source (package, Docker, docs)     |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment (Docker, K8s, systemd) |
| [SECURITY.md](SECURITY.md) | Security policy & hardening checklist        |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development workflow & PR process     |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards             |
| [CHANGELOG.md](CHANGELOG.md) | Version history & changes                |
| [FAQ.md](FAQ.md)     | Frequently asked questions                        |
| [ROADMAP.md](ROADMAP.md) | Future plans & milestones                     |
| [ADR.md](ADR.md)     | Architecture decision records                     |
| [SUPPORT.md](SUPPORT.md) | Getting help & reporting issues               |
| [NOTICE.md](NOTICE.md) | Copyright, license, third-party acknowledgements |
| [PRICING.md](PRICING.md) | Funding model & sponsorship                  |
| [GOVERNANCE.md](GOVERNANCE.md) | Project governance model                |
| [CITATIONS.md](CITATIONS.md) | How to cite Fed-Dup                     |
| [COPYING.md](COPYING.md) | License & copying information                 |
| [AUTHORS.md](AUTHORS.md) | Contributors list                            |
| [MAINTAINERS.md](MAINTAINERS.md) | Maintainer responsibilities            |
| [docs/](docs/)       | Extended documentation                            |

---

## License

Fed-Dup is released under the **MIT License**. See [LICENSE](LICENSE) and
[COPYING.md](COPYING.md).

## Support the Project

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/feddup)

See [PRICING.md](PRICING.md) for sponsorship details and
[SUPPORT.md](SUPPORT.md) for getting help.

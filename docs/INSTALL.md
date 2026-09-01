<!-- This document is mirrored from the root [INSTALL.md](../INSTALL.md). -->
<!-- The canonical version lives in the repository root. -->

# Installation Guide

This guide walks through installing Fed-Dup from source, verifying the
installation, and performing initial configuration.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1 — Clone the Repository](#step-1--clone-the-repository)
- [Step 2 — Create a Virtual Environment](#step-2--create-a-virtual-environment)
- [Step 3 — Install Dependencies](#step-3--install-dependencies)
- [Step 4 — Create the Configuration File](#step-4--create-the-configuration-file)
- [Step 5 — Verify the Installation](#step-5--verify-the-installation)
- [Step 6 — Run Fed-Dup](#step-6--run-fed-dup)
- [Docker Installation](#docker-installation)
- [Upgrading](#upgrading)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Fed-Dup requires the following on your system:

| Requirement   | Minimum Version | Check Command        |
|---------------|-----------------|----------------------|
| Python        | 3.11            | `python --version`   |
| Git           | 2.25+           | `git --version`      |
| pip           | 23+             | `pip --version`      |

You also need:

- **A source-host access token** with read access to the repositories you want
  to mirror (GitHub PAT, GitLab token, Codeberg/Gitea token).
- **A destination-host access token** with write/push access to the backup
  repository.

### Installing Python

- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install python3.11 python3.11-venv`
- **macOS (Homebrew):** `brew install python@3.11`
- **Windows:** Download from <https://www.python.org/downloads/> (ensure "Add
  to PATH" is checked).

### Installing Git

- **Linux:** `sudo apt install git` (or `dnf install git` on Fedora)
- **macOS:** `brew install git` or install Xcode Command Line Tools
- **Windows:** Download from <https://git-scm.com/download/win>

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/feddup/fed-dup.git
cd fed-dup
```

If you plan to contribute, fork first and clone your fork — see
[CONTRIBUTING.md](CONTRIBUTING.md).

---

## Step 2 — Create a Virtual Environment

Using a virtual environment keeps Fed-Dup's dependencies isolated from your
system Python.

**Linux / macOS:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Your prompt should now show `(.venv)` indicating the environment is active.

---

## Step 3 — Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

For development (testing, linting, type checking):
```bash
pip install -r requirements.txt pytest pytest-cov flake8 black mypy bandit
```

---

## Step 4 — Create the Configuration File

```bash
cp config.json.example config.json
```

Edit `config.json` and fill in:

- `github_token` — your source-host token (read access).
- `backup_token` — your destination-host token (write access).
- `repositories` — your list of `{source, destination}` pairs.
- `settings` — adjust if desired (defaults are fine to start).

**Secure the file:**
```bash
chmod 600 config.json
```

See [usage.md](usage.md) for full configuration details and
[SECURITY.md](SECURITY.md) for hardening guidance.

---

## Step 5 — Verify the Installation

### Check imports

```bash
python -c "import feddup; print(feddup.__version__)"
```

Expected output:
```
1.0.0
```

### Run the test suite (if dev dependencies installed)

```bash
pytest -v
```

All 46 tests should pass.

### Check Git is available

```bash
git --version
```

Fed-Dup shells out to `git` for all mirror operations, so it must be on your
`PATH`.

---

## Step 6 — Run Fed-Dup

### Web UI

```bash
streamlit run app.py
```

Open <http://localhost:8501> in your browser.

### Background worker

```bash
python worker.py
```

### Single-pass (cron / CI)

```bash
python worker.py --once
```

See [usage.md](usage.md) for detailed usage instructions.

---

## Docker Installation

If you prefer containers, Fed-Dup ships with a `Dockerfile` and
`docker-compose.yml`.

### Prerequisites

- Docker 20.10+
- Docker Compose v2+

### Steps

1. Ensure `config.json` exists in the project root (see Step 4 above).

2. Start the container:
   ```bash
   docker compose up -d
   ```

3. Verify it is healthy:
   ```bash
   docker compose ps
   ```
   The health column should show `healthy` after a few seconds.

4. Open <http://localhost:8501>.

For production deployment guidance, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## Upgrading

To upgrade Fed-Dup to a newer version:

```bash
cd fed-dup
git pull origin main
source .venv/bin/activate      # if using a venv
pip install -r requirements.txt --upgrade
```

Fed-Dup's config is forward-compatible — missing keys are backfilled from
defaults, so your existing `config.json` will keep working. Review
[CHANGELOG.md](CHANGELOG.md) for breaking changes between major versions.

If running Docker:
```bash
docker compose pull
docker compose up -d
```

---

## Uninstalling

1. Stop any running worker or Streamlit processes.
2. If using Docker: `docker compose down -v` (the `-v` flag removes volumes).
3. Remove the project directory:
   ```bash
   cd ..
   rm -rf fed-dup
   ```
4. Optionally remove the virtual environment and workspace:
   ```bash
   rm -rf fed-dup/.venv fed-dup/feddup_workspace
   ```

No system-wide changes are made during installation (all dependencies live in
the virtual environment), so uninstallation is clean.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'feddup'`

You are not in the project root, or the virtual environment is not activated.
Run `cd fed-dup && source .venv/bin/activate` and try again.

### `streamlit: command not found`

Streamlit is not installed or the venv is not active. Run
`pip install -r requirements.txt` inside the activated venv.

### `git: command not found`

Install Git (see Prerequisites) and ensure it is on your `PATH`.

### Authentication failed during sync

Your token is wrong, expired, or lacks the required scope. Verify:
- Source token has **read** access to the source repo.
- Destination token has **write** access to the destination repo.
- The destination repo exists and is empty (or already a mirror).

See [FAQ.md](FAQ.md) for more common issues, or [SUPPORT.md](SUPPORT.md) for
where to get help.

<!-- This document is mirrored from the root [BUILD.md](../BUILD.md). -->
<!-- The canonical version lives in the repository root. -->

# Build Guide

This document describes how to build Fed-Dup from source — including the
Python package, the Docker image, and the documentation artifacts. For simply
*running* Fed-Dup, see [INSTALL.md](INSTALL.md) instead.

## Table of Contents

- [Build Prerequisites](#build-prerequisites)
- [Building the Python Package](#building-the-python-package)
- [Building the Docker Image](#building-the-docker-image)
- [Building Documentation](#building-documentation)
- [Running Quality Gates](#running-quality-gates)
- [CI/CD Build Pipeline](#cicd-build-pipeline)
- [Reproducible Builds](#reproducible-builds)

---

## Build Prerequisites

In addition to the runtime prerequisites in [INSTALL.md](INSTALL.md), building
from source requires:

| Tool    | Purpose                          | Install                          |
|---------|----------------------------------|----------------------------------|
| `build` | Python PEP 517 build frontend    | `pip install build`             |
| `wheel` | Wheel creation                   | `pip install wheel`             |
| Docker  | Container image builds           | <https://docs.docker.com/get-docker/> |
| Node.js | (optional) docs site tooling     | <https://nodejs.org/>            |

---

## Building the Python Package

Fed-Dup can be packaged as a standard Python distribution (sdist + wheel).

### 1. Ensure a clean environment

```bash
cd fed-dup
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip build wheel
pip install -r requirements.txt
```

### 2. Run quality gates

Before building, ensure the code passes all checks:

```bash
black --check . && flake8 . && mypy feddup/ && pytest
```

See [Running Quality Gates](#running-quality-gates) below.

### 3. Build the distributions

```bash
python -m build
```

This produces:

```
dist/
├── feddup-1.0.0-py3-none-any.whl   # Wheel
└── feddup-1.0.0.tar.gz             # Source distribution
```

### 4. Verify the wheel

```bash
pip install dist/feddup-1.0.0-py3-none-any.whl
python -c "import feddup; print(feddup.__version__)"
```

### 5. (Optional) Publish to PyPI

> Only maintainers should publish. The `publish` workflow handles this
> automatically on release.

```bash
pip install twine
twine upload dist/*
```

---

## Building the Docker Image

### Using docker compose

```bash
docker compose build
```

This uses the provided `Dockerfile` and tags the image per the compose file.

### Using docker directly

```bash
docker build -t feddup:latest .
docker build -t feddup:1.0.0 .
```

### Verifying the image

```bash
docker run --rm feddup:latest python -c "import feddup; print(feddup.__version__)"
```

Expected output: `1.0.0`

### Image details

The `Dockerfile` is based on `python:3.11-slim` and:

- Installs `git` and `curl` (required for mirror operations and the
  healthcheck).
- Copies the application source.
- Installs Python dependencies.
- Runs the Streamlit UI and the background worker concurrently.
- Defines a healthcheck against `/_stcore/health` on port 8501.

See [DEPLOYMENT.md](DEPLOYMENT.md) for running the image in production.

---

## Building Documentation

Fed-Dup's documentation is written in Markdown and does not require a build
step for reading. However, if you want to generate a static site (e.g., for
GitHub Pages):

### GitHub Pages

The `.github/workflows/pages.yml` workflow automatically builds and deploys
the docs site from the `docs/` directory on pushes to `main`. No local build
is needed — just push and let CI handle it.

### Local preview

The `index.html` landing page can be opened directly in a browser or served
locally:

```bash
python -m http.server 8080
# Open http://localhost:8080/index.html
```

---

## Running Quality Gates

Fed-Dup enforces several quality gates. Run them locally before pushing:

### Formatting (black)

```bash
black feddup/ app.py worker.py tests/
```

Check without modifying:
```bash
black --check feddup/ app.py worker.py tests/
```

### Linting (flake8)

```bash
flake8 feddup/ app.py worker.py tests/
```

### Type checking (mypy)

```bash
mypy feddup/
```

### Security analysis (bandit)

```bash
bandit -r feddup/
```

### Tests (pytest)

```bash
pytest --cov=feddup --cov-report=term-missing
```

### All-in-one

```bash
black --check . && flake8 . && mypy feddup/ && bandit -r feddup/ && pytest --cov=feddup
```

If any gate fails, fix the issue before committing. The CI pipeline runs the
same checks (see the `ci` and `test` workflows).

---

## CI/CD Build Pipeline

Fed-Dup's CI/CD is defined in `.github/workflows/`. The key build-related
workflows:

| Workflow            | Trigger                    | Purpose                              |
|---------------------|----------------------------|--------------------------------------|
| `build.yml`         | push, PR                   | Build the Python package + Docker image |
| `test.yml`          | push, PR                   | Run the pytest suite with coverage   |
| `ci.yml`           | push, PR                   | Lint (flake8, black, mypy, bandit)  |
| `cd.yml`           | push to main (after merge) | Continuous delivery — build & push image |
| `release.yml`       | tag `v*`                  | Create GitHub Release + artifacts    |
| `publish.yml`       | release published          | Publish wheel/sdist to PyPI          |
| `deploy.yml`        | release / manual           | Deploy to hosting environment        |

See `.github/workflows/` for the full list and configuration.

---

## Reproducible Builds

To ensure builds are reproducible:

- **Pin dependencies:** `requirements.txt` uses `>=` minimum versions. For
  fully reproducible builds, generate a lock file:
  ```bash
  pip freeze > requirements.lock
  ```
  and install with `pip install -r requirements.lock`.
- **Pin CI actions:** All GitHub Actions in the workflows use pinned versions
  (and where possible, SHA-pinned for security via Scorecards).
- **Use the same base image:** The Dockerfile pins `python:3.11-slim`. Avoid
  `latest` tags in production.
- **Run in a clean environment:** Always build in a fresh virtual environment
  or container to avoid stale dependencies.

---

## Build Artifacts

The build produces the following artifacts:

| Artifact                          | Location              | Description                    |
|-----------------------------------|-----------------------|--------------------------------|
| Python wheel                      | `dist/*.whl`          | Installable Python package     |
| Source distribution               | `dist/*.tar.gz`       | Source tarball                 |
| Docker image                      | Docker (local/registry) | Container image              |
| Test coverage report              | `htmlcov/`            | HTML coverage report           |
| GitHub Release assets             | GitHub Releases       | Release notes + artifacts      |

Artifacts are uploaded by the CI workflows and attached to GitHub Releases.

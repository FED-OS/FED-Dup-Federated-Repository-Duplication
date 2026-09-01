# Contributing to Fed-Dup

First off — **thank you** for taking the time to contribute! 🎉

Fed-Dup is a community-driven project, and every contribution matters: bug
reports, feature ideas, documentation improvements, code patches, and even
just triaging issues are all welcome.

This document describes the workflow we follow so that the project stays
healthy, consistent, and easy to maintain.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Triaging](#issue-triaging)
- [Releases](#releases)

## Code of Conduct

By participating in this project you agree to abide by the
[Code of Conduct](CODE_OF_CONDUCT.md). Please read it — it is short and
applies to all communication channels (issues, PRs, discussions, chat, etc.).

## Getting Started

### Prerequisites

- Python **3.11 or newer**
- **Git** (with command-line access)
- A GitHub account

### Fork & Clone

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/fed-dup.git
   cd fed-dup
   ```
3. Add the upstream remote so you can sync with the main project:
   ```bash
   git remote add upstream https://github.com/feddup/fed-dup.git
   ```

### Set Up a Development Environment

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black mypy bandit
```

Verify the test suite passes before you start:

```bash
pytest
```

## Development Workflow

1. **Create a branch** from `main` for your work:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feat/my-new-feature
   ```
   Use a descriptive branch name prefixed by type: `feat/`, `fix/`, `docs/`,
   `refactor/`, `test/`, `chore/`.

2. **Make your changes.** Keep commits focused and atomic — one logical change
   per commit.

3. **Run the quality gates locally** (see [Coding Standards](#coding-standards)
   and [Testing](#testing)).

4. **Push to your fork** and open a pull request against `main`.

5. **Respond to review feedback.** Push additional commits — do not force-push
   during review unless a maintainer asks you to squash.

6. **Keep your branch up to date** with upstream `main` to avoid merge
   conflicts:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

## Commit Message Convention

Fed-Dup uses **Conventional Commits**. This enables automated changelog
generation and semantic version bumps.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type       | Purpose                                                        |
|------------|----------------------------------------------------------------|
| `feat`     | A new feature                                                  |
| `fix`      | A bug fix                                                      |
| `docs`     | Documentation only changes                                     |
| `style`    | Code style / formatting (no logic change)                      |
| `refactor` | Code refactoring (no feature, no fix)                          |
| `perf`     | Performance improvement                                        |
| `test`     | Adding or correcting tests                                     |
| `build`    | Build system or dependencies                                   |
| `ci`       | CI/CD configuration changes                                    |
| `chore`    | Miscellaneous maintenance                                      |
| `revert`   | Reverting a previous commit                                    |

### Examples

```
feat(engine): add retry logic for transient push failures
fix(utils): preserve https protocol when stripping credentials
docs(readme): add Docker quick-start section
ci(workflows): pin action versions for reproducibility
```

### Footer

Use the footer for **breaking changes** and **issue references**:

```
feat(config): require explicit destination per repo

BREAKING CHANGE: the global backup_url setting is removed; each
repository must specify its own destination.

Closes #42
```

> 💡 The `pr` workflow automatically validates PR titles against this
> convention. A PR titled `updated stuff` will fail the check.

## Pull Request Process

1. **Fill in the PR template.** It appears automatically when you open a PR.
   Answer every section — even "N/A" is better than a blank field.

2. **Link related issues** using GitHub keywords (`Closes #123`,
   `Refs #456`).

3. **Keep PRs small and focused.** Large PRs are harder to review and slower
   to merge. If your change spans multiple areas, split it into sequential
   PRs.

4. **Ensure CI is green.** All workflows must pass before a maintainer can
   merge. If a check is failing for reasons unrelated to your change, explain
   in a comment.

5. **Request review.** Tag a maintainer or the appropriate CODEOWNER. PRs
   are typically reviewed within 3–5 days.

6. **Merge strategy.** Maintainers use **squash-and-merge** for most PRs to
   keep the history clean. The squash commit message follows Conventional
   Commits.

### PR Checklist (from the template)

- [ ] PR title follows Conventional Commits
- [ ] Tests added / updated and passing (`pytest`)
- [ ] Code is lint-clean (`flake8`) and formatted (`black`)
- [ ] Type-checked (`mypy`) with no new errors
- [ ] Documentation updated if needed
- [ ] No secrets, tokens, or credentials in the diff
- [ ] `config.json` (not `.example`) is not committed

## Coding Standards

| Tool    | Command                  | Purpose                              |
|---------|--------------------------|--------------------------------------|
| `black` | `black feddup/ app.py worker.py tests/` | Formatting (line length 88) |
| `flake8`| `flake8 feddup/ app.py worker.py tests/`| Linting                     |
| `mypy`  | `mypy feddup/`           | Static type checking                 |
| `bandit`| `bandit -r feddup/`      | Security analysis                    |

Run them all before pushing:

```bash
black --check . && flake8 . && mypy feddup/ && bandit -r feddup/
```

### Style Notes

- Use **type hints** on all public functions.
- Keep functions short and focused — prefer pure functions in `utils.py`.
- **Never log or return raw tokens.** Use `feddup.engine._redact()` or
  `feddup.utils.sanitize_git_url()`.
- Prefer f-strings for string formatting.
- Raise specific exceptions; catch only what you handle.

## Testing

- Tests live in `tests/` and use **pytest**.
- Aim to maintain or increase coverage with every PR.
- Unit tests should be fast and deterministic. Mock `subprocess.run` and
  filesystem operations where appropriate — see `tests/test_engine.py` for
  patterns.
- Name test methods descriptively: `test_<scenario>`.

```bash
# Run all tests
pytest

# With coverage
pytest --cov=feddup --cov-report=term-missing --cov-report=html

# Run a single file
pytest tests/test_utils.py

# Verbose
pytest -v
```

## Documentation

- Keep `README.md` accurate and up to date.
- Extended docs live in `docs/`.
- When adding a new feature, document it in the relevant `docs/` page and
  update `CHANGELOG.md` under the `[Unreleased]` section.
- Use Markdown throughout; keep lines under ~100 characters where practical.

## Issue Triaging

- Search existing issues before opening a new one.
- Use the issue templates (bug report, feature request, custom) to provide
  context.
- Add relevant **labels** — the `labeler` workflow does this automatically for
  file-path-based labels, but semantic labels may need manual addition.
- Be respectful and constructive. See the
  [Code of Conduct](CODE_OF_CONDUCT.md).

## Releases

Releases are cut by maintainers following the
[release workflow](.github/workflows/release.yml). The version follows
**Semantic Versioning** (`MAJOR.MINOR.PATCH`):

- **PATCH** — bug fixes, no new features
- **MINOR** — new features, backward-compatible
- **MAJOR** — breaking changes

Each release publishes a GitHub Release with auto-generated notes and, where
applicable, a container image and PyPI package.

---

Questions? Open a [GitHub Discussion](https://github.com/feddup/fed-dup/discussions).
Happy hacking! 🛡️

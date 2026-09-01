<!-- This document is mirrored from the root [FAQ.md](../FAQ.md). -->
<!-- The canonical version lives in the repository root. -->

# Frequently Asked Questions

## General

### What is Fed-Dup?

Fed-Dup (Federated Repository Duplication Engine) is a database-free Git
mirroring tool. It duplicates repositories from a source host (GitHub, GitLab,
Bitbucket, Codeberg, Gitea) to a backup destination host using true Git
mirroring (`git clone --mirror` + `git push --mirror`). It ships with a
Streamlit web UI, a background worker, and Docker support.

### Why "database-free"?

Many mirroring tools require a database (SQLite, Postgres, Redis) to track
state. Fed-Dup stores all configuration and repository state in a single
human-readable `config.json` file. This makes it trivial to back up, inspect,
version-control, and migrate. The trade-off is that it is not designed for
high-throughput, multi-tenant SaaS scenarios — it is a self-hosted backup tool.

### Is Fed-Dup free?

Yes. Fed-Dup is licensed under the **MIT License** and is free to use, modify,
and distribute. See [LICENSE](LICENSE) and [PRICING.md](PRICING.md) for
details.

### Who maintains Fed-Dup?

Fed-Dup is a community project. See [AUTHORS.md](AUTHORS.md) and
[MAINTAINERS.md](MAINTAINERS.md) for the current list of contributors and
maintainers. Governance is described in [GOVERNANCE.md](GOVERNANCE.md).

---

## Setup & Configuration

### What are the prerequisites?

Python 3.11+, Git installed and on `PATH`, and access tokens for your source
and destination hosts. See [INSTALL.md](INSTALL.md) for a step-by-step guide.

### How do I get a source-host token?

- **GitHub:** Settings → Developer settings → Personal access tokens →
  Fine-grained tokens. Grant **read-only** access to the repositories you want
  to mirror.
- **GitLab:** User Settings → Access Tokens. Grant `read_repository`.
- **Codeberg / Gitea:** User Settings → Applications → Generate token. Grant
  read scope.

### How do I get a destination-host token?

You need **write** access on the destination. Create an empty repository on
the destination host first (Fed-Dup does not create repos — it pushes to
existing ones). Then generate a token with push/write scope.

### Where does Fed-Dup store tokens?

Tokens are stored in `config.json` in plaintext. The file is excluded from
version control via `.gitignore`. For production, prefer environment variables
(see `.env.example`) or a secrets manager, and restrict file permissions with
`chmod 600 config.json`. See [SECURITY.md](SECURITY.md) for the full hardening
checklist.

### Can I use SSH instead of HTTPS?

Fed-Dup's token injection uses the HTTPS `oauth2:{token}@` URL form, which
works across GitHub, GitLab, Gitea, and Codeberg. SSH is not currently
supported for the automated path, but you can manually configure SSH-based
remotes and use the worker's `--once` mode with pre-authenticated URLs. SSH
support is on the roadmap.

---

## Usage

### What does "true mirror" mean?

A true mirror (`git push --mirror`) forces **every** ref on the destination to
match the source exactly — branches, tags, notes, pull-request refs, and any
other custom refs. This means:

- **Branches deleted on the source are deleted on the destination.**
- Tags are overwritten if they diverge.
- No merge commit is created — the destination is an exact copy.

If you want an **additive** backup (never delete on destination), Fed-Dup is
not the right tool — consider `git push --all --follow-tags` in a custom
script instead.

### Will Fed-Dup create the destination repository?

No. The destination repository must already exist and be empty (or already a
mirror). Fed-Dup will overwrite refs but will not create the repo on the
remote host. Create it via your hosting platform's UI or API first.

### What happens if a sync fails?

`duplicate_repository()` returns `(False, error_message)`. The error message
has all token substrings redacted via `_redact()`. In the web UI, failures are
shown in the sync results table. In the worker, failures are logged but do not
abort the loop — other repos continue to sync. Failed repos are retried on the
next sync pass.

### How much disk space do I need?

Each repository is cloned as a bare mirror into `./feddup_workspace/`. A bare
mirror is typically similar in size to the `.git` directory of a full clone.
If `cleanup_after_sync` is enabled (default), the mirror is deleted after each
push, so only the largest single repo's worth of space is needed at any time.
If cleanup is disabled, mirrors accumulate — use `get_repo_size` in the UI to
monitor usage.

### Can I run multiple repos in parallel?

`max_parallel_syncs` in `config.json` controls the concurrency. The default is
3. Parallel execution is on the roadmap for the worker; the web UI's "Sync All
Now" processes sequentially with a progress bar but is being upgraded.

---

## Docker

### How do I run Fed-Dup in Docker?

```bash
docker compose up -d
```

The UI is available at `http://localhost:8501`. The compose file mounts
`config.json` and the workspace as named volumes. See
[DEPLOYMENT.md](DEPLOYMENT.md) for production guidance.

### The healthcheck is failing — what do I do?

The healthcheck hits `/_stcore/health` on port 8501. If it fails:

1. Ensure Streamlit started successfully (`docker compose logs feddup`).
2. Verify port 8501 is not already in use on the host.
3. Check that `config.json` is mounted and readable inside the container.

---

## Security

### Are my tokens safe?

Fed-Dup never writes tokens to disk beyond `config.json`. They are injected
into Git remote URLs at runtime and redacted from all error messages and
logs. However, `config.json` itself stores them in plaintext — secure the
file with `chmod 600` and never commit it. See [SECURITY.md](SECURITY.md).

### Should I expose the Streamlit UI to the internet?

**No — not without an authentication layer.** Anyone with UI access can read
configured tokens and trigger syncs. Put it behind a reverse proxy with TLS
and authentication (Caddy, Traefik, nginx + OAuth proxy, Cloudflare Access,
etc.). See [SECURITY.md](SECURITY.md) and [DEPLOYMENT.md](DEPLOYMENT.md).

### How do I report a security vulnerability?

Do **not** open a public issue. Use GitHub Security Advisories or email the
security address listed in [SECURITY.md](SECURITY.md). We follow coordinated
disclosure.

---

## Development

### How do I run the tests?

```bash
pip install pytest pytest-cov
pytest --cov=feddup --cov-report=term-missing
```

All 46 tests should pass. See [CONTRIBUTING.md](CONTRIBUTING.md).

### How do I contribute?

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow — fork, branch,
Conventional Commits, PR template, and the quality gates (black, flake8,
mypy, bandit, pytest).

### My PR title check is failing.

The `pr` workflow validates PR titles against Conventional Commits. Use a
prefix like `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `build:`,
`chore:`, or `revert:`. Example: `feat(engine): add retry logic`.

---

## Misc

### Where is the roadmap?

See [ROADMAP.md](ROADMAP.md) and [docs/ROADMAP.md](docs/ROADMAP.md).

### How do I cite Fed-Dup in a paper or project?

See [CITATIONS.md](CITATIONS.md).

### I found a bug — where do I report it?

Open a [bug report issue](https://github.com/feddup/fed-dup/issues/new?template=bug_report.md).
Please include reproduction steps and your environment details.

### I have a feature idea — where do I share it?

Open a [feature request issue](https://github.com/feddup/fed-dup/issues/new?template=feature_request.md)
or start a [Discussion](https://github.com/feddup/fed-dup/discussions).

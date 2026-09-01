# Architecture Decision Records (ADR)

This document collects the key architectural decisions made during the
design and development of Fed-Dup. Each record describes a decision, its
context, the chosen alternative, and the consequences.

The format is inspired by [Michael Nygard's ADR template](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

## Table of Contents

- [ADR-0001 — Database-free Configuration](#adr-0001--database-free-configuration)
- [ADR-0002 — True Git Mirroring](#adr-0002--true-git-mirroring)
- [ADR-0003 — HTTPS Token Injection](#adr-0003--https-token-injection)
- [ADR-0004 — Streamlit for the Web UI](#adr-0004--streamlit-for-the-web-ui)
- [ADR-0005 — Background Worker with --once Mode](#adr-0005--background-worker-with---once-mode)
- [ADR-0006 — Token Redaction in Error Paths](#adr-0006--token-redaction-in-error-paths)
- [ADR-0007 — Forward-compatible Config Backfilling](#adr-0007--forward-compatible-config-backfilling)
- [ADR-0008 — Host Allow-list for Source URLs](#adr-0008--host-allow-list-for-source-urls)
- [ADR-0009 — Docker as the Primary Deployment Vehicle](#adr-0009--docker-as-the-primary-deployment-vehicle)
- [ADR-0010 — MIT License](#adr-0010--mit-license)

---

## ADR-0001 — Database-free Configuration

**Date:** 2025-08-01
**Status:** Accepted

### Context

Fed-Dup needs to persist configuration (tokens, repository list, settings)
and optionally sync state. Many mirroring tools use SQLite, Postgres, or Redis
for this. However, the target users are individuals and small teams who want
a simple, self-hosted backup tool with minimal operational overhead.

### Decision

Store all configuration in a single `config.json` file. No database.

### Consequences

**Positive:**
- Trivial to install — no database to provision or manage.
- Human-readable and editable.
- Easy to back up (copy one file).
- Easy to version-control (tokens redacted / gitignored).
- Portable across environments.

**Negative:**
- Not suitable for high-throughput, multi-tenant, or concurrent-write
  scenarios (no transactional updates).
- Sync state history is limited (mitigated in v1.1 by storing last-sync info
  in the JSON file).

**Mitigation:** For users who need a database backend, a future v2.0 may add
an optional SQLite/Postgres backend (see [ROADMAP.md](ROADMAP.md)).

---

## ADR-0002 — True Git Mirroring

**Date:** 2025-08-01
**Status:** Accepted

### Context

Fed-Dup must duplicate repositories to a backup host. Options:
1. `git clone` + `git push` (non-mirror) — only pushes branches, loses tags,
   notes, and PR refs; may create merge conflicts.
2. `git clone --mirror` + `git push --mirror` — forces every ref to match
   exactly, including tags, notes, and custom refs.
3. Bundle-based backup — creates a `git bundle` file (not a live repo).

### Decision

Use option 2: `git clone --mirror` / `git remote update` followed by
`git push --mirror`.

### Consequences

**Positive:**
- Exact ref-for-ref fidelity — the destination is a true mirror.
- Handles all ref types (branches, tags, notes, PR refs).
- No merge conflicts — the destination is overwritten to match the source.
- Simple and well-understood Git semantics.

**Negative:**
- **Destructive** — branches deleted on the source are deleted on the
  destination. This is by design for a true mirror but may surprise users
  expecting additive backup.
- Requires the destination repo to be empty or already a mirror.

**Mitigation:** Document this behavior clearly in [README.md](README.md) and
[FAQ.md](FAQ.md).

---

## ADR-0003 — HTTPS Token Injection

**Date:** 2025-08-01
**Status:** Accepted

### Context

Git needs credentials to access private repos and push to destinations.
Options:
1. SSH keys — robust but requires per-host key management and SSH agent
   forwarding; not all hosts support it uniformly.
2. Git credential helper — stores tokens in the OS credential store; harder
   to configure in containers.
3. HTTPS URL with embedded token (`https://oauth2:{token}@host/path`) —
   simple, works across GitHub, GitLab, Gitea, Codeberg.

### Decision

Use option 3: inject the token into the HTTPS remote URL at runtime.

### Consequences

**Positive:**
- Works across all supported hosts (GitHub, GitLab, Bitbucket, Codeberg,
  Gitea).
- No SSH key management or credential helper configuration needed.
- Works in containers and CI without extra setup.

**Negative:**
- Tokens appear in the URL — risk of leaking into logs or error messages.
- Tokens are passed via command-line arguments (visible in process list).

**Mitigation:**
- `sanitize_git_url` strips credentials before logging or display.
- `_redact()` scrubs token substrings from all error messages and subprocess
  output.
- Tokens are never persisted in URLs in `config.json` — they are stored in
  separate fields and injected at runtime.
- See [SECURITY.md](SECURITY.md) for the full hardening checklist.

---

## ADR-0004 — Streamlit for the Web UI

**Date:** 2025-08-01
**Status:** Accepted

### Context

Fed-Dup benefits from a web UI for managing repos and triggering syncs.
Options:
1. Flask / FastAPI + custom HTML/JS — flexible but more code to maintain.
2. Streamlit — Python-native, rapid prototyping, built-in widgets.
3. No UI — CLI only.

### Decision

Use Streamlit.

### Consequences

**Positive:**
- Rapid development — the entire UI is in a single `app.py`.
- Python-native — no separate frontend build step.
- Built-in widgets (forms, buttons, progress bars, tables).
- Active ecosystem and good documentation.

**Negative:**
- Limited customization of layout and styling (mitigated by `styles.css`
  injection).
- No built-in authentication (mitigated by reverse proxy auth — see
  [DEPLOYMENT.md](DEPLOYMENT.md)).
- WebSocket-based — requires a reverse proxy that supports upgrades.

---

## ADR-0005 — Background Worker with --once Mode

**Date:** 2025-08-01
**Status:** Accepted

### Context

Fed-Dup needs to sync repos automatically. Options:
1. Long-running loop only — requires a always-on process.
2. `--once` mode only — requires external scheduling (cron/CI).
3. Both — a loop for always-on deployments and `--once` for scheduled/CI.

### Decision

Support both modes in `worker.py`.

### Consequences

**Positive:**
- Flexibility — always-on for self-hosted, `--once` for cron/CI/K8s CronJobs.
- `--once` exits with a non-zero code on failure, enabling CI gating.
- The loop reads the interval from config, so changes take effect without a
  restart.

**Negative:**
- Two code paths to maintain (mitigated by sharing `sync_all()` between them).

---

## ADR-0006 — Token Redaction in Error Paths

**Date:** 2025-08-01
**Status:** Accepted

### Context

Git error messages may echo the remote URL, which contains the injected token.
If these messages are logged or displayed, tokens leak.

### Decision

Implement `_redact(message, *tokens)` in `feddup/engine.py` and pass all
error messages and subprocess output through it before logging or returning.

### Consequences

**Positive:**
- Tokens never appear in logs, error messages, or the UI.
- Defense in depth — even if a token somehow reaches an error path, it is
  scrubbed.

**Negative:**
- Slight performance overhead (string replacement) — negligible for this use
  case.
- Redacted messages may be less readable (tokens replaced with `REDACTED`),
  but this is an acceptable trade-off.

---

## ADR-0007 — Forward-compatible Config Backfilling

**Date:** 2025-08-01
**Status:** Accepted

### Context

As Fed-Dup evolves, new settings will be added to `config.json`. Users with
old config files should not break on upgrade.

### Decision

`load_config()` backfills missing keys from `DEFAULT_SETTINGS` at load time.
The config file is not modified unless `save_config()` is explicitly called.

### Consequences

**Positive:**
- Old config files keep working after upgrades.
- No manual migration steps required for new settings.
- Defaults are centralized in one place (`_default_config()`).

**Negative:**
- The in-memory config may differ from the on-disk file (missing keys are
  added in memory but not written back until `save_config()`). This is
  acceptable — any UI "Save" action persists the full config.

---

## ADR-0008 — Host Allow-list for Source URLs

**Date:** 2025-08-01
**Status:** Accepted

### Context

To prevent SSRF and abuse, source URLs should be restricted to known,
trustworthy Git hosts.

### Decision

`validate_source_url` checks the host against an allow-list:
`github.com`, `gitlab.com`, `bitbucket.org`, `codeberg.org`, `gitea.com`.
Destination URLs are validated separately (HTTPS only, any host) since the
destination is user-controlled.

### Consequences

**Positive:**
- Reduces SSRF risk for source fetches.
- Clear error messages for unsupported hosts.

**Negative:**
- Users cannot mirror from arbitrary hosts (e.g., self-hosted Gitea on a
  custom domain). This is a deliberate trade-off for security.

**Mitigation:** Users can fork the project and extend the allow-list, or a
future version may make it configurable.

---

## ADR-0009 — Docker as the Primary Deployment Vehicle

**Date:** 2025-08-01
**Status:** Accepted

### Context

Fed-Dup should be easy to deploy in production. Options:
1. Python venv + systemd — traditional but requires per-host setup.
2. Docker / Docker Compose — reproducible, portable, easy to manage.
3. Both.

### Decision

Provide both, but make Docker the primary recommended path.

### Consequences

**Positive:**
- Docker provides a reproducible, isolated environment.
- `docker-compose.yml` enables one-command deploys.
- Healthcheck and volume management are built in.
- Kubernetes deployment is straightforward from the Docker image.

**Negative:**
- Users without Docker must use the venv + systemd path (documented in
  [DEPLOYMENT.md](DEPLOYMENT.md)).

---

## ADR-0010 — MIT License

**Date:** 2025-08-01
**Status:** Accepted

### Context

Fed-Dup is a community project intended for broad adoption.

### Decision

License under the MIT License.

### Consequences

**Positive:**
- Permissive — allows commercial and non-commercial use, modification, and
  redistribution.
- Simple and well-understood.
- Compatible with most other licenses.
- Encourages adoption and contribution.

**Negative:**
- No copyleft — derivative projects need not share their source. This is
  acceptable for a utility tool.

---

*New ADRs will be appended as significant architectural decisions are made.*

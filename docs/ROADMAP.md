<!-- This document is mirrored from the root [ROADMAP.md](../ROADMAP.md). -->
<!-- The canonical version lives in the repository root. -->

# Roadmap

This document outlines the planned direction for Fed-Dup. It is a living
document — items may be reprioritized, and community input is welcome via
[GitHub Discussions](https://github.com/feddup/fed-dup/discussions) and
feature requests.

## How to Influence the Roadmap

- **Upvote** existing feature requests with 👍.
- **Open** a new feature request describing your use case.
- **Sponsor** a feature via [Ko-fi](https://ko-fi.com/feddup) to accelerate
  development.
- **Contribute** a PR — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Current Status

**v1.0.0** is the initial stable release. It provides:

- Two-phase true Git mirroring (`clone --mirror` + `push --mirror`).
- Streamlit web UI with progress tracking.
- Background worker with `--once` cron/CI mode.
- JSON-based, database-free configuration.
- Token redaction and URL sanitization.
- Docker and Docker Compose deployment.
- Full CI/CD with 16 GitHub Actions workflows.
- Comprehensive documentation and test suite (46 tests).

---

## Short-Term (v1.1)

Focus: **Performance & observability.**

- [ ] **Parallel sync execution** — a real concurrency pool honoring
      `max_parallel_syncs`, replacing the current sequential loop in the
      worker and UI "Sync All Now".
- [ ] **Sync status history** — persist per-repo last-sync time, duration,
      and result (success/failure) in `config.json` for dashboard display.
- [ ] **Failure retry with exponential backoff** — automatically retry
      transient failures before reporting them as failed.
- [ ] **Structured logging** — optional JSON log output for log aggregation
      systems (ELK, Loki, Datadog).
- [ ] **Per-repository settings override** — allow individual repos to
      override global settings (e.g., cleanup, schedule).

---

## Medium-Term (v1.2 – v1.5)

Focus: **Automation & extensibility.**

- [ ] **Webhook-triggered sync** — expose a webhook endpoint that triggers an
      immediate sync for a specific repo or all repos when a push event is
      received from the source host.
- [ ] **Per-repository cron scheduling** — each repo can have its own sync
      schedule via cron expressions, independent of the global interval.
- [ ] **SSH transport support** — allow SSH-based Git remotes (with deploy
      keys) as an alternative to HTTPS token injection.
- [ ] **Web UI authentication** — built-in password or OIDC login so the UI
      can be safely exposed without an external auth proxy.
- [ ] **Multi-destination fan-out** — mirror one source to multiple
      destinations simultaneously.
- [ ] **Plugin / hook system** — run pre-sync and post-sync hooks (shell
      scripts or Python callables) for custom logic (notifications, size
      checks, etc.).
- [ ] **Mirror verification** — post-push verification step that compares ref
      counts between source and destination to confirm the mirror is exact.

---

## Long-Term (v2.0+)

Focus: **Scale & alternative backends.**

- [ ] **Optional database backend** — for users who want multi-tenant,
      high-throughput operation, add an optional SQLite/Postgres backend
      (JSON config remains the default for simple deployments).
- [ ] **Object storage destination** — push mirror bundles to S3, GCS, Azure
      Blob, or Backblaze B2 as an alternative to a live Git host.
- [ ] **Differential / incremental sync** — reduce bandwidth by detecting
      when no refs have changed and skipping the push phase.
- [ ] **Distributed worker pool** — for very large repo counts, support
      multiple worker nodes coordinating via a shared backend.
- [ ] **GraphQL / REST API** — a programmatic API alongside the Streamlit UI
      for integration with other tools and automation platforms.
- [ ] **Built-in notifications** — email, Slack, Discord, or webhook
      notifications on sync success/failure.
- [ ] **Mirror health dashboard** — a Grafana-compatible metrics endpoint
      (Prometheus) for monitoring mirror freshness and failure rates.

---

## Completed Milestones

### v1.0.0 — 2025-09-01 ✅

- Initial stable release.
- Core engine, config, utils, logger.
- Streamlit web UI and background worker.
- 46-test pytest suite.
- Docker + Docker Compose.
- 16 GitHub Actions workflows.
- Full documentation suite.

See [CHANGELOG.md](CHANGELOG.md) for details.

---

## Deprecation Policy

- Features are deprecated with a notice in [CHANGELOG.md](CHANGELOG.md) and
  the `CHANGELOG` `[Deprecated]` section.
- Deprecated features receive bug fixes for at least **one minor release
  cycle** before removal.
- Breaking changes require a **major version bump** (e.g., v2.0.0) and are
  documented with a migration guide.

---

## Versioning

Fed-Dup follows [Semantic Versioning](https://semver.org/):

| Bump   | When                                        |
|--------|---------------------------------------------|
| PATCH  | Bug fixes, no new features                  |
| MINOR  | New features, backward-compatible           |
| MAJOR  | Breaking changes (requires migration guide) |

---

*This roadmap is aspirational and not a commitment. Dates and priorities are
subject to change based on community feedback and maintainer availability.*

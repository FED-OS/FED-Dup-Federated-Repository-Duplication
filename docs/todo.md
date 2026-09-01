# Fed-Dup Project To-Do

This is the project-level to-do list, tracking feature work, improvements,
and known issues. It complements the [Roadmap](ROADMAP.md) with more
granular, actionable items.

> **Note:** This file tracks *project* tasks (features, improvements). The
> root [todo.md](../todo.md) is the build/development task tracker for the
> current release.

---

## Legend

- [ ] Not started
- [~] In progress
- [x] Complete

---

## v1.0.0 (Initial Release) — ✅ Complete

- [x] Core engine: `duplicate_repository()` with two-phase mirror
- [x] Configuration module: JSON-based, database-free
- [x] Utilities: URL sanitization, validation, workspace cleanup
- [x] Logger: idempotent `get_logger()`
- [x] Streamlit web UI: sidebar, repo management, sync dashboard
- [x] Background worker: continuous loop + `--once` mode
- [x] Token redaction in error paths
- [x] Forward-compatible config backfilling
- [x] Test suite: 46 pytest tests
- [x] Docker + Docker Compose deployment
- [x] 16 GitHub Actions workflows
- [x] Full documentation suite
- [x] Landing page (`index.html`) and social image

---

## v1.1 (Next Release) — Performance & Observability

- [ ] Parallel sync execution with concurrency pool
- [ ] Sync status history in config.json (last-sync time, result)
- [ ] Failure retry with exponential backoff
- [ ] Structured (JSON) logging option
- [ ] Per-repository settings override
- [ ] UI: show sync duration and history
- [ ] Worker: graceful shutdown on SIGTERM/SIGINT
- [ ] Add `--dry-run` flag to worker for previewing syncs

---

## v1.2 – v1.5 — Automation & Extensibility

- [ ] Webhook-triggered sync endpoint
- [ ] Per-repository cron scheduling
- [ ] SSH transport support (deploy keys)
- [ ] Built-in UI authentication (password / OIDC)
- [ ] Multi-destination fan-out (one source → many destinations)
- [ ] Pre-sync and post-sync hooks (shell + Python)
- [ ] Mirror verification (compare ref counts source vs. destination)
- [ ] Configurable source-host allow-list
- [ ] REST API for programmatic access
- [ ] Bulk import from CSV / JSON file

---

## v2.0+ — Scale & Alternative Backends

- [ ] Optional database backend (SQLite / Postgres)
- [ ] Object storage destination (S3, GCS, Azure Blob, B2)
- [ ] Differential / incremental sync (skip push if no ref changes)
- [ ] Distributed worker pool (multiple nodes coordinating)
- [ ] GraphQL API
- [ ] Built-in notifications (email, Slack, Discord, webhook)
- [ ] Prometheus metrics endpoint
- [ ] Grafana dashboard for mirror health
- [ ] Multi-tenant support (with database backend)

---

## Documentation Backlog

- [ ] Video walkthrough of setup and first sync
- [ ] Architecture diagram (visual)
- [ ] Data flow diagram (source → workspace → destination)
- [ ] Comparison table vs. other mirroring tools
- [ ] Troubleshooting decision tree
- [ ] Localization (i18n) of UI and docs

---

## Testing Backlog

- [ ] Integration tests with a local Gitea instance (Docker)
- [ ] End-to-end test: real clone → push → verify refs
- [ ] Performance benchmarks (large repos)
- [ ] Load testing (many repos in parallel)
- [ ] Mutation testing to assess test quality
- [ ] Increase coverage to > 95%

---

## CI/CD Backlog

- [ ] Add `pre-commit` hooks for local quality gates
- [ ] Add `renovate` as alternative to Dependabot (optional)
- [ ] Add semantic-release automation
- [ ] Add container image scanning (Trivy) to CI
- [ ] Add SBOM generation (CycloneDX / SPDX)
- [ ] Add signed releases (cosign)

---

## Known Issues

- [ ] Worker processes repos sequentially in the loop (parallelism is on the
      v1.1 roadmap)
- [ ] SSH-based remotes not supported (on the medium-term roadmap)
- [ ] Source host allow-list is hardcoded (configurable in a future version)
- [ ] No built-in UI authentication (use reverse proxy auth — see
      [DEPLOYMENT.md](DEPLOYMENT.md))

---

## How to Contribute

Want to help with an item on this list? See
[CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow. Comment on
the relevant issue or open a new one to claim a task.

---

*Last updated: 2025-09-01*

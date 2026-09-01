# Security Policy

## Supported Versions

Fed-Dup is under active development. Security fixes are applied to the latest
release line. The table below summarises the support status for each major
version.

| Version | Supported          | Notes                                  |
|---------|--------------------|----------------------------------------|
| 1.x     | ✅ Yes             | Current release line — all fixes land here first. |
| < 1.0   | ❌ No              | Pre-release prototypes — upgrade to 1.x.            |

When a new major version (2.x) is published, the previous major line receives
critical security fixes for **90 days** before entering end-of-life.

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Please report suspected vulnerabilities privately so maintainers can triage and
patch them before public disclosure. Choose whichever channel you prefer:

1. **GitHub Security Advisories (preferred).** Navigate to the
   *Security* tab → *Advisories* → *New draft security advisory*. This enables
   a private collaboration workspace and, once accepted, can be published as a
   GitHub-reviewed advisory (and optionally assigned a CVE).
2. **Email.** Send a description, reproduction steps, and any proof-of-concept
   to **security@fed-dup.dev** (replace with your project's address). Encrypt
   sensitive payloads with the project's PGP key if one is published.

### What to include

- Affected version (and commit hash if building from source).
- A concise description of the issue and its impact.
- Step-by-step reproduction instructions.
- Suggested fix or mitigation (optional but appreciated).
- Your preferred disclosure timeline.

### Response timeline

| Step                         | Target      |
|------------------------------|-------------|
| Acknowledge receipt          | ≤ 48 hours  |
| Initial triage & severity    | ≤ 5 days    |
| Fix or mitigation published  | ≤ 30 days (severity dependent) |
| Public advisory / CVE        | After fix is released, coordinated with reporter |

We follow a **coordinated disclosure** model. Reporters are credited in the
advisory unless they prefer to remain anonymous.

## Security Considerations Specific to Fed-Dup

Fed-Dup handles **Git access tokens** for both source and destination hosts.
Review the following before deploying.

### Token handling

- Tokens are injected into Git remote URLs at runtime using the
  `https://oauth2:{token}@host/...` form. They are **never** written to disk by
  the engine itself.
- All error messages returned by `feddup.engine.duplicate_repository` are
  passed through `_redact()`, which strips any token substrings before logging
  or surfacing to the UI.
- The `config.json` file stores tokens in **plaintext**. It is excluded from
  version control via `.gitignore`. In production, prefer environment variables
  (see `.env.example`) or a secrets manager, and restrict file permissions:
  ```bash
  chmod 600 config.json
  ```

### URL validation

- `feddup.utils.validate_source_url` restricts source hosts to an allow-list
  (`github.com`, `gitlab.com`, `bitbucket.org`, `codeberg.org`, `gitea.com`).
  Destination URLs are validated separately and may target any HTTPS host.
- `sanitize_git_url` strips embedded credentials from URLs before they are
  logged or displayed, and upgrades `http://` to `https://`.

### Workspace isolation

- Each mirror operation runs inside `./feddup_workspace/` (configurable). The
  workspace is cleaned up after each sync when `cleanup_after_sync` is enabled.
- In Docker deployments the workspace is a named volume, preventing leakage
  into the host filesystem.

### Network exposure

- The Streamlit UI binds to `0.0.0.0:8501` by default. In production, place it
  behind a reverse proxy with TLS termination and authentication (e.g., Caddy,
  Traefik, or nginx + OAuth proxy).
- Do **not** expose the UI directly to the public internet without an
  authentication layer — anyone with UI access can read configured tokens.

### Dependency supply chain

- The project uses Dependabot, `dependency-review-action`, and OpenSSF
  Scorecards workflows to monitor third-party dependencies.
- Lock-file hashes are verified during CI builds.

## Hardening Checklist

- [ ] Rotate tokens regularly (GitHub/GitLab support scoped, expiring tokens).
- [ ] Use fine-grained PATs with **read-only** scope for source repositories.
- [ ] Use separate, scoped tokens for each destination host.
- [ ] Enable `cleanup_after_sync` so mirrored repos do not persist on disk.
- [ ] Run the Docker image as a non-root user (the provided `Dockerfile` does).
- [ ] Mount `config.json` read-only when running in CI/cron mode (`--once`).
- [ ] Put the Streamlit UI behind TLS + authentication in production.
- [ ] Monitor logs for `REDACTED` placeholders — their presence indicates a
      token leaked into an error path and should be reported.

## Contact

- Security advisories: GitHub *Security* tab.
- General questions: GitHub Discussions (not for vulnerability reports).

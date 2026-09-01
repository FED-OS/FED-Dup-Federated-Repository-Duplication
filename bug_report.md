# Bug Report

<!-- Thank you for taking the time to report a bug! -->
<!-- Please fill in all sections below. Incomplete reports may be closed. -->

## Bug Description

<!-- A clear and concise description of what the bug is. -->

## Steps to Reproduce

<!-- Provide step-by-step instructions so we can reproduce the behavior. -->

1. 
2. 
3. 

## Expected Behavior

<!-- What did you expect to happen? -->

## Actual Behavior

<!-- What actually happened? -->

## Error Output / Logs

<!-- Paste any relevant error messages or log output. -->
<!-- IMPORTANT: Remove or redact any tokens, passwords, or secrets before pasting. -->
<!-- Fed-Dup redacts tokens automatically, but double-check! -->

```
Paste logs here (tokens removed)
```

## Environment

- **Fed-Dup version:** <!-- run: python -c "import feddup; print(feddup.__version__)" -->
- **Python version:** <!-- run: python --version -->
- **OS / platform:** <!-- e.g., Ubuntu 22.04, macOS 14, Windows 11 -->
- **Git version:** <!-- run: git --version -->
- **Deployment method:** <!-- e.g., pip/venv, Docker, docker-compose, systemd, cron -->

## Configuration (tokens removed)

<!-- Share your config.json with ALL tokens replaced with "REDACTED". -->
<!-- Do NOT paste real tokens. Use config.json.example as a template. -->

```json
{
  "github_token": "REDACTED",
  "backup_token": "REDACTED",
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

## Is This a Security Issue?

<!-- If this bug exposes tokens, credentials, or could lead to unauthorized -->
<!-- access, DO NOT use this form. See SECURITY.md for private reporting. -->

- [ ] No, this is not a security issue.
- [ ] Yes, and I will report it privately via [SECURITY.md](../SECURITY.md) instead.

## Additional Context

<!-- Add any other context about the problem: screenshots, related issues, -->
<!-- what you tried, workarounds, etc. -->

## Checklist

- [ ] I have searched existing issues and this is not a duplicate.
- [ ] I have removed all tokens and secrets from this report.
- [ ] I am using a [supported version](../SECURITY.md#supported-versions) of Fed-Dup.
- [ ] I have provided enough information for a maintainer to reproduce the issue.

---

**Thank you for helping improve Fed-Dup!** 🛡️

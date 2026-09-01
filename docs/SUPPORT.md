<!-- This document is mirrored from the root [SUPPORT.md](../SUPPORT.md). -->
<!-- The canonical version lives in the repository root. -->

# Support

## Getting Help

Thank you for using Fed-Dup! There are several channels for getting help,
reporting issues, and contributing back to the project. Please choose the one
that best fits your situation.

## Quick Reference

| Need                        | Where to go                                                       |
|-----------------------------|-------------------------------------------------------------------|
| Bug report                  | [Issue tracker → Bug Report](https://github.com/feddup/fed-dup/issues/new?template=bug_report.md) |
| Feature request             | [Issue tracker → Feature Request](https://github.com/feddup/fed-dup/issues/new?template=feature_request.md) |
| Question / discussion        | [GitHub Discussions](https://github.com/feddup/fed-dup/discussions) |
| Security vulnerability      | [SECURITY.md](SECURITY.md) — **do not open a public issue** |
| Documentation               | [docs/](docs/) and [FAQ.md](FAQ.md) |
| Contributing                | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

## Before You Ask

To help us help you quickly, please do the following before reaching out:

1. **Search existing issues and discussions.** Your question may already have
   been answered.
2. **Read the [FAQ](FAQ.md).** Common questions about setup, usage, Docker, and
   security are covered there.
3. **Check the [documentation](docs/).** Especially
   [INSTALL.md](INSTALL.md), [usage.md](usage.md), and
   [DEPLOYMENT.md](DEPLOYMENT.md).
4. **Update to the latest version.** Your issue may already be fixed:
   ```bash
   git pull
   pip install -r requirements.txt --upgrade
   ```

---

## Reporting a Bug

Open a [bug report](https://github.com/feddup/fed-dup/issues/new?template=bug_report.md)
and include:

- **Fed-Dup version** (`python -c "import feddup; print(feddup.__version__)"`)
- **Python version** (`python --version`)
- **OS / platform**
- **Git version** (`git --version`)
- **Steps to reproduce** — be as specific as possible.
- **Expected behavior** vs. **actual behavior**.
- **Logs** — copy the relevant log output. **Make sure no tokens are
  visible** — Fed-Dup redacts tokens, but double-check before pasting.
- **Configuration** — include your `config.json` **with tokens removed**. Use
  `config.json.example` as a template for what to share.

The more detail you provide, the faster we can reproduce and fix the issue.

---

## Requesting a Feature

Open a [feature request](https://github.com/feddup/fed-dup/issues/new?template=feature_request.md)
and describe:

- The problem you are trying to solve.
- Your proposed solution or desired behavior.
- Any alternatives you have considered.
- Additional context (screenshots, links, examples from other tools).

Feature requests are triaged and may be added to the
[Roadmap](ROADMAP.md). Upvotes from the community help prioritize.

---

## Asking Questions

For general questions, how-to guides, and discussion, use
[GitHub Discussions](https://github.com/feddup/fed-dup/discussions). This keeps
the issue tracker focused on actionable bugs and feature requests.

When asking a question:
- Use a clear, descriptive title.
- Provide context about what you are trying to achieve.
- Share what you have already tried.
- Tag the discussion with the appropriate category.

---

## Security Issues

**Security vulnerabilities must not be reported via the public issue
tracker.** See [SECURITY.md](SECURITY.md) for the private reporting process
(GitHub Security Advisories or email). We follow coordinated disclosure and
aim to acknowledge reports within 48 hours.

---

## Commercial Support

Fed-Dup is a community project and does not currently offer paid commercial
support. If you need enterprise-grade support, hosting, or customization,
consider:

- Self-hosting with the provided Docker setup (see
  [DEPLOYMENT.md](DEPLOYMENT.md)).
- Sponsoring a maintainer via [Ko-fi](https://ko-fi.com/feddup) to prioritize
  your issue or feature.
- Forking the project under the MIT License and customizing it for your needs.

See [PRICING.md](PRICING.md) for details on sponsorship and the project's
funding model.

---

## Community Guidelines

All interactions in the Fed-Dup community are governed by the
[Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and
patient. Maintainers and contributors are volunteers — kindness goes a long
way.

---

## Response Times

Fed-Dup is maintained by volunteers. We do our best, but we cannot guarantee
specific response times. As a general guideline:

| Channel              | Approximate Response Time |
|----------------------|---------------------------|
| Security reports     | ≤ 48 hours (acknowledgment) |
| Bug reports          | 3–7 days (triage)         |
| Feature requests     | 1–2 weeks (triage)        |
| Discussions          | Best-effort               |
| Pull requests        | 3–5 days (initial review) |

If your issue is urgent, consider sponsoring via
[Ko-fi](https://ko-fi.com/feddup) and mentioning the issue number.

---

## Sponsoring

If Fed-Dup has saved you time or helped you avoid data loss, consider
supporting the project:

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/feddup)

Sponsorship helps cover infrastructure costs and rewards maintainers for their
time. See [PRICING.md](PRICING.md) for sponsorship tiers.

---

Thank you for being part of the Fed-Dup community! 🛡️

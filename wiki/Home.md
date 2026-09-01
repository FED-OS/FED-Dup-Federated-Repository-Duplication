# Fed-Dup Wiki — Home

Welcome to the **Fed-Dup Wiki**! This wiki contains community-maintained
guides, tutorials, tips, and reference material that complement the official
documentation in the [main repository](https://github.com/feddup/fed-dup).

> **Note:** For official, maintained documentation, see the
> [docs/ directory](https://github.com/feddup/fed-dup/tree/main/docs) and the
> root-level markdown files. This wiki is for community-contributed content,
> recipes, and deep-dives.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Wiki Pages](#wiki-pages)
- [Contributing to the Wiki](#contributing-to-the-wiki)
- [Wiki vs. Official Docs](#wiki-vs-official-docs)

---

## Getting Started

New to Fed-Dup? Start here:

1. **[README](https://github.com/feddup/fed-dup/blob/main/README.md)** —
   project overview and quick start.
2. **[INSTALL.md](https://github.com/feddup/fed-dup/blob/main/INSTALL.md)** —
   step-by-step installation.
3. **[usage.md](https://github.com/feddup/fed-dup/blob/main/usage.md)** — daily
   usage guide.
4. Then come back here for community tips and advanced recipes.

---

## Wiki Pages

### Tutorials & Recipes

- *(coming soon)* **Mirroring a GitHub org to Gitea** — a complete walk-through.
- *(coming soon)* **Setting up cron-based sync on a VPS** — systemd + cron.
- *(coming soon)* **Mirroring to Codeberg for decentralization** — why and how.
- *(coming soon)* **Self-hosting with Caddy + TLS + OAuth** — production setup.

### Tips & Tricks

- *(coming soon)* **Bulk-importing repos from a CSV** — script and process.
- *(coming soon)* **Monitoring mirror freshness with a cron check** — alerting.
- *(coming soon)* **Rotating tokens safely** — zero-downtime token rotation.
- *(coming soon)* **Reducing disk usage** — cleanup strategies.

### Advanced Topics

- *(coming soon)* **Git mirror internals** — how `--mirror` actually works.
- *(coming soon)* **Token injection deep-dive** — the `oauth2:` URL form.
- *(coming soon)* **Writing custom pre/post-sync hooks** — extensibility.
- *(coming soon)* **Multi-destination fan-out patterns** — one source, many backups.

### Community

- *(coming soon)* **Fed-Dup in production** — user stories and setups.
- *(coming soon)* **Fed-Dup vs. other tools** — feature comparison.
- *(coming soon)* **FAQ from the community** — beyond the official FAQ.

---

## Contributing to the Wiki

The wiki is community-maintained. To contribute:

1. **Fork the repository** (the wiki lives in the `wiki/` directory).
2. **Create a new page** as a Markdown file in `wiki/` (e.g.,
   `wiki/Mirroring-a-GitHub-Org.md`).
3. **Add a link** to your page in the [Wiki Pages](#wiki-pages) section above.
4. **Open a PR** following the
   [Contributing guidelines](https://github.com/feddup/fed-dup/blob/main/CONTRIBUTING.md).

### Wiki Page Guidelines

- Use clear, descriptive titles.
- Include a brief introduction explaining the goal.
- Use code blocks for commands and configuration.
- **Never include real tokens or secrets** — always use placeholders like
  `ghp_YOUR_TOKEN`.
- Link to official docs where relevant.
- Add screenshots or diagrams if helpful.
- Keep content up to date — if something changes in the codebase, update the
  wiki page.

---

## Wiki vs. Official Docs

| Aspect               | Official Docs (`docs/`, root `*.md`) | Wiki (`wiki/`)            |
|----------------------|--------------------------------------|---------------------------|
| Maintained by        | Maintainers                          | Community                 |
| Authority            | Canonical / authoritative            | Supplementary / recipes   |
| Scope                | Core features, setup, deployment     | Tutorials, tips, deep-dives |
| Update frequency     | With each release                    | Community-driven          |
| Where to report bugs | Issue tracker                        | PR to update the wiki page |

If information in the wiki conflicts with official docs, **the official docs
are authoritative.** Please open an issue or PR to reconcile the difference.

---

## Community

- **[GitHub Discussions](https://github.com/feddup/fed-dup/discussions)** —
  ask questions, share setups, and discuss.
- **[Issue Tracker](https://github.com/feddup/fed-dup/issues)** — report bugs
  and request features.
- **[Ko-fi](https://ko-fi.com/feddup)** — support the project.

---

*This wiki is a living document. Contributions are welcome!*

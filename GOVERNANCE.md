# Governance

## Overview

Fed-Dup is an open-source, community-driven project. This document describes
how the project is governed, how decisions are made, and how roles and
responsibilities are assigned. It is designed to be lightweight and
transparent, reflecting the project's current size while allowing for growth.

---

## Roles

### Contributors

Anyone who submits a pull request, reports a bug, suggests a feature,
improves documentation, or helps in discussions is a **contributor**.
Contributors are listed in [AUTHORS.md](AUTHORS.md).

**Rights:**
- Open issues and pull requests.
- Participate in discussions and code review.
- Propose changes and new features.

**Responsibilities:**
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Adhere to the [Contributing guidelines](CONTRIBUTING.md).
- Provide constructive feedback and be responsive to review comments.

### Maintainers

Maintainers are contributors who have demonstrated sustained commitment to
the project and have been granted write access to the repository. They are
listed in [MAINTAINERS.md](MAINTAINERS.md).

**Rights:**
- All contributor rights.
- Merge pull requests (following the merge criteria in
  [MAINTAINERS.md](MAINTAINERS.md)).
- Triage and label issues.
- Manage releases.
- Moderate discussions.

**Responsibilities:**
- Review pull requests in a timely manner (target: 3–5 days).
- Ensure code quality (tests pass, linting clean, docs updated).
- Uphold the [Code of Conduct](CODE_OF_CONDUCT.md).
- Mentor new contributors.
- Participate in release planning.

### Lead Maintainer

The lead maintainer has final say on contentious decisions and is responsible
for the overall direction of the project. The lead maintainer is listed in
[MAINTAINERS.md](MAINTAINERS.md) with a "Lead" designation.

**Rights:**
- All maintainer rights.
- Final decision authority on disputes.
- Set the project roadmap (in consultation with maintainers and the
  community).
- Manage repository settings, CI/CD, and access control.

**Responsibilities:**
- Ensure the project remains healthy and sustainable.
- Facilitate consensus among maintainers.
- Communicate the project's direction to the community.
- Step down gracefully when no longer able to serve (see
  [Succession](#succession)).

---

## Decision-Making Process

### Consensus-Seeking

Fed-Dup uses a **consensus-seeking** model. Decisions are made through
discussion in issues, pull requests, and GitHub Discussions. The goal is to
reach broad agreement among maintainers and the community.

### Decision Tiers

| Decision Type                          | Process                                              |
|----------------------------------------|------------------------------------------------------|
| Minor (bug fix, small feature, docs)   | PR review + one maintainer approval → merge          |
| Moderate (new feature, config change)  | PR review + two maintainer approvals → merge         |
| Major (architecture, breaking change)  | ADR + maintainer discussion + community input → lead decides |
| Governance changes                     | This document must be updated via PR with maintainer consensus |

### Architecture Decisions

Significant architectural decisions are documented as
[Architecture Decision Records (ADRs)](ADR.md). ADRs are proposed via PR,
discussed openly, and merged once consensus is reached.

### Dispute Resolution

If maintainers cannot reach consensus:

1. The lead maintainer facilitates further discussion.
2. If consensus still cannot be reached, the lead maintainer makes the final
   decision.
3. The decision and rationale are documented (in an ADR if architectural, or
   in the PR/issue thread otherwise).

All decisions should be made in the spirit of what is best for the project and
its community.

---

## Becoming a Maintainer

Contributors may be invited to become maintainers based on:

1. **Sustained contribution** — a track record of high-quality PRs, reviews,
   issue triage, or documentation over a meaningful period (typically several
   months).
2. **Domain knowledge** — demonstrated understanding of the codebase, Git
   internals, and the project's goals.
3. **Community engagement** — constructive, respectful interactions aligned
   with the [Code of Conduct](CODE_OF_CONDUCT.md).
4. **Reliability** — responsiveness to review requests and issue reports.

### Process

1. An existing maintainer nominates the contributor (privately or in a
   maintainer discussion).
2. Maintainers discuss and reach consensus.
3. The lead maintainer extends an invitation.
4. The new maintainer is added to the [MAINTAINERS.md](MAINTAINERS.md) list
   and granted write access.
5. A welcome announcement is made (optional, in Discussions).

---

## Stepping Down

Maintainers may step down at any time by notifying the other maintainers.
Stepping down is normal and expected — life circumstances change. A stepping
-down maintainer:

- Is moved to an "Emeritus" section in [MAINTAINERS.md](MAINTAINERS.md) (with
  their consent).
- Retains their contributions and recognition in [AUTHORS.md](AUTHORS.md).
- May return to active maintainer status later if they choose.

### Inactivity

A maintainer who has been inactive (no commits, reviews, or discussions) for
**6 months** may be moved to emeritus status by the lead maintainer, after
attempting to contact them. This is not punitive — it is to keep the
maintainer list accurate. Emeritus maintainers can return at any time.

---

## Succession

If the lead maintainer steps down or is unable to continue:

1. The lead maintainer (or, if unreachable, the remaining maintainers)
   nominates a successor from the active maintainers.
2. Maintainers confirm the successor by consensus.
3. The new lead maintainer is announced in [MAINTAINERS.md](MAINTAINERS.md)
   and Discussions.
4. The outgoing lead maintainer transfers repository ownership / admin access
   if applicable.

If no successor is identified, the remaining maintainers collectively assume
the lead maintainer's responsibilities until a new lead is chosen.

---

## Code of Conduct Enforcement

The [Code of Conduct](CODE_OF_CONDUCT.md) is enforced by the maintainers.
Reports of violations are handled confidentially by the lead maintainer (or a
designated maintainer if the lead is the subject of the report). Enforcement
actions follow the guidelines in the Code of Conduct.

Maintainers who violate the Code of Conduct may have their privileges revoked,
regardless of their contribution history.

---

## Repository Access Control

| Role            | Access Level                                  |
|-----------------|-----------------------------------------------|
| Lead Maintainer | Admin (full repository control)               |
| Maintainer      | Write (push, merge, manage issues/PRs)        |
| Contributor     | Read + fork + PR (no direct push to main)     |

Access is granted via GitHub's collaborator system. The lead maintainer
manages access changes. Sensitive settings (secrets, branch protection,
CI/CD) are managed by the lead maintainer only.

---

## Transparency

- All decisions are made in public issues, PRs, and Discussions (except
  security reports and Code of Conduct reports, which are private).
- Maintainer discussions that affect the project direction are summarized
  publicly.
- The [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md) are kept up
  to date.
- Financial sponsorship is disclosed in [PRICING.md](PRICING.md).

---

## Changes to This Document

Changes to this governance model require a PR with consensus among active
maintainers. The lead maintainer has final approval on governance changes.

---

## Acknowledgements

This governance model is inspired by the practices of successful open-source
projects and the [Contributor Covenant](https://www.contributor-covenant.org/)
community guidelines. It is intentionally lightweight and may evolve as the
project grows.

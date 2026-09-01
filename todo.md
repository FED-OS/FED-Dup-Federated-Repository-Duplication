# Fed-Dup Build Plan

## Core Python Package
- [x] Create feddup/__init__.py, engine.py, config.py, utils.py, logger.py
- [x] Create app.py (Streamlit UI) and worker.py (background sync)
- [x] Create tests/ (test_engine.py, test_config.py, test_utils.py, __init__.py)

## Config & Deployment
- [x] Create requirements.txt, config.json.example, .env.example
- [x] Create .gitignore, .dockerignore, Dockerfile, docker-compose.yml
- [x] Create styles.css, index.html
- [x] Generate social-image.png

## GitHub Templates & Workflows
- [x] .github/DISCUSSION_WELCOME_README.md, PULL_REQUEST_TEMPLATE.md
- [x] .github/ISSUE_TEMPLATE/ (bug_report, feature_request, custom)
- [x] .github/workflows/ (16 workflows: build, test, ci, cd, deploy, release, publish, pr, stale, labeler, greetings, codeql, main, pages, dependency-review, scorecards)
- [x] .github/labeler.yml, .github/dependabot.yml, CODEOWNERS

## Root Docs
- [x] CLAUDE.md, AGENTS.md, AUTHORS.md, MAINTAINERS.md
- [x] SECURITY.md, LICENSE, README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md
- [x] CHANGELOG.md, FAQ.md, NOTICE.md, SUPPORT.md, usage.md
- [x] INSTALL.md, BUILD.md, DEPLOYMENT.md, ROADMAP.md, ADR.md, SUMMARY.md
- [x] todo.md (root), PRICING.md, COPYING.md, CITATIONS.md, GOVERNANCE.md
- [x] PULL_REQUEST_TEMPLATE.md (root), bug_report.md (root), feature_request.md (root)

## Docs Directory
- [x] docs/ (ADR, ROADMAP, DEPLOYMENT, BUILD, INSTALL, SUMMARY, todo, PRICING, COPYING, CITATIONS, GOVERNANCE, SUPPORT, CODE_OF_CONDUCT, CONTRIBUTING, usage, CHANGELOG, FAQ, NOTICE)

## Misc Directories
- [x] prompts/README.md, wiki/Home.md, discussion/README.md

## Verification & Packaging
- [x] Run pytest to verify tests pass
- [x] Run flake8/black to verify code style
- [x] Test app.py imports and runs
- [x] Create complete tree output
- [x] Package everything and verify

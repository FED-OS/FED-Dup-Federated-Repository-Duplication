# Prompts

This directory contains reusable AI / LLM prompts related to the Fed-Dup
project. These prompts can be used with ChatGPT, Claude, Gemini, Copilot, or
any other LLM to assist with development, documentation, debugging, and
feature planning for Fed-Dup.

## Table of Contents

- [Available Prompts](#available-prompts)
- [Usage](#usage)
- [Contributing Prompts](#contributing-prompts)
- [Prompt Guidelines](#prompt-guidelines)

---

## Available Prompts

The following prompts are available (or planned). Each prompt is designed to
be self-contained — copy and paste it into your LLM of choice.

### Development Prompts

- **`new-feature.md`** — *(planned)* Generate a scaffold for a new Fed-Dup
  feature, including code, tests, docs, and changelog entry.
- **`bug-investigation.md`** — *(planned)* Systematic prompt for
  investigating a bug: reproduce, isolate, root-cause, and propose a fix.
- **`code-review.md`** — *(planned)* Prompt an LLM to review a diff or PR
  against Fed-Dup's coding standards (black, flake8, mypy, bandit, security).
- **`refactor.md`** — *(planned)* Identify refactoring opportunities in a
  given module while preserving behavior.

### Documentation Prompts

- **`doc-update.md`** — *(planned)* Update documentation files after a code
  change, ensuring accuracy and consistency.
- **`changelog-entry.md`** — *(planned)* Generate a Conventional Commits and
  Keep a Changelog-formatted entry from a diff or PR description.
- **`adr-draft.md`** — *(planned)* Draft a new Architecture Decision Record
  from a design discussion.

### Testing Prompts

- **`test-generation.md`** — *(planned)* Generate pytest test cases for a
  given function or module, following the patterns in `tests/`.
- **`test-edge-cases.md`** — *(planned)* Identify and generate tests for edge
  cases (empty inputs, None, unicode, large values, etc.).

### Operations Prompts

- **`docker-troubleshoot.md`** — *(planned)* Diagnose Docker / Compose issues
  for Fed-Dup deployments.
- **`deployment-review.md`** — *(planned)* Review a deployment configuration
  for security and best practices.

---

## Usage

1. Choose a prompt from the list above.
2. Open the corresponding `.md` file in this directory.
3. Copy the prompt text.
4. Paste it into your LLM, filling in any bracketed placeholders
   (e.g., `[module name]`, `[error message]`).
5. Review the LLM's output critically — LLMs can hallucinate. Verify all
   generated code and suggestions against the actual codebase and
   documentation.

> **Warning:** Never paste real tokens, passwords, or secrets into an LLM
> prompt. Always redact sensitive values before sharing configuration or logs
> with any AI tool. See [SECURITY.md](../SECURITY.md).

---

## Contributing Prompts

We welcome community-contributed prompts! To add a prompt:

1. Create a new `.md` file in this directory with a descriptive name (e.g.,
   `new-feature.md`).
2. Structure the prompt clearly:
   - **Title** and **purpose** at the top.
   - The prompt text itself (copy-paste ready).
   - Notes on how to use it and any placeholders to fill in.
3. Add an entry to the [Available Prompts](#available-prompts) list in this
   README.
4. Open a PR following the [Contributing guidelines](../CONTRIBUTING.md).

---

## Prompt Guidelines

Good prompts for Fed-Dup should:

- **Be specific** — reference actual modules, functions, and file paths
  (e.g., `feddup/engine.py`, `duplicate_repository()`).
- **Include context** — mention the tech stack (Python 3.11, Streamlit,
  pytest, Git) so the LLM produces relevant output.
- **Specify the output format** — e.g., "return a pytest test class" or
  "output a Conventional Commits message."
- **Encourage verification** — remind the user to check the output against the
  real codebase.
- **Be token-safe** — instruct the user to redact secrets, and never include
  real tokens in example prompts.
- **Follow project conventions** — Conventional Commits, black formatting,
  type hints, and the test patterns in `tests/`.

---

## Related

- [CLAUDE.md](../CLAUDE.md) — Instructions for Claude Code / AI assistants
  working on the codebase.
- [AGENTS.md](../AGENTS.md) — General AI agent guidelines.
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Human contribution guide.

---

*This directory is a community resource. Prompts are provided as-is and are
not guaranteed to produce correct output. Always verify LLM-generated
content.*

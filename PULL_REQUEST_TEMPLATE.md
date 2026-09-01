# Pull Request Template

<!-- Thank you for contributing to Fed-Dup! Please fill in the sections below. -->
<!-- Remove any sections that are not applicable and mark them as N/A. -->

## Description

<!-- Provide a clear and concise description of what this PR does. -->
<!-- Link any related issues using "Closes #123" or "Refs #456". -->

## Type of Change

<!-- Check all that apply: -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] ♻️ Refactor (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test addition or correction
- [ ] 🔧 Build / CI configuration change
- [ ] 🗑️ Chore (dependencies, cleanup, etc.)

## Motivation and Context

<!-- Why is this change needed? What problem does it solve? -->
<!-- If this fixes a bug, describe how to reproduce it. -->

## How Has This Been Tested?

<!-- Describe the tests you ran to verify your changes. -->
<!-- Include details about your test environment if relevant. -->

- [ ] Ran `pytest` — all 46 tests pass
- [ ] Ran `black --check .` — no formatting issues
- [ ] Ran `flake8 .` — no lint errors
- [ ] Ran `mypy feddup/` — no type errors
- [ ] Ran `bandit -r feddup/` — no security issues
- [ ] Manually tested via the Streamlit UI (`streamlit run app.py`)
- [ ] Manually tested via the worker (`python worker.py --once`)

### Test Environment

- **Python version:** 
- **OS:** 
- **Git version:** 

## Screenshots / Output

<!-- If your change affects the UI or produces notable output, include screenshots or log excerpts. -->
<!-- Make sure NO tokens or secrets are visible in any screenshot or log. -->

## Checklist

<!-- Please confirm the following before requesting review: -->

- [ ] My PR title follows the [Conventional Commits](https://www.conventionalcommits.org/) convention (e.g., `feat:`, `fix:`, `docs:`)
- [ ] My code follows the project's style guidelines (`black`, `flake8`)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or my feature works
- [ ] New and existing unit tests pass locally (`pytest`)
- [ ] Any dependent changes have been merged and published
- [ ] I have NOT committed `config.json` (only `config.json.example`)
- [ ] I have NOT included any tokens, passwords, or secrets in my diff
- [ ] My commits are atomic and have clear messages

## Additional Notes

<!-- Anything else reviewers should know? Migration steps? Follow-up work? -->

---

**By submitting this pull request, I confirm that:**

- My contribution is licensed under the [MIT License](LICENSE).
- I have read and agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
- I have followed the [Contributing guidelines](CONTRIBUTING.md).

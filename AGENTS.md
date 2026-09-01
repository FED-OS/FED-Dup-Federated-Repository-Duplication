# AI Agents & Automation Guide for Fed-Dup

## 🤖 Agent Configuration

### GitHub Actions
- CI/CD pipelines in `.github/workflows/`
- Automated testing, building, and deployment
- Security scanning with CodeQL and Scorecards
- Dependency review on every PR
- Stale issue/PR management

### Dependabot
Updates dependencies automatically (`.github/dependabot.yml`):
- Python (`pip`) — weekly
- GitHub Actions — weekly
- Docker — weekly

## 🔄 Automation Workflows

| Trigger | Action |
|---------|--------|
| Push to main | Run CI, build, test |
| PR opened | Run tests, lint, security scan, label, greet |
| PR merged | Deploy to staging |
| Tag created | Release to PyPI and Docker Hub |
| Daily | Comprehensive tests, stale triage, scorecards |
| Weekly | CodeQL security analysis |

## 🛡️ Security Automation
- CodeQL scanning on every PR and weekly
- Dependency vulnerability scanning on PRs
- Scorecards security analysis daily
- Bandit security scan in CI

## 📊 Monitoring
- Test coverage reporting to Codecov
- Security alerts via GitHub Security tab
- Error logging in worker output

## 🔧 Agent Commands

### For Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=feddup tests/

# Lint code
flake8 feddup/ app.py worker.py

# Format code
black feddup/ app.py worker.py
```

### For Deployment
```bash
# Build Docker image
docker build -t feddup .

# Run locally
docker-compose up -d

# Run worker once (great for cron/CI)
python worker.py --once
```

## 🧠 AI-Assisted Development
- Use GitHub Copilot for code completion
- Claude for architectural decisions and refactors
- ChatGPT for complex algorithm explanations
- See `prompts/README.md` for ready-made prompts

## 📈 Continuous Improvement
- Review automated test results
- Monitor security alerts
- Track deployment success rate
- Analyze user feedback from issues/discussions

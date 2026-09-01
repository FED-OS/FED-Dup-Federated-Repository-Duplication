# Claude Development Guidelines for Fed-Dup

## 🎯 Project Purpose
Fed-Dup is a federated repository duplication engine — mirroring Git repositories to backup platforms.

## 🏗️ Architecture
- **UI Layer**: Streamlit web interface (`app.py`)
- **Core Engine**: Python with `subprocess` for Git operations (`feddup/engine.py`)
- **Config**: JSON-based, no database (`feddup/config.py`)
- **Background Sync**: `worker.py` runs on a configurable interval
- **Deployment**: Docker + Docker Compose

## 📁 Code Structure
```
feddup/          # Core package
├── engine.py    # Mirror logic
├── config.py    # Config management
├── utils.py     # Helpers (sanitize, validate, cleanup)
└── logger.py    # Logging
tests/           # Unit tests
app.py           # Streamlit UI
worker.py        # Background sync
```

## 🛠️ Development Rules
1. **No external dependencies beyond Streamlit** — keep the dependency surface tiny.
2. **Never log tokens or credentials** — always redact with `_redact()`.
3. **Validate all URLs before Git operations** (`validate_source_url`, `validate_destination_url`).
4. **Handle subprocess errors gracefully** — return `(success, message)` tuples.
5. **Write tests for all new features** — aim to keep coverage high.

## 🔐 Security Requirements
- Tokens stored only in `config.json`
- Never display tokens in UI/logs
- Validate URLs before processing
- Sanitize all user input (`sanitize_git_url`)

## 🧪 Testing
- Run: `pytest tests/ -v`
- Coverage: `pytest --cov=feddup tests/`
- Lint: `flake8 feddup/ app.py worker.py`
- Format: `black feddup/ app.py worker.py`

## 📝 Commit Conventions
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Test updates
- `chore:` Maintenance

## 🚀 Deployment
- Docker: `docker-compose up -d`
- Local: `streamlit run app.py`
- Worker runs automatically in background inside the container.

## 🧭 When Making Changes
- After editing `feddup/`, run the tests before declaring done.
- After editing `app.py`, confirm it still boots: `streamlit run app.py`.
- After editing `config.json` schema, update `config.json.example` and `docs/`.
- Bump `__version__` in `feddup/__init__.py` and record it in `CHANGELOG.md`.

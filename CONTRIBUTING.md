# Contributing to StreamGuard

Thank you for your interest in contributing! StreamGuard is open-source and built for the streaming community.

> 📖 **Looking to use the app, not contribute code?** See the [README](README.md) for the full user guide and setup instructions.

---

## Getting Started (Developer Setup)

### Prerequisites

- Python 3.11+
- Windows 10 / 11
- A `client_secret.json` from your Google Cloud Project — see the [README Setup Guide](README.md#step-2--set-up-your-google-cloud-project)

### Local Development Setup

```bash
# 1. Fork the repo, then clone your fork
git clone https://github.com/skwasimakram13/StreamGuard.git
cd StreamGuard

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

---

## How to Contribute

### Reporting Bugs

- Use the **Bug Report** issue template on GitHub
- Include your OS version, Python version (if running from source), and steps to reproduce
- For security-related bugs, see [SECURITY.md](SECURITY.md) — **do NOT open a public issue**

### Suggesting Features

- Use the **Feature Request** issue template
- Check existing issues first to avoid duplicates
- Explain the use case and how it benefits streamers

### Submitting a Pull Request

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feat/my-new-feature
   ```
2. Make your changes following the **Code Style Guide** below
3. Test with `python main.py`
4. Commit with a conventional message (see format below)
5. Push and open a PR against the `main` branch

---

## Code Style Guide

- **Formatting**: Follow PEP 8. Use 4 spaces for indentation.
- **Type hints**: All function signatures must include type hints.
- **Docstrings**: All public classes and methods must have docstrings.
- **Error handling**: Wrap all API calls in `try/except`. Log with `logger.error()` — never bare `print()`.
- **No hardcoded credentials**: Never commit any API key, token, or `client_secret.json`.
- **Async**: Use `asyncio.get_running_loop()` inside `async` functions — never `asyncio.get_event_loop()`.
- **Logging**: Use module-level `logger = logging.getLogger(__name__)`.

---

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add superchat reply bot
fix: resolve custom commands dict attribute error
docs: update README with new screenshots
refactor: extract chat polling into separate module
chore: pin dependency versions in requirements.txt
```

---

## Project Architecture

```
StreamGuard/
├── main.py            # UI (Flet), app state, background async loops
├── youtube_engine.py  # All YouTube Data API v3 interactions
├── config_manager.py  # Encrypted credential storage (singleton)
├── database.py        # SQLite viewer loyalty tracking
├── sentiment.py       # Google Gemini AI vibe analysis
├── version.py         # Single source of version truth
├── build.py           # PyInstaller build script
├── StreamGuard.spec   # PyInstaller spec file
└── installer.iss      # Inno Setup Windows installer script
```

**Key design rules:**
- `config_manager.py` is a **singleton** — all modules share one instance
- All YouTube API calls go through `youtube_engine.py` — never call `googleapiclient` directly from `main.py`
- Settings persistence is always done via `ConfigManager.set_setting()` — never write to files directly
- Background loops in `main.py` use `asyncio.create_task()` — never `threading.Thread`

---

## Code of Conduct

Be respectful. We're all here to help streamers. Harassment, discrimination, or toxic behaviour will result in a permanent ban from this project.

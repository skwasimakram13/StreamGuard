# Contributing to StreamGuard

Thank you for your interest in contributing! StreamGuard is an open-source tool for streamers, built by the community.

## Getting Started

### Prerequisites

- Python 3.11+
- A Google Cloud project with the YouTube Data API v3 enabled
- (Optional) A Google Gemini API key for AI Vibe Meter features

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/skwasimakram13/StreamGuard.git
cd StreamGuard

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

### Setting Up Your Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., `StreamGuard Dev`)
3. Enable the **YouTube Data API v3**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Set Application Type to **Desktop app**
6. Download the `client_secret.json`
7. Launch StreamGuard and select this file in the Setup Wizard

## How to Contribute

### Reporting Bugs

- Use the **Bug Report** issue template on GitHub
- Include your OS version, Python version, and steps to reproduce
- For security-related bugs, see [SECURITY.md](SECURITY.md) — do NOT open a public issue

### Suggesting Features

- Use the **Feature Request** issue template
- Check existing issues first to avoid duplicates
- Explain the use case and how it benefits streamers

### Submitting a Pull Request

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-new-feature`
3. Make your changes following the code style guide below
4. Test your changes with `python main.py`
5. Commit with a descriptive message: `git commit -m "feat: add XYZ feature"`
6. Push and open a Pull Request against `main`

## Code Style Guide

- **Formatting**: Follow PEP 8. Use 4 spaces for indentation.
- **Type hints**: All function signatures should include type hints.
- **Docstrings**: All public classes and methods must have docstrings.
- **Error handling**: Wrap all API calls in `try/except` blocks. Log errors with `logger.error()`, not `print()`.
- **No hardcoded credentials**: Never commit any API key, token, or `client_secret.json`.
- **Async**: Use `asyncio.get_running_loop()` inside `async` functions; never `asyncio.get_event_loop()`.
- **Logging**: Use module-level `logger = logging.getLogger(__name__)` — never `print()` for app logic.

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add superchat reply bot
fix: resolve custom commands dict attribute error
docs: update README with new screenshots
chore: pin dependency versions in requirements.txt
```

## Project Architecture

```
StreamGuard/
├── main.py            # UI (Flet), app state, background loops
├── youtube_engine.py  # All YouTube Data API v3 interactions
├── config_manager.py  # Encrypted credential storage (singleton)
├── database.py        # SQLite viewer loyalty tracking
├── sentiment.py       # Google Gemini AI vibe analysis
├── version.py         # Single source of version truth
├── build.py           # PyInstaller build script
├── StreamGuard.spec   # PyInstaller spec file
└── installer.iss      # Inno Setup Windows installer script
```

## Code of Conduct

Be respectful. We're all here to help streamers. Harassment, discrimination, or toxic behaviour will result in an immediate ban.

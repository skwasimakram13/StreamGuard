# Contributing to StreamGuard

Thank you for your interest in contributing! StreamGuard is open-source and built for the streaming community. Every contribution — whether it's a bug report, documentation improvement, or a new feature — is genuinely valued.

> 📖 **Looking to use the app, not contribute code?** See the [README](README.md) for the full user guide and setup instructions.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started (Developer Setup)](#getting-started-developer-setup)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Code Style Guide](#code-style-guide)
- [Commit Message Format](#commit-message-format)
- [Project Architecture](#project-architecture)
- [Testing Guidelines](#testing-guidelines)

---

## Code of Conduct

Be kind, inclusive, and professional. We are all here to help the streaming community. Harassment, discrimination, or toxic behavior of any kind will result in a permanent ban from this project. Treat every contributor and user with respect — regardless of experience level, background, or platform.

---

## Getting Started (Developer Setup)

### Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.11 or higher ([download](https://www.python.org/downloads/)) |
| **Operating System** | Windows 10 or 11 (64-bit) |
| **Git** | For version control |
| **Google Cloud credentials** | A `client_secret.json` from your own Google Cloud project — see the [README setup guide](README.md#step-2--set-up-your-google-cloud-project) |

### Local Development Setup

```bash
# 1. Fork the repository on GitHub, then clone your fork
git clone https://github.com/<your-username>/StreamGuard.git
cd StreamGuard

# 2. Create a virtual environment (strongly recommended — keeps your system Python clean)
python -m venv .venv
.venv\Scripts\activate

# 3. Install all Python dependencies
pip install -r requirements.txt

# 4. Launch the app to confirm everything works
python main.py
```

> ⚠️ **Never commit your `client_secret.json`.** The `.gitignore` excludes it by default, but always double-check before pushing.

---

## How to Contribute

### Reporting Bugs

1. Search [existing issues](https://github.com/skwasimakram13/StreamGuard/issues) to check if the bug has already been reported
2. If it has not been reported, open a new issue using the **🐛 Bug Report** template
3. Include:
   - Your OS version (Windows 10 / 11)
   - StreamGuard version (shown in the app header)
   - Python version if running from source (`python --version`)
   - Steps to reproduce the issue
   - Contents of `%APPDATA%\StreamGuard\system.log` (if applicable)
4. For **security vulnerabilities**, see [SECURITY.md](SECURITY.md) — **do NOT open a public issue**

### Suggesting Features

1. Search [existing issues](https://github.com/skwasimakram13/StreamGuard/issues) to check for duplicates
2. Open a new issue using the **💡 Feature Request** template
3. Clearly describe:
   - The problem you are solving
   - The proposed solution and its UX impact
   - Any alternatives you considered
   - Who among streamers would benefit and how

### Submitting a Pull Request

1. Fork the repository and create a descriptive feature branch:
   ```bash
   git checkout -b feat/superchat-reply-bot
   ```
2. Make your changes following the **Code Style Guide** below
3. Test your changes locally with `python main.py` and verify the full flow works
4. Add a summary of your changes to `CHANGELOG.md` under the `[Unreleased]` section
5. Commit using the **Conventional Commits** format (see below)
6. Push to your fork and open a Pull Request targeting the `main` branch
7. Fill out all sections of the **Pull Request Template** — incomplete PRs may be closed without review

---

## Code Style Guide

Consistency in code style makes the codebase easier to read, maintain, and contribute to. All submitted code must follow these rules:

### General Rules

- **Formatting**: Follow [PEP 8](https://peps.python.org/pep-0008/). Use **4 spaces** for indentation — no tabs.
- **Line length**: Maximum 120 characters per line.
- **Type hints**: All function signatures (including `self` methods) must include full type annotations.
- **Docstrings**: All public classes and all public/protected methods must have Google-style docstrings.
- **Error handling**: Wrap every external API call in a `try/except` block. Log errors with `logger.error()` — never use bare `print()` for diagnostics.

### Specific Rules

| Rule | Reason |
|---|---|
| Use `asyncio.get_running_loop()` inside `async def` functions | `asyncio.get_event_loop()` is deprecated in Python 3.10+ and raises a `DeprecationWarning` |
| Use `logger = logging.getLogger(__name__)` at module level | Enables per-module log filtering and consistent log formatting |
| Never write directly to credential files | Always use `ConfigManager.set_setting()` so encryption is always applied |
| Never call `googleapiclient` directly from `main.py` | All YouTube API logic belongs in `youtube_engine.py` |
| Never commit `client_secret.json`, `.env`, or any token file | The `.gitignore` covers these, but always verify before pushing |

### Example: Correct Function Style

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def delete_chat_message(live_chat_id: str, message_id: str) -> bool:
    """Delete a message from a YouTube Live chat.

    Args:
        live_chat_id: The ID of the live chat session.
        message_id: The ID of the specific message to delete.

    Returns:
        True if the deletion was successful, False otherwise.
    """
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _delete_sync, live_chat_id, message_id)
        logger.info("Deleted message %s from chat %s", message_id, live_chat_id)
        return True
    except HttpError as exc:
        logger.error("Failed to delete message %s: %s", message_id, exc)
        return False
```

---

## Commit Message Format

StreamGuard uses [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages. This enables automatic changelog generation and makes the git history easy to parse.

### Format

```
<type>(<optional scope>): <short description>

[optional body — explain the WHY, not just the WHAT]

[optional footer — e.g., Closes #42, BREAKING CHANGE: ...]
```

### Types

| Type | When to Use |
|---|---|
| `feat` | A new user-facing feature |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `refactor` | Code restructuring with no behavior change |
| `perf` | Performance improvements |
| `chore` | Build scripts, dependency updates, CI config changes |
| `style` | Code formatting changes (no logic change) |
| `test` | Adding or updating tests |

### Examples

```
feat(bots): add !shoutout command with channel lookup
fix(auth): resolve token refresh race condition on expired OAuth token
docs: update README with Flet build prerequisites
refactor(youtube_engine): extract quota error handling into dedicated method
chore: bump flet to 0.24.1 in requirements.txt
fix(installer): use dynamic ReleaseDir variable to resolve CI path mismatch
```

---

## Project Architecture

Understanding the codebase structure will help you contribute more effectively.

```
StreamGuard/
├── main.py              # UI (Flet), app state, background async polling loops
├── youtube_engine.py    # All YouTube Data API v3 interactions + retry logic
├── config_manager.py    # Encrypted credential storage singleton (AES-256 + keyring)
├── database.py          # SQLite viewer loyalty tracking
├── sentiment.py         # Google Gemini AI sentiment analysis
└── version.py           # Single source of version truth
```

### Data Flow

```
User Action (Flet UI in main.py)
    │
    ▼
youtube_engine.py  ◄──── Credentials from config_manager.py
    │
    ▼
YouTube Data API v3 (Google servers)
    │
    ▼
Result returned to main.py → UI update via Flet page.update()
```

### Key Design Rules

| Rule | Rationale |
|---|---|
| `config_manager.py` is a **singleton** | All modules share one thread-safe instance to prevent concurrent write conflicts on the encrypted credential file |
| All YouTube API calls go through `youtube_engine.py` | Centralizes retry logic (via `tenacity`), quota error handling, and HTTP error normalization |
| Settings saved via `ConfigManager.set_setting()` only | Ensures AES-256 encryption is always applied; direct file writes would expose credentials in plaintext |
| Background loops use `asyncio.create_task()` | Non-blocking cooperative multitasking that integrates correctly with Flet's async event loop |
| Never use `threading.Thread` | Mixing threads with Flet's async model causes unpredictable UI update race conditions |

---

## Testing Guidelines

StreamGuard does not currently have an automated test suite. Manual testing is the current standard. When submitting a PR:

1. **Run the full application**: `python main.py` — confirm the app launches without errors
2. **Test the affected flow end-to-end**: If you changed the Alerts Bot, test that it actually sends messages on schedule
3. **Test edge cases**: Empty banned word list, no active live stream, expired OAuth token, etc.
4. **Check the log file**: Review `%APPDATA%\StreamGuard\system.log` for unexpected `ERROR` or `WARNING` entries after running

> 💡 If you are adding a new module or significant functionality, consider adding a standalone test script in the repo root (e.g., `test_new_feature.py`) that exercises the code path with mock data. Unit tests are welcome but not yet enforced.

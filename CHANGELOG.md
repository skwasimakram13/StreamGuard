# Changelog

All notable changes to StreamGuard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-04-27

### 🚀 Major Release — Production-Ready

This release makes StreamGuard fully production-grade and ready for public use.

### Added
- `version.py` — Single source of truth for version number across all build scripts
- `SECURITY.md` — Comprehensive security policy documenting the BYOK architecture
- `CONTRIBUTING.md` — Contributor guidelines for open-source collaboration
- `CHANGELOG.md` — This file; tracks all changes going forward
- `pyproject.toml` — Modern Python packaging metadata
- `.github/workflows/build.yml` — Automated Windows EXE build via GitHub Actions
- `.github/ISSUE_TEMPLATE/` — Bug report and feature request templates
- `.github/PULL_REQUEST_TEMPLATE.md` — Pull request checklist
- `.gitignore` — Comprehensive ignore list (credentials, build artifacts, logs)
- `google-genai` added to `requirements.txt` (replaces deprecated `google-generativeai`)
- App version displayed in the UI header
- Window minimum size enforced (prevents unusable small-window layouts)

### Fixed
- **Critical**: `ft.run(target=main)` → `ft.app(main)` (caused `TypeError` crash on launch)
- **Critical**: `msg._replied = True` on a `dict` object (impossible in Python; used a `replied_ids` set instead)
- **Deprecation**: All `asyncio.get_event_loop()` calls inside `async` functions replaced with `asyncio.get_running_loop()`
- **Deprecation**: `google.generativeai` import warning in `sentiment.py` resolved (was a stale `__pycache__`; force-cleared)
- `requirements.txt` now pins minimum versions to prevent breakage on fresh installs

### Changed
- `build.py` now reads version from `version.py`
- `build.py` now collects `google-genai` package for PyInstaller
- `installer.iss` updated to `AppVersion=2.0.0` and `AppPublisherURL` added

---

## [1.0.0] - 2026-04-25

### Initial Release
- YouTube OAuth 2.0 BYOK authentication flow
- Live chat monitoring with real-time moderation
- Auto-delete banned words
- Superchat / membership highlights panel
- Time-based Alerts Bot
- Viewer Engagement Bot
- Custom Commands Bot (`!command | response` format)
- AI Vibe Meter powered by Google Gemini
- Loyalty / Top Chatters leaderboard with VIP toggle
- Encrypted credential storage (`AES-256` via `cryptography` + Windows Credential Manager)
- SQLite viewer database
- PyInstaller build pipeline + Inno Setup installer

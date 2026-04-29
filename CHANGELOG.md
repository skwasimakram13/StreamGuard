# Changelog

All notable changes to StreamGuard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

> Changes staged for the next release will appear here before tagging.

---

## [2.1.0] - 2026-04-29

### 📚 Documentation & Community Overhaul

This release focuses on making StreamGuard fully accessible to both end-users and open-source contributors through a complete overhaul of all project documentation and community templates.

### Added
- **README.md**: New **System Requirements** table (OS, RAM, disk, internet, Google Account)
- **README.md**: New **CI/CD Pipeline** section — documents trigger events, all build steps, and the full "how to tag a release" command walkthrough
- **README.md**: Expanded **FAQ** with 3 new entries: SmartScreen/UAC bypass guidance, Windows Defender false-positive explanation, and blank-on-launch troubleshooting
- **README.md**: Added **Moderation Controls reference table** in the User Guide section
- **README.md**: Added **Custom Commands examples** code block with real-world `!discord`, `!socials`, `!donate`, `!schedule` examples
- **CONTRIBUTING.md**: New **Table of Contents** and **data flow diagram** showing the UI → youtube_engine → API call path
- **CONTRIBUTING.md**: New **Testing Guidelines** section with manual test checklist
- **CONTRIBUTING.md**: Realistic **code style example** — correctly typed `async def` function with Google-style docstring
- **CONTRIBUTING.md**: Full **commit type reference table** with usage guidance for all conventional commit types
- **SECURITY.md**: Detailed **Credential Storage Model** table — every credential mapped to its storage location and encryption method
- **SECURITY.md**: **Network Connections** table — every external endpoint the app contacts, with purpose and trigger condition
- **SECURITY.md**: **Response Timeline SLA** table (72h acknowledgment, 7d confirmation, 14d patch for critical vulnerabilities)
- **SECURITY.md**: **"What Data Is Collected?"** section with explicit zero-data-collection answer
- `.github/ISSUE_TEMPLATE/bug_report.md`: Collapsible `<details>` log block, structured environment table, and frequency checklist
- `.github/ISSUE_TEMPLATE/feature_request.md`: **Priority self-assessment** checklist, **Implementation Hints** and **Reference Examples** sections
- `.github/PULL_REQUEST_TEMPLATE.md`: Categorized checklists (Code Quality, Security, Documentation, Dependencies), Before/After screenshot table, Breaking Changes section

### Changed
- **README.md**: Build documentation updated from legacy PyInstaller instructions to the current `flet build windows` workflow with exact PowerShell commands
- **README.md**: All version references updated to `2.1.0`
- **CHANGELOG.md**: Retroactively added `v2.0.3` and `v2.0.4` patch entries that were missing; added proper comparison diff links at the bottom of the file
- `version.py`: `__version__` → `2.1.0`; `__version_info__` → `(2, 1, 0)`
- `installer.iss`: `AppVersion` → `2.1.0`; `OutputBaseFilename` → `StreamGuard_Setup_v2.1.0`

---

## [2.0.4] - 2026-04-29

### Fixed
- **CI/CD**: Resolved installer build path mismatch — `installer.iss` now correctly uses the dynamic `{#ReleaseDir}` variable passed from the GitHub Actions workflow via `iscc /DReleaseDir=...`, allowing the Inno Setup step to locate the `flet build windows` output regardless of the exact subdirectory Flutter places it in
- **Uninstaller**: Replaced Python-level `ctypes.windll.user32.MessageBoxW()` call (which crashed post-uninstall) with a native Inno Setup Pascal `MsgBox()` in `[Code]` — the dialog now correctly prompts users whether to delete `%APPDATA%\StreamGuard\` configuration data during uninstallation
- **FilePicker**: Removed unsupported `allowed_extensions` type hint that caused a `TypeError` on Windows when opening the `client_secret.json` file picker dialog

### Changed
- `installer.iss`: `AppVersion` and `OutputBaseFilename` bumped to `2.0.4`
- `version.py`: `__version__` updated to `2.0.4`

---

## [2.0.3] - 2026-04-28

### Fixed
- **CI/CD**: Migrated from `pyinstaller` build pipeline to `flet build windows` (official Flet native build system) to resolve packaged app launch crashes caused by missing Flutter engine dependencies
- **CI/CD**: Added `Find and Verify Build Output` step to dynamically locate `StreamGuard.exe` within the `build/` tree and expose its directory as `RELEASE_DIR` for Inno Setup — prevents silent failures when Flutter changes its output subdirectory structure
- **Performance**: Eliminated startup latency caused by `flet` runtime initialization order; entry point now correctly uses `flet.app(main)` instead of deprecated `flet.run(target=main)`

### Added
- GitHub Actions workflow step: `workflow_dispatch` trigger — allows manually invoking the full build pipeline from the GitHub Actions UI without creating a tag
- Installer artifact upload for manual `workflow_dispatch` runs (7-day retention)

### Changed
- `build.yml`: Replaced `pyinstaller`-based build step with `flet build windows --project StreamGuard --yes`
- `build.yml`: Added dynamic `RELEASE_DIR` environment variable resolution using PowerShell `Get-ChildItem -Recurse`

---

## [2.0.0] - 2026-04-27

### 🚀 Major Release — Production-Ready

This release brings StreamGuard to full production quality, replacing the prototype PyInstaller pipeline with the official Flet-native build system and adding a complete open-source project scaffolding.

### Added
- `version.py` — Single source of truth for version number; consumed by `build.py`, `installer.iss`, and the CI workflow
- `SECURITY.md` — Comprehensive security policy documenting the BYOK architecture, threat model, and responsible disclosure process
- `CONTRIBUTING.md` — Full contributor guide covering local setup, code style, commit message format, and PR workflow
- `CHANGELOG.md` — This file; all future changes will be documented here
- `pyproject.toml` — Modern Python packaging metadata (PEP 517/518 compliant)
- `.github/workflows/build.yml` — Automated Windows EXE + installer build via GitHub Actions, triggered on `v*.*.*` tag push
- `.github/ISSUE_TEMPLATE/bug_report.md` — Structured bug report template with environment fields and log paste section
- `.github/ISSUE_TEMPLATE/feature_request.md` — Feature suggestion template with use-case and alternatives sections
- `.github/PULL_REQUEST_TEMPLATE.md` — PR checklist enforcing code style, credential hygiene, and CHANGELOG update
- `.gitignore` — Comprehensive ignore list covering credentials, build artifacts, virtual environments, and IDE files
- `google-genai>=1.0.0` added to `requirements.txt` (replaces the deprecated `google-generativeai` package)
- App version string displayed in the UI header at runtime
- Window minimum size constraint enforced to prevent unusable small-window layouts

### Fixed
- **Critical**: `ft.run(target=main)` replaced with `ft.app(main)` — the old call caused a `TypeError` crash immediately on launch in Flet 0.24+
- **Critical**: `msg._replied = True` attempted to set an attribute on a plain `dict` object (impossible in Python); replaced with a `replied_ids: set` to track processed messages correctly
- **Deprecation**: All `asyncio.get_event_loop()` calls inside `async def` functions replaced with `asyncio.get_running_loop()` (required in Python 3.10+)
- **Deprecation**: Stale `__pycache__` caused `google.generativeai` import warning in `sentiment.py` even after migrating to `google-genai`; resolved by clearing cache and verifying import paths
- `requirements.txt` now specifies minimum version bounds (`>=`) to prevent breakage on fresh installs with bleeding-edge package versions

### Changed
- `build.py` now reads `__version__` from `version.py` instead of having it hardcoded
- `build.py` now includes the `google-genai` package in the PyInstaller `collect_all()` list
- `installer.iss` updated: `AppVersion=2.0.0`, `AppPublisherURL` added

---

## [1.0.0] - 2026-04-25

### 🎉 Initial Release

First public release of StreamGuard — a free, privacy-first YouTube Live moderation desktop app.

### Added
- **Authentication**: YouTube OAuth 2.0 BYOK flow using a user-provided `client_secret.json`; tokens encrypted with AES-256 and stored via Windows Credential Manager
- **Live Chat Monitor**: Real-time polling of YouTube Live chat messages with color-coded message cards
- **Auto-Moderation**: Automatic deletion of messages matching a user-defined banned word list
- **Highlights Panel**: Automatic surfacing of Superchats, memberships, and milestone messages with gold-bordered cards
- **Alerts Bot**: Time-based message scheduler for cycling promotional announcements in live chat
- **Engagement Bot**: Dedicated like/subscribe/follow reminder bot with independent interval configuration
- **Custom Commands Bot**: `!command | response` format; StreamGuard replies automatically when commands are triggered by viewers
- **AI Vibe Meter**: Google Gemini AI-powered chat sentiment analysis (updates every 15 seconds); displays 🔥💖😡❓💬 mood indicators
- **Loyalty Leaderboard**: SQLite-backed viewer message count tracker with VIP toggle; persists across streams
- **Credential Storage**: AES-256 encryption via the `cryptography` library; encryption key stored in Windows Credential Manager via `keyring`
- **Build Pipeline**: PyInstaller build script (`build.py`) + Inno Setup installer script (`installer.iss`)

---

[Unreleased]: https://github.com/skwasimakram13/StreamGuard/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/skwasimakram13/StreamGuard/compare/v2.0.4...v2.1.0
[2.0.4]: https://github.com/skwasimakram13/StreamGuard/compare/v2.0.3...v2.0.4
[2.0.3]: https://github.com/skwasimakram13/StreamGuard/compare/v2.0.0...v2.0.3
[2.0.0]: https://github.com/skwasimakram13/StreamGuard/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/skwasimakram13/StreamGuard/releases/tag/v1.0.0


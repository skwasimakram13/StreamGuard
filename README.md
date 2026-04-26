<div align="center">

<img src="icon.ico" width="80" height="80" alt="StreamGuard Logo"/>

# StreamGuard

**Professional YouTube Live Stream Moderation & Bot Management**

[![GitHub Release](https://img.shields.io/github/v/release/skwasimakram13/StreamGuard?style=for-the-badge&logo=github)](https://github.com/skwasimakram13/StreamGuard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D4?style=for-the-badge&logo=windows)](https://github.com/skwasimakram13/StreamGuard/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/skwasimakram13/StreamGuard/build.yml?style=for-the-badge)](https://github.com/skwasimakram13/StreamGuard/actions)

> **StreamGuard** is a free, open-source desktop app that gives YouTube Live streamers real-time chat moderation, smart bots, and AI-powered audience insights — all with your own API credentials, stored securely on your machine.

[⬇️ Download Latest Release](https://github.com/skwasimakram13/StreamGuard/releases/latest) · [🐛 Report a Bug](https://github.com/skwasimakram13/StreamGuard/issues/new?template=bug_report.md) · [💡 Request a Feature](https://github.com/skwasimakram13/StreamGuard/issues/new?template=feature_request.md)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🛡️ **Auto-Moderation** | Automatically delete messages containing banned words in real-time |
| 💬 **Live Chat Feed** | Monitor your entire chat with color-coded message cards |
| ⭐ **Highlights Panel** | Superchats, memberships & milestones surfaced automatically |
| 🤖 **Alerts Bot** | Schedule promotional announcements on a timer |
| 📣 **Engagement Bot** | Auto-send like/subscribe reminders at set intervals |
| ⚡ **Custom Commands** | Define `!command` → response pairs for instant chat replies |
| 🧠 **AI Vibe Meter** | Gemini AI analyzes chat sentiment every 15 seconds (🔥💖😡❓💬) |
| 🏆 **Loyalty Tracker** | SQLite-backed viewer leaderboard with VIP designation |
| 🔐 **BYOK Security** | Your OAuth tokens are AES-256 encrypted on your machine. **Zero data sent to us.** |

---

## 🔐 Privacy & Security First

StreamGuard uses a **Bring Your Own Key (BYOK)** architecture:

- ✅ All credentials are stored **locally** in `%APPDATA%\StreamGuard\` — **never on any server**
- ✅ Your `client_secret.json` is **AES-256 encrypted** immediately after import
- ✅ OAuth tokens are stored encrypted and managed via **Windows Credential Manager**
- ✅ API calls go **directly** to Google's servers — no proxy, no middleman
- ✅ The app is fully **open-source** — audit every line yourself

---

## 🚀 Quick Start (Downloaded EXE)

1. **Download** `StreamGuard_Setup.exe` from the [Releases page](https://github.com/skwasimakram13/StreamGuard/releases/latest)
2. **Run the installer** — it installs to `Program Files\StreamGuard` with an optional desktop shortcut
3. **Set up a Google Cloud Project** (one-time, ~5 minutes):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project → Enable **YouTube Data API v3**
   - **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID** → **Desktop app**
   - Click **Download JSON** to save your `client_secret.json`
4. **Launch StreamGuard** → click **"Select client_secret.json"** → authorize in your browser
5. ✅ You're connected! StreamGuard will automatically find your active live stream.

---

## 🔧 Running From Source (Developers)

### Prerequisites

- Python 3.11 or higher
- Windows 10 / 11

### Setup

```bash
# Clone the repository
git clone https://github.com/skwasimakram13/StreamGuard.git
cd StreamGuard

# Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Build the Windows EXE Yourself

```bash
# Make sure you have the venv active and requirements installed
python build.py

# Output will be in: dist\StreamGuard\StreamGuard.exe
```

To create an installer (requires [Inno Setup](https://jrsoftware.org/isinfo.php)):
```
Run installer.iss in Inno Setup Compiler
Output: InnoSetupOutput\StreamGuard_Setup.exe
```

---

## 📋 Requirements

All Python dependencies are in `requirements.txt`. The key ones:

| Package | Purpose |
|---|---|
| `flet` | Cross-platform UI framework |
| `google-api-python-client` | YouTube Data API v3 |
| `google-auth-oauthlib` | OAuth 2.0 authentication flow |
| `google-genai` | Gemini AI for Vibe Meter |
| `cryptography` | AES-256 encryption of credentials |
| `keyring` | Windows Credential Manager integration |
| `tenacity` | Exponential backoff on API retries |
| `httplib2` | HTTP transport layer |

---

## 🗂️ Project Structure

```
StreamGuard/
├── main.py              # UI (Flet), app state, background async loops
├── youtube_engine.py    # All YouTube Data API v3 interactions + retry logic
├── config_manager.py    # Thread-safe encrypted credential storage (singleton)
├── database.py          # SQLite viewer loyalty tracking
├── sentiment.py         # Google Gemini AI vibe analysis engine
├── version.py           # Single source of version truth
├── build.py             # PyInstaller build script
├── StreamGuard.spec     # PyInstaller spec file
├── installer.iss        # Inno Setup Windows installer script
├── requirements.txt     # Python dependencies (pinned minimum versions)
├── pyproject.toml       # Modern Python packaging metadata
├── .github/
│   ├── workflows/
│   │   └── build.yml           # GitHub Actions: auto-build & release EXE
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

---

## 📖 User Guide

### Setting Up Bots

Go to the **Bots** tab:

- **Alerts Bot** — Enable it and set an interval (minutes). Enter one message per line. StreamGuard will cycle through them automatically during your stream.
- **Engagement Bot** — Same concept, but for like/subscribe reminders.
- **Custom Commands** — Format: `!command | Your response text`. Enable the bot and viewers can trigger replies by typing the command in chat.

### AI Vibe Meter

1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. In the **Bots** tab, paste your key in the **AI Vibe Meter** section and click **Save Key**
3. StreamGuard analyzes your chat every 15 seconds and shows the vibe emoji: 🔥 💖 😡 ❓ 💬

### Auto-Moderation

In the **Moderation** tab:
- Toggle **Auto-Mod** on
- Add banned words (comma-separated) in the Banned List Manager
- Click **Update List** — StreamGuard will now auto-delete any matching messages in real-time

### VIP Viewers

In the **Loyalty** tab, hit **Refresh** to see your top chatters ranked by message count. Toggle the **VIP** switch next to any viewer to mark them.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

```bash
# Quick contribution flow
git checkout -b feat/my-feature
# make your changes
git commit -m "feat: add my feature"
git push origin feat/my-feature
# Open a Pull Request
```

---

## 🔒 Security

For security vulnerabilities, please see [SECURITY.md](SECURITY.md).  
**Do not open a public GitHub issue for security bugs.**

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ for the streaming community

**[⬆ Back to Top](#streamguard)**

</div>

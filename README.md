<div align="center">

<img src="icon.ico" width="100" height="100" alt="StreamGuard Logo"/>

# StreamGuard

### Professional YouTube Live Stream Moderation & Bot Management

[![GitHub Release](https://img.shields.io/github/v/release/skwasimakram13/StreamGuard?style=for-the-badge&logo=github&color=238636)](https://github.com/skwasimakram13/StreamGuard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D4?style=for-the-badge&logo=windows)](https://github.com/skwasimakram13/StreamGuard/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/skwasimakram13/StreamGuard/build.yml?style=for-the-badge&label=CI%2FCD)](https://github.com/skwasimakram13/StreamGuard/actions)
[![Flet](https://img.shields.io/badge/Built%20With-Flet%200.24%2B-6C63FF?style=for-the-badge)](https://flet.dev)

> **StreamGuard** is a free, open-source Windows desktop application that gives YouTube Live streamers real-time chat moderation, intelligent bots, and AI-powered audience sentiment insights — all running on your own Google Cloud credentials, stored securely on your machine.  
> **Zero subscriptions. Zero servers. Your data stays yours.**

[⬇️ Download Latest Release](https://github.com/skwasimakram13/StreamGuard/releases/latest) &nbsp;·&nbsp; [🐛 Report a Bug](https://github.com/skwasimakram13/StreamGuard/issues/new?template=bug_report.md) &nbsp;·&nbsp; [💡 Request a Feature](https://github.com/skwasimakram13/StreamGuard/issues/new?template=feature_request.md) &nbsp;·&nbsp; [📖 Changelog](CHANGELOG.md)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🔐 Privacy & Security First](#-privacy--security-first)
- [🖥️ System Requirements](#️-system-requirements)
- [🚀 Installation (No Coding Required)](#-installation-no-coding-required)
  - [Step 1 — Download & Install StreamGuard](#step-1--download--install-streamguard)
  - [Step 2 — Set Up Your Google Cloud Project](#step-2--set-up-your-google-cloud-project)
  - [Step 3 — Connect StreamGuard to YouTube](#step-3--connect-streamguard-to-youtube)
- [📖 User Guide](#-user-guide)
  - [Live Chat Moderation Tab](#live-chat-moderation-tab)
  - [Bots Tab](#bots-tab)
  - [Loyalty / Top Chatters Tab](#loyalty--top-chatters-tab)
- [🔧 Running From Source (Developers)](#-running-from-source-developers)
- [🏗️ Building the Installer Yourself](#️-building-the-installer-yourself)
- [🗂️ Project Structure](#️-project-structure)
- [⚙️ CI/CD Pipeline](#️-cicd-pipeline)
- [❓ FAQ & Troubleshooting](#-faq--troubleshooting)
- [🤝 Contributing](#-contributing)
- [🔒 Security](#-security)
- [📄 License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🛡️ **Auto-Moderation** | Automatically delete messages containing banned words in real-time via YouTube Data API v3 |
| 💬 **Live Chat Feed** | Monitor your entire chat stream with color-coded message cards showing author names and timestamps |
| ⭐ **Highlights Panel** | Superchats, new memberships, and milestone messages are surfaced automatically with a gold border |
| 🤖 **Alerts Bot** | Schedule promotional announcements (links, socials, Discord invites) on a configurable timer |
| 📣 **Engagement Bot** | Auto-send like/subscribe/follow reminders at set intervals to boost channel growth |
| ⚡ **Custom Commands** | Define `!command → response` pairs; StreamGuard replies automatically when viewers trigger them |
| 🧠 **AI Vibe Meter** | Google Gemini AI analyzes chat sentiment every 15 seconds and reports mood with emojis (🔥💖😡❓💬) |
| 🏆 **Loyalty Tracker** | SQLite-backed viewer leaderboard tracking message counts across streams, with VIP designation |
| 🔐 **BYOK Security** | All OAuth tokens are AES-256 encrypted locally using the Windows Credential Manager. **Zero data ever leaves your machine.** |

---

## 🔐 Privacy & Security First

StreamGuard is built on a **Bring Your Own Key (BYOK)**, zero-trust architecture. Your credentials are never at risk:

| Security Mechanism | Detail |
|---|---|
| 🔒 Local-only credential storage | All data lives in `%APPDATA%\StreamGuard\` — **never on any StreamGuard server** |
| 🔐 AES-256 encryption | Your `client_secret.json` is encrypted immediately after import; the plaintext original is discarded |
| 🗝️ Windows Credential Manager | OAuth token encryption keys are stored in the OS keychain, not on the filesystem |
| 🔗 Direct API calls | All requests go directly to Google's servers — no proxy, no middleman, no analytics |
| 👀 Open source | Every line of code is publicly auditable on this repository |

> **What does StreamGuard connect to?**  
> - `accounts.google.com` — OAuth 2.0 authentication  
> - `www.googleapis.com` — YouTube Data API v3 for chat, moderation, and bot messages  
> - `generativelanguage.googleapis.com` — Google Gemini AI for sentiment analysis *(optional — only if you supply a Gemini API key)*

---

## 🖥️ System Requirements

| Requirement | Minimum |
|---|---|
| **Operating System** | Windows 10 (64-bit) or Windows 11 |
| **RAM** | 256 MB available |
| **Disk Space** | ~150 MB (installed) |
| **Internet** | Required for YouTube API calls |
| **Google Account** | A YouTube account with live streaming enabled |

> ⚠️ StreamGuard currently supports **Windows only**. macOS and Linux support is planned for a future release.

---

## 🚀 Installation (No Coding Required)

### Step 1 — Download & Install StreamGuard

1. Navigate to the [**Releases page**](https://github.com/skwasimakram13/StreamGuard/releases/latest)
2. Under **Assets**, download `StreamGuard_Setup_v2.1.3.exe`
3. Run the installer — Windows may show a SmartScreen prompt; click **More info → Run anyway** (the app is not yet code-signed)
4. Accept the defaults and click **Next** through the setup wizard
5. A **StreamGuard** shortcut will appear in your Start Menu (optional Desktop shortcut available)
6. Launch **StreamGuard** — the Setup Wizard will open

> 📌 You must complete **Step 2** before using the app. This is a one-time ~5 minute setup using your own Google account.

---

### Step 2 — Set Up Your Google Cloud Project

StreamGuard uses the official YouTube Data API v3 with your own Google Cloud credentials. This ensures the app can read your live chat, delete messages, and send bot responses — all authenticated **as you**, with no third-party access.

#### 2a. Create a Google Cloud Project

1. Go to [**console.cloud.google.com**](https://console.cloud.google.com/) and sign in with the **Google account you stream from**
2. Click the project dropdown at the top → **New Project**
3. Enter a name (e.g., `StreamGuard`) → click **Create**
4. Ensure your new project is selected in the dropdown before proceeding

#### 2b. Enable the YouTube Data API v3

1. In the left sidebar, navigate to **APIs & Services → Library**
2. Search for **YouTube Data API v3**
3. Click the result → click **Enable**

#### 2c. Configure the OAuth Consent Screen

1. Navigate to **APIs & Services → OAuth consent screen**
2. Select **External** → click **Create**
3. Fill in the required fields:
   - **App name**: `StreamGuard`
   - **User support email**: your email address
   - **Developer contact email**: your email address
4. Click **Save and Continue** through the Scopes and Test Users screens (leave defaults)
5. On the **Test users** page, click **+ Add Users** → add your own Google account email → **Save**
6. Click **Back to Dashboard**

> ⚠️ Your app remains in **Testing** mode permanently. This is expected and correct — it is only ever used by your own account. You do **not** need to publish or verify it.

#### 2d. Create Your OAuth 2.0 Client ID

1. Navigate to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth 2.0 Client ID**
3. Set **Application type** to **Desktop app**
4. Name it anything (e.g., `StreamGuard Desktop`) → click **Create**
5. In the confirmation dialog, click **Download JSON**
6. Save the file somewhere accessible (e.g., your Desktop). It will be named like `client_secret_XXXX.json`

> ✅ You now have your `client_secret.json`. **Keep it private — never share or commit this file.**

---

### Step 3 — Connect StreamGuard to YouTube

1. Launch **StreamGuard**
2. On the Setup Wizard, click **"Select client_secret.json"**
3. Browse to and select the JSON file downloaded in Step 2d
4. Your default browser will open a Google sign-in page
5. Sign in with the **same account you stream from** → click **Allow** on the permissions screen
6. Return to StreamGuard — the main dashboard will appear

> ✅ **You're connected!** StreamGuard will automatically detect your active live stream when you go live.  
> 🔒 Your credentials are AES-256 encrypted and stored locally. You will not need to repeat this process unless you explicitly log out.

---

## 📖 User Guide

### Live Chat Moderation Tab

This is your primary command center during live streams.

| Panel | Description |
|---|---|
| **Live Chat Feed** (left) | Real-time messages appear here as they arrive. Each card shows the author name, message content, and a 🗑️ delete button to manually remove any message from YouTube chat. |
| **Highlights** (center) | Superchats, new memberships, and gifted membership milestones are automatically separated and displayed here with a gold border — so you never miss a supporter. |
| **Moderation Controls** (right) | Master switch, Auto-Mod toggle, polling frequency slider, and banned word list manager. |

**Moderation Controls Reference:**

- **Master Switch** — Enables or disables all chat reading and bot activity for the session
- **Enable Auto-Mod** — When active, any message containing a word from your banned list is automatically deleted from YouTube Live chat in real-time
- **Polling Frequency** — How often (in seconds) StreamGuard polls for new messages. Lower values = more responsive, but consumes more YouTube API quota
- **Banned List Manager** — Enter words separated by commas; click **Update List** to persist the changes

---

### Bots Tab

#### ⏰ Alerts Bot

Sends scheduled messages to your live chat automatically. Ideal for promoting your social links, Discord server, merchandise, or upcoming events.

1. Toggle **Enable Alerts Bot** on
2. Set the **Interval** (in minutes) between each sent message
3. Enter your messages, one per line — StreamGuard cycles through them in order
4. Click **Save Messages**

#### 📣 Engagement Bot

Operates identically to the Alerts Bot, but purpose-built for like/subscribe/follow reminders. Configured separately so you can run both simultaneously at different intervals.

#### ⚡ Custom Commands Bot

Allows your viewers to trigger instant automated responses by typing `!commands` in chat.

**Setup:**
1. Toggle **Enable Commands Bot** on
2. Enter commands using the format: `!command | Response text goes here`  
   Example: `!discord | Join our community at https://discord.gg/yourlink`
3. Add one command per line → click **Save Commands**

**Example commands:**

```
!discord | Join our Discord: https://discord.gg/yourlink
!socials | Find us on Instagram & Twitter: @YourHandle
!donate | Support the stream: https://ko-fi.com/yourpage
!schedule | We go live every Tuesday and Friday at 7PM IST!
```

When a viewer types `!discord`, StreamGuard reads the incoming chat, matches the command, and automatically posts the configured response.

#### 🧠 AI Vibe Meter

Uses **Google Gemini AI** to analyze the aggregate mood of your chat every 15 seconds and displays a real-time sentiment emoji.

| Emoji | Meaning |
|-------|---------|
| 🔥 | Chat is hyped / excited |
| 💖 | Positive / happy and supportive |
| 😡 | Angry / hostile / negative |
| ❓ | Confused or questioning |
| 💬 | Neutral / mixed sentiment |

**To enable:**
1. Obtain a free API key from [**Google AI Studio**](https://aistudio.google.com/app/apikey) — no credit card required
2. Paste the key into the **Gemini API Key** field → click **Save Key**

---

### Loyalty / Top Chatters Tab

StreamGuard maintains a local SQLite database recording every viewer's chat activity across all of your streams.

- Click **Refresh** to load the leaderboard (top 50 viewers ranked by total message count)
- Use the **VIP** toggle next to any viewer to grant them VIP status

> 💡 VIP status is stored permanently in your local database and persists across all future streams. This is ideal for recognizing your most loyal community members.

---

## 🔧 Running From Source (Developers)

If you prefer to run StreamGuard directly from Python rather than using the pre-built installer:

### Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.11 or higher ([download](https://www.python.org/downloads/)) |
| **Operating System** | Windows 10 or 11 (64-bit) |
| **Git** | For cloning the repository |
| **Google Cloud credentials** | `client_secret.json` — see [Step 2](#step-2--set-up-your-google-cloud-project) |

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/skwasimakram13/StreamGuard.git
cd StreamGuard

# 2. Create and activate a virtual environment (strongly recommended)
python -m venv .venv
.venv\Scripts\activate

# 3. Install all Python dependencies
pip install -r requirements.txt

# 4. Launch the application
python main.py
```

> ⚠️ Never run with `sudo` or administrator privileges. StreamGuard does not require elevated permissions.

---

## 🏗️ Building the Installer Yourself

StreamGuard uses the **Flet native build system** (`flet build windows`) which bundles the app, Flutter engine, and all Python dependencies into a self-contained Windows executable — no Python installation required on the end-user's machine.

### Prerequisites

- Python 3.11+ with `flet` installed (`pip install -r requirements.txt`)
- **Flutter SDK** (required by `flet build`) — [install Flutter](https://flutter.dev/docs/get-started/install/windows)
- **Inno Setup 6** (for creating the Windows installer) — [download](https://jrsoftware.org/isinfo.php)
- Visual Studio 2022 with **Desktop development with C++** workload

### Build Steps

```powershell
# Step 1: Build the native Windows application
flet build windows `
  --project StreamGuard `
  --product StreamGuard `
  --org com.streamguard `
  --build-version 2.1.3 `
  --yes

# Step 2: The build output will be in:
# build\windows\x64\runner\Release\StreamGuard.exe

# Step 3: Compile the Windows installer (requires Inno Setup in PATH)
iscc installer.iss

# Step 4: The finished installer will be at:
# InnoSetupOutput\StreamGuard_Setup_v2.1.3.exe
```

> 💡 The CI/CD pipeline automates this entire process. See [⚙️ CI/CD Pipeline](#️-cicd-pipeline) for details.

---

## 🗂️ Project Structure

```
StreamGuard/
├── main.py                  # Core UI (Flet framework), application state, background async loops
├── youtube_engine.py        # All YouTube Data API v3 interactions + exponential backoff retry logic
├── config_manager.py        # Thread-safe encrypted credential storage singleton (AES-256 + keyring)
├── database.py              # SQLite viewer loyalty tracking and leaderboard management
├── sentiment.py             # Google Gemini AI vibe/sentiment analysis engine
├── version.py               # Single source of truth for version number across all build scripts
├── build.py                 # Legacy PyInstaller build script (kept for reference)
├── StreamGuard.spec         # PyInstaller spec file (legacy)
├── installer.iss            # Inno Setup Windows installer script (used in CI/CD)
├── requirements.txt         # Python dependencies with pinned minimum versions
├── pyproject.toml           # Modern Python packaging metadata (PEP 517/518)
├── icon.ico                 # Application icon
│
├── .github/
│   ├── workflows/
│   │   └── build.yml                    # GitHub Actions: automated build & release on version tag push
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                # Structured bug report template
│   │   └── feature_request.md          # Feature suggestion template
│   └── PULL_REQUEST_TEMPLATE.md        # PR checklist for contributors
│
├── CHANGELOG.md             # Version history following Keep a Changelog format
├── CONTRIBUTING.md          # Developer contribution guide and code style rules
├── SECURITY.md              # Security policy and vulnerability reporting procedure
└── LICENSE                  # MIT License
```

**Key architectural principles:**

| Rule | Rationale |
|---|---|
| `config_manager.py` is a **singleton** | All modules share one thread-safe instance to prevent concurrent write conflicts |
| All YouTube API calls go through `youtube_engine.py` | Centralizes retry logic, quota handling, and error normalization |
| Settings are always saved via `ConfigManager.set_setting()` | Ensures encryption is applied consistently; never write raw credential files |
| Background tasks use `asyncio.create_task()` | Non-blocking, cooperative multitasking; avoids threading complexity with the Flet event loop |

---

## ⚙️ CI/CD Pipeline

StreamGuard uses **GitHub Actions** for fully automated builds and releases. The pipeline is defined in [`.github/workflows/build.yml`](.github/workflows/build.yml).

### Trigger Events

| Event | Action |
|---|---|
| `git push` with a `v*.*.*` tag (e.g., `v2.1.3`) | Full build + GitHub Release created automatically |
| Manual `workflow_dispatch` trigger | Full build, installer uploaded as a build artifact (7-day retention) |

### Pipeline Steps

```
1. Checkout source code
2. Set up Python 3.12 with pip caching
3. Install Python dependencies (requirements.txt)
4. Read version from version.py → set VERSION output variable
5. Run: flet build windows --project StreamGuard --yes
6. Locate StreamGuard.exe in the build output (dynamic path resolution)
7. Compile installer: iscc /DReleaseDir="<build_dir>" installer.iss
8. Create GitHub Release with CHANGELOG.md as release notes
9. Attach InnoSetupOutput/StreamGuard_Setup_*.exe to the release
```

### Releasing a New Version

```bash
# 1. Update the version number
# Edit version.py: __version__ = "2.1.3"
# Edit installer.iss: AppVersion=2.1.3, OutputBaseFilename=StreamGuard_Setup_v2.1.3

# 2. Update CHANGELOG.md with the new version section

# 3. Commit, tag, and push
git add -A
git commit -m "chore: release v2.1.3"
git tag v2.1.3
git push origin main --tags
# GitHub Actions will build and publish the release automatically
```

---

## ❓ FAQ & Troubleshooting

**Q: The app says "No active live stream found." but I'm live.**  
A: Ensure you are live on the **exact same YouTube account** you authenticated with in Step 3. Premieres and scheduled streams are not supported — only active live broadcasts. Also confirm your live stream is publicly visible (not private).

**Q: I see a "This app isn't verified" screen from Google.**  
A: This is completely expected. Your Google Cloud project is in Testing mode, which shows this warning for any new browser sign-in. Click **"Advanced" → "Continue to StreamGuard (unsafe)"** → **"Allow"**. This screen only appears the very first time you authenticate.

**Q: The bot sends messages but they don't appear in my chat.**  
A: Ensure your OAuth consent screen includes the `youtube.force-ssl` scope (StreamGuard requests this automatically during authentication). If bots still fail, click **Logout** in the app header and re-authenticate from scratch.

**Q: How do I completely reset StreamGuard?**  
A: Click **Logout** in the top-right corner of the app. This clears all encrypted credentials. You can then import a new `client_secret.json` to start fresh. To delete all data, manually remove the `%APPDATA%\StreamGuard\` folder or use the option during uninstallation.

**Q: Where are my credentials and settings stored?**  
A: All application data is in `%APPDATA%\StreamGuard\` on your PC:

| File | Contents |
|---|---|
| `client_secret.enc` | AES-256 encrypted Google Cloud credentials |
| `settings.json` | App settings including Gemini API key and bot configuration |
| `loyalty.db` | SQLite database of viewer loyalty records |
| `system.log` | Application event log for troubleshooting |

**Q: I hit the YouTube API quota limit. What do I do?**  
A: YouTube's free tier provides ~10,000 units/day per project. StreamGuard displays **"API Quota Exceeded"** in the status bar when this limit is reached. The quota resets daily at midnight Pacific Time (UTC-8). To reduce API usage, increase the polling frequency slider (higher value = less frequent polling = fewer API calls).

**Q: Does StreamGuard support Twitch, Kick, or other platforms?**  
A: StreamGuard currently supports **YouTube Live only**. Support for additional platforms may be considered in future releases. Please open a [Feature Request](https://github.com/skwasimakram13/StreamGuard/issues/new?template=feature_request.md) to express interest.

**Q: Windows Defender / antivirus is flagging the installer.**  
A: This is a false positive common with unsigned applications built with Flet/Flutter. The installer and executable are built transparently in our public [GitHub Actions pipeline](https://github.com/skwasimakram13/StreamGuard/actions). You can audit the [build workflow](.github/workflows/build.yml) and [source code](https://github.com/skwasimakram13/StreamGuard) yourself. Code signing is planned for a future release.

**Q: The app window appears blank on launch.**  
A: This can occur if the Flutter WebView renderer encounters a compatibility issue. Try: right-click the app shortcut → **Run as administrator** once to initialize. If the issue persists, check `%APPDATA%\StreamGuard\system.log` for errors and [file a bug report](https://github.com/skwasimakram13/StreamGuard/issues/new?template=bug_report.md).

---

## 🤝 Contributing

Contributions from the community are welcome and appreciated! Please read [**CONTRIBUTING.md**](CONTRIBUTING.md) for the full developer setup, code style guide, commit message format, and PR workflow before submitting changes.

**Quick start for contributors:**

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/<your-username>/StreamGuard.git
cd StreamGuard
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt

# Create a feature branch
git checkout -b feat/my-awesome-feature

# Make your changes, then commit using Conventional Commits
git commit -m "feat: add channel points integration"

# Push and open a Pull Request against main
git push origin feat/my-awesome-feature
```

Please ensure all PRs:
- Follow the code style guide in `CONTRIBUTING.md`
- Do **not** include any credentials, tokens, or `client_secret.json` files
- Update `CHANGELOG.md` under the `[Unreleased]` section
- Pass a local run test with `python main.py`

---

## 🔒 Security

StreamGuard takes security seriously. Our BYOK architecture means your credentials are never exposed to any third party.

For **vulnerability reports**, please see [**SECURITY.md**](SECURITY.md) for the full disclosure process.  
**Do not open a public GitHub Issue for security bugs** — use the [GitHub Security Advisories](https://github.com/skwasimakram13/StreamGuard/security/advisories/new) channel instead.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

You are free to use, modify, and distribute this software. Contributions back to the project are always appreciated.

---

<div align="center">

Made with ❤️ for the streaming community

**[⬆ Back to Top](#streamguard)**

[![Star on GitHub](https://img.shields.io/github/stars/skwasimakram13/StreamGuard?style=social)](https://github.com/skwasimakram13/StreamGuard)

</div>

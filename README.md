<div align="center">

<img src="icon.ico" width="80" height="80" alt="StreamGuard Logo"/>

# StreamGuard

**Professional YouTube Live Stream Moderation & Bot Management**

[![GitHub Release](https://img.shields.io/github/v/release/skwasimakram13/StreamGuard?style=for-the-badge&logo=github)](https://github.com/skwasimakram13/StreamGuard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D4?style=for-the-badge&logo=windows)](https://github.com/skwasimakram13/StreamGuard/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/skwasimakram13/StreamGuard/build.yml?style=for-the-badge)](https://github.com/skwasimakram13/StreamGuard/actions)

> **StreamGuard** is a free, open-source Windows desktop app that gives YouTube Live streamers real-time chat moderation, smart bots, and AI-powered audience insights — all with your own API credentials, stored securely on your machine. Zero subscriptions. Zero servers. Your data stays yours.

[⬇️ Download Latest Release](https://github.com/skwasimakram13/StreamGuard/releases/latest) &nbsp;·&nbsp; [🐛 Report a Bug](https://github.com/skwasimakram13/StreamGuard/issues/new?template=bug_report.md) &nbsp;·&nbsp; [💡 Request a Feature](https://github.com/skwasimakram13/StreamGuard/issues/new?template=feature_request.md)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🔐 Privacy & Security First](#-privacy--security-first)
- [🚀 Installation (No Coding Required)](#-installation-no-coding-required)
  - [Step 1 — Download & Install StreamGuard](#step-1--download--install-streamguard)
  - [Step 2 — Set Up Your Google Cloud Project](#step-2--set-up-your-google-cloud-project)
  - [Step 3 — Connect StreamGuard to YouTube](#step-3--connect-streamguard-to-youtube)
- [📖 User Guide](#-user-guide)
  - [Live Chat Moderation Tab](#live-chat-moderation-tab)
  - [Bots Tab](#bots-tab)
  - [Loyalty / Top Chatters Tab](#loyalty--top-chatters-tab)
- [🔧 Running From Source (Developers)](#-running-from-source-developers)
- [🏗️ Building the EXE Yourself](#-building-the-exe-yourself)
- [🗂️ Project Structure](#️-project-structure)
- [❓ FAQ & Troubleshooting](#-faq--troubleshooting)
- [🤝 Contributing](#-contributing)
- [🔒 Security](#-security)
- [📄 License](#-license)

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
- ✅ Your `client_secret.json` is **AES-256 encrypted** immediately after import and the original file is not kept
- ✅ OAuth tokens are stored encrypted and managed via **Windows Credential Manager**
- ✅ API calls go **directly** to Google's servers — no proxy, no middleman
- ✅ The app is fully **open-source** — audit every line of code yourself

---

## 🚀 Installation (No Coding Required)

### Step 1 — Download & Install StreamGuard

1. Go to the [**Releases page**](https://github.com/skwasimakram13/StreamGuard/releases/latest)
2. Download `StreamGuard_Setup_v2.0.0.exe`
3. Run the installer — accept the defaults and click **Next** through the wizard
4. A **StreamGuard** shortcut will appear in your Start Menu (optionally on your Desktop)
5. Launch **StreamGuard** — you will see the Setup Wizard

> You need to complete **Step 2** before you can use the app. This is a one-time, ~5 minute setup.

---

### Step 2 — Set Up Your Google Cloud Project

StreamGuard connects directly to YouTube's official API using your own Google Cloud credentials. This is required so the app can read your live chat, delete messages, and send bot messages — all on your behalf.

#### 2a. Create a Google Cloud Project

1. Go to [**console.cloud.google.com**](https://console.cloud.google.com/) and sign in with your Google account (the one you stream from)
2. Click the project dropdown at the top → **New Project**
3. Give it a name (e.g. `StreamGuard`) → click **Create**
4. Make sure your new project is selected in the dropdown

#### 2b. Enable the YouTube Data API v3

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for **YouTube Data API v3**
3. Click it → click **Enable**

#### 2c. Configure the OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** → click **Create**
3. Fill in the required fields:
   - **App name**: `StreamGuard`
   - **User support email**: your email
   - **Developer contact email**: your email
4. Click **Save and Continue** through the next screens (Scopes and Test Users — you can leave them as defaults)
5. On the **Test users** page, click **+ Add Users** and add your own Google account email → **Save**
6. Click **Back to Dashboard**

> ⚠️ Your app will stay in **Testing** mode. This is fine — it's only used by you. You do not need to publish it.

#### 2d. Create Your OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth 2.0 Client ID**
3. Set **Application type** to **Desktop app**
4. Name it anything (e.g. `StreamGuard Desktop`) → click **Create**
5. A dialog will appear — click **Download JSON**
6. Save this file somewhere you can find it (e.g. your Desktop). It will be named something like `client_secret_XXXX.json`

> ✅ You now have your `client_secret.json`. Keep it safe — don't share it.

---

### Step 3 — Connect StreamGuard to YouTube

1. Launch **StreamGuard**
2. On the Setup Wizard screen, click **"Select client_secret.json"**
3. Navigate to and select the JSON file you downloaded in Step 2d
4. Your browser will open asking you to sign in to Google and grant permission
5. Sign in with the **same account you stream from** → click **Allow**
6. Return to StreamGuard — you will see the dashboard

> ✅ **You're connected!** StreamGuard will automatically detect your active live stream when you go live.

> 🔒 After this, StreamGuard encrypts and stores your credentials locally. You will not need to do this again unless you log out.

---

## 📖 User Guide

### Live Chat Moderation Tab

This is your main command center when you're live.

- **Live Chat Feed** (left panel) — Real-time messages appear here. Each card shows the author name and message. Click the 🗑️ (delete) icon on any card to manually remove a message from YouTube chat.
- **Highlights** (middle panel) — Superchats, new memberships, and milestone messages are automatically pulled out and displayed here with a gold border so you never miss them.
- **Moderation Controls** (right panel):
  - **Master Switch** — Turns all chat reading and bot activity on/off
  - **Enable Auto-Mod** — When on, any message containing a banned word is automatically deleted from YouTube chat in real-time
  - **Polling Frequency** — How often (in seconds) StreamGuard checks for new messages. Lower = more responsive, but uses more API quota.
  - **Banned List Manager** — Enter words separated by commas. Click **Update List** to save.

---

### Bots Tab

#### ⏰ Alerts Bot
Sends scheduled messages to your chat automatically (great for promos, social links, Discord invites).

1. Toggle **Enable Alerts Bot** on
2. Set the **Interval** — how many minutes between each message
3. Enter your messages, one per line (StreamGuard cycles through them in order)
4. Click **Save Messages**

#### 📣 Engagement Bot
Same as Alerts Bot, but specifically for like/subscribe/follow reminders.

#### ⚡ Custom Commands Bot
Let your chat trigger instant responses with `!commands`.

1. Toggle **Enable Commands Bot** on
2. Enter commands in the format: `!command | Your response text`  
   Example: `!discord | Join us at https://discord.gg/yourlink`
3. One command per line → click **Save Commands**

When a viewer types `!discord`, StreamGuard automatically replies with the configured response.

#### 🧠 AI Vibe Meter
Uses Google's Gemini AI to analyze the mood of your chat every 15 seconds and shows you one emoji:

| Emoji | Meaning |
|-------|---------|
| 🔥 | Chat is hyped / excited |
| 💖 | Positive / happy vibes |
| 😡 | Angry / negative |
| ❓ | Confused |
| 💬 | Neutral / mixed |

**To enable:**
1. Get a free API key from [**Google AI Studio**](https://aistudio.google.com/app/apikey) (free, no credit card needed)
2. Paste the key in the **Gemini API Key** field → click **Save Key**

---

### Loyalty / Top Chatters Tab

StreamGuard tracks every viewer who chats and records their message count in a local database.

- Click **Refresh** to load the leaderboard (top 50 by message count)
- Toggle the **VIP** switch on any viewer to mark them as a VIP

> 💡 VIP status is stored locally and persists across streams. Great for recognizing your most loyal regulars.

---

## 🔧 Running From Source (Developers)

If you want to run StreamGuard directly from Python instead of using the installer:

### Prerequisites

- **Python 3.11 or higher** — [Download here](https://www.python.org/downloads/)  
  *(Check your version: `python --version`)*
- **Windows 10 or 11**
- A Google Cloud OAuth `client_secret.json` (see [Step 2](#step-2--set-up-your-google-cloud-project) above)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/skwasimakram13/StreamGuard.git
cd StreamGuard

# 2. Create a virtual environment (strongly recommended)
python -m venv .venv
.venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

---

## 🏗️ Building the EXE Yourself

```bash
# Make sure your venv is active and requirements are installed
python build.py

# Output: dist\StreamGuard\StreamGuard.exe
```

To create a Windows installer (requires [Inno Setup](https://jrsoftware.org/isinfo.php)):
1. Open `installer.iss` in **Inno Setup Compiler**
2. Click **Build** → output: `InnoSetupOutput\StreamGuard_Setup_v2.0.0.exe`

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
│   ├── workflows/build.yml          # GitHub Actions: auto-build & release EXE on tag push
│   ├── ISSUE_TEMPLATE/bug_report.md
│   ├── ISSUE_TEMPLATE/feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

---

## ❓ FAQ & Troubleshooting

**Q: The app says "No active live stream found." but I'm live.**  
A: Make sure you are live on the **same YouTube account** you authenticated with. Premieres and scheduled streams don't count — you need to be actively streaming.

**Q: I get a "This app isn't verified" screen from Google.**  
A: This is normal because your Cloud project is in Testing mode. Click **"Continue"** → **"Allow"**. This screen only appears during the initial login.

**Q: The bot sends messages but they don't appear in my chat.**  
A: Your Google Cloud project's OAuth scope needs `youtube.force-ssl`. This is automatically requested by StreamGuard. If bots still don't send, try logging out and re-authenticating.

**Q: How do I reset / start fresh?**  
A: Click **Logout** in the top-right corner. This clears your encrypted credentials. You can then import a new `client_secret.json`.

**Q: Where are my credentials stored?**  
A: All data is in `%APPDATA%\StreamGuard\` on your PC. Credentials are AES-256 encrypted. Logs are in `%APPDATA%\StreamGuard\system.log`.

**Q: I hit the YouTube API quota limit.**  
A: YouTube's free tier allows ~10,000 units/day. StreamGuard shows "API Quota Exceeded" in the status bar when this happens. It resets at midnight Pacific Time. Increase the polling frequency slider to reduce API usage.

**Q: Does StreamGuard work with Twitch or other platforms?**  
A: Currently, StreamGuard only supports YouTube Live. Twitch/Kick support may be considered in future releases — please open a Feature Request.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for code style, commit format, and the PR workflow.

```bash
git checkout -b feat/my-feature
# make your changes
git commit -m "feat: describe your change"
git push origin feat/my-feature
# Open a Pull Request on GitHub
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

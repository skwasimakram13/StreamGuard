# Security Policy

## Supported Versions

The following versions of StreamGuard receive active security support:

| Version | Status | Notes |
|---------|--------|-------|
| 2.0.x   | ✅ **Active support** | Current stable release — all security patches applied |
| 1.0.x   | ❌ **End of life** | No further updates; please upgrade to v2.0.x |

> We strongly recommend always running the latest release. Older versions will not receive security patches.

---

## Architecture: Bring Your Own Key (BYOK)

StreamGuard is designed from the ground up with a **zero-trust, Bring Your Own Key (BYOK)** architecture. This means your private credentials never leave your machine and are never stored, processed, or even seen by any StreamGuard server — because there is no StreamGuard server.

### Credential Storage Model

| Credential | Storage Location | Encryption |
|---|---|---|
| `client_secret.json` contents | `%APPDATA%\StreamGuard\client_secret.enc` | AES-256 (Fernet) |
| OAuth 2.0 refresh & access tokens | `%APPDATA%\StreamGuard\client_secret.enc` | AES-256 (Fernet) |
| AES encryption key | Windows Credential Manager (OS keychain) | OS-level protection (DPAPI) |
| Gemini API key | `%APPDATA%\StreamGuard\settings.json` | Plaintext — protect with filesystem permissions |
| Viewer loyalty database | `%APPDATA%\StreamGuard\loyalty.db` | Unencrypted (no PII stored) |

**Key technical details:**
- The AES encryption key is generated once per installation using `os.urandom(32)` and stored in the OS keychain via `keyring` — it is never written to the filesystem
- The raw `client_secret.json` file is encrypted and stored as `.enc` immediately after import; the plaintext original is not retained by the app
- All OAuth token refresh operations use the official `google-auth-oauthlib` library — no custom token handling code

### Network Connections

StreamGuard makes direct API calls **only** to the following Google-owned endpoints:

| Endpoint | Purpose | When |
|---|---|---|
| `accounts.google.com` | OAuth 2.0 authentication and token refresh | During login and on token expiry |
| `www.googleapis.com` | YouTube Data API v3 (chat, moderation, bot messages) | While streaming is active |
| `generativelanguage.googleapis.com` | Google Gemini AI sentiment analysis | Every 15 seconds when AI Vibe Meter is enabled |

> **StreamGuard makes zero connections to any non-Google server.** There are no analytics, telemetry, crash reporting, or license validation calls. You can verify this by inspecting the source code — particularly `youtube_engine.py` and `sentiment.py`.

---

## What Data Is Collected?

**None.** StreamGuard collects no data whatsoever:

- ❌ No analytics or usage telemetry
- ❌ No crash reporting to any external service
- ❌ No email, name, or account identifiers sent anywhere
- ❌ No viewer chat content stored outside your local machine
- ✅ The only persistent data is your viewer loyalty database (`loyalty.db`) — stored **locally** on your PC

---

## Reporting a Vulnerability

If you discover a security vulnerability in StreamGuard, please **do not** open a public GitHub Issue. Disclosing a vulnerability publicly before it is patched puts all users at risk.

### Preferred Reporting Channel

1. **GitHub Security Advisories** *(preferred)*: Navigate to the repository's [Security tab](https://github.com/skwasimakram13/StreamGuard/security) and click **"Report a vulnerability"** — this opens a private, encrypted disclosure channel directly with the maintainers.

2. **Email** *(alternative)*: If you cannot use GitHub, contact the maintainer directly via the email address on their [GitHub profile](https://github.com/skwasimakram13).

### What to Include in Your Report

Please provide as much of the following as possible:

- **Description**: A clear explanation of the vulnerability and its potential impact
- **Affected versions**: Which version(s) of StreamGuard are affected
- **Steps to reproduce**: A precise, minimal sequence of steps that triggers the vulnerability
- **Proof of concept**: Code, screenshots, or logs demonstrating the issue (if safe to share)
- **Suggested fix** *(optional but appreciated)*: Your recommended remediation approach

### Response Timeline

| Milestone | Target |
|---|---|
| Initial acknowledgment of your report | Within **72 hours** |
| Confirmation of vulnerability (or closure if not applicable) | Within **7 days** |
| Patch release for confirmed critical vulnerabilities | Within **14 days** |
| Public disclosure (coordinated with reporter) | After patch is released |

We are committed to handling all security reports responsibly and transparently. Reporters who responsibly disclose valid vulnerabilities will be credited in the release notes (with your permission).

---

## Security Best Practices for Users

Follow these guidelines to keep your StreamGuard installation secure:

1. **Only use a Google Cloud project you own.** Never import a `client_secret.json` file received from someone else — it could grant a third party access to your YouTube account.

2. **Keep your `%APPDATA%\StreamGuard\` directory private.** Do not share, back up to an unencrypted cloud service, or sync this folder to any location you do not fully control.

3. **Revoke application access when you stop using StreamGuard.** Visit [Google Account Permissions](https://myaccount.google.com/permissions), find StreamGuard (listed under your OAuth app name), and click **Remove access**.

4. **Consider using a dedicated Google account.** If you stream professionally, consider using a separate Google account specifically for streaming. This limits the blast radius if credentials are ever compromised.

5. **Keep the app updated.** Always run the latest version of StreamGuard. Security patches are released as new `2.0.x` versions. Subscribe to [GitHub Releases](https://github.com/skwasimakram13/StreamGuard/releases) notifications to be informed of new releases.

6. **Protect your `settings.json`.** The Gemini API key is stored in plaintext in this file. Ensure your user profile has appropriate access controls and that the `%APPDATA%` directory is not accessible to other users on your machine.

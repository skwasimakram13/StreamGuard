# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | ✅ Active support  |
| 1.x.x   | ❌ End of life     |

## Architecture: Bring Your Own Key (BYOK)

StreamGuard is built on a **zero-trust, BYOK architecture**. This means:

- **We never store your credentials on any server.** All OAuth tokens and API keys are stored **exclusively on your local machine**.
- OAuth tokens are **AES-256 encrypted** using a key stored in the Windows Credential Manager (not in the filesystem).
- Your `client_secret.json` is encrypted and stored in `%APPDATA%\StreamGuard\` as `client_secret.enc`. The raw file is never kept.
- Your Gemini API key is stored in the local `settings.json` file — treat this file with appropriate filesystem permissions.

## What Data Is Collected?

**Absolutely nothing is sent to any StreamGuard server.** The app makes API calls directly to:
- `accounts.google.com` — for OAuth authentication
- `www.googleapis.com` — for YouTube Live API calls
- `generativelanguage.googleapis.com` — for Gemini sentiment analysis (optional, only if you provide an API key)

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public GitHub Issue.

Instead, please report it privately via:

1. **GitHub Security Advisories**: Navigate to the `Security` tab of the repository and click `Report a vulnerability`.
2. **Email**: If you cannot use GitHub, email the maintainer directly (see profile).

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional but appreciated)

We aim to respond to security reports within **72 hours** and release a patch within **14 days** for confirmed critical vulnerabilities.

## Security Best Practices for Users

1. **Only use a Google Cloud project you own.** Do not use a `client_secret.json` from an untrusted source.
2. **Never share your `%APPDATA%\StreamGuard\` directory.**
3. **Revoke access** via [Google Account Permissions](https://myaccount.google.com/permissions) if you no longer use the app.
4. **Use a dedicated Google account** for streaming with limited access if possible.

# StreamGuard Implementation Plan

This document outlines the plan to build "StreamGuard", a high-security local Windows desktop application built with Python and Flet for YouTube Live Stream moderation using a Bring Your Own Key (BYOK) architecture.

## User Review Required

> [!IMPORTANT]
> - **Encryption Key Storage:** The plan currently suggests deriving a key from the Windows machine GUID or securely storing it via the OS keyring (using `keyring` library) since deriving a deterministic key from hardware ID across reboots can sometimes be flaky. I will use the `keyring` library to securely store the Fernet key in the Windows Credential Manager. Let me know if you prefer a strictly hardware-derived approach (e.g., using WMI to get motherboard serial) despite the flakiness risks.
> - **Inno Setup:** The plan includes creating the `installer.iss` file. However, you will need to have Inno Setup installed on your machine to actually compile the `.iss` file into an `.exe` installer.
> - **Icon:** I will create a placeholder `icon.ico` using a base64 encoded string or a simple generated image. You can replace it later with your actual icon.

## Proposed Changes

---

### Security & Storage Architecture

#### [NEW] [config_manager.py](file:///d:/App/StreamerGuard/config_manager.py)
- Create `ConfigManager` class using the singleton pattern to ensure thread safety.
- Implement thread-safe read/write operations using `threading.Lock`.
- Configure paths to use `%APPDATA%\StreamGuard`.
- Implement `cryptography.fernet` for encryption/decryption.
- Use the `keyring` Python library to securely store and retrieve the Fernet key in the Windows Credential Manager.
- Handle secure saving and loading of `token.json`, `client_secret.json`, and general settings.

---

### Resilient YouTube Engine

#### [NEW] [youtube_engine.py](file:///d:/App/StreamerGuard/youtube_engine.py)
- Setup the Python `logging` module to log to `%APPDATA%\StreamGuard\system.log`.
- Create a `YouTubeEngine` class that integrates with `google-api-python-client`.
- Implement OAuth flow using `google-auth-oauthlib`, storing tokens via `ConfigManager`.
- Add exponential backoff logic for 5xx and 403 API errors using the `tenacity` library or a custom retry decorator.
- Implement a background heartbeat task using `asyncio` that checks internet connectivity and API quota status every 60 seconds, exposing a status variable for the UI.

---

### Professional Frontend UI

#### [NEW] [main.py](file:///d:/App/StreamerGuard/main.py)
- Initialize Flet app in async mode with a Dark-Material theme.
- Create a custom SnackBar wrapper for easy "Toast" notifications (success, errors, warnings).
- Implement a **Setup Wizard** view:
  - Step-by-step onboarding for BYOK.
  - File picker to select `client_secret.json`.
  - Visual Connection Status indicator (Green/Red).
- Implement a **Dashboard** view:
  - Real-time scrolling Chat Feed with "Delete message" buttons.
  - "Banned List" Manager with a bulk-import text area or file picker.
  - "Auto-Mod" toggle and a 'Sensitivity' slider.
- Manage navigation and state between the Setup Wizard and Dashboard based on whether valid credentials exist in `ConfigManager`.

---

### Production Build & Installer Logic

#### [NEW] [build.py](file:///d:/App/StreamerGuard/build.py)
- A Python script using `PyInstaller` programmatically (or generating a spec file) to create a directory build.
- Use `--noconsole` to hide the terminal.
- Use `--collect-all google-api-python-client`, `--collect-all google-auth-oauthlib`, and `--collect-all google-auth-httplib2` to bundle all necessary hidden imports.
- Include the application icon (`--icon=icon.ico`).

#### [NEW] [installer.iss](file:///d:/App/StreamerGuard/installer.iss)
- An Inno Setup script to package the PyInstaller output directory into a professional `.exe` installer.
- Publisher set to "StreamGuard Tools".
- Add prompts for Firewall exceptions.
- Implement a custom uninstaller step (`[Code]` section) to ask the user if they want to keep or delete the `%APPDATA%\StreamGuard` directory.

#### [NEW] [requirements.txt](file:///d:/App/StreamerGuard/requirements.txt)
- Include all necessary dependencies: `flet`, `google-api-python-client`, `google-auth-oauthlib`, `cryptography`, `pyinstaller`, `keyring`, `tenacity`.

## Verification Plan

### Automated Tests
- Since this involves UI and OAuth flows, automated unit testing is limited without mock tokens. We will rely on manual testing of the UI components and API responses.

### Manual Verification
- Run `main.py` directly to verify the Flet UI opens.
- Verify the Setup Wizard can correctly prompt for and securely store the `client_secret.json`.
- Check if `%APPDATA%\StreamGuard` is created and contains encrypted token files.
- Verify the YouTube engine attempts connection and logs to `system.log`.
- Run `build.py` to ensure PyInstaller successfully creates the `dist/` folder with all dependencies.

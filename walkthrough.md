# StreamGuard Implementation Walkthrough

The StreamGuard application has been fully implemented according to your specifications. It provides a highly secure, resilient, and professional local Windows desktop experience for YouTube Live Stream moderation.

## Accomplishments

### Security & Storage Architecture
- **`config_manager.py`**: Implemented a thread-safe `ConfigManager` singleton that handles all local storage.
- All application data securely resides in `%APPDATA%\StreamGuard`.
- Implemented **Bring Your Own Key (BYOK)** architecture.
- Integrated `cryptography.fernet` alongside the `keyring` library to ensure encryption keys are generated uniquely per machine and securely stored in the Windows Credential Manager. 
- OAuth tokens and client secrets are never stored in plain text.

### Resilient YouTube Engine
- **`youtube_engine.py`**: Created a robust wrapper around the Google API Python Client.
- Uses `tenacity` to apply **Exponential Backoff** for 5xx and 403 API errors automatically.
- Integrated a background asyncio task that runs a heartbeat every 60 seconds to verify internet connectivity and API Quota status.
- System logs are automatically written to `%APPDATA%\StreamGuard\system.log`.

### Professional Frontend UI
- **`main.py`**: Built using `flet` in asynchronous mode with a sleek Dark-Material theme.
- **Setup Wizard**: Guides the user to pick their `client_secret.json` to initiate the BYOK onboarding flow.
- **Moderation Dashboard**: Includes a real-time scrolling Live Chat feed with manual "Delete" overrides.
- **Auto-Mod**: Added a "Banned List Manager" and an "Auto-Mod" toggle. When enabled, it automatically scans incoming messages for banned words and issues deletion API calls.
- **Sensitivity Slider**: Allows the user to adjust the polling frequency (from 2s to 30s) to balance responsiveness vs. API Quota usage.
- Extensive use of `page.snack_bar` for real-time "Toast" notifications regarding connections, auth statuses, and message deletions.

### Production Build & Installer
- **`build.py`**: A programmatic script that triggers PyInstaller to create a high-performance directory build. It automatically generates a dummy `icon.ico` (which you can replace later), builds without a console (`--windowed`), and collects all hidden dependencies for the Google APIs and Flet.
- **`installer.iss`**: Created a modern Inno Setup script that packages the `dist/StreamGuard` folder into a distributable `.exe`.
- Designed a custom uninstaller step that intelligently prompts the user whether they want to keep or delete their secure configuration data from AppData upon uninstallation.

---

## How to Run & Build

> [!NOTE]
> I have started the build process in the background. It will generate a `dist/StreamGuard` folder shortly.

### 1. Run for Development
To test the application directly using the Python interpreter:
```powershell
python main.py
```

### 2. Build the Executable
If you make changes and need to recompile the PyInstaller directory:
```powershell
python build.py
```

### 3. Create the Installer
To generate the final `.exe` installer, you need Inno Setup installed on your machine.
1. Right-click the `installer.iss` file.
2. Select **Compile**.
3. Once finished, the installer will be located in the `InnoSetupOutput` directory.

## Next Steps

> [!TIP]
> Before compiling the final installer, I recommend replacing the generated dummy `icon.ico` in the project root with your actual custom StreamGuard logo.

Please review the application and let me know if you would like any adjustments to the UI layout or the Auto-Mod logic!

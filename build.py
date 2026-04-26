"""
StreamGuard — PyInstaller Build Script
Run: python build.py
Output: dist/StreamGuard/StreamGuard.exe
"""
import PyInstaller.__main__
import os
import sys
from version import __version__


def create_dummy_icon():
    icon_path = "icon.ico"
    if not os.path.exists(icon_path):
        import base64
        ico_data = b"AAABAAEAAQAAAAEAIABoAQAARgAAACgAAAABAAAAAgAAAAEAIAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
        with open(icon_path, "wb") as f:
            f.write(base64.b64decode(ico_data))
        print(f"Created dummy {icon_path}")


def build_app():
    print(f"Starting StreamGuard v{__version__} Build Process...")

    create_dummy_icon()

    args = [
        "main.py",
        f"--name=StreamGuard",
        "--windowed",          # No console window
        "--onedir",            # Directory build (faster startup than --onefile)
        "--icon=icon.ico",
        "--clean",
        "--noconfirm",
        # Flet
        "--collect-all=flet",
        # Google API stack
        "--collect-all=googleapiclient",
        "--collect-all=google_auth_oauthlib",
        "--collect-all=google.auth",
        "--collect-all=google.genai",
        "--collect-all=httplib2",
        # Cryptography / keyring
        "--collect-all=cryptography",
        "--collect-binaries=keyring",
        # Hidden imports for dynamic loaders
        "--hidden-import=config_manager",
        "--hidden-import=youtube_engine",
        "--hidden-import=database",
        "--hidden-import=sentiment",
        "--hidden-import=version",
        "--hidden-import=keyring.backends.Windows",
    ]

    PyInstaller.__main__.run(args)
    print(f"\nBuild complete — dist/StreamGuard/StreamGuard.exe  (v{__version__})")


if __name__ == "__main__":
    build_app()

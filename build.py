"""
StreamGuard — Build Script
Uses `flet pack` to package the app into a standalone executable.
No Visual Studio or Flutter installation is required!

Usage:
  python build.py

Output:
  dist/StreamGuard/StreamGuard.exe
"""
import subprocess
import sys
import os
from version import __version__

def build_app():
    print(f"Starting StreamGuard v{__version__} Build Process...")
    print("Using: flet pack (PyInstaller wrapper)\n")

    cmd = [
        sys.executable, "-m", "flet", "pack", "main.py",
        "--name", "StreamGuard",
        "--icon", "icon.ico",
        "--hidden-import", "config_manager",
        "--hidden-import", "youtube_engine",
        "--hidden-import", "database",
        "--hidden-import", "sentiment",
        "--hidden-import", "version",
        "--hidden-import", "keyring.backends.Windows",
        "--hidden-import", "google.genai",
        "--hidden-import", "cryptography",
    ]

    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

    if result.returncode == 0:
        exe_path = os.path.join("dist", "StreamGuard.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n✅ Build complete — {exe_path}  ({size_mb:.1f} MB)  v{__version__}")
        else:
            print("\n✅ Build complete — check the dist/ folder.")
    else:
        print("\n❌ Build failed.")
        sys.exit(1)

if __name__ == "__main__":
    build_app()

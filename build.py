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
        "flet", "build", "windows",
        "--project", "StreamGuard",
        "--product", "StreamGuard",
        "--org", "com.streamguard",
        "--build-version", __version__,
        "--yes",
    ]

    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

    if result.returncode == 0:
        exe_dir = os.path.join("build", "flutter", "windows")
        if os.path.exists(exe_dir):
            print(f"\n[SUCCESS] Build complete — check the {exe_dir} folder. v{__version__}")
        else:
            print("\n[SUCCESS] Build complete.")
    else:
        print("\n[ERROR] Build failed.")
        sys.exit(1)

if __name__ == "__main__":
    build_app()

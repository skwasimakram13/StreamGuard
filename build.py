"""
StreamGuard — Build Script
Uses `flet build windows` (the official Flet packaging tool for Flet 0.80+).

Requirements for local builds:
  1. Visual Studio 2022 (or Build Tools) with "Desktop development with C++" workload
     Download: https://visualstudio.microsoft.com/downloads/
  2. All Python dependencies: pip install -r requirements.txt

Usage:
  python build.py

Output:
  build/windows/x64/runner/Release/StreamGuard.exe
"""
import subprocess
import sys
import os
from version import __version__


def build_app():
    print(f"Starting StreamGuard v{__version__} Build Process...")
    print("Using: flet build windows (Flutter-based native Windows build)\n")

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        ["flet", "build", "windows", "--verbose"],
        env=env,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )

    if result.returncode == 0:
        exe_path = os.path.join(
            "build", "windows", "x64", "runner", "Release", "StreamGuard.exe"
        )
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n✅ Build complete — {exe_path}  ({size_mb:.1f} MB)  v{__version__}")
        else:
            print("\n✅ Build complete — check the build/windows/ folder.")
    else:
        print("\n❌ Build failed.")
        print("\nCommon fix: Install Visual Studio 2022 with 'Desktop development with C++' workload.")
        print("Download: https://visualstudio.microsoft.com/downloads/")
        sys.exit(1)


if __name__ == "__main__":
    build_app()

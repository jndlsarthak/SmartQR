#!/usr/bin/env python3
# ===== PHASE 3: Basic QR Generation =====
"""SmartQR launcher - installs deps if needed and runs the app."""

import os
import subprocess
import sys
from pathlib import Path

# Run from smartqr directory
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

def ensure_deps():
    """Install requirements if any package is missing."""
    required = ["sqlalchemy", "fastapi", "uvicorn", "qrcode", "PIL"]  # PIL = Pillow
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print("Installing dependencies...")
        cmd = [
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
            "--trusted-host", "pypi.org",
            "--trusted-host", "files.pythonhosted.org",
        ]
        try:
            subprocess.check_call(cmd, cwd=ROOT)
        except subprocess.CalledProcessError:
            print("If SSL errors occur, try: pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org")
            raise

if __name__ == "__main__":
    ensure_deps()
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

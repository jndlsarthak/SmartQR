#!/usr/bin/env python3
# ===== PHASE 3: Basic QR Generation =====
"""SmartQR launcher - installs deps if needed and runs the app."""

import os
import socket
import subprocess
import sys
from pathlib import Path

# Run from smartqr directory
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)


def get_local_ip() -> str | None:
    """Get this machine's LAN IP (for phone scanning on same network)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


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

    # Listen on all interfaces (0.0.0.0) so phones on same WiFi can connect
    host = "0.0.0.0"
    port = 8000

    # Auto-set SMARTQR_BASE_URL so new QRs encode the LAN IP (scannable by phone)
    if "SMARTQR_BASE_URL" not in os.environ:
        local_ip = get_local_ip()
        if local_ip:
            os.environ["SMARTQR_BASE_URL"] = f"http://{local_ip}:{port}"
            print(f"SmartQR: New QRs will use http://{local_ip}:{port} (phone-scannable on same WiFi)")

    import uvicorn
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

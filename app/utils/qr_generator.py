# ===== PHASE 3: Basic QR Generation =====
"""
QR code image generation and saving.
Generates simple black & white QR codes to static/qrcodes/.
"""

import os
from pathlib import Path

import qrcode


def get_qrcodes_dir() -> Path:
    """Return the absolute path to static/qrcodes/ directory."""
    # app/utils/qr_generator.py -> project root
    project_root = Path(__file__).resolve().parent.parent.parent
    return project_root / "static" / "qrcodes"


def generate_qr_image(
    data: str,
    filename: str,
    fill_color: str = "black",
    back_color: str = "white",
) -> str:
    """
    Generate a QR code PNG and save to static/qrcodes/.
    Returns the relative path to the saved file (e.g. qrcodes/{id}.png).
    """
    qrcodes_dir = get_qrcodes_dir()
    qrcodes_dir.mkdir(parents=True, exist_ok=True)

    filepath = qrcodes_dir / filename

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(str(filepath))

    return f"qrcodes/{filename}"

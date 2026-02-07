# ===== PHASE 3: Basic QR Generation =====
# ===== PHASE 6: Styling Engine =====
"""
QR code image generation and saving.
Supports custom colors and optional logo in center.
"""

from pathlib import Path

import qrcode
from PIL import Image


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_qrcodes_dir() -> Path:
    """Return the absolute path to static/qrcodes/ directory."""
    return _get_project_root() / "static" / "qrcodes"


def _resize_logo_safe(logo: Image.Image, qr_size: int, max_ratio: float = 0.2) -> Image.Image:
    """Resize logo to fit safely in QR center (max 20% of QR size by default)."""
    max_logo = int(qr_size * max_ratio)
    w, h = logo.size
    if w <= max_logo and h <= max_logo:
        return logo
    ratio = min(max_logo / w, max_logo / h)
    new_size = (int(w * ratio), int(h * ratio))
    return logo.resize(new_size, Image.Resampling.LANCZOS)


def _paste_logo_center(qr_img: Image.Image, logo_path: str | Path) -> Image.Image:
    """Paste resized logo in center of QR image. Returns new image."""
    path = Path(logo_path)
    if not path.is_absolute():
        path = _get_project_root() / path
    if not path.exists():
        return qr_img

    logo = Image.open(path).convert("RGBA")
    qr_img = qr_img.convert("RGBA")
    qr_w, qr_h = qr_img.size
    logo = _resize_logo_safe(logo, min(qr_w, qr_h))

    lw, lh = logo.size
    x = (qr_w - lw) // 2
    y = (qr_h - lh) // 2
    qr_img.paste(logo, (x, y), logo)
    return qr_img.convert("RGB")


def generate_qr_image(
    data: str,
    filename: str,
    fill_color: str = "black",
    back_color: str = "white",
    logo_path: str | Path | None = None,
) -> str:
    """
    Generate a QR code PNG and save to static/qrcodes/.
    Supports custom fill/back colors and optional logo in center.
    Uses high error correction when logo is present for better scan reliability.
    """
    qrcodes_dir = get_qrcodes_dir()
    qrcodes_dir.mkdir(parents=True, exist_ok=True)
    filepath = qrcodes_dir / filename

    error_level = qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_M
    qr = qrcode.QRCode(version=1, error_correction=error_level, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    if logo_path:
        img = _paste_logo_center(img, logo_path)

    img.save(str(filepath))
    return f"qrcodes/{filename}"

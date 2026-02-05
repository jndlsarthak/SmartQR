# ===== PHASE 3: Basic QR Generation =====
# ===== PHASE 4: Dynamic Redirect System =====
"""
Service layer for QR code creation.
Generates QR image and stores DB record.
QR encodes redirect URL (e.g. /r/{id}) so scans are tracked.
"""

import os
import uuid
from sqlalchemy.orm import Session

from app.models import QRCode
from app.utils.qr_generator import generate_qr_image

BASE_URL = os.environ.get("SMARTQR_BASE_URL", "http://127.0.0.1:8000")


def create_qr(
    db: Session,
    name: str,
    original_data: str,
    redirect_url: str | None = None,
    fill_color: str = "black",
    back_color: str = "white",
) -> QRCode:
    """
    Create a QR code: generate PNG, save to static/qrcodes/, store in DB.
    Returns the QRCode model instance.
    """
    qr_id = str(uuid.uuid4())
    filename = f"{qr_id}.png"

    # QR encodes our redirect URL so scans go through our server and get logged
    redirect_link = f"{BASE_URL.rstrip('/')}/r/{qr_id}"
    generate_qr_image(
        data=redirect_link,
        filename=filename,
        fill_color=fill_color,
        back_color=back_color,
    )

    # Store record in database
    qr = QRCode(
        id=qr_id,
        name=name,
        original_data=original_data,
        redirect_url=redirect_url or original_data,
        fill_color=fill_color,
        back_color=back_color,
        logo_path=None,
    )
    db.add(qr)
    db.commit()
    db.refresh(qr)

    return qr

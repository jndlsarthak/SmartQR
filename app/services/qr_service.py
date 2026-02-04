# ===== PHASE 3: Basic QR Generation =====
"""
Service layer for QR code creation.
Generates QR image and stores DB record.
"""

import uuid
from sqlalchemy.orm import Session

from app.models import QRCode
from app.utils.qr_generator import generate_qr_image


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

    # Generate and save QR image
    relative_path = generate_qr_image(
        data=original_data,
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

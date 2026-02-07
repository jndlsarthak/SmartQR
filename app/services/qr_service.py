# ===== PHASE 3: Basic QR Generation =====
# ===== PHASE 4: Dynamic Redirect System =====
# ===== PHASE 6: Styling Engine =====
# ===== PHASE 7: QR Templates =====
"""
Service layer for QR code creation.
Generates QR image and stores DB record.
QR encodes redirect URL (e.g. /r/{id}) so scans are tracked.
"""

import os
import uuid
from sqlalchemy.orm import Session

from app.models import QRCode
from app.services.styling_service import resolve_logo_path
from app.utils.qr_generator import generate_qr_image

BASE_URL = os.environ.get("SMARTQR_BASE_URL", "http://127.0.0.1:8000")


def create_qr(
    db: Session,
    name: str,
    original_data: str,
    redirect_url: str | None = None,
    fill_color: str = "black",
    back_color: str = "white",
    logo_path: str | None = None,
    use_redirect: bool = True,
) -> QRCode:
    """
    Create a QR code: generate PNG, save to static/qrcodes/, store in DB.
    use_redirect=True: QR encodes redirect URL (scans tracked). Default for URLs.
    use_redirect=False: QR encodes data directly (WiFi/vCard/Calendar templates).
    Returns the QRCode model instance.
    """
    qr_id = str(uuid.uuid4())
    filename = f"{qr_id}.png"

    if use_redirect:
        data_to_encode = f"{BASE_URL.rstrip('/')}/r/{qr_id}"
    else:
        data_to_encode = original_data

    resolved_logo = resolve_logo_path(logo_path)
    generate_qr_image(
        data=data_to_encode,
        filename=filename,
        fill_color=fill_color,
        back_color=back_color,
        logo_path=str(resolved_logo) if resolved_logo else None,
    )

    # Store record in database
    qr = QRCode(
        id=qr_id,
        name=name,
        original_data=original_data,
        redirect_url=redirect_url or original_data,
        fill_color=fill_color,
        back_color=back_color,
        logo_path=logo_path if resolved_logo else None,
    )
    db.add(qr)
    db.commit()
    db.refresh(qr)

    return qr

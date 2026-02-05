# ===== PHASE 4: Dynamic Redirect System =====
"""
Service for logging QR scan events.
"""

from sqlalchemy.orm import Session

from app.models import ScanEvent


def log_scan(
    db: Session,
    qr_id: str,
    ip_address: str | None = None,
    country: str | None = None,
    device_type: str | None = None,
) -> ScanEvent:
    """Log a scan event for a QR code."""
    event = ScanEvent(
        qr_id=qr_id,
        ip_address=ip_address,
        country=country,
        device_type=device_type,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

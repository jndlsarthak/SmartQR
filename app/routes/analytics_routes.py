# ===== PHASE 5: Scan Analytics Backend =====
"""
Analytics routes: stats per QR code.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QRCode
from app.utils.analytics import get_all_stats

router = APIRouter(tags=["analytics"])


@router.get("/qr/{qr_id}/stats")
def get_qr_stats(
    qr_id: str,
    db: Session = Depends(get_db),
):
    """Return analytics for a QR code: total scans, scans per day, unique vs repeat."""
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    return get_all_stats(db, qr_id)

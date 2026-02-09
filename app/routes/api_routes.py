# ===== PHASE 9: REST API =====
"""
Public REST API for QR generation and analytics.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QRCode
from app.services.qr_service import create_qr
from app.utils.analytics import get_all_stats

router = APIRouter(prefix="/api", tags=["api"])


class CreateQRBody(BaseModel):
    name: str
    data: str
    redirect_url: str | None = None
    fill_color: str | None = "black"
    back_color: str | None = "white"
    logo_path: str | None = None


@router.post("/qr")
def api_create_qr(body: CreateQRBody, db: Session = Depends(get_db)):
    """Create a new QR code. Returns JSON with id, image_url, redirect_url."""
    if not body.data.strip():
        raise HTTPException(status_code=400, detail="data cannot be empty")
    qr = create_qr(
        db=db,
        name=body.name,
        original_data=body.data,
        redirect_url=body.redirect_url,
        fill_color=body.fill_color or "black",
        back_color=body.back_color or "white",
        logo_path=body.logo_path,
    )
    return {
        "id": qr.id,
        "name": qr.name,
        "image_url": f"/static/qrcodes/{qr.id}.png",
        "redirect_url": f"/r/{qr.id}",
    }


@router.get("/qr/{qr_id}")
def api_get_qr(qr_id: str, db: Session = Depends(get_db)):
    """Get QR code details by ID."""
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    return {
        "id": qr.id,
        "name": qr.name,
        "original_data": (qr.original_data[:200] + "...") if len(qr.original_data) > 200 else qr.original_data,
        "redirect_url": qr.redirect_url,
        "fill_color": qr.fill_color,
        "back_color": qr.back_color,
        "logo_path": qr.logo_path,
        "created_at": qr.created_at.isoformat() if qr.created_at else None,
        "image_url": f"/static/qrcodes/{qr.id}.png",
    }


@router.get("/qr/{qr_id}/stats")
def api_get_qr_stats(qr_id: str, db: Session = Depends(get_db)):
    """Get analytics for a QR code."""
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    return get_all_stats(db, qr_id)

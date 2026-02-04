# ===== PHASE 3: Basic QR Generation =====
"""
QR creation routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.services.qr_service import create_qr


router = APIRouter(prefix="/qr", tags=["qr"])


class CreateQRRequest(BaseModel):
    name: str
    data: str
    redirect_url: str | None = None


@router.post("/create")
def create_qr_endpoint(
    request: CreateQRRequest,
    db: Session = Depends(get_db),
):
    """Create a new QR code and save to DB."""
    if not request.data.strip():
        raise HTTPException(status_code=400, detail="Data cannot be empty")
    qr = create_qr(
        db=db,
        name=request.name,
        original_data=request.data,
        redirect_url=request.redirect_url,
    )
    return {
        "id": qr.id,
        "name": qr.name,
        "image_url": f"/static/qrcodes/{qr.id}.png",
    }

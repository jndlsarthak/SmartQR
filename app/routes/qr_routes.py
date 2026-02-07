# ===== PHASE 3: Basic QR Generation =====
# ===== PHASE 6: Styling Engine =====
# ===== PHASE 7: QR Templates =====
"""
QR creation routes.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.qr_service import create_qr
from app.utils.qr_templates import format_calendar_event, format_vcard, format_wifi


router = APIRouter(prefix="/qr", tags=["qr"])


class CreateQRRequest(BaseModel):
    name: str
    data: str
    redirect_url: str | None = None
    fill_color: str | None = "black"
    back_color: str | None = "white"
    logo_path: str | None = None


class CreateTemplateQRRequest(BaseModel):
    name: str
    template_type: str = Field(..., pattern="^(wifi|vcard|calendar)$")
    template_data: dict
    fill_color: str | None = "black"
    back_color: str | None = "white"
    logo_path: str | None = None


def _qr_response(qr):
    return {
        "id": qr.id,
        "name": qr.name,
        "image_url": f"/static/qrcodes/{qr.id}.png",
        "redirect_url": f"/r/{qr.id}" if qr.redirect_url else None,
    }


@router.post("/create")
def create_qr_endpoint(
    request: CreateQRRequest,
    db: Session = Depends(get_db),
):
    """Create a new QR code and save to DB. Supports custom colors and optional logo."""
    if not request.data.strip():
        raise HTTPException(status_code=400, detail="Data cannot be empty")
    qr = create_qr(
        db=db,
        name=request.name,
        original_data=request.data,
        redirect_url=request.redirect_url,
        fill_color=request.fill_color or "black",
        back_color=request.back_color or "white",
        logo_path=request.logo_path,
    )
    return _qr_response(qr)


@router.post("/create/template")
def create_template_qr_endpoint(
    request: CreateTemplateQRRequest,
    db: Session = Depends(get_db),
):
    """Create a QR from a template (WiFi, vCard, or Calendar). Data encoded directly - no redirect."""
    d = request.template_data or {}
    if request.template_type == "wifi":
        ssid = d.get("ssid") or d.get("SSID")
        if not ssid:
            raise HTTPException(status_code=400, detail="template_data must include 'ssid'")
        formatted = format_wifi(
            ssid=str(ssid),
            password=str(d.get("password", "")),
            encryption=str(d.get("encryption", "WPA")),
            hidden=bool(d.get("hidden", False)),
        )
    elif request.template_type == "vcard":
        first_name = d.get("first_name") or d.get("firstname")
        if not first_name:
            raise HTTPException(status_code=400, detail="template_data must include 'first_name'")
        formatted = format_vcard(
            first_name=str(first_name),
            last_name=str(d.get("last_name", d.get("lastname", ""))),
            organization=str(d.get("organization", "")),
            title=str(d.get("title", "")),
            phone=str(d.get("phone", "")),
            email=str(d.get("email", "")),
            website=str(d.get("website", "")),
            address=str(d.get("address", "")),
        )
    elif request.template_type == "calendar":
        summary = d.get("summary") or d.get("title")
        start_raw = d.get("start")
        end_raw = d.get("end")
        if not summary or not start_raw or not end_raw:
            raise HTTPException(
                status_code=400,
                detail="template_data must include 'summary', 'start', and 'end' (ISO datetime strings)",
            )
        try:
            start = start_raw if isinstance(start_raw, datetime) else datetime.fromisoformat(str(start_raw).replace("Z", "+00:00"))
            end = end_raw if isinstance(end_raw, datetime) else datetime.fromisoformat(str(end_raw).replace("Z", "+00:00"))
        except (ValueError, TypeError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid start/end datetime: {e}") from e
        formatted = format_calendar_event(
            summary=str(summary),
            start=start,
            end=end,
            location=str(d.get("location", "")),
            description=str(d.get("description", "")),
        )
    else:
        raise HTTPException(status_code=400, detail="template_type must be wifi, vcard, or calendar")

    qr = create_qr(
        db=db,
        name=request.name,
        original_data=formatted,
        redirect_url=formatted,
        fill_color=request.fill_color or "black",
        back_color=request.back_color or "white",
        logo_path=request.logo_path,
        use_redirect=False,
    )
    return _qr_response(qr)

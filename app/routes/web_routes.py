# ===== PHASE 8: Web Interface =====
"""
Web UI routes: dashboard, create form, stats page.
"""

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QRCode
from app.services.qr_service import create_qr
from app.utils.analytics import get_all_stats
from app.utils.qr_templates import format_calendar_event, format_vcard, format_wifi

router = APIRouter(tags=["web"])
_templates_dir = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_templates_dir))


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), created: str | None = None):
    """List all QR codes."""
    qrcodes = db.query(QRCode).order_by(QRCode.created_at.desc()).all()
    items = [
        {
            "id": qr.id,
            "name": qr.name,
            "image_url": f"/static/qrcodes/{qr.id}.png",
            "scan_count": len(qr.scan_events),
            "created_at": qr.created_at,
        }
        for qr in qrcodes
    ]
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "qrcodes": items, "created": created},
    )


@router.get("/create", response_class=HTMLResponse)
def create_form(request: Request):
    """Show create QR form."""
    return templates.TemplateResponse("create_qr.html", {"request": request})


@router.post("/create")
async def create_submit(request: Request, db: Session = Depends(get_db)):
    """Process create QR form."""
    form = await request.form()
    mode = form.get("mode", "url")

    try:
        if mode == "url":
            name = form.get("name", "").strip()
            data = form.get("data", "").strip()
            if not name or not data:
                return templates.TemplateResponse(
                    "create_qr.html",
                    {"request": request, "error": "Name and URL/data are required"},
                )
            qr = create_qr(db=db, name=name, original_data=data, redirect_url=data)
        elif mode == "wifi":
            name = form.get("wifi_name", "WiFi").strip() or "WiFi"
            ssid = form.get("ssid", "").strip()
            if not ssid:
                return templates.TemplateResponse(
                    "create_qr.html",
                    {"request": request, "error": "SSID is required"},
                )
            formatted = format_wifi(
                ssid=ssid,
                password=form.get("password", ""),
                encryption=form.get("encryption", "WPA"),
            )
            qr = create_qr(db=db, name=name, original_data=formatted, redirect_url=formatted, use_redirect=False)
        elif mode == "vcard":
            name = form.get("vcard_name", "Contact").strip() or "Contact"
            first_name = form.get("first_name", "").strip()
            if not first_name:
                return templates.TemplateResponse(
                    "create_qr.html",
                    {"request": request, "error": "First name is required"},
                )
            formatted = format_vcard(
                first_name=first_name,
                last_name=form.get("last_name", ""),
                phone=form.get("phone", ""),
                email=form.get("email", ""),
            )
            qr = create_qr(db=db, name=name, original_data=formatted, redirect_url=formatted, use_redirect=False)
        elif mode == "calendar":
            name = form.get("calendar_name", "Event").strip() or "Event"
            summary = form.get("summary", "").strip()
            start_s = form.get("start", "").strip()
            end_s = form.get("end", "").strip()
            if not summary or not start_s or not end_s:
                return templates.TemplateResponse(
                    "create_qr.html",
                    {"request": request, "error": "Summary, start, and end are required"},
                )
            try:
                start = datetime.fromisoformat(start_s.replace("Z", "+00:00"))
                end = datetime.fromisoformat(end_s.replace("Z", "+00:00"))
            except ValueError:
                return templates.TemplateResponse(
                    "create_qr.html",
                    {"request": request, "error": "Invalid date format. Use datetime-local."},
                )
            formatted = format_calendar_event(
                summary=summary,
                start=start,
                end=end,
                location=form.get("location", ""),
            )
            qr = create_qr(db=db, name=name, original_data=formatted, redirect_url=formatted, use_redirect=False)
        else:
            return templates.TemplateResponse(
                "create_qr.html",
                {"request": request, "error": "Invalid mode"},
            )
        return RedirectResponse(url=f"/dashboard?created={qr.id}", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            "create_qr.html",
            {"request": request, "error": str(e)},
        )


@router.get("/stats/{qr_id}", response_class=HTMLResponse)
def stats_page(request: Request, qr_id: str, db: Session = Depends(get_db)):
    """Stats page for a QR code."""
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found")
    stats = get_all_stats(db, qr_id)
    context = {
        "request": request,
        "qr": {
            "id": qr.id,
            "name": qr.name,
            "image_url": f"/static/qrcodes/{qr.id}.png",
        },
        "stats": stats,
    }
    return templates.TemplateResponse("stats.html", context)

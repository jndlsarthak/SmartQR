# ===== PHASE 4: Dynamic Redirect System =====
"""
Redirect routes: /r/{qr_id} fetches QR, logs scan, redirects.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QRCode
from app.services.tracking_service import log_scan


router = APIRouter(tags=["redirect"])


def _get_client_ip(request: Request) -> str | None:
    """Extract client IP, respecting X-Forwarded-For when behind a proxy."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


def _infer_device_type(user_agent: str | None) -> str | None:
    """Simple device type inference from User-Agent."""
    if not user_agent:
        return None
    ua = user_agent.lower()
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return "mobile"
    if "tablet" in ua or "ipad" in ua:
        return "tablet"
    return "desktop"


@router.get("/r/{qr_id}")
def redirect_to_url(
    qr_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Fetch QR, log scan event, redirect to stored redirect_url."""
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found")

    # Log scan event
    ip = _get_client_ip(request)
    ua = request.headers.get("User-Agent")
    device = _infer_device_type(ua)
    log_scan(db, qr_id=qr_id, ip_address=ip, device_type=device)

    # Redirect to stored URL (redirect_url or original_data)
    target = qr.redirect_url or qr.original_data
    if not target:
        raise HTTPException(status_code=400, detail="QR has no redirect URL")
    return RedirectResponse(url=target, status_code=302)

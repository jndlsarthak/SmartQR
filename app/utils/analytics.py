# ===== PHASE 5: Scan Analytics Backend =====
"""
Analytics logic: total scans, scans per day, unique vs repeat (by IP).
"""

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import ScanEvent


def get_total_scans(db: Session, qr_id: str) -> int:
    """Count total scan events for a QR code."""
    return db.query(func.count(ScanEvent.id)).filter(ScanEvent.qr_id == qr_id).scalar() or 0


def get_scans_per_day(db: Session, qr_id: str) -> list[dict]:
    """
    Scans grouped by day for a QR code.
    Returns list of {date: "YYYY-MM-DD", count: int}.
    """
    # SQLite: date(timestamp); PostgreSQL: func.date(ScanEvent.timestamp)
    rows = (
        db.query(func.date(ScanEvent.timestamp).label("day"), func.count(ScanEvent.id).label("count"))
        .filter(ScanEvent.qr_id == qr_id)
        .group_by(func.date(ScanEvent.timestamp))
        .order_by(func.date(ScanEvent.timestamp))
        .all()
    )
    return [{"date": str(day), "count": count} for day, count in rows]


def get_unique_vs_repeat(db: Session, qr_id: str) -> dict:
    """
    Unique vs repeat scans by IP.
    Returns {total_scans, unique_visitors (distinct IPs), repeat_scans (total - unique)}.
    """
    total = get_total_scans(db, qr_id)
    unique_visitors = (
        db.query(func.count(func.distinct(ScanEvent.ip_address)))
        .filter(ScanEvent.qr_id == qr_id)
        .scalar()
        or 0
    )
    # Repeat scans = total - unique (each unique IP counted once; rest are "repeat" scan events)
    repeat_scans = max(0, total - unique_visitors)
    return {
        "total_scans": total,
        "unique_visitors": unique_visitors,
        "repeat_scans": repeat_scans,
    }


def get_all_stats(db: Session, qr_id: str) -> dict:
    """Aggregate stats for a QR code: total, per day, unique vs repeat."""
    return {
        "qr_id": qr_id,
        "scans_per_day": get_scans_per_day(db, qr_id),
        **get_unique_vs_repeat(db, qr_id),
    }

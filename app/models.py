# ===== PHASE 2: Database Models =====
"""
SQLAlchemy models for QR codes and scan tracking.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class QRCode(Base):
    __tablename__ = "qrcodes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    original_data = Column(Text, nullable=False)
    redirect_url = Column(Text, nullable=True)
    fill_color = Column(String(50), default="black")
    back_color = Column(String(50), default="white")
    logo_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    scan_events = relationship("ScanEvent", back_populates="qr_code", cascade="all, delete-orphan")


class ScanEvent(Base):
    __tablename__ = "scan_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    qr_id = Column(String(36), ForeignKey("qrcodes.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    country = Column(String(100), nullable=True)
    device_type = Column(String(100), nullable=True)

    qr_code = relationship("QRCode", back_populates="scan_events")

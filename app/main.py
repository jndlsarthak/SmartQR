# ===== PHASE 1: Project Setup =====
# ===== PHASE 2: Database Models =====
"""
SmartQR - Dynamic QR Code Management Platform
FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine

import app.models  # noqa: F401 - register models with Base before create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown logic if needed


app = FastAPI(
    title="SmartQR",
    description="Dynamic QR Code Management Platform",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    """Health check / root endpoint."""
    return {"status": "SmartQR Running"}

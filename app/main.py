# ===== PHASE 1: Project Setup =====
# ===== PHASE 2: Database Models =====
# ===== PHASE 3: Basic QR Generation =====
# ===== PHASE 4: Dynamic Redirect System =====
"""
SmartQR - Dynamic QR Code Management Platform
FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes import qr_routes, redirect_routes

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


app.include_router(qr_routes.router)
app.include_router(redirect_routes.router)

# Serve generated QR images
static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def root():
    """Health check / root endpoint."""
    return {"status": "SmartQR Running"}

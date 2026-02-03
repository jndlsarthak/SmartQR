# ===== PHASE 1: Project Setup =====
"""
SmartQR - Dynamic QR Code Management Platform
FastAPI application entry point.
"""

from fastapi import FastAPI

app = FastAPI(
    title="SmartQR",
    description="Dynamic QR Code Management Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    """Health check / root endpoint."""
    return {"status": "SmartQR Running"}

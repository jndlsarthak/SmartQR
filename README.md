# SmartQR – Dynamic QR Code Management Platform

A full-stack QR Code SaaS-style system.

## Phase 1: Project Setup

### Run the app

```bash
cd smartqr
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000 — you should see `{"status": "SmartQR Running"}`.

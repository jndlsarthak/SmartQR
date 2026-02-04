# SmartQR – Dynamic QR Code Management Platform

A full-stack QR Code SaaS-style system.

## Phase 1: Project Setup

### Run the app

**Option 1 — One command (recommended):**
```bash
cd smartqr
python run.py
```
This installs dependencies if needed, then starts the server.

**Option 2 — Manual:**
```bash
cd smartqr
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**If you get SSL certificate errors when installing:**
```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

**If using Anaconda**, run with Anaconda's Python:
```bash
/opt/anaconda3/bin/python run.py
# or: conda activate base && python run.py
```

Visit http://127.0.0.1:8000 — you should see `{"status": "SmartQR Running"}`.

## Phase 3: Create a QR Code

```bash
curl -X POST http://127.0.0.1:8000/qr/create \
  -H "Content-Type: application/json" \
  -d '{"name": "My QR", "data": "https://example.com"}'
```

The QR image is saved to `static/qrcodes/{id}.png` and viewable at `/static/qrcodes/{id}.png`.

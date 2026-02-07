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

## Phase 4: Dynamic Redirect

Scanning a QR (or visiting `http://127.0.0.1:8000/r/{qr_id}`) logs the scan and redirects to the destination URL.

```bash
# Visit the redirect link (simulates a scan)
curl -L http://127.0.0.1:8000/r/{qr_id}
```

## Phase 5: Scan Analytics

Stats per QR: total scans, scans per day, unique vs repeat (by IP).

```bash
curl http://127.0.0.1:8000/qr/{qr_id}/stats
```
Returns: `total_scans`, `unique_visitors`, `repeat_scans`, `scans_per_day`.

## Phase 6: Custom Styling

Custom colors and optional logo in the center of the QR.

```bash
# Custom colors
curl -X POST http://127.0.0.1:8000/qr/create \
  -H "Content-Type: application/json" \
  -d '{"name": "Branded", "data": "https://example.com", "fill_color": "#1a1a2e", "back_color": "#eaeaea"}'

# With logo (place logo in static/logos/ and pass path)
curl -X POST http://127.0.0.1:8000/qr/create \
  -H "Content-Type: application/json" \
  -d '{"name": "With Logo", "data": "https://example.com", "logo_path": "static/logos/logo.png"}'
```

## Phase 7: QR Templates

WiFi, vCard contact, and Calendar event templates. Data is encoded directly (no redirect).

```bash
# WiFi - scan to connect
curl -X POST http://127.0.0.1:8000/qr/create/template \
  -H "Content-Type: application/json" \
  -d '{"name": "My WiFi", "template_type": "wifi", "template_data": {"ssid": "MyNetwork", "password": "secret123", "encryption": "WPA"}}'

# vCard - scan to add contact
curl -X POST http://127.0.0.1:8000/qr/create/template \
  -H "Content-Type: application/json" \
  -d '{"name": "Contact", "template_type": "vcard", "template_data": {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "phone": "+1234567890"}}'

# Calendar event - scan to add to calendar
curl -X POST http://127.0.0.1:8000/qr/create/template \
  -H "Content-Type: application/json" \
  -d '{"name": "Event", "template_type": "calendar", "template_data": {"summary": "Team Meeting", "start": "2025-02-15T09:00:00", "end": "2025-02-15T10:00:00", "location": "Conference Room A"}}'
```

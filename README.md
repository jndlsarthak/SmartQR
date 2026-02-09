# SmartQR – Dynamic QR Code Management Platform

A full-stack QR Code SaaS-style system. Create, track, and manage dynamic QR codes with analytics, custom styling, and ready-to-use templates.

---

## Features

- **Dynamic QR Generation** — Create QR codes from URLs or custom data; scans are tracked before redirect
- **Scan Analytics** — Total scans, unique visitors, repeat scans, and scans per day
- **Custom Styling** — Fill/background colors and optional logo overlay
- **QR Templates** — WiFi (connect to network), vCard (add contact), Calendar (add event)
- **Web Dashboard** — List QRs, create via form, view stats
- **REST API** — Programmatic access for integrations
- **Phone-Scannable** — Auto-detects LAN IP so QRs work when scanned on the same WiFi

---

## Tech Stack

| Layer       | Technology        |
|------------|-------------------|
| Backend    | Python, FastAPI   |
| Database   | SQLite (PostgreSQL-ready) |
| QR Gen     | qrcode, Pillow    |
| Frontend   | Jinja2, HTML/CSS  |

---

## Quick Start

### 1. Install & run

```bash
cd smartqr
pip install -r requirements.txt
python run.py
```

The server starts at **http://127.0.0.1:8000** and listens on all interfaces (`0.0.0.0`) so phones on the same WiFi can connect. New QRs automatically use your LAN IP for scanning.

### 2. Open the dashboard

Visit **http://127.0.0.1:8000/dashboard** to view QRs and create new ones.

### 3. API docs

Interactive API docs: **http://127.0.0.1:8000/docs**

---

## Project Structure

```
smartqr/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # SQLAlchemy config
│   ├── models.py            # QRCode, ScanEvent
│   ├── schemas.py
│   ├── utils/
│   │   ├── qr_generator.py  # QR image generation
│   │   ├── qr_templates.py  # WiFi, vCard, Calendar
│   │   └── analytics.py     # Scan stats
│   ├── services/
│   │   ├── qr_service.py
│   │   ├── tracking_service.py
│   │   └── styling_service.py
│   ├── routes/
│   │   ├── qr_routes.py     # /qr/create, /qr/create/template
│   │   ├── api_routes.py    # /api/qr, /api/qr/{id}, /api/qr/{id}/stats
│   │   ├── redirect_routes.py  # /r/{id}
│   │   ├── analytics_routes.py # /qr/{id}/stats
│   │   └── web_routes.py    # /dashboard, /create, /stats/{id}
│   └── templates/           # Jinja2 HTML
├── static/
│   ├── qrcodes/             # Generated QR images
│   └── logos/               # Logo assets
├── run.py                   # Launcher (auto LAN IP, 0.0.0.0)
├── requirements.txt
└── README.md
```

---

## API Reference

### Web UI

| URL                | Description                    |
|--------------------|--------------------------------|
| `/dashboard`       | List all QR codes              |
| `/create`          | Create QR form (URL, WiFi, vCard, Calendar) |
| `/stats/{qr_id}`   | Stats page for a QR            |
| `/docs`            | Swagger UI                     |

### Redirect

| Method | Endpoint   | Description                                  |
|--------|------------|----------------------------------------------|
| GET    | `/r/{qr_id}` | Redirect (logs scan, redirects to destination) |

### Create QR (URL / custom data)

| Method | Endpoint       | Description                     |
|--------|----------------|---------------------------------|
| POST   | `/qr/create`   | Create QR from URL or custom data |
| POST   | `/api/qr`      | Same, under API prefix          |

**Body (JSON):**
```json
{
  "name": "My QR",
  "data": "https://example.com",
  "redirect_url": "https://example.com",
  "fill_color": "black",
  "back_color": "white",
  "logo_path": "static/logos/logo.png"
}
```

### Create QR (Templates)

| Method | Endpoint              | Description        |
|--------|------------------------|--------------------|
| POST   | `/qr/create/template`  | Create WiFi, vCard, or Calendar QR |

**Body (JSON):**
```json
{
  "name": "My WiFi",
  "template_type": "wifi",
  "template_data": {
    "ssid": "NetworkName",
    "password": "secret",
    "encryption": "WPA",
    "hidden": false
  }
}
```

Template types:
- **wifi** — `ssid` (required), `password`, `encryption` (WPA/WEP/nopass), `hidden`
- **vcard** — `first_name` (required), `last_name`, `organization`, `title`, `phone`, `email`, `website`, `address`
- **calendar** — `summary` (required), `start` (required), `end` (required), `location`, `description`

### Get QR details

| Method | Endpoint        | Description      |
|--------|-----------------|------------------|
| GET    | `/api/qr/{id}`  | QR details (name, data, colors, created_at) |

### Analytics

| Method | Endpoint              | Description                          |
|--------|------------------------|--------------------------------------|
| GET    | `/qr/{id}/stats`       | Stats (total, unique, repeat, per day) |
| GET    | `/api/qr/{id}/stats`   | Same, under API prefix               |

**Response:**
```json
{
  "qr_id": "...",
  "total_scans": 42,
  "unique_visitors": 18,
  "repeat_scans": 24,
  "scans_per_day": [
    { "date": "2025-02-02", "count": 10 },
    { "date": "2025-02-03", "count": 32 }
  ]
}
```

---

## Environment Variables

| Variable          | Default              | Description                          |
|-------------------|----------------------|--------------------------------------|
| `SMARTQR_BASE_URL`| `http://127.0.0.1:8000` | Base URL for redirect links in QRs |

If unset, `run.py` auto-sets this to your LAN IP so new QRs are scannable on the same WiFi.

---

## Phone Scanning

For QRs to work when scanned on a phone:

1. Phone and computer must be on the same WiFi
2. Use `python run.py` — it binds to `0.0.0.0` and sets `SMARTQR_BASE_URL` to your LAN IP
3. Create **new** QRs after starting the app (existing QRs keep their old URLs)

> **Note:** "Can't reach server" when scanning is a common local dev issue—usually WiFi/firewall related. The project runs fine; deployment to a server with a public URL works normally.

If you run with `uvicorn` manually, set the base URL:
```bash
export SMARTQR_BASE_URL=http://192.168.1.100:8000
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Troubleshooting

**SSL certificate errors when installing**
```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

**"Can't connect to server" when scanning**
- This is a common local dev issue (WiFi/firewall)—the project is fine; deploy to a server and it works.
- Use `python run.py` (binds to `0.0.0.0`, sets LAN IP)
- Ensure phone and computer are on the same WiFi
- Create new QRs after starting the app

**405 Method Not Allowed**
- `/qr/create` and `/api/qr` require **POST**, not GET. Use curl or the Swagger UI at `/docs`.

---

## License

MIT

# ===== PHASE 7: QR Templates =====
"""
QR code data formatters for WiFi, vCard, and Calendar event templates.
Formats data according to standard specs so phones parse correctly when scanned.
"""

from datetime import datetime


def _escape_wifi(value: str) -> str:
    """Escape special chars for WiFi format: ; : \" \\"""
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(":", "\\:").replace('"', '\\"')


def format_wifi(
    ssid: str,
    password: str = "",
    encryption: str = "WPA",
    hidden: bool = False,
) -> str:
    """
    Format WiFi config for QR code.
    Standard: WIFI:T:WPA;S:SSID;P:password;H:false;;
    Encryption: WPA, WPA2, WEP, or nopass (for open networks).
    """
    ssid = _escape_wifi(ssid.strip())
    password = _escape_wifi(password) if password else ""
    enc = encryption.strip().upper() if encryption else "WPA"
    if enc == "NOPASS" or enc == "OPEN":
        enc = "nopass"
    elif enc not in ("WEP", "WPA2", "WPA3"):
        enc = "WPA"

    parts = [f"WIFI:T:{enc};S:{ssid};"]
    if password and enc != "nopass":
        parts.append(f"P:{password};")
    if hidden:
        parts.append("H:true;")
    parts.append(";")
    return "".join(parts)


def format_vcard(
    first_name: str,
    last_name: str = "",
    organization: str = "",
    title: str = "",
    phone: str = "",
    email: str = "",
    website: str = "",
    address: str = "",
) -> str:
    """
    Format vCard 3.0 for QR code.
    When scanned, phones offer to add contact.
    """
    full_name = f"{first_name.strip()} {last_name.strip()}".strip() or first_name
    n_value = f"{last_name};{first_name};;;"

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{full_name}",
        f"N:{n_value}",
    ]
    if organization:
        lines.append(f"ORG:{organization.strip()}")
    if title:
        lines.append(f"TITLE:{title.strip()}")
    if phone:
        lines.append(f"TEL:{phone.strip()}")
    if email:
        lines.append(f"EMAIL:{email.strip()}")
    if website:
        url = website.strip()
        if not url.startswith("http"):
            url = f"https://{url}"
        lines.append(f"URL:{url}")
    if address:
        lines.append(f"ADR;TYPE=HOME:;;{address.strip()};;;;")
    lines.append("END:VCARD")
    return "\r\n".join(lines)


def _format_ical_datetime(dt: datetime) -> str:
    """Format datetime for iCal: YYYYMMDDTHHMMSSZ"""
    return dt.strftime("%Y%m%dT%H%M%SZ")


def format_calendar_event(
    summary: str,
    start: datetime,
    end: datetime,
    location: str = "",
    description: str = "",
) -> str:
    """
    Format iCal VEVENT for QR code.
    When scanned, phones offer to add to calendar.
    """
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "BEGIN:VEVENT",
        f"SUMMARY:{summary.strip()}",
        f"DTSTART:{_format_ical_datetime(start)}",
        f"DTEND:{_format_ical_datetime(end)}",
    ]
    if location:
        lines.append(f"LOCATION:{location.strip()}")
    if description:
        # Escape newlines in description
        desc = description.strip().replace("\r\n", "\\n").replace("\n", "\\n")
        lines.append(f"DESCRIPTION:{desc}")
    lines.extend(["END:VEVENT", "END:VCALENDAR"])
    return "\r\n".join(lines)

# ===== PHASE 6: Styling Engine =====
"""
Styling service: validates and resolves colors and logo paths for QR generation.
"""

from pathlib import Path


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def resolve_logo_path(logo_path: str | None) -> Path | None:
    """
    Resolve logo path relative to project root.
    Returns absolute Path if file exists, else None.
    """
    if not logo_path or not logo_path.strip():
        return None
    path = Path(logo_path.strip())
    if not path.is_absolute():
        path = _get_project_root() / path
    return path if path.exists() else None


def validate_color(color: str | None) -> str:
    """Return a valid color string; default to black/white if invalid."""
    if not color or not color.strip():
        return "black"
    return color.strip()

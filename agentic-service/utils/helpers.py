"""
Agentic Service — Helper Utilities
====================================
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    """Return current UTC datetime as ISO string."""
    return utc_now().isoformat()


def safe_truncate(text: str, max_len: int = 500) -> str:
    """Truncate text safely for logging."""
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

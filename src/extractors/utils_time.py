from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from dateutil import parser as dtparser

def to_iso(ts: Optional[str]) -> Optional[str]:
    if not ts:
        return None
    try:
        dt = dtparser.parse(str(ts))
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return None

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
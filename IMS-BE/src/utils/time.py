from __future__ import annotations
import datetime as dt

def utcnow() -> dt.datetime:
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

def parse_date(s: str | None):
    if not s:
        return None
    return dt.date.fromisoformat(s)

def parse_datetime(s: str | None):
    if not s:
        return None
    return dt.datetime.fromisoformat(s)

from __future__ import annotations
from typing import Optional, Any
import json
from passlib.hash import bcrypt
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, verify_jwt_in_request, get_jwt_identity
)
from infrastructure.databases import db, jwt
from domain.models.identity import User

def set_password(u: User, pw: str) -> None:
    u.password_hash = bcrypt.hash(pw)

def check_password(u: User, pw: str) -> bool:
    try:
        return bcrypt.verify(pw, u.password_hash)
    except Exception:
        return False

def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)

def _json_loads(txt: str | None) -> Any:
    if not txt:
        return None
    try:
        return json.loads(txt)
    except Exception:
        return None

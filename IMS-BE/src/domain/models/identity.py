from __future__ import annotations
from typing import Any, Dict, List
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum
from infrastructure.databases import db
from utils.time import utcnow
from security.rbac import Roles
import json

def _json_dumps(obj: Any) -> str:
    import json as _j
    return _j.dumps(obj, ensure_ascii=False)

def _json_loads(txt: str | None) -> Any:
    if not txt:
        return None
    try:
        return json.loads(txt)
    except Exception:
        return None

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(SAEnum(Roles), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120))
    location = db.Column(db.String(120))
    headline = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    intern_profile = relationship("InternProfile", backref="user", uselist=False)

    def set_password(self, pw: str) -> None:
        from security.auth import set_password as _sp
        _sp(self, pw)

    def check_password(self, pw: str) -> bool:
        from security.auth import check_password as _cp
        return _cp(self, pw)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "email": self.email, "role": self.role.value,
            "name": self.name, "department": self.department, "location": self.location,
            "headline": self.headline, "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat(),
        }

class InternProfile(db.Model):
    __tablename__ = "intern_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    skills_json = db.Column(db.Text)  # JSON array
    school = db.Column(db.String(255))
    major = db.Column(db.String(255))
    gpa = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="Active")  # Active|Paused|Completed

    def set_skills(self, arr: List[str]) -> None:
        self.skills_json = _json_dumps(arr or [])

    def get_skills(self) -> List[str]:
        return _json_loads(self.skills_json) or []

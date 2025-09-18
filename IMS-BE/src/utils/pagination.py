from __future__ import annotations
from typing import Any, Dict, List, Tuple
from flask import request
from infrastructure.databases import db
from domain.models.identity import User
from domain.models.recruitment import RecruitmentCampaign, Application
from domain.models.identity import InternProfile
from domain.models.training import TrainingProgram, Project
from domain.models.assignment import Assignment
from domain.models.evaluation import Evaluation
from domain.models.schedule import ScheduleItem
from domain.models.kpi import KPIRecord
from domain.models.messaging import Notification, ChatThread, ChatMessage

def qstr(key: str, default: str | None = None) -> str | None:
    v = request.args.get(key, default)
    return v if v != "" else default

def qint(key: str, default: int) -> int:
    try:
        return int(request.args.get(key, default))
    except Exception:
        return default

def paginated_query(query, page: int, limit: int) -> Tuple[list, int]:
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all() if limit > 0 else query.all()
    return items, total

def paginated(items: List[Any], page: int, limit: int, total: int) -> Dict[str, Any]:
    def _to(obj):
        if hasattr(obj, "to_public_dict"):
            return obj.to_public_dict()
        if isinstance(obj, User):
            return obj.to_public_dict()
        if isinstance(obj, RecruitmentCampaign):
            return {"id": obj.id, "title": obj.title, "status": obj.status.value,
                    "description": obj.description, "created_by": obj.created_by,
                    "created_at": obj.created_at.isoformat()}
        if isinstance(obj, Application):
            return {"id": obj.id, "camp_id": obj.camp_id, "user_id": obj.user_id,
                    "status": obj.status.value, "note": obj.note,
                    "created_at": obj.created_at.isoformat()}
        if isinstance(obj, InternProfile):
            return {"id": obj.id, "user_id": obj.user_id, "skills": obj.get_skills(),
                    "school": obj.school, "major": obj.major, "gpa": obj.gpa,
                    "start_date": obj.start_date.isoformat() if obj.start_date else None,
                    "end_date": obj.end_date.isoformat() if obj.end_date else None,
                    "status": obj.status}
        if isinstance(obj, TrainingProgram):
            return {"id": obj.id, "title": obj.title, "goal": obj.goal, "created_by": obj.created_by}
        if isinstance(obj, Project):
            return {"id": obj.id, "prog_id": obj.prog_id, "title": obj.title,
                    "description": obj.description, "owner_id": obj.owner_id}
        if isinstance(obj, Assignment):
            return {"id": obj.id, "proj_id": obj.proj_id, "intern_id": obj.intern_id,
                    "status": obj.status.value,
                    "due_date": obj.due_date.isoformat() if obj.due_date else None}
        if isinstance(obj, Evaluation):
            return {"id": obj.id, "intern_id": obj.intern_id, "evaluator_id": obj.evaluator_id,
                    "score": obj.score, "comment": obj.comment,
                    "created_at": obj.created_at.isoformat()}
        if isinstance(obj, ScheduleItem):
            return {"id": obj.id, "intern_id": obj.intern_id, "title": obj.title, "type": obj.type.value,
                    "start_time": obj.start_time.isoformat(), "end_time": obj.end_time.isoformat(),
                    "location": obj.location}
        if isinstance(obj, KPIRecord):
            return {"id": obj.id, "intern_id": obj.intern_id, "kpi_key": obj.kpi_key,
                    "value": obj.value, "period": obj.period, "note": obj.note}
        if isinstance(obj, Notification):
            return {"id": obj.id, "user_id": obj.user_id, "type": obj.type,
                    "payload": obj.get_payload(), "is_read": obj.is_read,
                    "created_at": obj.created_at.isoformat()}
        if isinstance(obj, ChatThread):
            return {"id": obj.id, "user_a_id": obj.user_a_id,
                    "user_b_id": obj.user_b_id, "created_at": obj.created_at.isoformat()}
        if isinstance(obj, ChatMessage):
            return {"id": obj.id, "thread_id": obj.thread_id, "sender_id": obj.sender_id,
                    "content": obj.content, "created_at": obj.created_at.isoformat()}
        return obj
    return {"items": [_to(i) for i in items], "page": page, "limit": limit, "total": total}

from __future__ import annotations
from flask import Blueprint, request, jsonify, g
from sqlalchemy import and_, or_
from infrastructure.databases import db
from utils.responses import ok, created, no_content
from utils.pagination import qstr, qint, paginated_query, paginated
from utils.time import utcnow, parse_date, parse_datetime
from security.rbac import (
    Roles, roles_required, require_login, current_user,
    BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, ConflictError, UnprocessableError
)
from domain.models.identity import User, InternProfile
from domain.models.recruitment import RecruitmentCampaign, CampaignStatus, Application, ApplicationStatus
from domain.models.training import TrainingProgram, Project
from domain.models.assignment import Assignment, AssignmentStatus
from domain.models.evaluation import Evaluation
from domain.models.schedule import ScheduleItem, ScheduleType
from domain.models.kpi import KPIRecord
from domain.models.messaging import Notification, ChatThread, ChatMessage

bp = Blueprint("chat", __name__)

@bp.post("/threads/start")
@require_login
def start_thread():
    u = current_user()
    data = request.get_json(force=True, silent=True) or {}
    other_id = data.get("user_id")
    if not other_id:
        raise BadRequestError("user_id is required")
    if int(other_id) == u.id:
        raise BadRequestError("Cannot start thread with yourself")
    existing = db.session.query(ChatThread).filter(
        or_(
            and_(ChatThread.user_a_id == u.id, ChatThread.user_b_id == int(other_id)),
            and_(ChatThread.user_a_id == int(other_id), ChatThread.user_b_id == u.id),
        )
    ).first()
    if existing:
        return ok({"thread": {"id": existing.id, "user_a_id": existing.user_a_id, "user_b_id": existing.user_b_id}})
    t = ChatThread(user_a_id=u.id, user_b_id=int(other_id))
    db.session.add(t); db.session.commit()
    return created({"thread": {"id": t.id, "user_a_id": t.user_a_id, "user_b_id": t.user_b_id}})

@bp.get("/threads")
@require_login
def list_threads():
    u = current_user()
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(ChatThread).filter(
        or_(ChatThread.user_a_id == u.id, ChatThread.user_b_id == u.id)
    ).order_by(ChatThread.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.get("/threads/<int:tid>/messages")
@require_login
def list_messages(tid: int):
    u = current_user()
    t = db.session.get(ChatThread, tid)
    if not t or (t.user_a_id != u.id and t.user_b_id != u.id):
        raise NotFoundError("Thread not found")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 20))
    q = db.session.query(ChatMessage).filter_by(thread_id=tid).order_by(ChatMessage.id.asc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.post("/threads/<int:tid>/messages")
@require_login
def post_message(tid: int):
    u = current_user()
    t = db.session.get(ChatThread, tid)
    if not t or (t.user_a_id != u.id and t.user_b_id != u.id):
        raise NotFoundError("Thread not found")
    data = request.get_json(force=True, silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        raise BadRequestError("content is required")
    m = ChatMessage(thread_id=tid, sender_id=u.id, content=content)
    db.session.add(m); db.session.commit()
    return created({"message": {"id": m.id}})

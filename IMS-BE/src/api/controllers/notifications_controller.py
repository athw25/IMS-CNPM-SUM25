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

bp = Blueprint("notifications", __name__)

@bp.get("/notifications")
@require_login
def list_notifications():
    u = current_user()
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(Notification).filter_by(user_id=u.id).order_by(Notification.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.post("/notifications")
@roles_required(Roles.Admin)
def create_notification():
    data = request.get_json(force=True, silent=True) or {}
    user_id = data.get("user_id"); type_ = (data.get("type") or "").strip()
    if not (user_id and type_):
        raise BadRequestError("user_id and type are required")
    if not db.session.get(User, int(user_id)):
        raise BadRequestError("Invalid user_id")
    n = Notification(user_id=int(user_id), type=type_, is_read=False)
    n.set_payload(data.get("payload"))
    db.session.add(n); db.session.commit()
    return created({"notification": {"id": n.id}})

@bp.patch("/notifications/<int:nid>/read")
@require_login
def mark_notification_read(nid: int):
    u = current_user()
    n = db.session.get(Notification, nid)
    if not n or n.user_id != u.id:
        raise NotFoundError("Notification not found")
    n.is_read = True
    db.session.commit()
    return ok({"updated": True})

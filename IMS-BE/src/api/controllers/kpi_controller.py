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

bp = Blueprint("kpi", __name__)

@bp.post("/kpi")
@roles_required(Roles.HR, Roles.Coordinator)
def create_kpi():
    data = request.get_json(force=True, silent=True) or {}
    intern_id = data.get("intern_id"); kpi_key = (data.get("kpi_key") or "").strip()
    value = data.get("value"); period = (data.get("period") or "").strip()
    if not (intern_id and kpi_key and value is not None and period):
        raise BadRequestError("intern_id, kpi_key, value, period are required")
    intern = db.session.get(InternProfile, int(intern_id))
    if not intern:
        raise BadRequestError("Invalid intern_id")
    try:
        value = float(value)
    except Exception:
        raise BadRequestError("value must be a number")
    k = KPIRecord(intern_id=intern.id, kpi_key=kpi_key, value=value, period=period, note=data.get("note"))
    db.session.add(k); db.session.commit()
    return created({"kpi": {"id": k.id}})

@bp.get("/kpi")
def list_kpi():
    intern_id = qstr("intern_id"); period = qstr("period"); key = qstr("key")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(KPIRecord)
    if intern_id:
        q = q.filter(KPIRecord.intern_id == int(intern_id))
    if period:
        q = q.filter(KPIRecord.period == period)
    if key:
        q = q.filter(KPIRecord.kpi_key == key)
    q = q.order_by(KPIRecord.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

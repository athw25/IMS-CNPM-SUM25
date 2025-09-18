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

bp = Blueprint("schedule", __name__)

@bp.post("/schedule")
@roles_required(Roles.HR, Roles.Coordinator)
def create_schedule_item():
    data = request.get_json(force=True, silent=True) or {}
    intern_id = data.get("intern_id"); title = (data.get("title") or "").strip()
    type_ = data.get("type"); start_time = parse_datetime(data.get("start_time")); end_time = parse_datetime(data.get("end_time"))
    if not (intern_id and title and type_ and start_time and end_time):
        raise BadRequestError("intern_id, title, type, start_time, end_time are required")
    if type_ not in ScheduleType._value2member_map_:
        raise BadRequestError("Invalid type")
    intern = db.session.get(InternProfile, int(intern_id))
    if not intern:
        raise BadRequestError("Invalid intern_id")
    si = ScheduleItem(intern_id=intern.id, title=title, type=ScheduleType(type_), start_time=start_time, end_time=end_time, location=data.get("location"))
    db.session.add(si); db.session.commit()
    return created({"schedule_item": {"id": si.id}})

@bp.get("/schedule")
def list_schedule():
    intern_id = qstr("intern_id")
    from_ = parse_datetime(qstr("from")); to_ = parse_datetime(qstr("to"))
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(ScheduleItem)
    if intern_id:
        q = q.filter(ScheduleItem.intern_id == int(intern_id))
    if from_:
        q = q.filter(ScheduleItem.start_time >= from_)
    if to_:
        q = q.filter(ScheduleItem.end_time <= to_)
    q = q.order_by(ScheduleItem.start_time.asc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.patch("/schedule/<int:sid>")
@roles_required(Roles.HR, Roles.Coordinator)
def patch_schedule_item(sid: int):
    si = db.session.get(ScheduleItem, sid)
    if not si:
        raise NotFoundError("Schedule item not found")
    data = request.get_json(force=True, silent=True) or {}
    for k in ["title", "location"]:
        if k in data:
            setattr(si, k, data[k])
    if "type" in data:
        if data["type"] not in ScheduleType._value2member_map_:
            raise BadRequestError("Invalid type")
        si.type = ScheduleType(data["type"])
    if "start_time" in data:
        si.start_time = parse_datetime(data["start_time"])
    if "end_time" in data:
        si.end_time = parse_datetime(data["end_time"])
    db.session.commit()
    return ok({"updated": True})

@bp.delete("/schedule/<int:sid>")
@roles_required(Roles.HR, Roles.Coordinator)
def delete_schedule_item(sid: int):
    si = db.session.get(ScheduleItem, sid)
    if not si:
        raise NotFoundError("Schedule item not found")
    db.session.delete(si); db.session.commit()
    return no_content()

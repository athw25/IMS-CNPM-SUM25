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

bp = Blueprint("applications", __name__)

@bp.post("/applications")
@roles_required(Roles.Intern)
def create_application():
    data = request.get_json(force=True, silent=True) or {}
    camp_id = data.get("camp_id")
    if not camp_id:
        raise BadRequestError("camp_id is required")
    rc = db.session.get(RecruitmentCampaign, int(camp_id))
    if not rc or rc.status != CampaignStatus.Open:
        raise BadRequestError("Campaign must exist and be Open")
    u = current_user()
    if db.session.query(Application.id).filter_by(camp_id=rc.id, user_id=u.id).first():
        raise ConflictError("You have already applied to this campaign")
    app_obj = Application(camp_id=rc.id, user_id=u.id, status=ApplicationStatus.Pending, note=data.get("note"))
    db.session.add(app_obj); db.session.commit()
    return created({"application": {"id": app_obj.id}})

@bp.get("/applications")
@roles_required(Roles.HR)
def list_applications():
    camp_id = qstr("camp_id"); status = qstr("status")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(Application)
    if camp_id:
        q = q.filter(Application.camp_id == int(camp_id))
    if status and status in ApplicationStatus._value2member_map_:
        q = q.filter(Application.status == ApplicationStatus(status))
    q = q.order_by(Application.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.patch("/applications/<int:aid>")
@roles_required(Roles.HR)
def patch_application(aid: int):
    app_obj = db.session.get(Application, aid)
    if not app_obj:
        raise NotFoundError("Application not found")
    data = request.get_json(force=True, silent=True) or {}
    if "status" in data and data["status"] in ApplicationStatus._value2member_map_:
        new = ApplicationStatus(data["status"])
        if app_obj.status != ApplicationStatus.Pending:
            raise UnprocessableError("Only Pending applications can be decided")
        if new not in (ApplicationStatus.Approved, ApplicationStatus.Rejected):
            raise UnprocessableError("Invalid status transition")
        app_obj.status = new
    if "note" in data:
        app_obj.note = data["note"]
    db.session.commit()
    return ok({"updated": True})

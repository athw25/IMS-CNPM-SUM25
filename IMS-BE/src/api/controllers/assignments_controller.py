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

bp = Blueprint("assignments", __name__)

@bp.post("/assignments")
@roles_required(Roles.Coordinator, Roles.Mentor)
def create_assignment():
    data = request.get_json(force=True, silent=True) or {}
    proj_id = data.get("proj_id"); intern_id = data.get("intern_id")
    if not proj_id or not intern_id:
        raise BadRequestError("proj_id and intern_id are required")
    proj = db.session.get(Project, int(proj_id))
    intern = db.session.get(InternProfile, int(intern_id))
    if not proj or not intern:
        raise BadRequestError("Invalid proj_id or intern_id")
    a = Assignment(proj_id=proj.id, intern_id=intern.id, status=AssignmentStatus.Pending,
                   due_date=parse_date(data.get("due_date")))
    db.session.add(a); db.session.commit()
    return created({"assignment": {"id": a.id}})

@bp.get("/assignments")
def list_assignments():
    proj_id = qstr("proj_id"); intern_id = qstr("intern_id"); status = qstr("status")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(Assignment)
    if proj_id:
        q = q.filter(Assignment.proj_id == int(proj_id))
    if intern_id:
        q = q.filter(Assignment.intern_id == int(intern_id))
    if status and status in AssignmentStatus._value2member_map_:
        q = q.filter(Assignment.status == AssignmentStatus(status))
    q = q.order_by(Assignment.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.patch("/assignments/<int:aid>/status")
@roles_required(Roles.Coordinator, Roles.Mentor)
def update_assignment_status(aid: int):
    a = db.session.get(Assignment, aid)
    if not a:
        raise NotFoundError("Assignment not found")
    data = request.get_json(force=True, silent=True) or {}
    new = data.get("status")
    if new not in AssignmentStatus._value2member_map_:
        raise BadRequestError("Invalid status")
    new_status = AssignmentStatus(new)
    if a.status == AssignmentStatus.Pending and new_status == AssignmentStatus.Doing:
        a.status = AssignmentStatus.Doing
    elif a.status == AssignmentStatus.Doing and new_status == AssignmentStatus.Done:
        a.status = AssignmentStatus.Done
    elif a.status == new_status:
        pass
    else:
        raise UnprocessableError("Invalid state transition")
    db.session.commit()
    return ok({"updated": True, "status": a.status.value})

@bp.delete("/assignments/<int:aid>")
@roles_required(Roles.Coordinator, Roles.Mentor)
def delete_assignment(aid: int):
    a = db.session.get(Assignment, aid)
    if not a:
        raise NotFoundError("Assignment not found")
    if a.status == AssignmentStatus.Done:
        raise ConflictError("Cannot delete a Done assignment")
    db.session.delete(a); db.session.commit()
    return no_content()

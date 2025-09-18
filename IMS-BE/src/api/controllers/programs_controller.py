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

bp = Blueprint("programs", __name__)

@bp.post("/training-programs")
@roles_required(Roles.HR, Roles.Coordinator)
def create_program():
    data = request.get_json(force=True, silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        raise BadRequestError("title is required")
    prog = TrainingProgram(title=title, goal=data.get("goal"), created_by=current_user().id)
    db.session.add(prog); db.session.commit()
    return created({"program": {"id": prog.id}})

@bp.get("/training-programs")
def list_programs():
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(TrainingProgram).order_by(TrainingProgram.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.delete("/training-programs/<int:pid>")
@roles_required(Roles.HR, Roles.Coordinator)
def delete_program(pid: int):
    prog = db.session.get(TrainingProgram, pid)
    if not prog:
        raise NotFoundError("Program not found")
    has_projects = db.session.query(Project.id).filter_by(prog_id=pid).first()
    if has_projects:
        raise ConflictError("Cannot delete program with projects")
    db.session.delete(prog); db.session.commit()
    return no_content()

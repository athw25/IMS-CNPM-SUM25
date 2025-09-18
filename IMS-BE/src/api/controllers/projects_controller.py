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

bp = Blueprint("projects", __name__)

@bp.post("/projects")
@roles_required(Roles.Coordinator, Roles.Mentor)
def create_project():
    data = request.get_json(force=True, silent=True) or {}
    prog_id = data.get("prog_id")
    title = (data.get("title") or "").strip()
    owner_id = data.get("owner_id") or current_user().id
    if not prog_id or not title:
        raise BadRequestError("prog_id and title are required")
    prog = db.session.get(TrainingProgram, int(prog_id))
    if not prog:
        raise BadRequestError("Program not found")
    owner = db.session.get(User, int(owner_id))
    if not owner or owner.role not in (Roles.Mentor, Roles.Coordinator):
        raise BadRequestError("owner must be Mentor or Coordinator")
    proj = Project(prog_id=prog.id, title=title, description=data.get("description"), owner_id=owner.id)
    db.session.add(proj); db.session.commit()
    return created({"project": {"id": proj.id}})

@bp.get("/projects")
def list_projects():
    prog_id = qstr("prog_id")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(Project)
    if prog_id:
        q = q.filter(Project.prog_id == int(prog_id))
    q = q.order_by(Project.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.delete("/projects/<int:proj_id>")
@roles_required(Roles.Coordinator, Roles.Mentor)
def delete_project(proj_id: int):
    proj = db.session.get(Project, proj_id)
    if not proj:
        raise NotFoundError("Project not found")
    has_assignments = db.session.query(Assignment.id).filter_by(proj_id=proj_id).first()
    if has_assignments:
        raise ConflictError("Cannot delete project with assignments")
    db.session.delete(proj); db.session.commit()
    return no_content()

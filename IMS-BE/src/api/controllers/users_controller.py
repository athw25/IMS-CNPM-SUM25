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

bp = Blueprint("users", __name__)

@bp.get("/users")
@roles_required(Roles.Admin, Roles.HR)
def list_users():
    role = qstr("role")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(User)
    if role and role in Roles._value2member_map_:
        q = q.filter(User.role == Roles(role))
    q = q.order_by(User.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.post("/users")
@roles_required(Roles.Admin, Roles.HR)
def create_user():
    creator = current_user()
    data = request.get_json(force=True, silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()
    role = data.get("role") or Roles.Intern.value
    if not email or not password or not name:
        raise BadRequestError("email, password, name are required")
    target_role = Roles(role) if role in Roles._value2member_map_ else Roles.Intern
    if creator.role == Roles.HR and target_role == Roles.Admin:
        raise ForbiddenError("HR cannot create Admin users")
    if db.session.query(User.id).filter_by(email=email).first():
        raise ConflictError("Email already registered")
    u = User(email=email, name=name, role=target_role); u.set_password(password)
    db.session.add(u); db.session.commit()
    if target_role == Roles.Intern and not u.intern_profile:
        ip = InternProfile(user_id=u.id, status="Active"); ip.skills_json = "[]"
        db.session.add(ip); db.session.commit()
    return created({"user": u.to_public_dict()})

@bp.get("/users/<int:user_id>")
def get_user_public(user_id: int):
    u = db.session.get(User, user_id)
    if not u:
        raise NotFoundError("User not found")
    return ok({"user": u.to_public_dict()})

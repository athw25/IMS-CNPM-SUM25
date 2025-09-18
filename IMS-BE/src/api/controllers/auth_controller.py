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

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, verify_jwt_in_request

bp = Blueprint("auth", __name__)

ALLOW_SELF_REGISTER_INTERN = True

@bp.post("/auth/register")
def register():
    data = request.get_json(force=True, silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()
    role = data.get("role") or Roles.Intern.value
    if not email or not password or not name:
        raise BadRequestError("email, password, name are required")
    target_role = Roles(role) if role in Roles._value2member_map_ else Roles.Intern

    caller = None
    try:
        verify_jwt_in_request(optional=True)
        caller = current_user()
    except Exception:
        caller = None

    if caller is None:
        if not ALLOW_SELF_REGISTER_INTERN or target_role != Roles.Intern:
            raise ForbiddenError("Only Intern self-registration is allowed")
    else:
        if caller.role == Roles.HR:
            if target_role == Roles.Admin:
                raise ForbiddenError("HR cannot create Admin users")
        elif caller.role == Roles.Admin:
            pass
        else:
            raise ForbiddenError("Only Admin/HR can create users")

    if db.session.query(User.id).filter_by(email=email).first():
        raise ConflictError("Email already registered")
    u = User(email=email, role=target_role, name=name); u.set_password(password)
    db.session.add(u); db.session.commit()
    if target_role == Roles.Intern and not u.intern_profile:
        ip = InternProfile(user_id=u.id, status="Active")
        ip.skills_json = "[]"
        db.session.add(ip); db.session.commit()
    return created({"user": u.to_public_dict()})

@bp.post("/auth/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    u = db.session.query(User).filter_by(email=email).first()
    if not u or not u.check_password(password):
        raise UnauthorizedError("Invalid credentials")
    access = create_access_token(identity=str(u.id))
    refresh = create_refresh_token(identity=str(u.id))
    return ok({"access_token": access, "refresh_token": refresh, "user": u.to_public_dict()})

@bp.post("/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    u = current_user()
    if not u:
        raise UnauthorizedError("Invalid user")
    access = create_access_token(identity=str(u.id))
    return ok({"access_token": access})

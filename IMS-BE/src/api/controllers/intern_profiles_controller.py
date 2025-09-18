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
import json

bp = Blueprint("intern_profiles", __name__)

@bp.get("/intern-profiles")
@roles_required(Roles.HR, Roles.Coordinator)
def list_intern_profiles():
    user_id = qstr("user_id"); status = qstr("status")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(InternProfile)
    if user_id:
        q = q.filter(InternProfile.user_id == int(user_id))
    if status:
        q = q.filter(InternProfile.status == status)
    q = q.order_by(InternProfile.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.post("/intern-profiles")
@roles_required(Roles.HR, Roles.Coordinator)
def create_intern_profile():
    data = request.get_json(force=True, silent=True) or {}
    user_id = data.get("user_id")
    if not user_id:
        raise BadRequestError("user_id is required")
    u = db.session.get(User, int(user_id))
    if not u or u.role != Roles.Intern:
        raise BadRequestError("user_id must reference an Intern")
    if db.session.query(InternProfile.id).filter_by(user_id=u.id).first():
        raise ConflictError("Intern profile already exists")
    ip = InternProfile(
        user_id=u.id, school=data.get("school"), major=data.get("major"),
        gpa=data.get("gpa"), start_date=parse_date(data.get("start_date")),
        end_date=parse_date(data.get("end_date")), status=data.get("status") or "Active",
    )
    if "skills" in data:
        ip.skills_json = json.dumps(data.get("skills") or [], ensure_ascii=False)
    db.session.add(ip); db.session.commit()
    return created({"intern_profile": {"id": ip.id, "user_id": ip.user_id}})

@bp.get("/intern-profiles/<int:ip_id>")
@roles_required(Roles.HR, Roles.Coordinator)
def get_intern_profile(ip_id: int):
    ip = db.session.get(InternProfile, ip_id)
    if not ip:
        raise NotFoundError("Intern profile not found")
    return ok({
        "intern_profile": {
            "id": ip.id, "user_id": ip.user_id,
            "skills": (json.loads(ip.skills_json) if ip.skills_json else []),
            "school": ip.school, "major": ip.major, "gpa": ip.gpa,
            "start_date": ip.start_date.isoformat() if ip.start_date else None,
            "end_date": ip.end_date.isoformat() if ip.end_date else None,
            "status": ip.status,
        }
    })

@bp.patch("/intern-profiles/<int:ip_id>")
@roles_required(Roles.HR, Roles.Coordinator)
def patch_intern_profile(ip_id: int):
    ip = db.session.get(InternProfile, ip_id)
    if not ip:
        raise NotFoundError("Intern profile not found")
    data = request.get_json(force=True, silent=True) or {}
    if "skills" in data:
        ip.skills_json = json.dumps(data.get("skills") or [], ensure_ascii=False)
    for key in ["school", "major", "gpa", "status"]:
        if key in data:
            setattr(ip, key, data[key])
    if "start_date" in data:
        ip.start_date = parse_date(data.get("start_date"))
    if "end_date" in data:
        ip.end_date = parse_date(data.get("end_date"))
    db.session.commit()
    return ok({"updated": True})

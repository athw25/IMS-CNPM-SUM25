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

bp = Blueprint("evaluations", __name__)

@bp.post("/evaluations")
@roles_required(Roles.Mentor, Roles.Coordinator, Roles.HR)
def create_evaluation():
    data = request.get_json(force=True, silent=True) or {}
    intern_id = data.get("intern_id"); score = data.get("score")
    if intern_id is None or score is None:
        raise BadRequestError("intern_id and score are required")
    intern = db.session.get(InternProfile, int(intern_id))
    if not intern:
        raise BadRequestError("Invalid intern_id")
    try:
        score = int(score)
    except Exception:
        raise BadRequestError("score must be integer")
    if not (0 <= score <= 100):
        raise BadRequestError("score must be in [0100]")
    ev = Evaluation(intern_id=intern.id, evaluator_id=current_user().id, score=score, comment=data.get("comment"))
    db.session.add(ev); db.session.commit()
    return created({"evaluation": {"id": ev.id}})

@bp.get("/evaluations")
def list_evaluations():
    intern_id = qstr("intern_id"); page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(Evaluation)
    if intern_id:
        q = q.filter(Evaluation.intern_id == int(intern_id))
    q = q.order_by(Evaluation.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.get("/interns/<int:intern_id>/avg-score")
def get_avg_score(intern_id: int):
    evals = db.session.query(Evaluation).filter_by(intern_id=intern_id).all()
    if not evals:
        return ok({"intern_id": intern_id, "avg_score": None})
    avg = sum(e.score for e in evals) / len(evals)
    return ok({"intern_id": intern_id, "avg_score": round(avg, 2)})

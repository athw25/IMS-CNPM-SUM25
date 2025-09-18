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

bp = Blueprint("me", __name__)

@bp.get("/me")
@require_login
def get_me():
    u = current_user()
    return ok({"user": u.to_public_dict()})

@bp.patch("/me")
@require_login
def patch_me():
    u = current_user()
    data = request.get_json(force=True, silent=True) or {}
    for key in ["name", "department", "location", "headline", "avatar_url"]:
        if key in data:
            setattr(u, key, data[key])
    db.session.commit()
    return ok({"user": u.to_public_dict()})

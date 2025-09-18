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

bp = Blueprint("campaigns", __name__)

@bp.post("/campaigns")
@roles_required(Roles.HR)
def create_campaign():
    data = request.get_json(force=True, silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        raise BadRequestError("title is required")
    rc = RecruitmentCampaign(
        title=title,
        status=CampaignStatus(data.get("status")) if data.get("status") in CampaignStatus._value2member_map_ else CampaignStatus.Open,
        description=data.get("description"),
        created_by=current_user().id,
    )
    db.session.add(rc); db.session.commit()
    return created({"campaign": {"id": rc.id}})

@bp.get("/campaigns")
def list_campaigns():
    status = qstr("status")
    page = max(1, qint("page", 1)); limit = max(1, qint("limit", 10))
    q = db.session.query(RecruitmentCampaign)
    if status and status in CampaignStatus._value2member_map_:
        q = q.filter(RecruitmentCampaign.status == CampaignStatus(status))
    q = q.order_by(RecruitmentCampaign.id.desc())
    items, total = paginated_query(q, page, limit)
    return ok(paginated(items, page, limit, total))

@bp.patch("/campaigns/<int:cid>")
@roles_required(Roles.HR)
def patch_campaign(cid: int):
    rc = db.session.get(RecruitmentCampaign, cid)
    if not rc:
        raise NotFoundError("Campaign not found")
    data = request.get_json(force=True, silent=True) or {}
    if "title" in data and data["title"]:
        rc.title = data["title"]
    if "status" in data and data["status"] in CampaignStatus._value2member_map_:
        rc.status = CampaignStatus(data["status"])
    if "description" in data:
        rc.description = data["description"]
    db.session.commit()
    return ok({"updated": True})

@bp.delete("/campaigns/<int:cid>")
@roles_required(Roles.HR)
def delete_campaign(cid: int):
    rc = db.session.get(RecruitmentCampaign, cid)
    if not rc:
        raise NotFoundError("Campaign not found")
    has_app = db.session.query(Application.id).filter_by(camp_id=cid).first()
    if has_app:
        raise ConflictError("Cannot delete campaign with applications")
    db.session.delete(rc); db.session.commit()
    return no_content()

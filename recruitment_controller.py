from flask import Blueprint, request, jsonify
from pydantic import ValidationError as PydValidationError
from api.schemas.recruitment_schema import (
    CreateCampaignDTO, UpdateCampaignDTO, CampaignResponseDTO
)
from services.recruitment_service import RecruitmentService
from infrastructure.repositories.recruitment_repository import CampaignRepository, ApplicationRepository

# responses helpers (tuỳ dự án bạn có)
try:
    from api.responses import success_response, error_response
except Exception:
    def success_response(data, code=200): return (jsonify(data), code)
    def error_response(msg, code=400):   return ({"error": msg}, code)

bp = Blueprint("recruitment_bp", __name__, url_prefix="/api")

_service = RecruitmentService(CampaignRepository(), ApplicationRepository())

@bp.route("/recruitments", methods=["GET"])
def list_campaigns():
    status = request.args.get("status")
    items = _service.list_campaigns(status)
    data = [CampaignResponseDTO(campID=i.campID, title=i.title, status=i.status).dict() for i in items]
    return success_response(data, 200)

@bp.route("/recruitments", methods=["POST"])
def create_campaign():
    try:
        dto = CreateCampaignDTO(**(request.get_json() or {}))
        c = _service.create_campaign(dto.title, dto.status)
        return success_response(CampaignResponseDTO(campID=c.campID, title=c.title, status=c.status).dict(), 201)
    except PydValidationError as e:
        return error_response(e.errors(), 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route("/recruitments/<int:camp_id>", methods=["PUT"])
def update_campaign(camp_id: int):
    try:
        dto = UpdateCampaignDTO(**(request.get_json() or {}))
        c = _service.update_campaign(camp_id, dto.title, dto.status)
        return success_response(CampaignResponseDTO(campID=c.campID, title=c.title, status=c.status).dict(), 200)
    except PydValidationError as e:
        return error_response(e.errors(), 400)
    except Exception as e:
        code = 404 if "not found" in str(e).lower() else 400
        return error_response(str(e), code)

@bp.route("/recruitments/<int:camp_id>", methods=["DELETE"])
def delete_campaign(camp_id: int):
    try:
        _service.delete_campaign(camp_id)
        return success_response({"message": "deleted"}, 200)
    except Exception as e:
        code = 409 if "existing applications" in str(e).lower() else 404 if "not found" in str(e).lower() else 400
        return error_response(str(e), code)

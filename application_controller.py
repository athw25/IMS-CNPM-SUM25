from flask import Blueprint, request, jsonify
from pydantic import ValidationError as PydValidationError
from api.schemas.recruitment_schema import (
    CreateApplicationDTO, UpdateApplicationDTO, ApplicationResponseDTO
)
from services.recruitment_service import RecruitmentService
from infrastructure.repositories.recruitment_repository import CampaignRepository, ApplicationRepository

try:
    from api.responses import success_response, error_response
except Exception:
    def success_response(data, code=200): return (jsonify(data), code)
    def error_response(msg, code=400):   return ({"error": msg}, code)

bp = Blueprint("application_bp", __name__, url_prefix="/api")
_service = RecruitmentService(CampaignRepository(), ApplicationRepository())

@bp.route("/applications", methods=["GET"])
def list_applications():
    camp_id = request.args.get("campID", type=int)
    user_id = request.args.get("userID", type=int)
    items = _service.list_applications(camp_id, user_id)
    data = [ApplicationResponseDTO(appID=i.appID, campID=i.campID, userID=i.userID, status=i.status).dict() for i in items]
    return success_response(data, 200)

@bp.route("/applications", methods=["POST"])
def create_application():
    try:
        dto = CreateApplicationDTO(**(request.get_json() or {}))
        a = _service.create_application(dto.campID, dto.userID, dto.status)
        return success_response(ApplicationResponseDTO(appID=a.appID, campID=a.campID, userID=a.userID, status=a.status).dict(), 201)
    except PydValidationError as e:
        return error_response(e.errors(), 400)
    except Exception as e:
        code = 404 if "campaign not found" in str(e).lower() else 409 if "closed" in str(e).lower() else 400
        return error_response(str(e), code)

@bp.route("/applications/<int:app_id>", methods=["PUT"])
def update_application(app_id: int):
    try:
        dto = UpdateApplicationDTO(**(request.get_json() or {}))
        a = _service.update_application(app_id, dto.status)
        return success_response(ApplicationResponseDTO(appID=a.appID, campID=a.campID, userID=a.userID, status=a.status).dict(), 200)
    except PydValidationError as e:
        return error_response(e.errors(), 400)
    except Exception as e:
        code = 404 if "not found" in str(e).lower() else 400
        return error_response(str(e), code)

@bp.route("/applications/<int:app_id>", methods=["DELETE"])
def delete_application(app_id: int):
    try:
        _service.delete_application(app_id)
        return success_response({"message": "deleted"}, 200)
    except Exception as e:
        code = 404 if "not found" in str(e).lower() else 400
        return error_response(str(e), code)

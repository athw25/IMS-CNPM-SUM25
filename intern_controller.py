#intern_controller.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError as MsValidationError

from src.api.schemas.identity_schema import (
    CreateInternSchema, UpdateInternSchema, InternResponseSchema
)
from src.services.identity_service import IdentityService
from src.infrastructure.repositories.identity_repository import UserRepository, InternRepository

# Exceptions
try:
    from src.domain.exceptions import ValidationError, NotFoundError, ConflictError
except Exception:
    class ValidationError(Exception): ...
    class NotFoundError(Exception): ...
    class ConflictError(Exception): ...

interns_bp = Blueprint("interns_bp", __name__)
_service = IdentityService(UserRepository(), InternRepository())

@interns_bp.get("")
def list_interns():
    items = _service.list_interns()
    schema = InternResponseSchema()
    return jsonify([schema.dump({"internID": i.internID, "userID": i.userID, "skill": i.skill}) for i in items]), 200

@interns_bp.post("")
def create_intern():
    try:
        dto = CreateInternSchema().load(request.get_json() or {})
        i = _service.create_intern(dto.userID, dto.skill)
        return InternResponseSchema().dump({"internID": i.internID, "userID": i.userID, "skill": i.skill}), 201
    except MsValidationError as e:
        return {"error": e.messages}, 400
    except ValidationError as e:
        return {"error": str(e)}, 400
    except ConflictError as e:
        return {"error": str(e)}, 409
    except NotFoundError as e:
        return {"error": str(e)}, 404

@interns_bp.put("/<int:intern_id>")
def update_intern(intern_id: int):
    try:
        dto = UpdateInternSchema().load(request.get_json() or {})
        i = _service.update_intern(intern_id, dto.skill)
        return InternResponseSchema().dump({"internID": i.internID, "userID": i.userID, "skill": i.skill}), 200
    except MsValidationError as e:
        return {"error": e.messages}, 400
    except NotFoundError as e:
        return {"error": str(e)}, 404

@interns_bp.delete("/<int:intern_id>")
def delete_intern(intern_id: int):
    try:
        _service.delete_intern(intern_id)
        return {"message": "deleted"}, 200
    except NotFoundError as e:
        return {"error": str(e)}, 404

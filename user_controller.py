#user_controller.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError as MsValidationError

from src.api.schemas.identity_schema import (
    CreateUserSchema, UpdateUserSchema, UserResponseSchema
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

users_bp = Blueprint("users_bp", __name__)
_service = IdentityService(UserRepository(), InternRepository())

@users_bp.get("")
def list_users():
    role = request.args.get("role")
    items = _service.list_users(role)
    schema = UserResponseSchema()
    return jsonify([schema.dump({"userID": u.userID, "name": u.name, "email": u.email, "role": u.role}) for u in items]), 200

@users_bp.post("")
def create_user():
    try:
        dto = CreateUserSchema().load(request.get_json() or {})
        u = _service.create_user(dto.name, dto.email, dto.role)
        return UserResponseSchema().dump({"userID": u.userID, "name": u.name, "email": u.email, "role": u.role}), 201
    except MsValidationError as e:
        return {"error": e.messages}, 400
    except ValidationError as e:
        return {"error": str(e)}, 400
    except ConflictError as e:
        return {"error": str(e)}, 409

@users_bp.put("/<int:user_id>")
def update_user(user_id: int):
    try:
        dto = UpdateUserSchema().load(request.get_json() or {})
        u = _service.update_user(user_id, dto.name, dto.email, dto.role)
        return UserResponseSchema().dump({"userID": u.userID, "name": u.name, "email": u.email, "role": u.role}), 200
    except MsValidationError as e:
        return {"error": e.messages}, 400
    except ValidationError as e:
        return {"error": str(e)}, 400
    except ConflictError as e:
        return {"error": str(e)}, 409
    except NotFoundError as e:
        return {"error": str(e)}, 404

@users_bp.delete("/<int:user_id>")
def delete_user(user_id: int):
    try:
        _service.delete_user(user_id)
        return {"message": "deleted"}, 200
    except ConflictError as e:
        return {"error": str(e)}, 409
    except NotFoundError as e:
        return {"error": str(e)}, 404

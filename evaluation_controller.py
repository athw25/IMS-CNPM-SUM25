from flask import Blueprint, request, jsonify
from marshmallow import ValidationError as MsValidationError

from src.api.schemas.evaluation_schema import (
    CreateEvaluationSchema, UpdateEvaluationSchema,
    EvaluationResponseSchema, AvgResponseSchema
)
from src.services.evaluation_service import EvaluationService
from src.infrastructure.repositories.evaluation_repository import EvaluationRepository
from src.infrastructure.repositories.identity_repository import InternRepository
from src.domain.exceptions import DomainError, ValidationError, NotFoundError

evaluations_bp = Blueprint("evaluations_bp", __name__)
_service = EvaluationService(EvaluationRepository(), InternRepository())

@evaluations_bp.get("")
def list_by_intern():
    try:
        intern_id = request.args.get("internID", type=int)
        if not intern_id:
            return {"error": "internID is required"}, 400
        items = _service.list_by_intern(intern_id)
        schema = EvaluationResponseSchema()
        data = [schema.dump({"evalID": i.evalID, "internID": i.internID, "score": i.score}) for i in items]
        return jsonify(data), 200
    except NotFoundError as e:
        return {"error": str(e)}, 404
    except DomainError as e:
        return {"error": str(e)}, 400

@evaluations_bp.post("")
def create():
    try:
        dto = CreateEvaluationSchema().load(request.get_json() or {})
        e = _service.create(dto.internID, dto.score)
        return EvaluationResponseSchema().dump({"evalID": e.evalID, "internID": e.internID, "score": e.score}), 201
    except MsValidationError as e:
        return {"error": e.messages}, 400
    except ValidationError as e:
        msg = str(e)
        code = 422 if "in [0..100]" in msg or "number" in msg else 400
        return {"error": msg}, code
    except NotFoundError as e:
        return {"error": str(e)}, 404

@evaluations_bp.put("/<int:eval_id>")
def update(eval_id: int):
    try:
        dto = UpdateEvaluationSchema().load(request.get_json() or {})
        e = _service.update(eval_id, dto.score)
        return EvaluationResponseSchema().dump({"evalID": e.evalID, "internID": e.internID, "score": e.score}), 200
    except MsValidationError as e:
        return {"error": e.messages}, 400
    except ValidationError as e:
        msg = str(e)
        code = 422 if "in [0..100]" in msg or "number" in msg else 400
        return {"error": msg}, code
    except NotFoundError as e:
        return {"error": str(e)}, 404

@evaluations_bp.delete("/<int:eval_id>")
def delete(eval_id: int):
    try:
        _service.delete(eval_id)
        return {"message": "deleted"}, 200
    except NotFoundError as e:
        return {"error": str(e)}, 404

@evaluations_bp.get("/avg")
def avg():
    try:
        intern_id = request.args.get("internID", type=int)
        if not intern_id:
            return {"error": "internID is required"}, 400
        avg_score = _service.avg_by_intern(intern_id)
        return AvgResponseSchema().dump({"internID": intern_id, "avgScore": avg_score}), 200
    except NotFoundError as e:
        return {"error": str(e)}, 404

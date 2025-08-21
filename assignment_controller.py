from flask import Blueprint, request, jsonify
from src.enums import AssignmentStatus
from src.api.schemas.assignment_schema import CreateAssignmentSchema, AssignmentResponseSchema, UpdateAssignmentStatusSchema
from src.api.responses import success, error
from src.domain.exceptions import ValidationError, NotFoundError, ConflictError

def create_assignment_blueprint(work_service):
    bp = Blueprint("assignments", __name__, url_prefix="/api/assignments")

    @bp.get("")
    def list_assignments():
        proj_id = request.args.get("projID", type=int)
        intern_id = request.args.get("internID", type=int)
        status_str = request.args.get("status")
        status = AssignmentStatus(status_str) if status_str else None

        records = work_service.list_assignments(proj_id, intern_id, status)
        data = AssignmentResponseSchema(many=True).dump([r.__dict__ for r in records])
        return jsonify(success(data=data))

    @bp.post("")
    def create_assignment():
        payload = request.get_json(force=True)
        errors = CreateAssignmentSchema().validate(payload or {})
        if errors:
            return jsonify(error("VALIDATION_ERROR", errors)), 400
        try:
            dto = payload
            resp = work_service.create_assignment(
                CreateAssignmentSchema().load(dto)
            )
            data = AssignmentResponseSchema().dump(resp.__dict__)
            return jsonify(success(data=data)), 201
        except (ValidationError, NotFoundError) as e:
            return jsonify(error("BAD_REQUEST", str(e))), 400

    @bp.patch("/<int:assignment_id>/status")
    def update_status(assignment_id: int):
        payload = request.get_json(force=True)
        errors = UpdateAssignmentStatusSchema().validate(payload or {})
        if errors:
            return jsonify(error("VALIDATION_ERROR", errors)), 400
        try:
            status = AssignmentStatus(payload["status"])
            resp = work_service.update_status(assignment_id, type("DTO", (), {"status": status}))
            data = AssignmentResponseSchema().dump(resp.__dict__)
            return jsonify(success(data=data)))
        except NotFoundError as e:
            return jsonify(error("NOT_FOUND", str(e))), 404
        except ConflictError as e:
            return jsonify(error("CONFLICT", str(e))), 409

    @bp.delete("/<int:assignment_id>")
    def delete_assignment(assignment_id: int):
        try:
            work_service.delete_assignment(assignment_id)
            return jsonify(success(message="Deleted")), 200
        except NotFoundError as e:
            return jsonify(error("NOT_FOUND", str(e))), 404
        except ConflictError as e:
            return jsonify(error("CONFLICT", str(e))), 409

    return bp

from flask import Blueprint, request
from api.schemas.training_schema import (
    CreateProgramSchema, ProgramResponseSchema,
    CreateProjectSchema, ProjectResponseSchema
)
from api.responses import success_response, error_response
from dependency_container import training_service
from marshmallow import ValidationError as MarshmallowValidationError

training_bp = Blueprint("training", __name__, url_prefix="/api")

# Program APIs
@training_bp.route("/programs", methods=["GET"])
def list_programs():
    programs = training_service.get_programs()
    return success_response(ProgramResponseSchema(many=True).dump(programs))

@training_bp.route("/programs", methods=["POST"])
def create_program():
    try:
        data = CreateProgramSchema().load(request.json)
        result = training_service.create_program(data)
        return success_response(ProgramResponseSchema().dump(result))
    except MarshmallowValidationError as e:
        return error_response(str(e))

@training_bp.route("/programs/<int:program_id>", methods=["PUT"])
def update_program(program_id):
    try:
        data = CreateProgramSchema().load(request.json)
        result = training_service.update_program(program_id, data)
        return success_response(ProgramResponseSchema().dump(result))
    except MarshmallowValidationError as e:
        return error_response(str(e))

@training_bp.route("/programs/<int:program_id>", methods=["DELETE"])
def delete_program(program_id):
    try:
        training_service.delete_program(program_id)
        return success_response({"message": "Program deleted"})
    except Exception as e:
        return error_response(str(e))


# Project APIs
@training_bp.route("/projects", methods=["GET"])
def list_projects():
    program_id = request.args.get("progID", type=int)
    projects = training_service.get_projects_by_program(program_id)
    return success_response(ProjectResponseSchema(many=True).dump(projects))

@training_bp.route("/projects", methods=["POST"])
def create_project():
    try:
        data = CreateProjectSchema().load(request.json)
        result = training_service.create_project(data)
        return success_response(ProjectResponseSchema().dump(result))
    except MarshmallowValidationError as e:
        return error_response(str(e))

@training_bp.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    try:
        data = CreateProjectSchema().load(request.json)
        result = training_service.update_project(project_id, data)
        return success_response(ProjectResponseSchema().dump(result))
    except MarshmallowValidationError as e:
        return error_response(str(e))

@training_bp.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    try:
        training_service.delete_project(project_id)
        return success_response({"message": "Project deleted"})
    except Exception as e:
        return error_response(str(e))

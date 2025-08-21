#training_controller.py
from flask import Blueprint, request, jsonify
from dependency_container import training_service
from api.schemas.training_schema import training_schema, trainings_schema

training_bp = Blueprint("training", __name__)

@training_bp.route("/", methods=["GET"])
def get_all_trainings():
    programs = training_service.get_all_trainings()
    return jsonify(trainings_schema.dump(programs))

@training_bp.route("/<int:program_id>", methods=["GET"])
def get_training(program_id):
    program = training_service.get_training(program_id)
    return jsonify(training_schema.dump(program))

@training_bp.route("/", methods=["POST"])
def create_training():
    data = request.get_json()
    program = training_service.create_training(data)
    return jsonify(training_schema.dump(program)), 201

@training_bp.route("/<int:program_id>", methods=["PUT"])
def update_training(program_id):
    data = request.get_json()
    program = training_service.update_training(program_id, data)
    return jsonify(training_schema.dump(program))

@training_bp.route("/<int:program_id>", methods=["DELETE"])
def delete_training(program_id):
    training_service.delete_training(program_id)
    return jsonify({"message": "Deleted successfully"})

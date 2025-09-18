from __future__ import annotations
from flask import Flask, jsonify, g
from flask_cors import CORS
from config import AppConfig
from infrastructure.databases import db, jwt
from utils.time import utcnow
from security.rbac import APIError
from api.controllers import (
    auth_controller, me_controller, users_controller, intern_profiles_controller,
    campaigns_controller, applications_controller, programs_controller, projects_controller,
    assignments_controller, evaluations_controller, schedule_controller, kpi_controller,
    notifications_controller, chat_controller, admin_controller, root_controller
)

def create_app() -> Flask:
    cfg = AppConfig.load()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = cfg.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = cfg.JWT_SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = cfg.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["JSON_SORT_KEYS"] = cfg.JSON_SORT_KEYS

    db.init_app(app)
    jwt.init_app(app)

    # CORS
    origins = cfg.CORS_ORIGINS
    if origins == "*":
        CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    else:
        allowed = [o.strip() for o in origins.split(",") if o.strip()]
        CORS(app, resources={r"/*": {"origins": allowed}}, supports_credentials=True)

    # Error handlers
    @app.errorhandler(APIError)
    def _api_error(e: APIError):
        return jsonify({"error": {"code": e.code, "message": e.message}}), e.code

    @app.errorhandler(404)
    def _404(_):
        return jsonify({"error": {"code": 404, "message": "Not Found"}}), 404

    @app.errorhandler(405)
    def _405(_):
        return jsonify({"error": {"code": 405, "message": "Method Not Allowed"}}), 405

    @app.errorhandler(Exception)
    def _500(e: Exception):
        return jsonify({"error": {"code": 500, "message": str(e)}}), 500

    @app.before_request
    def _attach_now():
        g.now = utcnow()

    # Register blueprints (no url_prefix to keep paths identical)
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(me_controller.bp)
    app.register_blueprint(users_controller.bp)
    app.register_blueprint(intern_profiles_controller.bp)
    app.register_blueprint(campaigns_controller.bp)
    app.register_blueprint(applications_controller.bp)
    app.register_blueprint(programs_controller.bp)
    app.register_blueprint(projects_controller.bp)
    app.register_blueprint(assignments_controller.bp)
    app.register_blueprint(evaluations_controller.bp)
    app.register_blueprint(schedule_controller.bp)
    app.register_blueprint(kpi_controller.bp)
    app.register_blueprint(notifications_controller.bp)
    app.register_blueprint(chat_controller.bp)
    app.register_blueprint(admin_controller.bp)
    app.register_blueprint(root_controller.bp)


    return app

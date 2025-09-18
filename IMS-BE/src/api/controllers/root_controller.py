from __future__ import annotations
from flask import Blueprint
from utils.responses import ok
from utils.time import utcnow

bp = Blueprint("root", __name__)

@bp.get("/")
def index():
    return ok({
        "name": "IMS API",
        "status": "ok",
        "time": utcnow().isoformat()
    })

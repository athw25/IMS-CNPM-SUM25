# src/security/rbac.py
from __future__ import annotations
import enum
from functools import wraps
from typing import Optional
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from infrastructure.databases import db

class Roles(str, enum.Enum):
    Admin = "Admin"
    HR = "HR"
    Coordinator = "Coordinator"
    Mentor = "Mentor"
    Intern = "Intern"

def current_user():
    """Lazy-import User to avoid circular import with domain.models.identity"""
    ident = get_jwt_identity()
    if not ident:
        return None
    # lazy import here
    from domain.models.identity import User
    return db.session.get(User, int(ident))

class APIError(Exception):
    code = 500
    message = "Internal Server Error"
    def __init__(self, message: str | None = None, code: int | None = None):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.code = code or self.code

class BadRequestError(APIError):
    code = 400; message = "Bad Request"

class UnauthorizedError(APIError):
    code = 401; message = "Unauthorized"

class ForbiddenError(APIError):
    code = 403; message = "Forbidden"

class NotFoundError(APIError):
    code = 404; message = "Not Found"

class ConflictError(APIError):
    code = 409; message = "Conflict"

class UnprocessableError(APIError):
    code = 422; message = "Unprocessable Entity"

def roles_required(*allowed_roles: Roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                raise UnauthorizedError("Missing or invalid token")
            user = current_user()
            if user is None:
                raise UnauthorizedError("User not found")
            if allowed_roles and user.role.value not in {r.value if isinstance(r, enum.Enum) else r for r in allowed_roles}:
                raise ForbiddenError("Insufficient role")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def require_login(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            raise UnauthorizedError("Missing or invalid token")
        return fn(*args, **kwargs)
    return wrapper

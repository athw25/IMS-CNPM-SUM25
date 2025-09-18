from __future__ import annotations
from typing import Any, Tuple
from flask import jsonify

def ok(data: Any) -> Tuple[Any, int]:
    return jsonify(data), 200

def created(data: Any) -> Tuple[Any, int]:
    return jsonify(data), 201

def no_content() -> Tuple[Any, int]:
    return "", 204

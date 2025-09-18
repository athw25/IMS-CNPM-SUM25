from __future__ import annotations
from infrastructure.databases import db
from utils.time import utcnow
import json

def _json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False)

def _json_loads(txt):
    if not txt:
        return None
    try:
        return json.loads(txt)
    except Exception:
        return None

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    payload_json = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def set_payload(self, obj):
        self.payload_json = _json_dumps(obj)

    def get_payload(self):
        return _json_loads(self.payload_json)

class ChatThread(db.Model):
    __tablename__ = "chat_threads"
    id = db.Column(db.Integer, primary_key=True)
    user_a_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_b_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey("chat_threads.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

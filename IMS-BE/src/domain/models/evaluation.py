from __future__ import annotations
from infrastructure.databases import db
from utils.time import utcnow

class Evaluation(db.Model):
    __tablename__ = "evaluations"
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey("intern_profiles.id"), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 0100
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

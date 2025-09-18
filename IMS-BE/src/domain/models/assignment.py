from __future__ import annotations
import enum
from infrastructure.databases import db

class AssignmentStatus(str, enum.Enum):
    Pending = "Pending"
    Doing = "Doing"
    Done = "Done"

class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    intern_id = db.Column(db.Integer, db.ForeignKey("intern_profiles.id"), nullable=False)
    status = db.Column(db.Enum(AssignmentStatus), default=AssignmentStatus.Pending, nullable=False)
    due_date = db.Column(db.Date)

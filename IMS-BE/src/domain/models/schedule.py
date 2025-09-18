from __future__ import annotations
import enum
from infrastructure.databases import db

class ScheduleType(str, enum.Enum):
    Interview = "Interview"
    Onboarding = "Onboarding"
    Training = "Training"
    Work = "Work"

class ScheduleItem(db.Model):
    __tablename__ = "schedule_items"
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey("intern_profiles.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(ScheduleType), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))

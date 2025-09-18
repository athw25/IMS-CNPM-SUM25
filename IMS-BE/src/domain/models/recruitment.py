from __future__ import annotations
import enum
from infrastructure.databases import db
from utils.time import utcnow
from sqlalchemy import UniqueConstraint

class CampaignStatus(str, enum.Enum):
    Open = "Open"
    Closed = "Closed"

class RecruitmentCampaign(db.Model):
    __tablename__ = "recruitment_campaigns"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(CampaignStatus), default=CampaignStatus.Open, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

class ApplicationStatus(str, enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer, db.ForeignKey("recruitment_campaigns.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.Pending, nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    __table_args__ = (UniqueConstraint("camp_id", "user_id", name="uq_app_camp_user"),)

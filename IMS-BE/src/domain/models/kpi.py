from __future__ import annotations
from infrastructure.databases import db

class KPIRecord(db.Model):
    __tablename__ = "kpi_records"
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey("intern_profiles.id"), nullable=False)
    kpi_key = db.Column(db.String(120), nullable=False)
    value = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(20), nullable=False)  # week|month|quarter
    note = db.Column(db.String(255))

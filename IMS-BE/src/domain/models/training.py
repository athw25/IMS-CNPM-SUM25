from __future__ import annotations
from infrastructure.databases import db

class TrainingProgram(db.Model):
    __tablename__ = "training_programs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    goal = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    prog_id = db.Column(db.Integer, db.ForeignKey("training_programs.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

# training_models.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.databases.db_base import Base

class TrainingProgram(Base):
    __tablename__ = "training_programs"

    progID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    goal: Mapped[str | None] = mapped_column(String(255))

    # Quan hệ 1-n với Project
    projects: Mapped[list["Project"]] = relationship(back_populates="program")

class Project(Base):
    __tablename__ = "projects"

    projID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    progID: Mapped[int] = mapped_column(ForeignKey("training_programs.progID"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Quan hệ n-1 với TrainingProgram
    program: Mapped["TrainingProgram"] = relationship(back_populates="projects")
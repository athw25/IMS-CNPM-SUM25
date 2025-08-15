# work_models.py
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SAEnum
from src.infrastructure.databases.db_base import Base
from enums import AssignmentStatus

class Assignment(Base):
    __tablename__ = "assignments"

    assignID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    projID:   Mapped[int] = mapped_column(ForeignKey("projects.projID"), nullable=False)
    internID: Mapped[int] = mapped_column(ForeignKey("intern_profiles.internID"), nullable=False)
    status:   Mapped[AssignmentStatus] = mapped_column(SAEnum(AssignmentStatus, native_enum=False, length=10, validate_strings=True), nullable=False, default=AssignmentStatus.Pending)

    project = relationship("Project", back_populates="assignments")
    intern  = relationship("InternProfile", viewonly=True, lazy="raise")

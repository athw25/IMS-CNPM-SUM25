# work_models.py
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SAEnum
from db_base import Base
from enums import AssignmentStatus

class Assignment(Base):
    __tablename__ = "assignments"

    assignID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    projID: Mapped[int] = mapped_column(
        ForeignKey("projects.projID", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )

    internID: Mapped[int] = mapped_column(
        ForeignKey("intern_profiles.internID", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )

    status: Mapped[AssignmentStatus] = mapped_column(
        SAEnum(AssignmentStatus, native_enum=False, length=10, validate_strings=True),
        nullable=False,
        default=AssignmentStatus.Pending
    )

    # Quan hệ 1 chiều để giảm phụ thuộc
    project = relationship("Project", viewonly=True, lazy="raise")
    intern = relationship("InternProfile", viewonly=True, lazy="raise")

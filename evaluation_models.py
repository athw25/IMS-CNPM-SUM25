# evaluation_models.py
from __future__ import annotations

from sqlalchemy import Integer, Float, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.databases.db_base import Base


class Evaluation(Base):

    __tablename__ = "evaluations"

    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 100", name="ck_evaluations_score_0_100"),
        Index("idx_evaluations_internID", "internID"),
    )

    evalID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    internID: Mapped[int] = mapped_column(
        ForeignKey("intern_profiles.internID"),
        nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Evaluation(evalID={self.evalID}, internID={self.internID}, score={self.score})"

from typing import Optional, List
from sqlalchemy import select, func
from src.infrastructure.databases.db_base import SessionLocal
from src.infrastructure.models.evaluation_models import Evaluation  # đường dẫn đúng file bạn đang có

from dataclasses import dataclass

# Domain tối giản cho Evaluation
@dataclass
class EvaluationDomain:
    evalID: int | None
    internID: int
    score: float

class EvaluationRepository:
    def get_by_id(self, eval_id: int) -> Optional[EvaluationDomain]:
        with SessionLocal() as s:
            obj = s.get(Evaluation, eval_id)
            return self._to_domain(obj) if obj else None

    def list_by_intern(self, intern_id: int) -> List[EvaluationDomain]:
        with SessionLocal() as s:
            stmt = select(Evaluation).where(Evaluation.internID == intern_id)
            return [self._to_domain(x) for x in s.execute(stmt).scalars().all()]

    def create(self, e: EvaluationDomain) -> EvaluationDomain:
        with SessionLocal() as s:
            obj = Evaluation(internID=e.internID, score=e.score)
            s.add(obj)
            s.commit()
            s.refresh(obj)
            return self._to_domain(obj)

    def update(self, e: EvaluationDomain) -> EvaluationDomain:
        with SessionLocal() as s:
            obj = s.get(Evaluation, e.evalID)
            if not obj:
                return None  # để service quyết định ném NotFound
            obj.score = e.score
            s.commit()
            s.refresh(obj)
            return self._to_domain(obj)

    def delete(self, eval_id: int) -> bool:
        with SessionLocal() as s:
            obj = s.get(Evaluation, eval_id)
            if not obj:
                return False
            s.delete(obj)
            s.commit()
            return True

    def avg_by_intern(self, intern_id: int) -> Optional[float]:
        with SessionLocal() as s:
            avg_val = s.execute(
                select(func.avg(Evaluation.score)).where(Evaluation.internID == intern_id)
            ).scalar()
            return float(avg_val) if avg_val is not None else None

    # ---- helpers
    def _to_domain(self, o: Evaluation) -> EvaluationDomain:
        return EvaluationDomain(evalID=o.evalID, internID=o.internID, score=o.score)

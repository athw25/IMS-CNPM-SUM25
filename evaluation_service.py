from typing import List, Optional
from src.domain.exceptions import ValidationError, NotFoundError
from src.infrastructure.repositories.evaluation_repository import (
    EvaluationRepository, EvaluationDomain
)
from src.infrastructure.repositories.identity_repository import InternRepository

class EvaluationService:
    def __init__(self, eval_repo: EvaluationRepository, intern_repo: InternRepository):
        self.eval_repo = eval_repo
        self.intern_repo = intern_repo

    # ----- validators
    def _validate_score(self, score: float):
        if score is None:
            raise ValidationError("Score is required")
        try:
            s = float(score)
        except Exception:
            raise ValidationError("Score must be a number")
        if s < 0 or s > 100:
            # DB đã có CheckConstraint, nhưng ta vẫn kiểm tra sớm để trả lỗi đẹp
            raise ValidationError("Score must be in [0..100]")

    def _ensure_intern_exists(self, intern_id: int):
        intern = self.intern_repo.get_by_id(intern_id)
        if not intern:
            raise NotFoundError("Intern not found")

    # ----- use cases
    def create(self, intern_id: int, score: float) -> EvaluationDomain:
        self._ensure_intern_exists(intern_id)
        self._validate_score(score)
        return self.eval_repo.create(EvaluationDomain(None, intern_id, float(score)))

    def list_by_intern(self, intern_id: int) -> List[EvaluationDomain]:
        self._ensure_intern_exists(intern_id)
        return self.eval_repo.list_by_intern(intern_id)

    def update(self, eval_id: int, score: float) -> EvaluationDomain:
        self._validate_score(score)
        cur = self.eval_repo.get_by_id(eval_id)
        if not cur:
            raise NotFoundError("Evaluation not found")
        # đảm bảo intern còn tồn tại (phòng trường hợp dữ liệu bị xóa ở nơi khác)
        self._ensure_intern_exists(cur.internID)
        cur.score = float(score)
        updated = self.eval_repo.update(cur)
        if not updated:
            raise NotFoundError("Evaluation not found")
        return updated

    def delete(self, eval_id: int) -> None:
        ok = self.eval_repo.delete(eval_id)
        if not ok:
            raise NotFoundError("Evaluation not found")

    def avg_by_intern(self, intern_id: int) -> Optional[float]:
        self._ensure_intern_exists(intern_id)
        return self.eval_repo.avg_by_intern(intern_id)

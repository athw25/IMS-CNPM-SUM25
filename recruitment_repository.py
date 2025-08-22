# Repository: quản lý database (ở đây giả lập bằng list)

from typing import List, Optional
from recruitment_schema import Recruitment, RecruitmentCreate

class RecruitmentRepository:
    def __init__(self):
        self._db: List[Recruitment] = []
        self._id_counter = 1

    def add(self, recruitment: RecruitmentCreate) -> Recruitment:
        new_item = Recruitment(id=self._id_counter, **recruitment.dict())
        self._db.append(new_item)
        self._id_counter += 1
        return new_item

    def get_all(self) -> List[Recruitment]:
        return self._db

    def get_by_id(self, recruitment_id: int) -> Optional[Recruitment]:
        return next((r for r in self._db if r.id == recruitment_id), None)

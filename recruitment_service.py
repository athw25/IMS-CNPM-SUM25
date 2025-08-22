# Service: xử lý business logic

from typing import List, Optional
from recruitment_repository import RecruitmentRepository
from recruitment_schema import Recruitment, RecruitmentCreate

class RecruitmentService:
    def __init__(self, repository: RecruitmentRepository):
        self.repository = repository

    def create_recruitment(self, data: RecruitmentCreate) -> Recruitment:
        return self.repository.add(data)

    def list_recruitments(self) -> List[Recruitment]:
        return self.repository.get_all()

    def get_recruitment(self, recruitment_id: int) -> Optional[Recruitment]:
        return self.repository.get_by_id(recruitment_id)

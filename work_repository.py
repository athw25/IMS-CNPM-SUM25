from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.enums import AssignmentStatus
from src.infrastructure.models.work_models import AssignmentORM
from src.domain.models.assignment import Assignment

class AssignmentRepository:
    def __init__(self, session: Session):
        self.session = session

    # Mapping helpers
    @staticmethod
    def _to_domain(row: AssignmentORM) -> Assignment:
        return Assignment(
            id=row.id,
            title=row.title,
            description=row.description,
            project_id=row.project_id,
            intern_id=row.intern_id,
            status=row.status,
            is_deleted=row.is_deleted,
        )

    def create(self, a: Assignment) -> Assignment:
        row = AssignmentORM(
            title=a.title,
            description=a.description,
            project_id=a.project_id,
            intern_id=a.intern_id,
            status=a.status,
            is_deleted=a.is_deleted,
        )
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return self._to_domain(row)

    def get(self, assignment_id: int) -> Optional[Assignment]:
        row = self.session.get(AssignmentORM, assignment_id)
        if row is None or row.is_deleted:
            return None
        return self._to_domain(row)

    def list(
        self,
        proj_id: Optional[int] = None,
        intern_id: Optional[int] = None,
        status: Optional[AssignmentStatus] = None,
    ) -> List[Assignment]:
        stmt = select(AssignmentORM).where(AssignmentORM.is_deleted == False)
        if proj_id is not None:
            stmt = stmt.where(AssignmentORM.project_id == proj_id)
        if intern_id is not None:
            stmt = stmt.where(AssignmentORM.intern_id == intern_id)
        if status is not None:
            stmt = stmt.where(AssignmentORM.status == status)
        rows = self.session.execute(stmt).scalars().all()
        return [self._to_domain(r) for r in rows]

    def update_status(self, assignment_id: int, new_status: AssignmentStatus) -> Optional[Assignment]:
        row = self.session.get(AssignmentORM, assignment_id)
        if row is None or row.is_deleted:
            return None
        row.status = new_status
        self.session.flush()
        self.session.refresh(row)
        return self._to_domain(row)

    def soft_delete(self, assignment_id: int) -> bool:
        row = self.session.get(AssignmentORM, assignment_id)
        if row is None or row.is_deleted:
            return False
        row.is_deleted = True
        self.session.flush()
        return True

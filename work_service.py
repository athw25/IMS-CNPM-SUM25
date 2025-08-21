from typing import Optional, List
from src.enums import AssignmentStatus
from src.domain.dtos.assignment_dto import CreateAssignmentDTO, AssignmentResponseDTO, UpdateAssignmentStatusDTO
from src.domain.exceptions import ValidationError, NotFoundError, ConflictError
from src.domain.models.assignment import Assignment
from src.infrastructure.repositories.work_repository import AssignmentRepository

class WorkService:
    def __init__(self, assignment_repo: AssignmentRepository, intern_exists_fn, project_exists_fn):
        self.assignment_repo = assignment_repo
        # inject lightweight existence checks to avoid circular deps
        self.intern_exists_fn = intern_exists_fn
        self.project_exists_fn = project_exists_fn

    # Rules
    def _validate_fk(self, project_id: int, intern_id: int):
        if not self.project_exists_fn(project_id):
            raise NotFoundError(f"Project id={project_id} not found")
        if not self.intern_exists_fn(intern_id):
            raise NotFoundError(f"Intern id={intern_id} not found")

    @staticmethod
    def _can_transition(current: AssignmentStatus, target: AssignmentStatus) -> bool:
        allowed = {
            AssignmentStatus.PENDING: {AssignmentStatus.DOING},
            AssignmentStatus.DOING: {AssignmentStatus.DONE},
            AssignmentStatus.DONE: set(),
        }
        return target in allowed[current]

    # Use-cases
    def create_assignment(self, dto: CreateAssignmentDTO) -> AssignmentResponseDTO:
        self._validate_fk(dto.project_id, dto.intern_id)
        entity = Assignment(
            id=None,
            title=dto.title,
            description=dto.description,
            project_id=dto.project_id,
            intern_id=dto.intern_id,
            status=AssignmentStatus.PENDING,
        )
        created = self.assignment_repo.create(entity)
        return AssignmentResponseDTO(**created.__dict__)

    def list_assignments(self, proj_id: Optional[int], intern_id: Optional[int], status: Optional[AssignmentStatus]) -> List[AssignmentResponseDTO]:
        records = self.assignment_repo.list(proj_id, intern_id, status)
        return [AssignmentResponseDTO(**a.__dict__) for a in records]

    def update_status(self, assignment_id: int, dto: UpdateAssignmentStatusDTO) -> AssignmentResponseDTO:
        current = self.assignment_repo.get(assignment_id)
        if current is None:
            raise NotFoundError(f"Assignment id={assignment_id} not found")

        if not self._can_transition(current.status, dto.status):
            raise ConflictError(f"Invalid status transition: {current.status} -> {dto.status}")

        updated = self.assignment_repo.update_status(assignment_id, dto.status)
        return AssignmentResponseDTO(**updated.__dict__)

    def delete_assignment(self, assignment_id: int) -> None:
        current = self.assignment_repo.get(assignment_id)
        if current is None:
            raise NotFoundError(f"Assignment id={assignment_id} not found")
        if current.status == AssignmentStatus.DONE:
            raise ConflictError("Cannot delete an assignment in DONE status")
        ok = self.assignment_repo.soft_delete(assignment_id)
        if not ok:
            raise ConflictError("Delete failed")

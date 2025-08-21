from dataclasses import dataclass
from typing import Optional
from src.enums import AssignmentStatus

@dataclass
class CreateAssignmentDTO:
    title: str
    description: Optional[str]
    project_id: int
    intern_id: int

@dataclass
class AssignmentResponseDTO:
    id: int
    title: str
    description: Optional[str]
    project_id: int
    intern_id: int
    status: AssignmentStatus

@dataclass
class UpdateAssignmentStatusDTO:
    status: AssignmentStatus

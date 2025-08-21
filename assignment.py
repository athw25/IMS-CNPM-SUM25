from dataclasses import dataclass
from typing import Optional
from src.enums import AssignmentStatus

@dataclass
class Assignment:
    id: Optional[int]
    title: str
    description: Optional[str]
    project_id: int
    intern_id: int
    status: AssignmentStatus = AssignmentStatus.PENDING
    is_deleted: bool = False

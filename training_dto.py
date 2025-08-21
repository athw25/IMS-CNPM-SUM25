from dataclasses import dataclass
from datetime import date
from typing import Optional

# DTO cho TrainingProgram
@dataclass
class CreateProgramDTO:
    name: str
    description: Optional[str]
    start_date: date
    end_date: date

@dataclass
class ProgramResponseDTO:
    id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: date


# DTO cho Project
@dataclass
class CreateProjectDTO:
    program_id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date

@dataclass
class ProjectResponseDTO:
    id: int
    program_id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date

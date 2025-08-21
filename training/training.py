from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class TrainingProgram:
    id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: date


@dataclass
class Project:
    id: int
    program_id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date

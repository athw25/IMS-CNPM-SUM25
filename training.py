#training.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TrainingProgram:
    id: int
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str

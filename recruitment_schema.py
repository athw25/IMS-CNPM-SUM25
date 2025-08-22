from pydantic import BaseModel
from typing import Optional

class RecruitmentCreate(BaseModel):
    title: str
    description: str
    company: str

class Recruitment(RecruitmentCreate):
    id: int

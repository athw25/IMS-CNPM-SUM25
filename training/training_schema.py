from pydantic import BaseModel
from typing import Optional, List

# ---- Program DTO ----
class CreateProgramDTO(BaseModel):
    title: str
    goal: Optional[str] = None

class ProgramResponseDTO(BaseModel):
    progID: int
    title: str
    goal: Optional[str] = None

    class Config:
        orm_mode = True


# ---- Project DTO ----
class CreateProjectDTO(BaseModel):
    progID: int
    title: str

class ProjectResponseDTO(BaseModel):
    projID: int
    progID: int
    title: str

    class Config:
        orm_mode = True

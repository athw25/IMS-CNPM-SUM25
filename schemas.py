# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# --- USER ---
class CreateUser(BaseModel):
    name: str
    email: EmailStr
    role: str  # HR / Intern / Mentor / Admin

class UserResponse(BaseModel):
    userID: int
    name: str
    email: EmailStr
    role: str

# --- INTERN PROFILE ---
class CreateIntern(BaseModel):
    userID: int
    skill: Optional[str] = None

class InternResponse(BaseModel):
    internID: int
    userID: int
    skill: Optional[str] = None

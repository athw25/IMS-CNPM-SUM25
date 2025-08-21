#identify.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDomain:
    userID: Optional[int]
    name: str
    email: str
    role: str  # dùng enums.Role nếu muốn type-strict

@dataclass
class InternProfileDomain:
    internID: Optional[int]
    userID: int
    skill: Optional[str] = None

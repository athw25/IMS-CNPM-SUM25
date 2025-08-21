#identity_schema.py
from dataclasses import dataclass
from typing import Optional
from marshmallow_dataclass import class_schema

# ---- USER DTOs ----
@dataclass
class CreateUserDTO:
    name: str
    email: str
    role: str
CreateUserSchema = class_schema(CreateUserDTO)

@dataclass
class UpdateUserDTO:
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
UpdateUserSchema = class_schema(UpdateUserDTO)

@dataclass
class UserResponseDTO:
    userID: int
    name: str
    email: str
    role: str
UserResponseSchema = class_schema(UserResponseDTO)

# ---- INTERN DTOs ----
@dataclass
class CreateInternDTO:
    userID: int
    skill: Optional[str] = None
CreateInternSchema = class_schema(CreateInternDTO)

@dataclass
class UpdateInternDTO:
    skill: Optional[str] = None
UpdateInternSchema = class_schema(UpdateInternDTO)

@dataclass
class InternResponseDTO:
    internID: int
    userID: int
    skill: Optional[str] = None
InternResponseSchema = class_schema(InternResponseDTO)

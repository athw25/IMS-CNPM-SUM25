from dataclasses import dataclass
from typing import Optional

# Input
@dataclass
class CreateUserDTO:
    name: str
    email: str
    role: str  # nên dùng enums.Role.value

@dataclass
class UpdateUserDTO:
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

# Output
@dataclass
class UserResponseDTO:
    userID: int
    name: str
    email: str
    role: str

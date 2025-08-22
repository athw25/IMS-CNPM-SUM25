from dataclasses import dataclass
from typing import Optional

# Input
@dataclass
class CreateInternDTO:
    userID: int
    skill: Optional[str] = None

@dataclass
class UpdateInternDTO:
    skill: Optional[str] = None

# Output
@dataclass
class InternResponseDTO:
    internID: int
    userID: int
    skill: Optional[str] = None

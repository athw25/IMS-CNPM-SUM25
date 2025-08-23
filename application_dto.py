from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateApplicationDTO:
    campID: int
    userID: int
    status: str  # enums.ApplicationStatus.value

@dataclass
class UpdateApplicationDTO:
    status: Optional[str] = None

@dataclass
class ApplicationResponseDTO:
    appID: int
    campID: int
    userID: int
    status: str

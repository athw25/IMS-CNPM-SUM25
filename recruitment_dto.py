from dataclasses import dataclass
from typing import Optional

# Input (Campaign)
@dataclass
class CreateCampaignDTO:
    title: str
    status: str  # enums.CampaignStatus.value

@dataclass
class UpdateCampaignDTO:
    title: Optional[str] = None
    status: Optional[str] = None

# Output (Campaign)
@dataclass
class CampaignResponseDTO:
    campID: int
    title: str
    status: str

# Input (Application)
@dataclass
class CreateApplicationDTO:
    campID: int
    userID: int              # nộp hồ sơ bởi user (thường là Intern user)
    status: str              # enums.ApplicationStatus.value

@dataclass
class UpdateApplicationDTO:
    status: Optional[str] = None

# Output (Application)
@dataclass
class ApplicationResponseDTO:
    appID: int
    campID: int
    userID: int
    status: str

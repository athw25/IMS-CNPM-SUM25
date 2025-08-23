from dataclasses import dataclass
from typing import Optional

@dataclass
class RecruitmentCampaignDomain:
    campID: Optional[int]
    title: str
    status: str  # dùng enums.CampaignStatus.value

@dataclass
class ApplicationDomain:
    appID: Optional[int]
    campID: int
    userID: int
    status: str  # enums.ApplicationStatus.value

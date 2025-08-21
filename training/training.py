from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RecruitmentCampaign:
    """
    Entity: Recruitment Campaign
    Đại diện cho một chiến dịch tuyển dụng thực tập sinh
    """
    id: Optional[int]
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    status: str = "OPEN"   # OPEN, CLOSED, ARCHIVED


@dataclass
class Application:
    """
    Entity: Application
    Đại diện cho đơn ứng tuyển vào một campaign
    """
    id: Optional[int]
    intern_id: int
    campaign_id: int
    applied_at: datetime = datetime.utcnow()
    status: str = "PENDING"   # PENDING, APPROVED, REJECTED

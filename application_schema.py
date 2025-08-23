from enum import Enum
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


class ApplicationSchema(BaseModel):
    appID: int = Field(..., description="Mã đơn ứng tuyển")
    campID: int = Field(..., description="Mã chiến dịch tuyển dụng")
    userID: int = Field(..., description="Mã người dùng (intern nộp đơn)")
    status: ApplicationStatus = Field(default=ApplicationStatus.Pending,
                                      description="Trạng thái đơn: Pending/Approved/Rejected")

    class Config:
        schema_extra = {
            "example": {
                "appID": 1,
                "campID": 101,
                "userID": 1001,
                "status": "Pending"
            }
        }
from pydantic import BaseModel
from typing import Optional

# ---- Campaign DTOs ----
class CreateCampaignDTO(BaseModel):
    title: str
    status: str

class UpdateCampaignDTO(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None

class CampaignResponseDTO(BaseModel):
    campID: int
    title: str
    status: str

# ---- Application DTOs ----
class CreateApplicationDTO(BaseModel):
    campID: int
    userID: int
    status: str

class UpdateApplicationDTO(BaseModel):
    status: str

class ApplicationResponseDTO(BaseModel):
    appID: int
    campID: int
    userID: int
    status: str

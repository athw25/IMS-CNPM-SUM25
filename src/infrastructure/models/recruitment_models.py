# recruitment_models.py
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SAEnum
from src.infrastructure.databases.db_base import Base
from enums import CampaignStatus, ApplicationStatus


class RecruitmentCampaign(Base):
    __tablename__ = "recruitment_campaigns"

    campID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[CampaignStatus] = mapped_column(
        SAEnum(CampaignStatus, native_enum=False, length=10, validate_strings=True),
        nullable=False,
        default=CampaignStatus.Open
    )

    applications: Mapped[list["Application"]] = relationship(
        back_populates="campaign"
    )


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("campID", "userID", name="uq_applications_campID_userID"),
    )

    appID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    campID: Mapped[int] = mapped_column(
        ForeignKey("recruitment_campaigns.campID"),
        nullable=False
    )
    userID: Mapped[int] = mapped_column(
        ForeignKey("users.userID"),
        nullable=False
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        SAEnum(ApplicationStatus, native_enum=False, length=10, validate_strings=True),
        nullable=False,
        default=ApplicationStatus.Pending
    )

    campaign: Mapped["RecruitmentCampaign"] = relationship(
        back_populates="applications"
    )

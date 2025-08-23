from typing import List, Optional
from domain.models.recruitment import RecruitmentCampaignDomain, ApplicationDomain
from infrastructure.repositories.recruitment_repository import CampaignRepository, ApplicationRepository

# Exceptions & Enums
try:
    from domain.exceptions import DomainError, ValidationError, NotFoundError, ConflictError
except Exception:
    class DomainError(Exception): ...
    class ValidationError(DomainError): ...
    class NotFoundError(DomainError): ...
    class ConflictError(DomainError): ...

from enums import CampaignStatus, ApplicationStatus  # enum .value là string
# Nếu muốn kiểm tra user tồn tại, có thể import:
# from infrastructure.repositories.identity_repository import UserRepository

class RecruitmentService:
    def __init__(self,
                 campaign_repo: CampaignRepository,
                 application_repo: ApplicationRepository,
                 # user_repo: Optional[UserRepository] = None
                 ):
        self.campaign_repo = campaign_repo
        self.application_repo = application_repo
        # self.user_repo = user_repo

    # ------- Campaign -------
    def list_campaigns(self, status: Optional[str] = None) -> List[RecruitmentCampaignDomain]:
        return self.campaign_repo.list(status)

    def create_campaign(self, title: str, status: str) -> RecruitmentCampaignDomain:
        if not title or not title.strip():
            raise ValidationError("title is required")
        if status not in {x.value for x in CampaignStatus}:
            raise ValidationError("invalid campaign status")
        return self.campaign_repo.create(RecruitmentCampaignDomain(None, title.strip(), status))

    def update_campaign(self, camp_id: int, title: Optional[str], status: Optional[str]) -> RecruitmentCampaignDomain:
        cur = self.campaign_repo.get_by_id(camp_id)
        if not cur:
            raise NotFoundError("Campaign not found")
        if title is not None:
            if not title.strip():
                raise ValidationError("title cannot be empty")
            cur.title = title.strip()
        if status is not None:
            if status not in {x.value for x in CampaignStatus}:
                raise ValidationError("invalid campaign status")
            cur.status = status
        updated = self.campaign_repo.update(cur)
        if not updated:
            raise NotFoundError("Campaign not found")
        return updated

    def delete_campaign(self, camp_id: int) -> None:
        if self.campaign_repo.count_applications(camp_id) > 0:
            raise ConflictError("Cannot delete campaign with existing applications")
        ok = self.campaign_repo.delete(camp_id)
        if not ok:
            raise NotFoundError("Campaign not found")

    # ------- Application -------
    def list_applications(self, camp_id: Optional[int] = None, user_id: Optional[int] = None) -> List[ApplicationDomain]:
        return self.application_repo.list(camp_id, user_id)

    def create_application(self, camp_id: int, user_id: int, status: str) -> ApplicationDomain:
        camp = self.campaign_repo.get_by_id(camp_id)
        if not camp:
            raise NotFoundError("Campaign not found")
        if camp.status == CampaignStatus.Closed.value:
            raise ConflictError("Campaign is closed")
        if status not in {x.value for x in ApplicationStatus}:
            raise ValidationError("invalid application status")

        # Nếu cần: kiểm tra user tồn tại và role Intern
        # if self.user_repo and not self.user_repo.get_by_id(user_id):
        #     raise NotFoundError("User not found")

        return self.application_repo.create(ApplicationDomain(None, camp_id, user_id, status))

    def update_application(self, app_id: int, status: str) -> ApplicationDomain:
        if status not in {x.value for x in ApplicationStatus}:
            raise ValidationError("invalid application status")
        cur = self.application_repo.get_by_id(app_id)
        if not cur:
            raise NotFoundError("Application not found")
        cur.status = status
        updated = self.application_repo.update(cur)
        if not updated:
            raise NotFoundError("Application not found")
        return updated

    def delete_application(self, app_id: int) -> None:
        ok = self.application_repo.delete(app_id)
        if not ok:
            raise NotFoundError("Application not found")

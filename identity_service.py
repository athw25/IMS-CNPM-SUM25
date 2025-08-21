#identity_service.py
from typing import List, Optional
from src.domain.models.identity import UserDomain, InternProfileDomain
from src.infrastructure.repositories.identity_repository import UserRepository, InternRepository

# Exceptions chung (dùng của bạn nếu đã có)
try:
    from src.domain.exceptions import DomainError, ValidationError, NotFoundError, ConflictError
except Exception:
    class DomainError(Exception): ...
    class ValidationError(DomainError): ...
    class NotFoundError(DomainError): ...
    class ConflictError(DomainError): ...

from src.enums import Role

class IdentityService:
    def __init__(self, user_repo: UserRepository, intern_repo: InternRepository):
        self.user_repo = user_repo
        self.intern_repo = intern_repo

    # -------- USERS --------
    def list_users(self, role: Optional[str] = None) -> List[UserDomain]:
        return self.user_repo.list(role)

    def create_user(self, name: str, email: str, role: str) -> UserDomain:
        if not name or not name.strip():
            raise ValidationError("name is required")
        if not email or not email.strip():
            raise ValidationError("email is required")
        if role not in {Role.HR.value, Role.Intern.value, Role.Mentor.value, Role.Admin.value}:
            raise ValidationError("invalid role")

        if self.user_repo.get_by_email(email.strip()):
            raise ConflictError("Email already exists")

        return self.user_repo.create(UserDomain(None, name.strip(), email.strip(), role))

    def update_user(self, user_id: int, name: Optional[str], email: Optional[str], role: Optional[str]) -> UserDomain:
        cur = self.user_repo.get_by_id(user_id)
        if not cur:
            raise NotFoundError("User not found")

        if email is not None:
            email = email.strip()
            if not email:
                raise ValidationError("email cannot be empty")
            other = self.user_repo.get_by_email(email)
            if other and other.userID != user_id:
                raise ConflictError("Email already exists")
            cur.email = email

        if name is not None:
            name = name.strip()
            if not name:
                raise ValidationError("name cannot be empty")
            cur.name = name

        if role is not None:
            if role not in {Role.HR.value, Role.Intern.value, Role.Mentor.value, Role.Admin.value}:
                raise ValidationError("invalid role")
            # Nếu đang có InternProfile mà role đổi khác Intern -> chặn
            has_profile = self.intern_repo.get_by_user(user_id)
            if has_profile and role != Role.Intern.value:
                raise ConflictError("Cannot change role away from Intern while intern profile exists")
            cur.role = role

        updated = self.user_repo.update(cur)
        if not updated:
            raise NotFoundError("User not found")
        return updated

    def delete_user(self, user_id: int) -> None:
        profile = self.intern_repo.get_by_user(user_id)
        if profile:
            raise ConflictError("Cannot delete user having an intern profile")
        ok = self.user_repo.delete(user_id)
        if not ok:
            raise NotFoundError("User not found")

    # -------- INTERN PROFILES --------
    def list_interns(self) -> List[InternProfileDomain]:
        return self.intern_repo.list()

    def create_intern(self, user_id: int, skill: Optional[str]) -> InternProfileDomain:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        if user.role != Role.Intern.value:
            raise ValidationError("User role must be Intern")
        if self.intern_repo.get_by_user(user_id):
            raise ConflictError("Intern profile already exists for this user")

        return self.intern_repo.create(InternProfileDomain(None, user_id, (skill or None)))

    def update_intern(self, intern_id: int, skill: Optional[str]) -> InternProfileDomain:
        cur = self.intern_repo.get_by_id(intern_id)
        if not cur:
            raise NotFoundError("Intern profile not found")
        cur.skill = (skill.strip() if skill is not None and skill.strip() else cur.skill)
        updated = self.intern_repo.update(cur)
        if not updated:
            raise NotFoundError("Intern profile not found")
        return updated

    def delete_intern(self, intern_id: int) -> None:
        ok = self.intern_repo.delete(intern_id)
        if not ok:
            raise NotFoundError("Intern profile not found")

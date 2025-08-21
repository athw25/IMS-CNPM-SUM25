#identity_repository.py
from typing import Optional, List
from sqlalchemy import select
from src.infrastructure.databases.db_base import SessionLocal
from src.infrastructure.models.identity_models import User as UserORM, InternProfile as InternORM
from src.domain.models.identity import UserDomain, InternProfileDomain

# ---------- USER ----------
class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[UserDomain]:
        with SessionLocal() as s:
            obj = s.get(UserORM, user_id)
            return self._to_domain(obj) if obj else None

    def get_by_email(self, email: str) -> Optional[UserDomain]:
        with SessionLocal() as s:
            obj = s.execute(select(UserORM).where(UserORM.email == email)).scalar_one_or_none()
            return self._to_domain(obj) if obj else None

    def list(self, role: Optional[str] = None) -> List[UserDomain]:
        with SessionLocal() as s:
            stmt = select(UserORM).order_by(UserORM.userID.asc())
            if role:
                stmt = stmt.where(UserORM.role == role)
            return [self._to_domain(x) for x in s.execute(stmt).scalars().all()]

    def create(self, u: UserDomain) -> UserDomain:
        with SessionLocal() as s:
            obj = UserORM(name=u.name, email=u.email, role=u.role)
            s.add(obj); s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def update(self, u: UserDomain) -> Optional[UserDomain]:
        with SessionLocal() as s:
            obj = s.get(UserORM, u.userID)
            if not obj:
                return None
            obj.name  = u.name if u.name is not None else obj.name
            obj.email = u.email if u.email is not None else obj.email
            obj.role  = u.role if u.role is not None else obj.role
            s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def delete(self, user_id: int) -> bool:
        with SessionLocal() as s:
            obj = s.get(UserORM, user_id)
            if not obj:
                return False
            s.delete(obj); s.commit()
            return True

    def _to_domain(self, o: UserORM) -> UserDomain:
        return UserDomain(userID=o.userID, name=o.name, email=o.email, role=o.role)


# ---------- INTERN PROFILE ----------
class InternRepository:
    def get_by_id(self, intern_id: int) -> Optional[InternProfileDomain]:
        with SessionLocal() as s:
            obj = s.get(InternORM, intern_id)
            return self._to_domain(obj) if obj else None

    def get_by_user(self, user_id: int) -> Optional[InternProfileDomain]:
        with SessionLocal() as s:
            obj = s.execute(select(InternORM).where(InternORM.userID == user_id)).scalar_one_or_none()
            return self._to_domain(obj) if obj else None

    def list(self) -> List[InternProfileDomain]:
        with SessionLocal() as s:
            stmt = select(InternORM).order_by(InternORM.internID.asc())
            return [self._to_domain(x) for x in s.execute(stmt).scalars().all()]

    def create(self, i: InternProfileDomain) -> InternProfileDomain:
        with SessionLocal() as s:
            obj = InternORM(userID=i.userID, skill=i.skill)
            s.add(obj); s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def update(self, i: InternProfileDomain) -> Optional[InternProfileDomain]:
        with SessionLocal() as s:
            obj = s.get(InternORM, i.internID)
            if not obj:
                return None
            obj.skill = i.skill if i.skill is not None else obj.skill
            s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def delete(self, intern_id: int) -> bool:
        with SessionLocal() as s:
            obj = s.get(InternORM, intern_id)
            if not obj:
                return False
            s.delete(obj); s.commit()
            return True

    def _to_domain(self, o: InternORM) -> InternProfileDomain:
        return InternProfileDomain(internID=o.internID, userID=o.userID, skill=o.skill)

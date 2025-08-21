# services.py
from fastapi import HTTPException, status
from .schemas import CreateUser, CreateIntern
from .repositories import UserRepository, InternRepository

class IdentityService:
    def __init__(self, user_repo: UserRepository, intern_repo: InternRepository):
        self.user_repo = user_repo
        self.intern_repo = intern_repo

    # --- USER ---
    def create_user(self, u: CreateUser):
        if self.user_repo.get_by_email(u.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        return self.user_repo.create(u)

    def delete_user(self, user_id: int):
        if self.intern_repo.get_by_user(user_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail="Delete intern profile first")
        if not self.user_repo.delete(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"deleted": True}

    # --- INTERN ---
    def create_intern(self, i: CreateIntern):
        user = self.user_repo.get_by_id(i.userID)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.role != "Intern":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not an Intern")
        if self.intern_repo.get_by_user(i.userID):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Intern profile already exists")
        return self.intern_repo.create(i)

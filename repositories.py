# repositories.py
from typing import List, Optional
from .schemas import CreateUser, UserResponse, CreateIntern, InternResponse

class UserRepository:
    def __init__(self):
        self.users = []
        self.next_id = 1001

    def create(self, u: CreateUser) -> UserResponse:
        new_user = UserResponse(userID=self.next_id, **u.dict())
        self.next_id += 1
        self.users.append(new_user)
        return new_user

    def get_by_id(self, id: int) -> Optional[UserResponse]:
        return next((u for u in self.users if u.userID == id), None)

    def get_by_email(self, email: str) -> Optional[UserResponse]:
        return next((u for u in self.users if u.email == email), None)

    def list(self, role: Optional[str] = None) -> List[UserResponse]:
        if role:
            return [u for u in self.users if u.role == role]
        return self.users

    def update(self, updated_user: UserResponse) -> bool:
        for i, u in enumerate(self.users):
            if u.userID == updated_user.userID:
                self.users[i] = updated_user
                return True
        return False

    def delete(self, id: int) -> bool:
        for i, u in enumerate(self.users):
            if u.userID == id:
                del self.users[i]
                return True
        return False


class InternRepository:
    def __init__(self):
        self.profiles = []
        self.next_id = 2001

    def create(self, i: CreateIntern) -> InternResponse:
        new_profile = InternResponse(internID=self.next_id, **i.dict())
        self.next_id += 1
        self.profiles.append(new_profile)
        return new_profile

    def get_by_id(self, id: int) -> Optional[InternResponse]:
        return next((p for p in self.profiles if p.internID == id), None)

    def get_by_user(self, userID: int) -> Optional[InternResponse]:
        return next((p for p in self.profiles if p.userID == userID), None)

    def list(self) -> List[InternResponse]:
        return self.profiles

    def update(self, updated_profile: InternResponse) -> bool:
        for i, p in enumerate(self.profiles):
            if p.internID == updated_profile.internID:
                self.profiles[i] = updated_profile
                return True
        return False

    def delete(self, id: int) -> bool:
        for i, p in enumerate(self.profiles):
            if p.internID == id:
                del self.profiles[i]
                return True
        return False

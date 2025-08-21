# main.py
from fastapi import FastAPI
from .schemas import CreateUser, CreateIntern
from .repositories import UserRepository, InternRepository
from .services import IdentityService

app = FastAPI()

user_repo = UserRepository()
intern_repo = InternRepository()
service = IdentityService(user_repo, intern_repo)

# --- USER ---
@app.get("/api/users")
def list_users(role: str = None):
    return user_repo.list(role)

@app.post("/api/users", status_code=201)
def create_user(u: CreateUser):
    return service.create_user(u)

@app.put("/api/users/{user_id}")
def update_user(user_id: int, u: CreateUser):
    user = user_repo.get_by_id(user_id)
    if not user:
        return {"error": "User not found"}
    updated = user.copy(update=u.dict())
    user_repo.update(updated)
    return updated

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    return service.delete_user(user_id)

# --- INTERN ---
@app.get("/api/interns")
def list_interns():
    return intern_repo.list()

@app.post("/api/interns", status_code=201)
def create_intern(i: CreateIntern):
    return service.create_intern(i)

@app.put("/api/interns/{intern_id}")
def update_intern(intern_id: int, i: CreateIntern):
    profile = intern_repo.get_by_id(intern_id)
    if not profile:
        return {"error": "Intern profile not found"}
    updated = profile.copy(update=i.dict())
    intern_repo.update(updated)
    return updated

@app.delete("/api/interns/{intern_id}")
def delete_intern(intern_id: int):
    if not intern_repo.delete(intern_id):
        return {"error": "Intern profile not found"}
    return {"deleted": True}

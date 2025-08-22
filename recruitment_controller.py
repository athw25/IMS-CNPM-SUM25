from fastapi import APIRouter
from typing import List
from recruitment_service import RecruitmentService
from recruitment_repository import RecruitmentRepository
from recruitment_schema import Recruitment, RecruitmentCreate

router = APIRouter()

repository = RecruitmentRepository()
service = RecruitmentService(repository)

@router.post("/recruitments", response_model=Recruitment)
def create_recruitment(data: RecruitmentCreate):
    return service.create_recruitment(data)

@router.get("/recruitments", response_model=List[Recruitment])
def list_recruitments():
    return service.list_recruitments()

@router.get("/recruitments/{recruitment_id}", response_model=Recruitment)
def get_recruitment(recruitment_id: int):
    return service.get_recruitment(recruitment_id)

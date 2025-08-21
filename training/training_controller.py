from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from . import schemas, repository, service

router = APIRouter(prefix="/api", tags=["Training"])

# -------- Program API --------
@router.get("/programs", response_model=list[schemas.ProgramResponseDTO])
def list_programs(db: Session = Depends(get_db)):
    return repository.ProgramRepository.list(db)

@router.post("/programs", response_model=schemas.ProgramResponseDTO)
def create_program(data: schemas.CreateProgramDTO, db: Session = Depends(get_db)):
    return repository.ProgramRepository.create(db, data)

@router.put("/programs/{progID}", response_model=schemas.ProgramResponseDTO)
def update_program(progID: int, data: schemas.CreateProgramDTO, db: Session = Depends(get_db)):
    obj = repository.ProgramRepository.update(db, progID, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Program not found")
    return obj

@router.delete("/programs/{progID}")
def delete_program(progID: int, db: Session = Depends(get_db)):
    return service.ProgramService.delete_program(db, progID)


# -------- Project API --------
@router.get("/projects", response_model=list[schemas.ProjectResponseDTO])
def list_projects(progID: int, db: Session = Depends(get_db)):
    return repository.ProjectRepository.list_by_program(db, progID)

@router.post("/projects", response_model=schemas.ProjectResponseDTO)
def create_project(data: schemas.CreateProjectDTO, db: Session = Depends(get_db)):
    return repository.ProjectRepository.create(db, data)

@router.put("/projects/{projID}", response_model=schemas.ProjectResponseDTO)
def update_project(projID: int, data: schemas.CreateProjectDTO, db: Session = Depends(get_db)):
    obj = repository.ProjectRepository.update(db, projID, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj

@router.delete("/projects/{projID}")
def delete_project(projID: int, db: Session = Depends(get_db)):
    return service.ProjectService.delete_project(db, projID)

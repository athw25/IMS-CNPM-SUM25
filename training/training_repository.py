from sqlalchemy.orm import Session
from . import entities, schemas

# ---- ProgramRepository ----
class ProgramRepository:
    @staticmethod
    def create(db: Session, program: schemas.CreateProgramDTO):
        obj = entities.TrainingProgram(**program.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_id(db: Session, progID: int):
        return db.query(entities.TrainingProgram).filter_by(progID=progID).first()

    @staticmethod
    def list(db: Session):
        return db.query(entities.TrainingProgram).all()

    @staticmethod
    def update(db: Session, progID: int, data: schemas.CreateProgramDTO):
        obj = ProgramRepository.get_by_id(db, progID)
        if obj:
            for k, v in data.dict().items():
                setattr(obj, k, v)
            db.commit()
            db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, progID: int):
        obj = ProgramRepository.get_by_id(db, progID)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# ---- ProjectRepository ----
class ProjectRepository:
    @staticmethod
    def create(db: Session, project: schemas.CreateProjectDTO):
        obj = entities.Project(**project.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_id(db: Session, projID: int):
        return db.query(entities.Project).filter_by(projID=projID).first()

    @staticmethod
    def list_by_program(db: Session, progID: int):
        return db.query(entities.Project).filter_by(progID=progID).all()

    @staticmethod
    def update(db: Session, projID: int, data: schemas.CreateProjectDTO):
        obj = ProjectRepository.get_by_id(db, projID)
        if obj:
            for k, v in data.dict().items():
                setattr(obj, k, v)
            db.commit()
            db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, projID: int):
        obj = ProjectRepository.get_by_id(db, projID)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

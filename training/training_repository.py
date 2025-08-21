from sqlalchemy.orm import Session
from ..models.training_models import TrainingProgram, Project

class ProgramRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TrainingProgram).all()

    def get_by_id(self, program_id: int):
        return self.db.query(TrainingProgram).filter(TrainingProgram.id == program_id).first()

    def create(self, program: TrainingProgram):
        self.db.add(program)
        self.db.commit()
        self.db.refresh(program)
        return program

    def update(self, program: TrainingProgram):
        self.db.commit()
        self.db.refresh(program)
        return program

    def delete(self, program: TrainingProgram):
        self.db.delete(program)
        self.db.commit()


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_program(self, program_id: int):
        return self.db.query(Project).filter(Project.program_id == program_id).all()

    def get_by_id(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project: Project):
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project):
        self.db.delete(project)
        self.db.commit()

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .repository import ProgramRepository, ProjectRepository

class ProgramService:
    @staticmethod
    def delete_program(db: Session, progID: int):
        program = ProgramRepository.get_by_id(db, progID)
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        if program.projects:  # còn project
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Cannot delete Program with existing Projects")
        return ProgramRepository.delete(db, progID)


class ProjectService:
    @staticmethod
    def delete_project(db: Session, projID: int, assignment_repo=None):
        project = ProjectRepository.get_by_id(db, projID)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Sau khi tích hợp với TV4 (Assignment)
        if assignment_repo:
            count = assignment_repo.count_by_project(db, projID)
            if count > 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="Cannot delete Project with existing Assignments")

        return ProjectRepository.delete(db, projID)

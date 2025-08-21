from domain.dtos.training_dto import (
    CreateProgramDTO, ProgramResponseDTO,
    CreateProjectDTO, ProjectResponseDTO
)
from infrastructure.models.training_models import TrainingProgram, Project
from infrastructure.repositories.training_repository import ProgramRepository, ProjectRepository
from domain.exceptions import ValidationError, NotFoundError


class TrainingService:
    def __init__(self, program_repo: ProgramRepository, project_repo: ProjectRepository):
        self.program_repo = program_repo
        self.project_repo = project_repo

    # Training Program
    def create_program(self, dto: CreateProgramDTO) -> ProgramResponseDTO:
        program = TrainingProgram(**dto.__dict__)
        program = self.program_repo.create(program)
        return ProgramResponseDTO(**program.__dict__)

    def get_programs(self):
        return [ProgramResponseDTO(**p.__dict__) for p in self.program_repo.get_all()]

    def update_program(self, program_id: int, dto: CreateProgramDTO):
        program = self.program_repo.get_by_id(program_id)
        if not program:
            raise NotFoundError("Program not found")

        for k, v in dto.__dict__.items():
            setattr(program, k, v)
        program = self.program_repo.update(program)
        return ProgramResponseDTO(**program.__dict__)

    def delete_program(self, program_id: int):
        program = self.program_repo.get_by_id(program_id)
        if not program:
            raise NotFoundError("Program not found")
        if program.projects:  # không cho xóa nếu còn project
            raise ValidationError("Cannot delete program with existing projects")
        self.program_repo.delete(program)

    # Project
    def create_project(self, dto: CreateProjectDTO):
        program = self.program_repo.get_by_id(dto.program_id)
        if not program:
            raise NotFoundError("Program not found")
        project = Project(**dto.__dict__)
        project = self.project_repo.create(project)
        return ProjectResponseDTO(**project.__dict__)

    def get_projects_by_program(self, program_id: int):
        projects = self.project_repo.get_all_by_program(program_id)
        return [ProjectResponseDTO(**p.__dict__) for p in projects]

    def update_project(self, project_id: int, dto: CreateProjectDTO):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")

        for k, v in dto.__dict__.items():
            setattr(project, k, v)
        project = self.project_repo.update(project)
        return ProjectResponseDTO(**project.__dict__)

    def delete_project(self, project_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        # check assignment ở người 4 → tạm raise lỗi giả định
        if hasattr(project, "assignments") and project.assignments:
            raise ValidationError("Cannot delete project with assignments")
        self.project_repo.delete(project)

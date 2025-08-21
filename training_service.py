#training_service.py
from domain.models.training import TrainingProgram
from infrastructure.repositories.training_repository import TrainingRepository
from datetime import datetime

class TrainingService:
    def __init__(self):
        self.repo = TrainingRepository()

    def get_all_trainings(self):
        return self.repo.get_all()

    def get_training(self, program_id: int):
        return self.repo.get_by_id(program_id)

    def create_training(self, data: dict):
        program = TrainingProgram(
            id=None,
            name=data["name"],
            description=data.get("description", ""),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            status=data["status"]
        )
        return self.repo.create(program)

    def update_training(self, program_id: int, data: dict):
        return self.repo.update(program_id, data)

    def delete_training(self, program_id: int):
        self.repo.delete(program_id)

# Instance để inject vào controller
training_service = TrainingService()

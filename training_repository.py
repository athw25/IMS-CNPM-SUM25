#training_repository.py
from infrastructure.databases import SessionLocal
from infrastructure.models.training_models import TrainingProgramORM
from domain.models.training import TrainingProgram

class TrainingRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        result = self.db.query(TrainingProgramORM).all()
        return [self._to_domain(x) for x in result]

    def get_by_id(self, program_id: int):
        obj = self.db.query(TrainingProgramORM).get(program_id)
        return self._to_domain(obj) if obj else None

    def create(self, domain_obj: TrainingProgram):
        orm_obj = TrainingProgramORM(
            name=domain_obj.name,
            description=domain_obj.description,
            start_date=domain_obj.start_date,
            end_date=domain_obj.end_date,
            status=domain_obj.status
        )
        self.db.add(orm_obj)
        self.db.commit()
        self.db.refresh(orm_obj)
        return self._to_domain(orm_obj)

    def update(self, program_id: int, data: dict):
        obj = self.db.query(TrainingProgramORM).get(program_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_domain(obj)

    def delete(self, program_id: int):
        obj = self.db.query(TrainingProgramORM).get(program_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()

    def _to_domain(self, orm_obj):
        return TrainingProgram(
            id=orm_obj.id,
            name=orm_obj.name,
            description=orm_obj.description,
            start_date=orm_obj.start_date,
            end_date=orm_obj.end_date,
            status=orm_obj.status
        )

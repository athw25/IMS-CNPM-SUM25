from src.infrastructure.databases.db_base import engine, Base

from src.models import (
    identity_models,
    recruitment_models,
    training_models,
    work_models,
    evaluation_models,
)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Đã tạo xong các bảng trên MySQL.")

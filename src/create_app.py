# src/create_app.py
from src.infrastructure.databases.db_base import engine, Base

# Import tất cả các lớp để chắc chắn đăng ký vào Base.metadata
from src.infrastructure.models.identity_models import User, InternProfile
from src.infrastructure.models.recruitment_models import RecruitmentCampaign, Application
from src.infrastructure.models.training_models import TrainingProgram, Project
from src.infrastructure.models.work_models import Assignment
from src.infrastructure.models.evaluation_models import Evaluation

def main():
    # Debug: in ra các bảng đã có trong metadata trước khi tạo
    print("-> Models loaded:", [cls.__name__ for cls in [
        User, InternProfile, RecruitmentCampaign, Application,
        TrainingProgram, Project, Assignment, Evaluation
    ]])
    print("-> Tables in metadata (before create_all):",
          list(Base.metadata.tables.keys()))

    Base.metadata.create_all(engine)

    print("-> Tables in metadata (after create_all):",
          list(Base.metadata.tables.keys()))
    print("Đã tạo xong các bảng trên MySQL.")

if __name__ == "__main__":
    main()

from db_base import SessionLocal, engine
from training_models import Base, TrainingProgram, Project

if __name__ == "__main__":
    # Tạo bảng
    Base.metadata.create_all(engine)

    with SessionLocal() as sess:
        # Tạo 1 chương trình
        p = TrainingProgram(title="Python Bootcamp", goal="Nắm Python cơ bản")
        sess.add(p)
        sess.commit()

        # Thêm 2 dự án vào chương trình
        sess.add_all([
            Project(progID=p.progID, title="IMS Backend"),
            Project(progID=p.progID, title="Data ETL")
        ])
        sess.commit()

        print(" Tạo Program/Project OK")
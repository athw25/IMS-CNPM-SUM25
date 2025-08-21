from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Base từ SQLAlchemy declarative_base()

class TrainingProgram(Base):
    __tablename__ = "programs"

    progID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    goal = Column(String, nullable=True)

    projects = relationship("Project", back_populates="program", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    projID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    progID = Column(Integer, ForeignKey("programs.progID"), nullable=False)
    title = Column(String, nullable=False)

    program = relationship("TrainingProgram", back_populates="projects")

# identity_models.py

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.databases.db_base import Base
from enums import Role  # Role = Enum('HR', 'Intern', 'Mentor', 'Admin')


class User(Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # lưu Enum dạng VARCHAR

    # Quan hệ 1–1 với InternProfile (tùy chọn, back_populates phải thống nhất)
    intern_profile: Mapped["InternProfile"] = relationship(
        back_populates="user",
        uselist=False,
    )


class InternProfile(Base):
    __tablename__ = "intern_profiles"

    internID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.userID", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        unique=True,  # đảm bảo quan hệ 1–1
    )
    skill: Mapped[str] = mapped_column(String(255), nullable=False)

    # Quan hệ 1–1 với User
    user: Mapped[User] = relationship(
        back_populates="intern_profile",
        uselist=False,
    )

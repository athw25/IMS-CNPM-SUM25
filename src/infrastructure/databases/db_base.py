# db_base.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()  # đọc biến từ .env

class Base(DeclarativeBase):
    pass

MYSQL_URL = os.getenv(
    "MYSQL_URL",
    "mysql+pymysql://root:1234@127.0.0.1:3306/IMS?charset=utf8mb4"
)

engine = create_engine(
    MYSQL_URL,
    echo=True,          # in SQL ra console để debug
    pool_pre_ping=True, # chống mất kết nối
    future=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)

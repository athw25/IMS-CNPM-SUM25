from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cấu hình MySQL
DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/Project_CNPM"

# Kết nối MySQL
engine = create_engine(DATABASE_URL, echo=True)

# Tạo Session để thao tác DB
SessionLocal = sessionmaker(bind=engine)

# Base class cho các model
Base = declarative_base()

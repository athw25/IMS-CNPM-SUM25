 db_base.py
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Kết nối MySQL (thay username, password, db_name của bạn)
DATABASE_URL = "mysql+pymysql://root:password@localhost/ims_db"

engine = create_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
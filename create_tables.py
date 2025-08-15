from database import Base, engine
from models import User

# Tạo bảng dựa trên class model
Base.metadata.create_all(bind=engine)

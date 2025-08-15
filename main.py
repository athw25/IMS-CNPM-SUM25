from sqlalchemy import create_engine, text

# Kết nối SQLite (tạo file database.sqlite)
engine = create_engine("sqlite:///database.sqlite")

# Tạo kết nối
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello from SQLAlchemy'"))
    for row in result:
        print(row[0])
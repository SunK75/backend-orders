from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ On Render, copy test.db to /tmp and use that path
if os.path.exists("test.db") and not os.path.exists("/tmp/test.db"):
    import shutil
    shutil.copy("test.db", "/tmp/test.db")

# ✅ Fallback to /tmp path if DATABASE_URL not set
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:////tmp/test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

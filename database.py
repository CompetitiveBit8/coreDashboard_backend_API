from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///db.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# metadata = MetaData()

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
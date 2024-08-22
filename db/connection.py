from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbtype   = "postgresql"
user     = "postgres"
password = "Salam@123"
host     = "127.0.0.1"
port     = "5432"
db       = "course"

SQLALCHEMY_DATABASE_URL = f"sqlite:///./blogs.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
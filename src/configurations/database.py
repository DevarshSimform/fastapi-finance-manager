from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

DATABASE_URL = config('DATABASE_URL')

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    with SessionLocal() as db:
        yield db
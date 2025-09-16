import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clinic.db")

engine_kwargs = {"pool_pre_ping": True}
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
# SQLite needs this for multithreaded FastAPI
connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

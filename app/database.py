import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("postgresql://clinic_db_1dxu_user:JC4nkDSkspwspanYT2UzIvgEmQNyZpBY@dpg-d33d8dmmcj7s73a9njng-a.oregon-postgres.render.com/clinic_db_1dxu", "sqlite:///./clinic.db")

engine_kwargs = {"pool_pre_ping": True}
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    # SQLite needs this for multithreaded FastAPI
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSON
from .database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    address = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    role = Column(String, nullable=False)
    data = Column(JSON, nullable=False)   # ✅ store structured dict safely
    created_at = Column(DateTime(timezone=True), server_default=func.now())

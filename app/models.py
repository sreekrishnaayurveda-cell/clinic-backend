from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    contact = Column(String)
    address = Column(String)
    occupation = Column(String)
    marital_status = Column(String)

    observations = relationship("Observation", back_populates="patient")

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    role = Column(String)  # Nurse, Doctor, Therapist
    date_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    vitals = Column(JSON, nullable=True)
    ayurveda_findings = Column(JSON, nullable=True)
    red_flags = Column(JSON, nullable=True)

    patient = relationship("Patient", back_populates="observations")

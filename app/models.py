from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

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

    # Relationship: one patient can have many observations
    observations = relationship(
        "Observation",
        back_populates="patient",
        cascade="all, delete-orphan"
    )


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)  # Nurse / Doctor / Therapist
    data = Column(JSON, nullable=False)    # structured JSON per role
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship: link back to patient
    patient = relationship("Patient", back_populates="observations")

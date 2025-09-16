from pydantic import BaseModel, Field
from typing import Optional
import datetime


# ========================
# PATIENT SCHEMAS
# ========================

class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None
    marital_status: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None
    marital_status: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


# ========================
# OBSERVATION SCHEMAS
# ========================

class ObservationCreate(BaseModel):
    patient_id: int
    role: str = Field(pattern="^(Nurse|Doctor|Therapist)$")
    notes: Optional[str] = None
    date_time: Optional[datetime.datetime] = None


class ObservationResponse(BaseModel):
    id: int
    patient_id: int
    role: str
    notes: Optional[str] = None
    date_time: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import datetime

class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None
    marital_status: Optional[str] = None

class PatientResponse(PatientCreate):
    id: int
    class Config:
        from_attributes = True  # pydantic v2

class ObservationCreate(BaseModel):
    patient_id: int
    role: str = Field(pattern="^(Nurse|Doctor|Therapist)$")
    date_time: Optional[datetime.datetime] = None
    vitals: Optional[Dict] = None
    ayurveda_findings: Optional[Dict] = None
    red_flags: Optional[List[str]] = None

class ObservationResponse(ObservationCreate):
    id: int
    class Config:
        from_attributes = True

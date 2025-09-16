from __future__ import annotations

# ==== Nurse Observation ====
class Vitals(BaseModel):
pulse: Optional[int] = Field(None, description="beats per minute")
bp: Optional[str] = Field(None, description="e.g., '120/80'")
spo2: Optional[int] = Field(None, ge=0, le=100)
temp_f: Optional[float] = None
height_cm: Optional[float] = None
weight_kg: Optional[float] = None
bmi: Optional[float] = None

class NurseObservation(BaseModel):
date_time: Optional[str] = Field(None, description="ISO or human date")
vitals: Optional[Vitals] = None
bowel: Optional[str] = None
bladder: Optional[str] = None
appetite: Optional[str] = None
sleep: Optional[str] = None
daily_notes: Optional[str] = None
red_flag: Optional[bool] = False
red_flag_notes: Optional[List[str]] = None

# ==== Doctor Observation ====
class DoctorObservation(BaseModel):
selected_samhita: Optional[str] = Field(None, description="Charaka / Sushruta / Ashtanga Hridayam / Other")
samhita_interpretation: Optional[str] = None
nidana: Optional[str] = None
poorvaroopa: Optional[str] = None
roopa: Optional[str] = None
upashaya: Optional[str] = None
anupashaya: Optional[str] = None
samprapti: Optional[str] = None
differential_diagnosis: Optional[List[str]] = None
prognosis: Optional[str] = None
chikitsa_sutra: Optional[str] = None
classical_medicines: Optional[List[str]] = None
references: Optional[List[str]] = None

# ==== Therapist Observation ====
class TherapistObservation(BaseModel):
prescribed_therapy: Optional[str] = None
oil_used: Optional[str] = None
decoction_used: Optional[str] = None
target_area: Optional[str] = None
pressure: Optional[str] = None
speed: Optional[str] = None
temperature: Optional[str] = None
duration_minutes: Optional[int] = None
checklist: Optional[Dict[str, bool]] = None
aftercare_instructions: Optional[str] = None
session_notes: Optional[str] = None

# Union type for role-specific data
ObservationData = Union[NurseObservation, DoctorObservation, TherapistObservation]

class ObservationCreate(BaseModel):
patient_id: int
role: Role
data: ObservationData

class ObservationOut(BaseModel):
id: int
patient_id: int
role: Role
data: Dict[str, Any]
created_at: datetime

class Config:
from_attributes = True

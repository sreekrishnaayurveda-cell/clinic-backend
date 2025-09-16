from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas

# ==== Patients ====

def create_patient(db: Session, payload: schemas.PatientCreate) -> models.Patient:
db_patient = models.Patient(
name=payload.name,
age=payload.age,
gender=payload.gender,
contact=payload.contact,
address=payload.address,
occupation=payload.occupation,
marital_status=payload.marital_status,
)
db.add(db_patient)
db.commit()
db.refresh(db_patient)
return db_patient


def get_patient(db: Session, patient_id: int) -> Optional[models.Patient]:
return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

# ==== Observations ====

def create_observation(db: Session, payload: schemas.ObservationCreate) -> models.Observation:
# Verify patient exists
patient = get_patient(db, payload.patient_id)
if not patient:
raise HTTPException(status_code=404, detail="Patient not found")

# Ensure data matches role schema
# Pydantic already validated, but we normalize to dict for storage
data_dict = payload.data.model_dump(exclude_none=True)

db_obs = models.Observation(
patient_id=payload.patient_id,
role=payload.role.value,
data=data_dict,
)
db.add(db_obs)
db.commit()
db.refresh(db_obs)
return db_obs


def get_observation(db: Session, obs_id: int) -> Optional[models.Observation]:
return db.query(models.Observation).filter(models.Observation.id == obs_id).first()


def reset_database(db: Session) -> None:
# Danger: deletes all rows (keeps tables)
db.query(models.Observation).delete()
db.query(models.Patient).delete()
db.commit()

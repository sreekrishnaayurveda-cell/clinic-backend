from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def create_observation(db: Session, obs: schemas.ObservationCreate):
    payload = obs.model_dump()
    if not payload.get("date_time"):
        payload["date_time"] = datetime.datetime.utcnow()
    db_obs = models.Observation(**payload)
    db.add(db_obs)
    db.commit()
    db.refresh(db_obs)
    return db_obs

def get_observation(db: Session, obs_id: int):
    return db.query(models.Observation).filter(models.Observation.id == obs_id).first()

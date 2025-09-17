from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


# -------------------- Patients --------------------
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


def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


# -------------------- Observations --------------------
def create_observation(db: Session, payload: schemas.ObservationCreate) -> models.Observation:
    patient = get_patient(db, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

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


def get_observation(db: Session, obs_id: int):
    return db.query(models.Observation).filter(models.Observation.id == obs_id).first()


def reset_database(db: Session):
    db.query(models.Observation).delete()
    db.query(models.Patient).delete()
    db.commit()

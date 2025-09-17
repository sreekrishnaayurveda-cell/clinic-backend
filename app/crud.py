from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


def create_patient(db: Session, payload: schemas.PatientCreate) -> models.Patient:
    """Create a new patient."""
    db_patient = models.Patient(**payload.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient(db: Session, patient_id: int):
    """Fetch patient by ID."""
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def create_observation(db: Session, payload: schemas.ObservationCreate) -> models.Observation:
    """Create an observation, validating data per role."""
    # ✅ Ensure patient exists
    patient = get_patient(db, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # ✅ Role-based validation
    data_dict = None
    if payload.role == schemas.Role.Nurse:
        try:
            obs = schemas.NurseObservation(**payload.data)
            data_dict = obs.model_dump(exclude_none=True)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid NurseObservation data: {str(e)}")

    elif payload.role == schemas.Role.Doctor:
        try:
            obs = schemas.DoctorObservation(**payload.data)
            data_dict = obs.model_dump(exclude_none=True)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid DoctorObservation data: {str(e)}")

    elif payload.role == schemas.Role.Therapist:
        try:
            obs = schemas.TherapistObservation(**payload.data)
            data_dict = obs.model_dump(exclude_none=True)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid TherapistObservation data: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    # ✅ Save to DB
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
    """Fetch observation by ID."""
    return db.query(models.Observation).filter(models.Observation.id == obs_id).first()


def reset_database(db: Session):
    """Delete all patients and observations (testing only)."""
    db.query(models.Observation).delete()
    db.query(models.Patient).delete()
    db.commit()

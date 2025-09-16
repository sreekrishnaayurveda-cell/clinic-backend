import os
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# -------------------------
# Load API Key from Environment
# -------------------------
API_KEY = os.getenv("API_KEY")


# -------------------------
# DB Session Dependency
# -------------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# API Key Auth Dependency
# -------------------------
def require_api_key(
    x_api_key: str = Header(None),
    authorization: str = Header(None)
):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: API_KEY not set"
        )

    expected = API_KEY.strip()

    # Option 1: X-API-Key header
    if x_api_key and x_api_key.strip() == expected:
        return True

    # Option 2: Authorization: Bearer <API_KEY>
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip()
        if token == expected:
            return True

    # If neither matched
    raise HTTPException(status_code=401, detail="Invalid or missing API key")


# -------------------------
# App Initialization
# -------------------------
app = FastAPI(
    title="Sreekrishna Ayurveda Clinic API",
    version="1.0.0",
    dependencies=[Depends(require_api_key)]  # enforce API key globally
)

# Enable CORS (open for dev, restrict origins later in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)


# -------------------------
# Public Routes
# -------------------------
@app.get("/health", dependencies=[])
def health():
    """Health check (no authentication required)."""
    return {"status": "ok"}


@app.get("/debug/echo", dependencies=[])
def echo(request: Request):
    """Echo back request headers (for debugging API key headers)."""
    return {"headers": dict(request.headers)}


# -------------------------
# Protected Routes
# -------------------------
@app.delete("/reset")
def reset_database(db: Session = Depends(get_db)):
    """
    Danger: Deletes all patients and observations.
    Only use this in testing/demo environments!
    """
    db.query(models.Observation).delete()
    db.query(models.Patient).delete()
    db.commit()
    return {"message": "All patients and observations deleted"}


# -------------------------
# Patients
# -------------------------
@app.post("/patients", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)


@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# -------------------------
# Observations
# -------------------------
@app.post("/observations", response_model=schemas.ObservationResponse)
def create_observation(obs: schemas.ObservationCreate, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, obs.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.create_observation(db, obs)


@app.get("/observations/{obs_id}", response_model=schemas.ObservationResponse)
def read_observation(obs_id: int, db: Session = Depends(get_db)):
    obs = crud.get_observation(db, obs_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return obs

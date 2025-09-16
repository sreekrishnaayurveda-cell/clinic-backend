import os
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

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
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_KEY not set")

    expected = API_KEY.strip()

    if x_api_key and x_api_key.strip() == expected:
        return True

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip()
        if token == expected:
            return True

    raise HTTPException(status_code=401, detail="Invalid or missing API key")


# -------------------------
# App Initialization
# -------------------------
app = FastAPI(
    title="Sreekrishna Ayurveda Clinic API",
    version="1.0.0",
    dependencies=[Depends(require_api_key)]  # global enforcement
)

# CORS (open for dev, restrict later)
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
# Public Routes (no auth)
# -------------------------
@app.get("/health", dependencies=[])
def health():
    """Health check (no authentication required)."""
    return {"status": "ok"}


@app.get("/debug/echo", dependencies=[])
def echo(request: Request):
    """Echo back request headers (no authentication required)."""
    return {"headers": dict(request.headers)}


# -------------------------
# Protected Routes
# -------------------------
@app.delete("/reset")
def reset_database(db: Session = Depends(get_db)):
    db.query(models.Observation).delete()
    db.query(models.Patient).delete()
    db.commit()
    return {"message": "All patients and observations deleted"}


@app.post("/patients", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)


@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


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

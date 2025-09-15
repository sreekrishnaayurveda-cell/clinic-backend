import os
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Sreekrishna Ayurveda API", version="1.0.0")

# Basic CORS (Actions are server-to-server, but keeping open for flexibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (simple approach for prototype)
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_api_key(
    x_api_key: str = Header(None),
    authorization: str = Header(None)
):
    """
    Accepts either:
      - X-API-Key: <API_KEY>
      - Authorization: Bearer <API_KEY>
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_KEY not set")

    # Check X-API-Key header
    if x_api_key and x_api_key.strip() == API_KEY.strip():
        return True

    # Check Authorization: Bearer header
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "").strip()
        if token == API_KEY.strip():
            return True

    # If neither matched
    raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug/echo")
def echo(request: Request):
    """
    Debug endpoint: returns all request headers
    """
    return {"headers": dict(request.headers)}

@app.post("/patients", response_model=schemas.PatientResponse, dependencies=[Depends(require_api_key)])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse, dependencies=[Depends(require_api_key)])
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/observations", response_model=schemas.ObservationResponse, dependencies=[Depends(require_api_key)])
def create_observation(obs: schemas.ObservationCreate, db: Session = Depends(get_db)):
    # Optional: validate patient exists
    patient = crud.get_patient(db, obs.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.create_observation(db, obs)

@app.get("/observations/{obs_id}", response_model=schemas.ObservationResponse, dependencies=[Depends(require_api_key)])
def read_observation(obs_id: int, db: Session = Depends(get_db)):
    obs = crud.get_observation(db, obs_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return obs

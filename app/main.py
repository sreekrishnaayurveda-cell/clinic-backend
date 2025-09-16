import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import Base, engine, SessionLocal
from .security import require_api_key

# -------------------- App Setup --------------------
app = FastAPI(
    title="Sreekrishna Ayurveda Clinic API",
    version="1.0.0",
    description="Internal API for patient registration, vitals recording, "
                "clinical observations, and therapy documentation at "
                "Sreekrishna Ayurveda Clinic.",
)

# Enable CORS (open for now; restrict later in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically on startup (simple dev approach)
Base.metadata.create_all(bind=engine)

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- System & Debug --------------------
@app.get("/health")
async def health():
    """Check API health."""
    return {"status": "ok"}

@app.get("/debug/echo")
async def debug_echo(request: Request):
    """Echo headers back (useful for debugging API key issues)."""
    return {"headers": {k: v for k, v in request.headers.items()}}

@app.delete("/reset", dependencies=[Depends(require_api_key)])
async def reset(db: Session = Depends(get_db)):
    """Delete all patients and observations (testing only)."""
    crud.reset_database(db)
    return {"detail": "Database reset"}

# -------------------- Patients --------------------
@app.post("/patients",
          response_model=schemas.PatientOut,
          dependencies=[Depends(require_api_key)])
async def create_patient(payload: schemas.PatientCreate,
                         db: Session = Depends(get_db)):
    return crud.create_patient(db, payload)

@app.get("/patients/{patient_id}",
         response_model=schemas.PatientOut,
         dependencies=[Depends(require_api_key)])
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# -------------------- Observations --------------------
@app.post("/observations",
          response_model=schemas.ObservationOut,
          dependencies=[Depends(require_api_key)])
async def create_observation(payload: schemas.ObservationCreate,
                             db: Session = Depends(get_db)):
    obs = crud.create_observation(db, payload)
    return schemas.ObservationOut(
        id=obs.id,
        patient_id=obs.patient_id,
        role=obs.role,
        data=obs.data,
        created_at=obs.created_at,
    )

@app.get("/observations/{obs_id}",
         response_model=schemas.ObservationOut,
         dependencies=[Depends(require_api_key)])
async def get_observation(obs_id: int, db: Session = Depends(get_db)):
    obs = crud.get_observation(db, obs_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return schemas.ObservationOut(
        id=obs.id,
        patient_id=obs.patient_id,
        role=obs.role,
        data=obs.data,
        created_at=obs.created_at,
    )

# -------------------- Entrypoint --------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

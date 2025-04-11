# from fastapi import FastAPI,Depends
# from fastapi.middleware.cors import CORSMiddleware

# from routes import model_routes
# import asyncio

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# app.include_router(model_routes.router, prefix= "/prediction")

# if __name__ == "__main__":
#     import uvicorn
#     from watchgod import watch
#     uvicorn.run("main:app", host = "127.0.0.1", port = 8000,reload=True, workers=2)

    # --------------------

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from routes import model_routes  # Assuming your prediction routes are in model_routes

# Create all models in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for patient and CBC report validation
from pydantic import BaseModel
from typing import List

class PatientCreate(BaseModel):
    name: str
    contact: str
    next_appointment: str

class CBCReportCreate(BaseModel):
    patient_id: int
    rbc: float
    hgb: float
    wbc: float
    plt: float
    neutp: float

# Route to create a new patient
@app.post("/patients/")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(
        name=patient.name,
        contact=patient.contact,
        next_appointment=patient.next_appointment
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# Route to get all patients
@app.get("/patients/", response_model=List[PatientCreate])
def get_patients(db: Session = Depends(get_db)):
    print(db.query(models.Patient).all())
    return db.query(models.Patient).all()

@app.get("/patients/{id}")
async def get_patient(id, db:Session=Depends(get_db)):
    print(db.query(models.Patient).get(id))
    return db.query(models.Patient).get(id)

# Route to create a CBC report
@app.post("/cbc-reports/")
def create_cbc_report(report: CBCReportCreate, db: Session = Depends(get_db)):
    new_report = models.CBCReport(**report.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

# Route to get all CBC reports
@app.get("/cbc-reports/")
def get_cbc_reports(db: Session = Depends(get_db)):
    return db.query(models.CBCReport).all()

# Prediction routes included from model_routes
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Include the routes for predictions (you mentioned these are in model_routes)
app.include_router(model_routes.router, prefix="/prediction")

# If running the app directly
if __name__ == "__main__":
    import uvicorn
    from watchgod import watch
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=2)

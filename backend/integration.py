
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import CBCReport, Patient
from services.model_services import ModelService

app = FastAPI()
model_service = ModelService()

@app.get("/predict/{patient_id}")
def predict(patient_id: int, db: Session = Depends(get_db)):
    # Get the latest CBC report for the patient
    report = db.query(CBCReport).filter(CBCReport.patient_id == patient_id).order_by(CBCReport.uploaded_at.desc()).first()

    if not report:
        return {"error": "No CBC report found for this patient"}

    # Prepare data for the model
    data = {
        "RBC": report.rbc,
        "WBC": report.wbc,
        "HGB": report.hgb,
        "PLT": report.plt,
        "NEUTp": report.neutp,
    }

    # Get predictions
    pkl_prediction = model_service.predict_with_pkl(data)
    h5_prediction = model_service.predict_with_h5(data)

    return {
        "patient_id": patient_id,
        "pkl_prediction": pkl_prediction,
        "h5_prediction": h5_prediction,
    }

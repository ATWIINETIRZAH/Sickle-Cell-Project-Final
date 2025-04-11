from fastapi import APIRouter, Depends
from services.model_services import ModelService

router = APIRouter()
model_service = ModelService()

@router.post("/predict-pkl")
async def predict_with_pkl_model(data: dict):
    result = model_service.predict_with_pkl(data)
    return {"prediction": result}

@router.post("/predict-h5")
async def predict_with_h5_model(data: dict):
    result = model_service.predict_with_h5(data)
    return {"prediction": result}
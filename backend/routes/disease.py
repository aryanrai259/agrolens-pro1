from fastapi import APIRouter, UploadFile, File
from model.leaf_predict import predict_leaf_disease

router = APIRouter()

@router.post("/api/predict-disease")
async def predict_disease(file: UploadFile = File(...)):
    prediction, confidence = predict_leaf_disease(file.filename)

    remedies = {
        "Tomato_Healthy": "No action needed. Your plant is healthy.",
        "Tomato_Bacterial_spot": "Use copper-based fungicides. Avoid overhead watering.",
        "Tomato_Early_blight": "Apply fungicides. Improve drainage and remove infected leaves.",
        "Tomato_Leaf_Mold": "Improve air circulation. Use sulfur-based spray.",
        "Tomato_Late_blight": "Remove infected leaves and apply anti-blight spray."
    }

    return {
        "prediction": prediction,
        "confidence": confidence,
        "remedy": remedies[prediction]
    }

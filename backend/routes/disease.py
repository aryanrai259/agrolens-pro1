from fastapi import APIRouter, UploadFile, File
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("PLANT_ID_API_KEY:", os.getenv("PLANT_ID_API_KEY"))


router = APIRouter()

API_KEY = os.getenv("PLANT_ID_API_KEY")
PLANT_ID_URL = "https://plant.id/api/v3/identification"

@router.post("/api/predict-disease")
async def predict_disease(file: UploadFile = File(...)):
    if not API_KEY:
        return {"error": "API key missing. Set PLANT_ID_API_KEY in your .env file."}

    image_bytes = await file.read()
    files = {"images": (file.filename, image_bytes, file.content_type)}
    headers = {"Api-Key": API_KEY}

    # Request health assessment too
    data = {
        "health": "all"  # You can use "all" or "only" per your use case
    }

    try:
        # Plant.id expects JSON data for fields except images, so use data as a separate arg
        response = requests.post(PLANT_ID_URL, headers=headers, files=files, data=data, timeout=40)
    except Exception as e:
        return {"error": f"Failed to connect to Plant.id API: {e}"}

    print("Plant.id API status:", response.status_code)
    print("Plant.id API response:", response.text)

    if response.status_code not in (200, 201):
        return {
            "predicted_class": "Unknown",
            "confidence": "0%",
            "remedy": "Could not connect to Plant.id API.",
            "status_code": response.status_code,
            "api_response": response.text
        }

    # Parse response
    result = response.json().get("result", {})

    # 1. Check if a plant is found at all
    if not result.get("is_plant", False):
        return {
            "predicted_class": "Not a plant",
            "confidence": "0%",
            "remedy": "No plant detected in the image."
        }

    # 2. Health assessment
    is_healthy = result.get("is_healthy", None)
    if is_healthy is True:
        return {
            "predicted_class": "Healthy",
            "confidence": "100%",
            "remedy": "No action needed. Your plant is healthy."
        }
    elif is_healthy is False:
        # If diseases are detected
        diseases = result.get("disease", {}).get("suggestions", [])
        if diseases:
            top = diseases[0]
            remedy = None
            # Plant.id v3: treatment is a dict, so get the "prevention" or "treatment" if present
            treatment = top.get("treatment", {})
            if "prevention" in treatment:
                remedy = treatment["prevention"]
            elif "treatment" in treatment:
                remedy = treatment["treatment"]
            else:
                remedy = "No remedy provided."

            return {
                "predicted_class": top.get("name", "Unknown Disease"),
                "confidence": f"{top.get('probability', 0)*100:.1f}%",
                "remedy": remedy
            }
        else:
            return {
                "predicted_class": "Diseased",
                "confidence": "0%",
                "remedy": "Plant appears diseased, but no specific disease detected."
            }

    # 3. If health not present, fallback to classification
    suggestions = result.get("classification", {}).get("suggestions", [])
    if suggestions:
        top = suggestions[0]
        return {
            "predicted_class": top.get("name", "Unknown"),
            "confidence": f"{top.get('probability', 0)*100:.1f}%",
            "remedy": "No health assessment available, but this is the predicted plant."
        }

    return {
        "predicted_class": "Unknown",
        "confidence": "0%",
        "remedy": "No useful response from Plant.id API.",
        "raw_result": result
    }

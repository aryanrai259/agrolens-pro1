import requests
import os

API_KEY = os.getenv("KINDWISE_API_KEY")  # Store your API key in .env

def predict_leaf_disease(image_path: str):
    url = "https://api.plant.id/v2/health_assessment"

    with open(image_path, "rb") as image_file:
        files = {
            "images": (image_path, image_file, "image/jpeg")
        }
        headers = {
            "Api-Key": API_KEY
        }
        response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return {
            "predicted_class": "Unknown",
            "confidence": "0%",
            "remedy": "Could not connect to Kindwise API."
        }

    data = response.json()
    if data.get("is_healthy"):
        return {
            "predicted_class": "Healthy",
            "confidence": "100%",
            "remedy": "No action needed."
        }

    top = data["diseases"][0]
    return {
        "predicted_class": top["name"],
        "confidence": f"{top['probability']*100:.1f}%",
        "remedy": top.get("treatment", "No remedy provided.")
    }

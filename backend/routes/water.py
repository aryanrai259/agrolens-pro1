from fastapi import APIRouter
from backend.utils.weather import is_rain_expected
import backend.state.data_store as store  # ✅ shared state

router = APIRouter()

@router.get("/api/should-water")
def should_water():
    print("🔍 latest_data in should-water route:", store.latest_data)
    print("🧠 Memory ID in water.py:", id(store.latest_data))
    
    if store.latest_data is None:
        return {"message": "No sensor data received yet"}

    rain_expected = is_rain_expected()
    moisture = store.latest_data.moisture

    if moisture < 40 and not rain_expected:
        return {
            "should_water": True,
            "reason": "Soil is dry and no rain expected. You should water."
        }
    elif rain_expected:
        return {
            "should_water": False,
            "reason": "Rain is expected soon. Skip watering."
        }
    else:
        return {
            "should_water": False,
            "reason": f"Soil moisture is {moisture}%. No need to water."
        }

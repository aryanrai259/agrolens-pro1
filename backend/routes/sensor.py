from fastapi import APIRouter
from backend.state.data_store import latest_data, SensorData

router = APIRouter()

@router.post("/api/sensor-data")
def receive_sensor_data(data: SensorData):
    print("📥 Sensor data received and stored:", data)
    print("🧠 Memory ID in sensor.py:", id(data))
    # Update the shared object directly
    import backend.state.data_store as store
    store.latest_data = data
    return {"message": "Sensor data received successfully"}

@router.get("/api/sensor-data")
def get_sensor_data():
    import backend.state.data_store as store
    if store.latest_data is None:
        return {"message": "No sensor data received yet"}
    return store.latest_data

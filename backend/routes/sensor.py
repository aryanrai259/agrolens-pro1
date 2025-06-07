from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Define the expected sensor data format
class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    moisture: float
    ph: float

# In-memory storage (latest value only)
latest_data: Optional[SensorData] = None

# POST route to receive data from ESP8266
@router.post("/api/sensor-data")
def receive_sensor_data(data: SensorData):
    global latest_data
    latest_data = data
    return {"message": "Sensor data received successfully"}

# GET route to return latest data to frontend
@router.get("/api/sensor-data")
def get_sensor_data():
    if latest_data is None:
        return {"message": "No sensor data received yet"}
    return latest_data


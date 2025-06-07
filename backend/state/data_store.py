from typing import Optional
from pydantic import BaseModel

class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    moisture: float
    ph: float

latest_data: Optional[SensorData] = None

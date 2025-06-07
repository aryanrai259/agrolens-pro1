import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")

def is_rain_expected():
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    res = requests.get(url).json()

    # Look at forecast for the next 6 hours (2 intervals)
    try:
        next_6_hours = res["list"][:2]  # 3-hour intervals
        for entry in next_6_hours:
            if "rain" in entry:
                return True
        return False
    except:
        return False  # Fail-safe

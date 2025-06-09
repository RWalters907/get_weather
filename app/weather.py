import requests
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_by_zip(zip_code, country_code="us"):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not found")

    print(f"Fetching weather for zip code: {zip_code}")
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={API_KEY}&units=imperial"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        print(f"Current weather in {zip_code}: {temp}°F, {description}")
        return temp, description
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

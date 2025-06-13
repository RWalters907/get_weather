import httpx
from fastapi import HTTPException
from app.config import OPENWEATHER_API_KEY

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

async def get_weather_by_zip(zip_code: str):
    params = {
        "zip": f"{zip_code},US",
        "appid": OPENWEATHER_API_KEY,
        "units": "imperial"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(BASE_CURRENT_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "zip": zip_code,
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "pressure": data["main"]["pressure"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
            }

    except httpx.HTTPStatusError as exc:
        print(f"[HTTP Error] Zip: {zip_code}, Status: {exc.response.status_code}, Detail: {exc.response.text}")
        return {
            "zip": zip_code,
            "error": f"API error: {exc.response.status_code}"
        }

    except httpx.RequestError as exc:
        print(f"[Request Error] An error occurred while requesting {exc.request.url!r}: {exc}")
        return {
            "zip": zip_code,
            "error": "Network error contacting weather service"
        }

    except Exception as e:
        print(f"[Unhandled Error] Zip: {zip_code}, Error: {e}")
        return {
            "zip": zip_code,
            "error": "Unexpected error occurred"
        }


async def get_forecast_by_zip(zip_code: str):
    params = {
        "zip": f"{zip_code},US",
        "appid": OPENWEATHER_API_KEY,
        "units": "imperial"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(BASE_FORECAST_URL, params=params)
            response.raise_for_status()
            data = response.json()
            # The "list" contains 3-hour forecast data points, 40 entries (5 days)
            return {
                "zip": zip_code,
                "forecast_list": data["list"]  # We will parse this later in the route/template
            }

    except httpx.HTTPStatusError as exc:
        print(f"[HTTP Error] Forecast Zip: {zip_code}, Status: {exc.response.status_code}, Detail: {exc.response.text}")
        return {
            "zip": zip_code,
            "error": f"API error: {exc.response.status_code}"
        }

    except httpx.RequestError as exc:
        print(f"[Request Error] Forecast An error occurred while requesting {exc.request.url!r}: {exc}")
        return {
            "zip": zip_code,
            "error": "Network error contacting weather service"
        }

    except Exception as e:
        print(f"[Unhandled Error] Forecast Zip: {zip_code}, Error: {e}")
        return {
            "zip": zip_code,
            "error": "Unexpected error occurred"
        }

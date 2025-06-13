from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from pathlib import Path
from .config import ZIP_CODES_BY_DAY
from .weather import get_weather_by_zip, get_forecast_by_zip
import asyncio

router = APIRouter()

# Absolute path to templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def summarize_forecast(forecast_list):
    """Summarize the 3-day forecast from 3-hour interval data."""
    # Group forecast items by date (YYYY-MM-DD)
    days = {}
    now = datetime.now()

    for entry in forecast_list:
        dt_txt = entry["dt_txt"]  # format "YYYY-MM-DD HH:MM:SS"
        date_str = dt_txt.split(" ")[0]

        # Only include next 3 full days after today
        forecast_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if forecast_date <= now.date():
            continue

        if (forecast_date - now.date()).days > 3:
            continue

        if date_str not in days:
            days[date_str] = {
                "temps": [],
                "descriptions": [],
                "icons": []
            }
        days[date_str]["temps"].append(entry["main"]["temp"])
        days[date_str]["descriptions"].append(entry["weather"][0]["description"].title())
        days[date_str]["icons"].append(entry["weather"][0]["icon"])

    # Summarize each day: high, low, main weather (most common description & icon)
    summary = []
    for date_str, info in days.items():
        high = max(info["temps"])
        low = min(info["temps"])

        # Get most common description and icon
        desc = max(set(info["descriptions"]), key=info["descriptions"].count)
        icon = max(set(info["icons"]), key=info["icons"].count)

        summary.append({
            "date": date_str,
            "high": high,
            "low": low,
            "description": desc,
            "icon": icon
        })

    return summary


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Initial page load, no weather data yet
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": None,
        "weather_data": None
    })


@router.post("/", response_class=HTMLResponse)
async def get_weather_today(request: Request):
    today = datetime.now().strftime("%A")
    zips_today = ZIP_CODES_BY_DAY.get(today, [])

    if not zips_today:
        if today in ["Saturday", "Sunday"]:
            message = "No Pools. Hope you are having a great weekend!"
        else:
            message = "No Pools Today. Enjoy your day off!"
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": message,
            "weather_data": None
        })

    weather_data = []

    # Fetch current weather and forecast concurrently per zip
    async def fetch_zip(zip_code):
        current = await get_weather_by_zip(zip_code)
        forecast = await get_forecast_by_zip(zip_code)
        if "error" in current or "error" in forecast:
            return {"zip": zip_code, "error": current.get("error") or forecast.get("error")}

        forecast_summary = summarize_forecast(forecast["forecast_list"])

        return {
            "zip": zip_code,
            "current": current,
            "forecast": forecast_summary
        }

    tasks = [fetch_zip(zip_code) for zip_code in zips_today]
    weather_data = await asyncio.gather(*tasks)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"Weather for {today}",
        "weather_data": weather_data
    })

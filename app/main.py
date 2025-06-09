from fastapi import FastAPI, HTTPException
from app.weather import get_weather_by_zip
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

class ZipCodeRequest(BaseModel):
    zip_codes: List[str]

@app.post("/weather")
async def get_weather(request: ZipCodeRequest):
    results = []
    for zip_code in request.zip_codes:
        try:
            temp, description = get_weather_by_zip(zip_code)
            results.append({
                "zip_code": zip_code,
                "temperature": temp,
                "description": description
            })
        except HTTPException as e:
            results.append({
                "zip_code": zip_code,
                "error": str(e.detail)
            })
    return {"weather_data": results}

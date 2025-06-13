from dotenv import load_dotenv
import os

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if OPENWEATHER_API_KEY is None:
    print("⚠️ OPENWEATHER_API_KEY not loaded. Check your .env file and environment.")
else:
    print("✅ OPENWEATHER_API_KEY loaded successfully.")

# ✅ This is the part that was missing
ZIP_CODES_BY_DAY = {
    "Monday": [],
    "Tuesday": ["85029", "85051", "85304", "85306", "85308", "85310"],
    "Wednesday": ["85381"],
    "Thursday": ["85374", "85375"],
    "Friday": [],
    "Saturday": [],
    "Sunday": []
}

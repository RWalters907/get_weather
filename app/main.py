from fastapi import FastAPI
from app.routes import router  # Import the router from routes.py

app = FastAPI()

# Include routes from routes.py
app.include_router(router)

from config import get_settings
from fastapi import FastAPI
from fraud_detection.api.routes import router

settings = get_settings()

app = FastAPI(title="Training Service")

app.include_router(router)

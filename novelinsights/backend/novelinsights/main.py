# novelinsights/backend/novelinsights/main.py

from dotenv import load_dotenv
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from novelinsights.api.routes import router as api_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Novel Insights")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],  # Get from env or use default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
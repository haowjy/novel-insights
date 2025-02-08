# novelinsights/backend/novelinsights/api/routes.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to Novel Insights API"}

@router.get("/test")
async def test():
    return {"message": "Test route"}

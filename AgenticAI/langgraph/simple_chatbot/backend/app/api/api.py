from app.api.endpoints import health, search
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(search.router, tags=["search"])

from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from .user import router as user_router

api_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(verify_api_key)]
)

api_router.include_router(user_router, prefix="/user", tags=["user"])

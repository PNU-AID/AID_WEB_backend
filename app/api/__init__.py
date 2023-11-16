from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.study import router as study_router
from app.api.user import router as user_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(study_router, prefix="/study", tags=["Study"])

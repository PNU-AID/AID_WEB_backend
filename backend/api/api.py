from fastapi import APIRouter

from .endpoint import auth_router, submit_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(submit_router, prefix="/submit", tags=["submit"])

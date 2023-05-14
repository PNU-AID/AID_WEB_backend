from fastapi import APIRouter

from .endpoint import admin_router, auth_router, submit_router

api_router = APIRouter()  # API ROUTER를 선언해준다


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(submit_router, prefix="/submit", tags=["submit"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])

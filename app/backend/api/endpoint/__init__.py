from backend.api.endpoint.admin import router as admin_router  # noqa
from backend.api.endpoint.auth import router as auth_router  # noqa
from backend.api.endpoint.sender import router as sender_router  # noqa
from backend.api.endpoint.submit import router as submit_router  # noqa
from fastapi import APIRouter

api_router = APIRouter()  # API ROUTER를 선언해준다

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(submit_router, prefix="/submit", tags=["submit"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(sender_router, prefix="/sender", tags=["sender"])

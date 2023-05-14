from fastapi import APIRouter

from .admin import router as admin_router  # noqa
from .auth import router as auth_router  # noqa
from .submit import router as submit_router  # noqa

api_router = APIRouter()  # API ROUTER를 선언해준다

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(submit_router, prefix="/submit", tags=["submit"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])

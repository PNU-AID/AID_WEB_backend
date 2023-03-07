from fastapi import APIRouter

from .api_test import test_router
from .endpoint import auth_router

api_router = APIRouter()

api_router.include_router(test_router, prefix="/test", tags=["test"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

from fastapi import APIRouter

from .api_test import test_router

api_router = APIRouter()

api_router.include_router(test_router, prefix="/test", tags=["test"])

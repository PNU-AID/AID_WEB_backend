from backend.api.v1 import (
    admin_router,
    auth_router,
    question_board_router,
    sender_router,
    study_board_router,
    submit_router,
)
from fastapi import APIRouter

api_router = APIRouter()  # API ROUTER를 선언해준다


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(submit_router, prefix="/submit", tags=["submit"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(sender_router, prefix="/sender", tags=["sender"])
api_router.include_router(question_board_router, prefix="/question_board", tags=["question_board"])
api_router.include_router(study_board_router, prefix="/study_board", tags=["study_board"])

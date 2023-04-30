from fastapi import APIRouter

from .endpoint import admin_router, auth_router, submit_router

api_router = APIRouter()  # API ROUTER를 선언해준다

api_router.include_router(
    auth_router, prefix="/auth", tags=["auth"]
)  # api_router.include_router()를 통해 각 APIRouter를 메인 FastAPI 애플리케이션에 더할 수  있다.
api_router.include_router(
    submit_router, prefix="/submit", tags=["submit"]
)  # include_router를 통해 api의 prefix,태그지정을 할 수 있음.


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(submit_router, prefix="/submit", tags=["submit"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])

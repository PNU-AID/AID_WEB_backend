from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.api import api_router
from app.core import settings
from app.database.mongodb import initiate_database

app = FastAPI(
    title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, docs_url=None, redoc_url=None, openapi_url=None
)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")


@app.get("/api/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/api/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.on_event("startup")  # 서버 실행시
async def startup():
    await initiate_database()


# @app.on_event("shutdown")
# async def shutdown():
#     db_manager.close_db_connection()

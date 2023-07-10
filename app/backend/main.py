from backend.api import api_router
from backend.core import logger
from backend.database import db_manager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None, redoc_url=None)

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


@app.on_event("startup")  # 서버 실행시
async def startup():
    logger.add_logger("db_log", "db_log")
    logger.add_logger("server_log", "server_log")

    await db_manager.connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await db_manager.close_db_connection()

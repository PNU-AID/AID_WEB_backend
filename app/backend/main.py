from backend.api import api_router
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


app.include_router(
    api_router, prefix="/api"
)  # 여기서 api_router는 ./api/endpoint/api.py에 있는 api_router변수로, submit, auth api가 include돼있다.


# @app.on_event("startup")  # 서버 실행시
# def start():
# make_dummy_submit()
# make_super_user()


# @app.on_event("shutdown")
# def finish():
#     delete_dummy_submit()
#     delete_super_user()

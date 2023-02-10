import uvicorn
from fastapi import FastAPI

from .api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def start():
    # TODO
    # DB 연결
    # client = MongoClient(
    #     "mongodb://admin_user:password@localhost:27017/?authMechanism=DEFAULT"
    # )
    # db = client["submit"]
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

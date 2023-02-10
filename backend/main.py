import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test():
    return {"message": "test"}


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

import uvicorn
from database.mongodb import db
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test():
    print(db["user"].find_one())
    return {"message": "test"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

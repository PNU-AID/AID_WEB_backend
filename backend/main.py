import uvicorn
from api import api_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def start():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

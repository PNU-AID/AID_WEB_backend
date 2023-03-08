import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api import api_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates/css"), name="static")
template = Jinja2Templates(directory="templates")  # terminal 기준 path

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def start():
    pass


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return template.TemplateResponse("home.html", context={"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

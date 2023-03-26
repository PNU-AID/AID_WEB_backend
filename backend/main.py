import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api import api_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates"), name="static")
template = Jinja2Templates(directory="templates")  # terminal 기준 path

app.include_router(api_router, prefix="")


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request, msg: str = None):
    return template.TemplateResponse("home.html", context={"request": request, "msg": msg})


@app.on_event("startup")
def start():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

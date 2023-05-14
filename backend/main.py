import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api import api_router
from .utils import delete_dummy_submit, make_dummy_submit

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates"), name="static")

template = Jinja2Templates(directory="templates")  # terminal 기준 path


app.include_router(
    api_router, prefix=""
)  # 여기서 api_router는 ./api/endpoint/api.py에 있는 api_router변수로, submit, auth api가 include돼있다.


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request, msg: str = None):
    return template.TemplateResponse("home.html", context={"request": request, "msg": msg})


@app.on_event("startup")  # 서버 실행시
def start():
    make_dummy_submit()


@app.on_event("shutdown")
def finish():
    delete_dummy_submit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

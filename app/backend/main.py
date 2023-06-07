from backend.api import api_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

app.mount("/static", StaticFiles(directory="templates"), name="static")

template = Jinja2Templates(directory="templates")  # terminal 기준 path


app.include_router(
    api_router, prefix=""
)  # 여기서 api_router는 ./api/endpoint/api.py에 있는 api_router변수로, submit, auth api가 include돼있다.


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request, msg: str = None):
    return template.TemplateResponse("home.html", context={"request": request, "msg": msg})


@app.get("/faq", response_class=HTMLResponse)
def faq_page(request: Request):
    return template.TemplateResponse("faq.html", context={"request": request})


# @app.on_event("startup")  # 서버 실행시
# def start():
# make_dummy_submit()
# make_super_user()


# @app.on_event("shutdown")
# def finish():
#     delete_dummy_submit()
#     delete_super_user()

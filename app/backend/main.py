from typing import Any

import jinja2
from backend.api import api_router
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(docs_url=None, redoc_url=None)

origins = [
    "*",
]

whitelist_ip = ["180.182.223.158", "211.203.66.57", "118.218.116.166", "59.22.85.34"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@jinja2.pass_context
def url_for(context: dict, name: str, **path_params: Any) -> str:
    request = context["request"]
    http_url = request.url_for(name, **path_params)
    if request.url.scheme == "https" or "x-forwarded-for" in request.headers.keys():
        return str(http_url).replace("http", "https", 1)
    else:
        return str(http_url)


@app.middleware("http")
async def ip_check(request: Request, call_next):
    path = request.scope["path"]
    ip = request.headers.get("X-Forwarded-For").split(", ")[0]
    if "admin" in path:
        if ip not in whitelist_ip:
            data = {"message": "you are not allowed to access this resource"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
    response = await call_next(request)
    return response


app.mount("/static", StaticFiles(directory="templates"), name="static")

template = Jinja2Templates(directory="templates")  # terminal 기준 path
template.env.globals["url_for"] = url_for


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

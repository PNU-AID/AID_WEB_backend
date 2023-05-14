from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.crud.submit import read_all_submit, read_submit

router = APIRouter()

template = Jinja2Templates(directory="templates")  # terminal 기준 path


# 로그인 화면
@router.get("", response_class=HTMLResponse)
def login_page(request: Request):
    return template.TemplateResponse("login.html", context={"request": request})


@router.post("", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "password":
        return submission_list_page(request)
    else:
        return template.TemplateResponse("login.html", context={"request": request, "message": "잘못된 ID입니다."})


@router.get("", response_class=HTMLResponse)
def submission_list_page(request: Request):
    """admin 페이지 반환"""

    all_data = read_all_submit()
    # TODO

    return template.TemplateResponse("submission_list.html", context={"request": request, "submission": all_data})


@router.get("/detail", response_class=HTMLResponse)
def submission_detail_page(request: Request, submit_id: str):
    submit_info = read_submit(submit_id)
    print(submit_info)
    return template.TemplateResponse(
        "submission_detail.html",
        context={"request": request, "submit_info": submit_info},
    )

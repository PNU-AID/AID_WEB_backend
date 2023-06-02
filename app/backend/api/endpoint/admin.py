from math import ceil

from backend.crud.submit import (
    get_count,
    read_all_submit,
    read_submit,
    update_is_pass,
)
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

template = Jinja2Templates(directory="templates")  # terminal 기준 path

"""
# 로그인 화면
@router.get("", response_class=HTMLResponse)
def login_page(request: Request):
    return template.TemplateResponse("login.html", context={"request": request})


@router.post("", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = db["user"].find_one({"username": "admin"})
    if username == "admin" and user["password"] == password:
        all_data = read_all_submit()
        return template.TemplateResponse("submission_list.html", context={"request": request, "submission": all_data})
    else:
        return template.TemplateResponse("login.html", context={"request": request, "message": "잘못된 ID입니다."})
"""


@router.get("", response_class=HTMLResponse)
def submission_list_page(request: Request, submit_page: int = 1):
    """admin 페이지 반환"""

    limit = 10
    interval = 2
    data_cnt = get_count()
    last_page = ceil(data_cnt / limit)

    all_data = read_all_submit()

    offset = (submit_page - 1) * limit
    selected = all_data.limit(limit).skip(offset)
    first_idx = 1 if submit_page <= 1 + interval else submit_page - interval
    last_idx = last_page if last_page <= submit_page + interval else submit_page + interval
    return template.TemplateResponse(
        "submission_list.html",
        context={
            "request": request,
            "submission": selected,
            "first_idx": first_idx,
            "last_idx": last_idx,
            "cur_page": submit_page,
            "data_cnt": data_cnt,
        },
    )


@router.get("/detail", response_class=HTMLResponse)
def submission_detail_page(request: Request, submit_id: str):
    submit_info = read_submit(submit_id)
    return template.TemplateResponse(
        "submission_detail.html",
        context={"request": request, "submit_info": submit_info},
    )


@router.post("/change_status")
async def change_pass_status(request: Request):
    data = await request.form()
    is_pass = True if data["is_pass"] == "pass" else False
    submit_id = data["submit_id"]
    update_is_pass(submit_id, is_pass)
    redirect_url = f"/admin/detail?submit_id={submit_id}"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

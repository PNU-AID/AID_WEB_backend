from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.crud.submit import read_all_submit, read_submit
from backend.database import db

router = APIRouter()

template = Jinja2Templates(directory="templates")  # terminal 기준 path


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


@router.get("/detail", response_class=HTMLResponse)
def submission_detail_page(request: Request, submit_id: str):
    submit_info = read_submit(submit_id)
    return template.TemplateResponse(
        "submission_detail.html",
        context={"request": request, "submit_info": submit_info},
    )


# TODO 합격 불합격 체크리스트 api만들기
@router.post("/change_status")
async def change_status(request: Request, submit_id: str):
    test_val = await request.form()
    print(test_val)

    return {"message": "test"}

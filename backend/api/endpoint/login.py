from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # templates 디렉토리 경로 설정


@router.get("", response_class=HTMLResponse)
def login_page(request: Request):
    """로그인 페이지 반환"""
    return templates.TemplateResponse("login.html", {"request": request})

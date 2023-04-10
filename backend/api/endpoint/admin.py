from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

template = Jinja2Templates(directory="templates")  # terminal 기준 path


@router.get("", response_class=HTMLResponse)
def admin_page(request: Request):
    """admin 페이지 반환"""

    # TODO
    # 모든 내용 가져오기
    return template.TemplateResponse("admin.html", context={"request": request})

from fastapi import APIRouter, Request, responses, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.crud import create_submit
from backend.scheme.submit import SubmitForm

##submit에 관한 api를 담은 코드

router = APIRouter() #submit ROUTER 를 선언해준다. 

template = Jinja2Templates(directory="templates")  # terminal 기준 path 


@router.get("", response_class=HTMLResponse) #get request (http request)
def submit_page(request: Request):
    """submit 페이지 반환"""
    return template.TemplateResponse("submit.html", context={"request": request})


@router.post("") #post request(http request)
async def submit(request: Request):
    """form받고 필수항목 작성 완료시 homt으로 redirect, 그렇지 않으면 기존 내용 유지하며 submit 페이지 반환"""
    form = SubmitForm(request)
    await form.load_data()

    if form.is_valid(): #form이 valid 하면 
        create_submit(form.send_data()) #crud폴더의 create_submit 함수 
        return responses.RedirectResponse("/?msg=success", status_code=status.HTTP_302_FOUND) #

    return template.TemplateResponse("submit.html", context=form.__dict__) #jinja template을 return

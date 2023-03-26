from fastapi import APIRouter, Request, responses, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.crud import create_submit
from backend.scheme.submit import SubmitForm

router = APIRouter()

template = Jinja2Templates(directory="templates")  # terminal 기준 path


@router.get("", response_class=HTMLResponse)
def submit_page(request: Request):
    return template.TemplateResponse("submit.html", context={"request": request})


@router.post("")
async def submit(request: Request):
    form = SubmitForm(request)
    await form.load_data()

    if form.is_valid():
        create_submit(form.send_data())
        return responses.RedirectResponse("/?msg=success", status_code=status.HTTP_302_FOUND)

    return template.TemplateResponse("submit.html", context=form.__dict__)

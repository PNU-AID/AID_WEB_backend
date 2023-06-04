import smtplib
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from fastapi import APIRouter, Request, status, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.crud.user import read_all_is_pass_email
from backend.core import settings

router = APIRouter()

template = Jinja2Templates(directory="templates")  # terminal 기준 path


@router.get("", response_class=HTMLResponse)
def sender_page(request: Request):
    return template.TemplateResponse("sender.html", context={"request": request})


@router.post("/send_email")
async def sender(request: Request, background_tasks: BackgroundTasks):
    # SMTP 서버를 dictionary로 정의
    smtp_info = {
        'gmail.com': ('smtp.gmail.com', 587),
        'naver.com': ('smtp.naver.com', 587),
        'outlook.com': ('smtp-mail.outlook.com', 587),
        'hotmail.com': ('smtp-mail.outlook.com', 587),
        'yahoo.com': ('smtp.mail.yahoo.com', 587),
        'nate.com': ('smtp.mail.nate.com', 465),
        'daum.net': ('smtp.daum.net', 465),
        'hanmail.net': ('smtp.daum.net', 465)
    }

    # 메일 보내는 함수 정의 (발신 메일, 수신 메일(여러개 가능), 제목, 본문, 비밀번호)
    def send_email(From, To, subject, message, passwd='', subtype='plain'):
        
        # 멀티파트로 메일을 만들기 위한 포맷 생성
        form = MIMEBase('multipart', 'mixed')
        
        # 입력받은 메일주소와 제목, 본문 등의 문자열을 인코딩해서 form에 입력
        form['From'] = From
        form['To'] = ', '.join(To) # 수신 메일 리스트를 문자열로 변환 (,와 한칸 공백을 추가해서 구분)
        form['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
        msg = MIMEText(message.encode('utf-8'), _subtype=subtype, _charset='utf-8')
        form.attach(msg)
            
        # SMTP 서버 로그인 및 작성된 메일 보내기
        id, host = From.rsplit("@",1) # 발신인 메일 주소의 @를 기준으로 id와 host로 나눔
        smtp_server, port = smtp_info[host] # dict를 이용해서 host와 port 정보들을 받아옴
        
        # SMTP 서버 접속 여부 확인
        if port == 587:
            smtp = smtplib.SMTP(smtp_server, port)
            rcode1, _ = smtp.ehlo()
            rcode2, _ = smtp.starttls()
        else:
            smtp = smtplib.SMTP_SSL(smtp_server, port)
            rcode1, _ = smtp.ehlo()
            rcode2 = 220  
        if rcode1 != 250 or rcode2 != 220:
            smtp.quit()
            return '연결에 실패하였습니다.'
        
        smtp.login(From, passwd)
        smtp.sendmail(From, To, form.as_string())    
        smtp.quit()


    # 실제 함수 실행 부분
    me = settings.email_id
    data = await request.form()
    is_pass = True if data["status"] == "true" else False # 합격/불합격 선택 여부 확인
    receivers = read_all_is_pass_email(True) if is_pass else read_all_is_pass_email(False)

    subject = data["subject"] # 제목
    message = data["message"] # 본문

    background_tasks.add_task(send_email, me, receivers, subject, message, passwd=settings.email_pw)

    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

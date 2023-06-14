import re
from datetime import datetime

from fastapi import Request

# fastapi.Request 클래스를 사용하여 HTTP 요청에서 전달받은 "폼 데이터"를 처리하는 SubmitForm 클래스를 정의하는 코드다.


class SubmitForm:
    """
    load_data()를 통해 아래 변수를 생성
    username: str
    email: EmailStr
    student_id: str
    python_skill: str
    motivation: str
    field: str
    github: Optional[str]
    blog: Optional[str]
    ai_subject: Optional[str]
    want_to_do: Optional[str]
    course: Optional[str]
    project_exp: Optional[str]
    """

    def __init__(self, request: Request):
        self.request = request
        self.created_time = datetime.now()
        self.is_pass = False
        self.errors = []

    async def load_data(self):  # load_data 메서드를 사용하여 전달받은 폼 데이터를 로드하고,
        form = await self.request.form()
        for k, v in form.items():
            setattr(self, k, v)

    def send_data(self) -> dict:
        send_list = {}
        for k, v in self.__dict__.items():
            if not (k == "request" or k == "errors"):
                send_list[k] = v
        return send_list

    def is_valid(self):
        if self.username == "":
            return False

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, self.email):  # 정규식을 사용하여 이메일 폼 확인
            return False

        if len(self.student_id) != 9:
            return False

        return True

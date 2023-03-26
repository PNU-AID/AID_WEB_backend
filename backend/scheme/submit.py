from fastapi import Request


class SubmitForm:
    # username: str
    # email: EmailStr
    # student_id: str
    # python_skill: str
    # motivation: str
    # github: Optional[str]
    # blog: Optional[str]
    # ai_subject: Optional[str]
    # study_want: Optional[str]
    # project_want: Optional[str]
    # course: Optional[str]
    # project_exp: Optional[str]

    def __init__(self, request: Request):
        self.request = request
        self.errors = []

    async def load_data(self):
        form = await self.request.form()
        for k, v in form.items():
            setattr(self, k, v)

    def send_data(self):
        send_list = {}
        for k, v in self.__dict__.items():
            if k != "request":
                send_list[k] = v
        return send_list

    def is_valid(self):
        if self.username == "":
            return False
        return True

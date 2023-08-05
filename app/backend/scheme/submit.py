from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# fastapi.Request 클래스를 사용하여 HTTP 요청에서 전달받은 "폼 데이터"를 처리하는 SubmitForm 클래스를 정의하는 코드다.


class SubmitForm(BaseModel):
    name: str  # 실제 이름
    email: EmailStr  # 이메일
    student_id: str  # 학번
    phone_number: str  # 전화번호
    motivation: str  # 지원 동기
    github: Optional[str]  # 깃허브 주소
    blog: Optional[str]  # 블로그 주소
    ai_exp: Optional[str]  # ai 관련 경험
    personal_info_agree: bool  # 개인정보 수집 동의 여부

    # TODO
    # @validator("phone_number")
    # def phone_num_valid(cls, v):
    #     pass

    # @validator("personal_info_agree")
    # def agree_check(cls, v):
    #     pass


class SubmitFormforAdmin(SubmitForm):
    opinion: Optional[dict]  # 개인 의견
    is_pass: bool = Field(default=False)  # 합격 여부

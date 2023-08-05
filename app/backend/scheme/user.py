from datetime import datetime

from backend.core.utils import ObjectIdStr, get_random_name
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

# 위 코드는 Pydantic을 사용하여 MongoDB에서 사용될 "User 데이터 모델과 관련된 클래스"들을 정의하고 있다.


class UserBase(BaseModel):
    # base 모델
    # User 클래스는 BaseModel을 상속받아 nick_name, email, is_club_member, admin 필드를 정의
    # https://www.mongodb.com/community/forums/t/why-do-we-need-alias-id-in-pydantic-model-of-fastapi/170728/3
    email: EmailStr = Field(...)


class UserSignUp(UserBase):
    # 회원가입 모델
    password: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"email": "test@example.com", "password": "password"}}


class UserLogIn(UserBase):
    # 로그인 모델
    password: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"email": "test@example.com", "password": "password"}}


class UserInDB(UserBase):
    # db 삽입시 모델
    hash_password: str
    created_time: datetime = Field(default_factory=datetime.now)
    is_admin: bool = False
    is_member: bool = False
    is_active: bool = False
    submit: dict = {}
    articles: list = []
    nick_name: str = Field(default_factory=get_random_name)


class UserOutDB(UserBase):
    # db output시 모델
    id: ObjectIdStr = Field(alias="_id")
    hash_password: str
    created_time: datetime
    is_admin: bool
    is_member: bool
    is_active: bool
    submit: dict
    articles: list
    nick_name: str


class UserOut(UserBase):
    # api return시 모델
    created_time: datetime
    is_admin: bool
    is_member: bool
    is_active: bool
    submit: dict
    articles: list
    nick_name: str


class Token(BaseModel):
    access_token: str
    token_type: str
    email: EmailStr

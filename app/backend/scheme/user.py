from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

# 위 코드는 Pydantic을 사용하여 MongoDB에서 사용될 "User 데이터 모델과 관련된 클래스"들을 정의하고 있다.


class User(BaseModel):
    # User 클래스는 BaseModel을 상속받아 nick_name, email, is_club_member, admin 필드를 정의
    # https://www.mongodb.com/community/forums/t/why-do-we-need-alias-id-in-pydantic-model-of-fastapi/170728/3
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserCreate(User):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"email": "test@example.com", "password": "password"}}


class UserLogIn(User):
    pass

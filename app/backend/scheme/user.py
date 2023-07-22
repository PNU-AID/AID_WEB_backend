from datetime import datetime
from typing import List

from backend.utils import ObjectIdStr
from pydantic import BaseModel, EmailStr, Field

# 위 코드는 Pydantic을 사용하여 MongoDB에서 사용될 "User 데이터 모델과 관련된 클래스"들을 정의하고 있다.


class User(BaseModel):
    # User 클래스는 BaseModel을 상속받아 nick_name, email, is_club_member, admin 필드를 정의
    # https://www.mongodb.com/community/forums/t/why-do-we-need-alias-id-in-pydantic-model-of-fastapi/170728/3
    nick_name: str = Field(...)
    email: EmailStr = Field(...)
    is_club_member: bool = Field(default=False)
    admin: bool = Field(default=False)
    email: str = Field(...)
    real_name: str = Field(...)
    application: str = Field(...)
    articles: List[str] = []


{
    "title": "user",
    "required": [
        "_id",
        "password",
        "is_member",
        "is_admin",
        "email",
        "nick_name",
        "real_name",
        "application",
        "articles",
    ],
    "properties": {
        "_id": {"bsonType": "objectId"},
        "name": {"bsonType": "string"},
        "is_member": {"bsonType": "bool"},
        "is_admin": {"bsonType": "bool"},
        "email": {"bsonType": "string"},
        "nick_name": {"bsonType": "string"},
        "real_name": {"bsonType": "string"},
        "application": {"bsonType": "array"},
        "articles": {"bsonType": "array"},
    },
}


# UserCreate 클래스는 User 클래스를 상속받아 create_time, password 필드를 추가로 정의하고 있습니다.
class UserCreate(User):
    #  create_time 필드의 기본값으로 현재 시간을 사용하도록 설정되어 있습니다.
    create_time: datetime = Field(default_factory=datetime.now)
    password: str = Field(...)
    # TODO
    # 비밀번호 hasing


class UserUpdate(User):
    # UserUpdate 클래스는 User 클래스를 상속받아 _id 필드를 id 필드로 aliasing하고 있다.
    id: str = Field(..., alias="_id")


class UserOut(User):
    # UserOut 클래스는 User 클래스를 상속받아 _id 필드를 id 필드로 aliasing하고 있다. id 필드는 ObjectIdStr 형식으로 정의되어 있다.
    id: ObjectIdStr = Field(..., alias="_id")


def serializeDict(item) -> dict:
    # serializeDict 함수는 MongoDB의 결과물을 Python 딕셔너리 형식으로 변환하여 반환한다. _id 필드는 id 필드로 변환된다.
    return {
        **{"id": str(item[i]) for i in item if i == "_id"},
        **{i: item[i] for i in item if i != "_id"},
    }

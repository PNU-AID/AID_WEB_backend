from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from utils import ObjectIdStr


class User(BaseModel):
    # https://www.mongodb.com/community/forums/t/why-do-we-need-alias-id-in-pydantic-model-of-fastapi/170728/3
    nick_name: str = Field(...)
    email: EmailStr = Field(...)
    is_club_member: bool = Field(default=False)
    admin: bool = Field(default=False)


class UserCreate(User):
    create_time: datetime = Field(default_factory=datetime.now)
    password: str = Field(...)
    # TODO
    # 비밀번호 hasing


class UserOut(User):
    id: ObjectIdStr = Field(..., alias="_id")


def serializeDict(item) -> dict:
    return {
        **{"id": str(item[i]) for i in item if i == "_id"},
        **{i: item[i] for i in item if i != "_id"},
    }
